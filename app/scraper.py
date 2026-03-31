"""Skyscanner 航班價格擷取模組。"""

import logging
import os
from datetime import date, datetime, timezone

import requests

from app import db
from app.models import FlightPrice, ScrapeLog, TrackedFlight

logger = logging.getLogger(__name__)

SKYSCANNER_API_BASE = 'https://partners.api.skyscanner.net/apiservices/v3'


def scrape_flight_price(tracked_flight):
    """擷取單一班機的價格資訊。

    Args:
        tracked_flight: TrackedFlight 資料模型實例。

    Returns:
        成功時回傳 FlightPrice 實例，失敗時回傳 None。
    """
    api_key = os.getenv('SKYSCANNER_API_KEY', '')
    if not api_key:
        _log_failure(tracked_flight, 'SKYSCANNER_API_KEY 未設定')
        return None

    try:
        price_data = _fetch_price_from_skyscanner(
            api_key=api_key,
            origin=tracked_flight.origin,
            destination=tracked_flight.destination,
            flight_number=tracked_flight.flight_number,
        )

        if price_data is None:
            _log_failure(tracked_flight, '未找到匹配的航班價格資料')
            return None

        flight_price = FlightPrice(
            flight_number=tracked_flight.flight_number,
            price=price_data['price'],
            scrape_date=date.today(),
            departure_time=price_data.get('departure_time'),
            airline=tracked_flight.airline,
            origin=tracked_flight.origin,
            destination=tracked_flight.destination,
            tracked_flight_id=tracked_flight.id,
        )
        db.session.add(flight_price)

        scrape_log = ScrapeLog(
            flight_number=tracked_flight.flight_number,
            status='success',
            price=price_data['price'],
        )
        db.session.add(scrape_log)
        db.session.commit()

        logger.info(
            '成功擷取 %s 價格: %s',
            tracked_flight.flight_number,
            price_data['price'],
        )
        return flight_price

    except Exception as e:
        db.session.rollback()
        _log_failure(tracked_flight, str(e))
        return None


def scrape_all_active_flights():
    """擷取所有啟用追蹤班機的價格。

    先檢查當日是否已有資料，僅對無資料的班機執行爬蟲。

    Returns:
        包含成功、失敗、跳過數量的字典。
    """
    today = date.today()
    active_flights = TrackedFlight.query.filter_by(is_active=True).all()
    results = {
        'success': 0, 'failed': 0, 'skipped': 0,
        'total': len(active_flights),
    }

    for flight in active_flights:
        # 檢查當日是否已有資料
        existing = FlightPrice.query.filter_by(
            flight_number=flight.flight_number,
            scrape_date=today,
        ).first()
        if existing:
            results['skipped'] += 1
            logger.debug('跳過 %s: 當日已有資料', flight.flight_number)
            continue

        result = scrape_flight_price(flight)
        if result:
            results['success'] += 1
        else:
            results['failed'] += 1

    logger.info(
        '抓取完成: 共 %d 筆, 成功 %d, 失敗 %d, 跳過 %d',
        results['total'],
        results['success'],
        results['failed'],
        results['skipped'],
    )
    return results


def force_scrape_all_active_flights():
    """強制擷取所有啟用追蹤班機的價格（不檢查當日資料）。

    Returns:
        包含成功與失敗數量的字典。
    """
    active_flights = TrackedFlight.query.filter_by(is_active=True).all()
    results = {'success': 0, 'failed': 0, 'total': len(active_flights)}

    for flight in active_flights:
        result = scrape_flight_price(flight)
        if result:
            results['success'] += 1
        else:
            results['failed'] += 1

    logger.info(
        '強制抓取完成: 共 %d 筆, 成功 %d, 失敗 %d',
        results['total'],
        results['success'],
        results['failed'],
    )
    return results


def _fetch_price_from_skyscanner(api_key, origin, destination, flight_number):
    """從 Skyscanner API 擷取航班價格。

    Args:
        api_key: Skyscanner API 金鑰。
        origin: 出發地 IATA 代碼。
        destination: 抵達地 IATA 代碼。
        flight_number: 班次編號。

    Returns:
        包含 price 與 departure_time 的字典，或 None。
    """
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json',
    }

    # 使用 Skyscanner Flights Indicative API 搜尋價格
    payload = {
        'query': {
            'market': 'TW',
            'locale': 'zh-TW',
            'currency': 'TWD',
            'queryLegs': [
                {
                    'originPlace': {'queryPlace': {'iata': origin}},
                    'destinationPlace': {'queryPlace': {'iata': destination}},
                    'anytime': True,
                }
            ],
        }
    }

    try:
        response = requests.post(
            f'{SKYSCANNER_API_BASE}/flights/indicative/search',
            json=payload,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        # 從回應中解析價格資訊
        quotes = data.get('content', {}).get('results', {}).get('quotes', {})
        for quote_id, quote in quotes.items():
            min_price = quote.get('minPrice', {})
            price_amount = min_price.get('amount')
            if price_amount:
                departure_info = (
                    quote.get('outboundLeg', {})
                    .get('departureDateTime', {})
                )
                departure_time = None
                if departure_info:
                    try:
                        departure_time = datetime(
                            year=departure_info.get('year', 2026),
                            month=departure_info.get('month', 1),
                            day=departure_info.get('day', 1),
                            hour=departure_info.get('hour', 0),
                            minute=departure_info.get('minute', 0),
                        )
                    except (ValueError, TypeError):
                        pass

                return {
                    'price': float(price_amount),
                    'departure_time': departure_time,
                }

        return None

    except requests.RequestException as e:
        logger.error('Skyscanner API 請求失敗: %s', e)
        raise


def _log_failure(tracked_flight, error_message):
    """記錄擷取失敗的日誌。"""
    logger.error(
        '擷取 %s 價格失敗: %s',
        tracked_flight.flight_number,
        error_message,
    )
    try:
        scrape_log = ScrapeLog(
            flight_number=tracked_flight.flight_number,
            status='failed',
            error_message=error_message,
        )
        db.session.add(scrape_log)
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception('記錄抓取失敗日誌時發生錯誤')
