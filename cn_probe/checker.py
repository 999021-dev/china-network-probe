"""核心检测逻辑：DNS 解析、TCP 握手延迟、HTTP 可达性。"""

from __future__ import annotations

import http.client
import socket
import ssl
import time
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class CheckResult:
    target: dict
    dns_resolved: Optional[str] = None
    dns_error: Optional[str] = None
    tcp_latency_ms: Optional[float] = None
    tcp_error: Optional[str] = None
    http_status: Optional[int] = None
    http_error: Optional[str] = None
    overall_ok: bool = False


def resolve_dns(host: str, timeout: float = 3.0) -> Tuple[Optional[str], Optional[str]]:
    socket.setdefaulttimeout(timeout)
    try:
        ip = socket.gethostbyname(host)
        return ip, None
    except socket.gaierror as exc:
        return None, f"DNS 解析失败: {exc}"
    except socket.timeout:
        return None, "DNS 解析超时"
    except Exception as exc:
        return None, f"DNS 错误: {exc}"


def measure_tcp_latency(
    host: str, port: int, timeout: float = 3.0, samples: int = 3
) -> Tuple[Optional[float], Optional[str]]:
    """通过 TCP 三次握手测量延迟。多次采样取最小值，更接近网络下限。"""
    latencies = []
    last_error: Optional[str] = None
    for _ in range(samples):
        try:
            start = time.perf_counter()
            sock = socket.create_connection((host, port), timeout=timeout)
            elapsed = (time.perf_counter() - start) * 1000.0
            sock.close()
            latencies.append(elapsed)
        except socket.timeout:
            last_error = "TCP 连接超时"
        except OSError as exc:
            last_error = f"TCP 连接失败: {exc}"
        except Exception as exc:
            last_error = f"TCP 错误: {exc}"
    if latencies:
        return min(latencies), None
    return None, last_error


def check_http(
    host: str, scheme: str = "https", timeout: float = 5.0
) -> Tuple[Optional[int], Optional[str]]:
    """发送 HEAD 请求，验证服务是否真实响应（区分网络可达 vs 应用层可用）。"""
    conn = None
    try:
        if scheme == "https":
            ctx = ssl.create_default_context()
            conn = http.client.HTTPSConnection(host, timeout=timeout, context=ctx)
        else:
            conn = http.client.HTTPConnection(host, timeout=timeout)
        conn.request("HEAD", "/", headers={"User-Agent": "cn-network-probe/0.1"})
        resp = conn.getresponse()
        return resp.status, None
    except socket.timeout:
        return None, "HTTP 请求超时"
    except ssl.SSLError as exc:
        return None, f"SSL 错误: {exc}"
    except Exception as exc:
        return None, f"HTTP 错误: {type(exc).__name__}"
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


def check_target(target: dict, timeout: float = 5.0) -> CheckResult:
    """完整流程：DNS → TCP 延迟 → HTTP HEAD。任一环节失败提早返回。"""
    result = CheckResult(target=target)

    ip, dns_err = resolve_dns(target["host"], timeout=min(3.0, timeout))
    result.dns_resolved = ip
    result.dns_error = dns_err
    if not ip:
        return result

    latency, tcp_err = measure_tcp_latency(
        target["host"], target.get("port", 443), timeout=min(3.0, timeout)
    )
    result.tcp_latency_ms = latency
    result.tcp_error = tcp_err
    if latency is None:
        return result

    status, http_err = check_http(
        target["host"], target.get("scheme", "https"), timeout=timeout
    )
    result.http_status = status
    result.http_error = http_err

    # 任何 1xx-5xx 状态都说明服务器在响应；只有完全无响应才算异常
    result.overall_ok = status is not None and 100 <= status < 600
    return result
