"""检测本机出口 IP 归属地，判断是否处于中国大陆网络。"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Dict


GEO_APIS = [
    "http://ip-api.com/json/?fields=status,country,countryCode,regionName,city,isp,query",
    "https://ipinfo.io/json",
]


def _normalize(data: dict, source: str) -> Dict[str, object]:
    if "ip-api.com" in source:
        return {
            "ip": data.get("query"),
            "country": data.get("country"),
            "country_code": data.get("countryCode"),
            "region": data.get("regionName"),
            "city": data.get("city"),
            "isp": data.get("isp"),
            "source": "ip-api.com",
        }
    if "ipinfo.io" in source:
        return {
            "ip": data.get("ip"),
            "country": data.get("country"),
            "country_code": data.get("country"),
            "region": data.get("region"),
            "city": data.get("city"),
            "isp": data.get("org"),
            "source": "ipinfo.io",
        }
    return {"raw": data, "source": source}


def get_public_ip_info(timeout: float = 5.0) -> Dict[str, object]:
    last_error = None
    for api in GEO_APIS:
        try:
            req = urllib.request.Request(
                api, headers={"User-Agent": "cn-network-probe/0.1"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return _normalize(data, api)
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            continue
    return {"error": f"无法获取出口 IP 信息 ({last_error})"}


def is_china_mainland(geo: dict) -> bool:
    return geo.get("country_code") == "CN"
