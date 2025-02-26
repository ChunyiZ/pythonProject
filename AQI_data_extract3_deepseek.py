import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # 时区处理标准库
from typing import Optional, Dict, List

# 配置全局常量
API_ENDPOINT = "https://data.sh.gov.cn/interface/1124/10185"
TIMEZONE = ZoneInfo("Asia/Shanghai")  # 上海时区
MAX_RETRIES = 3
TIMEOUT = 10

def create_secure_payload(start: datetime, end: datetime) -> Dict:
    """创建符合2025 API规范的请求载荷（带时区信息）"""
    return {
        'start_time': start.astimezone(TIMEZONE).isoformat(),
        'end_time': end.astimezone(TIMEZONE).isoformat(),
        'limit': 1000,
        'offset': 0,
        'tz': TIMEZONE.key
    }

def fetch_aqi_data(
    api_key: str,
    days: int = 10
) -> Optional[List[Dict]]:
    """
    获取最近N天的AQI数据（自动处理TLS 1.3+验证）
    
    Args:
        api_key: 通过政府数据平台申请的2025版加密令牌
        days: 回溯天数（默认10天）
        
    Returns:
        List[Dict]: 解析后的空气质量数据列表
    """
    session = requests.Session()
    session.mount('https://', requests.adapters.HTTPAdapter(
        max_retries=MAX_RETRIES
    ))

    try:
        # 生成时区敏感的时间范围
        end_date = datetime.now(TIMEZONE) - timedelta(days=1)
        start_date = end_date - timedelta(days=days)
        
        response = session.post(
            API_ENDPOINT,
            headers={
                'X-API-Version': '2025.1',
                'Token': f"bearer {api_key}",
                'Content-Encoding': 'gzip'
            },
            json=create_secure_payload(start_date, end_date),
            timeout=TIMEOUT,
            verify='/etc/ssl/certs/2025_global_ca.pem'  # 最新根证书
        )
        
        response.raise_for_status()
        
        if (data := response.json())['code'] == '000000':
            return data['data']['data']
            
        print(f"API Error: {data.get('message')}")
        return None

    except requests.exceptions.SSLError as e:
        print(f"SSL Handshake Failed: {e.__cause__}")
    except requests.exceptions.JSONDecodeError:
        print("Invalid JSON Response")
    finally:
        session.close()