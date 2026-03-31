"""航班資訊查詢模組。

根據班次代碼查詢航空公司、出發地、抵達地。
查詢鏈：DB 快取 → Flightradar24 → AviationStack → IATA 對照表。
所有查詢函式回傳航段列表 [{airline, origin, destination}, ...]。
"""

import logging
import os
import re

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# 常見航空公司 IATA 代碼對照表（作為 API 查詢失敗時的備援）
AIRLINE_CODES = {
    'CI': '中華航空',
    'BR': '長榮航空',
    'IT': '台灣虎航',
    'JX': '星宇航空',
    'AE': '華信航空',
    'CX': '國泰航空',
    'HX': '香港航空',
    'NH': '全日空',
    'JL': '日本航空',
    'MM': '樂桃航空',
    'KE': '大韓航空',
    'OZ': '韓亞航空',
    'SQ': '新加坡航空',
    'TG': '泰國航空',
    'VN': '越南航空',
    'MH': '馬來西亞航空',
    'CZ': '中國南方航空',
    'CA': '中國國際航空',
    'MU': '中國東方航空',
    'UA': '聯合航空',
    'AA': '美國航空',
    'DL': '達美航空',
    'TR': '酷航',
    'QF': '澳洲航空',
    'EK': '阿聯酋航空',
}


def lookup_flight_info(flight_number):
    """根據班次代碼查詢航班資訊。

    查詢鏈：DB 快取 → Flightradar24 → AviationStack → IATA 對照表。

    Args:
        flight_number: 班次代碼，例如 'CI100' 或 'CI-100'。

    Returns:
        成功時回傳航段列表 [{'airline', 'origin', 'destination'}, ...]，
        失敗時回傳 None。
    """
    normalized = re.sub(r'[-\s]', '', flight_number.upper())

    # ① DB 快取
    result = _lookup_from_db_cache(normalized, flight_number)
    if result:
        return result

    # ② Flightradar24 爬取
    result = _lookup_via_flightradar24(normalized)
    if result:
        return result

    # ③ AviationStack API
    result = _lookup_via_aviationstack(normalized)
    if result:
        return result

    # ④ IATA 代碼對照表（僅航空公司）
    result = _lookup_from_code_table(normalized)
    if result:
        return result

    logger.warning('無法查詢班次 %s 的航班資訊', flight_number)
    return None


def _lookup_from_db_cache(normalized, original):
    """從 tracked_flights 表查詢同班次已有紀錄。

    Returns:
        航段列表或 None。
    """
    try:
        from app.models import TrackedFlight
        existing = TrackedFlight.query.filter(
            TrackedFlight.flight_number.in_([normalized, original]),
            TrackedFlight.origin != '',
            TrackedFlight.destination != '',
        ).first()

        if existing:
            logger.info('DB 快取命中: %s', normalized)
            return [{
                'airline': existing.airline,
                'origin': existing.origin,
                'destination': existing.destination,
            }]
    except Exception as e:
        logger.debug('DB 快取查詢失敗: %s', e)

    return None


def _lookup_via_flightradar24(flight_number):
    """透過 Flightradar24 網頁爬取航班資訊。

    Returns:
        航段列表（可能多段）或 None。
    """
    url = f'https://www.flightradar24.com/data/flights/{flight_number.lower()}'
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        ),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            logger.warning(
                'Flightradar24 回傳狀態碼 %d', response.status_code
            )
            return None

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        airline = _extract_fr24_airline(soup, flight_number)
        routes = _extract_fr24_routes(soup, airline or '')

        if routes:
            logger.info('Flightradar24 查詢成功: %d 段航線', len(routes))
            return routes

        return None

    except requests.RequestException as e:
        logger.warning('Flightradar24 請求失敗: %s', e)
        return None
    except Exception as e:
        logger.warning('Flightradar24 解析失敗: %s', e)
        return None


def _extract_fr24_routes(soup, airline):
    """從 Flightradar24 頁面解析所有不重複航段。

    Returns:
        航段列表 [{'airline', 'origin', 'destination'}, ...]，無資料回傳空列表。
    """
    routes = []
    seen = set()

    table = soup.find('table', {'id': 'tbl-datatable'})
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 5:
                # FR24 欄位：[0]摘要 [1]空 [2]日期 [3]FROM [4]TO [5]機型 ...
                origin = _parse_iata_from_text(cols[3].get_text(strip=True))
                destination = _parse_iata_from_text(cols[4].get_text(strip=True))
                if origin and destination:
                    key = f'{origin}-{destination}'
                    if key not in seen:
                        seen.add(key)
                        routes.append({
                            'airline': airline,
                            'origin': origin,
                            'destination': destination,
                        })

    return routes


def _parse_iata_from_text(text):
    """從文字中提取 IATA 機場代碼。

    支援格式：「Tokyo Narita (NRT)」「Taipei(TPE)」「NRT」
    """
    match = re.search(r'\(([A-Z]{3})\)', text)
    if match:
        return match.group(1)
    match = re.match(r'^[A-Z]{3}$', text.strip())
    if match:
        return text.strip()
    return None


def _extract_fr24_airline(soup, flight_number):
    """從 Flightradar24 頁面解析航空公司名稱。"""
    title = soup.find('title')
    if title:
        title_text = title.get_text(strip=True)
        parts = title_text.split(' - ')
        if len(parts) >= 2:
            airline_part = parts[1].replace('Flight Tracker', '').strip()
            if airline_part:
                return airline_part

    match = re.match(r'^([A-Z]{2})\d+', flight_number)
    if match:
        return AIRLINE_CODES.get(match.group(1), '')

    return ''


def _lookup_via_aviationstack(flight_number):
    """透過 AviationStack API 查詢航班資訊。

    Returns:
        航段列表或 None。
    """
    api_key = os.getenv('AVIATIONSTACK_API_KEY', '')
    if not api_key:
        logger.debug('AVIATIONSTACK_API_KEY 未設定，跳過 API 查詢')
        return None

    try:
        response = requests.get(
            'http://api.aviationstack.com/v1/flights',
            params={
                'access_key': api_key,
                'flight_iata': flight_number,
                'limit': 1,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        flights = data.get('data', [])
        if not flights:
            return None

        flight = flights[0]
        return [{
            'airline': flight.get('airline', {}).get('name', ''),
            'origin': flight.get('departure', {}).get('iata', ''),
            'destination': flight.get('arrival', {}).get('iata', ''),
        }]

    except Exception as e:
        logger.error('AviationStack API 查詢失敗: %s', e)
        return None


def _lookup_from_code_table(flight_number):
    """從內建 IATA 代碼對照表解析航空公司名稱。

    Returns:
        航段列表（僅含航空公司）或 None。
    """
    match = re.match(r'^([A-Z]{2})\d+', flight_number)
    if not match:
        return None

    airline_code = match.group(1)
    airline_name = AIRLINE_CODES.get(airline_code)
    if not airline_name:
        return None

    return [{
        'airline': airline_name,
        'origin': '',
        'destination': '',
    }]
