"""航班資訊查詢模組。

根據班次代碼查詢航空公司、出發地、抵達地。
優先使用 AviationStack API，失敗時使用內建 IATA 代碼對照表。
"""

import logging
import os
import re

import requests

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

    Args:
        flight_number: 班次代碼，例如 'CI100' 或 'CI-100'。

    Returns:
        成功時回傳字典 {'airline', 'origin', 'destination'}，
        失敗時回傳 None。
    """
    # 正規化班次代碼：移除連字號與空白
    normalized = re.sub(r'[-\s]', '', flight_number.upper())

    # 嘗試 AviationStack API
    result = _lookup_via_aviationstack(normalized)
    if result:
        return result

    # 備援：從 IATA 代碼對照表解析航空公司
    result = _lookup_from_code_table(normalized)
    if result:
        return result

    logger.warning('無法查詢班次 %s 的航班資訊', flight_number)
    return None


def _lookup_via_aviationstack(flight_number):
    """透過 AviationStack API 查詢航班資訊。"""
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
        return {
            'airline': flight.get('airline', {}).get('name', ''),
            'origin': flight.get('departure', {}).get('iata', ''),
            'destination': flight.get('arrival', {}).get('iata', ''),
        }

    except Exception as e:
        logger.error('AviationStack API 查詢失敗: %s', e)
        return None


def _lookup_from_code_table(flight_number):
    """從內建 IATA 代碼對照表解析航空公司名稱。

    僅能取得航空公司，無法取得出發地與抵達地。
    """
    # 提取前 2 碼作為航空公司代碼
    match = re.match(r'^([A-Z]{2})\d+', flight_number)
    if not match:
        return None

    airline_code = match.group(1)
    airline_name = AIRLINE_CODES.get(airline_code)
    if not airline_name:
        return None

    return {
        'airline': airline_name,
        'origin': '',
        'destination': '',
    }
