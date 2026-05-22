"""生成 README 用的运行截图 (SVG)。

构造两个典型场景的截图，对比展示工具价值：
  1. 海外直连国内服务（高延迟、部分服务被地区限制）
  2. 使用回国加速器后（低延迟、全部可达）

不联网，使用 mock 数据，确保截图稳定可复现。
"""

import os
import sys

# 让 tools/ 能 import 项目代码
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)

from rich.console import Console  # noqa: E402

from cn_probe import reporter as _reporter  # noqa: E402
from cn_probe.checker import CheckResult  # noqa: E402


def make_result(category: str, name: str, host: str, **kw) -> CheckResult:
    return CheckResult(
        target={"category": category, "name": name, "host": host, "port": 443, "scheme": "https"},
        **kw,
    )


def render_scenario(title: str, geo: dict, results: list, output_path: str) -> None:
    console = Console(record=True, width=110, force_terminal=True, color_system="truecolor")
    _reporter.console = console
    _reporter.print_geo(geo)
    _reporter.print_results(results)
    console.save_svg(output_path, title=title)
    print(f"✓ generated: {output_path}")


GEO_DIRECT = {
    "ip": "203.0.113.42",
    "country": "United States",
    "country_code": "US",
    "region": "California",
    "city": "San Francisco",
    "isp": "Comcast Cable",
    "source": "ip-api.com",
}

GEO_VPN = {
    "ip": "47.243.x.x",
    "country": "China",
    "country_code": "CN",
    "region": "Shanghai",
    "city": "Shanghai",
    "isp": "回国加速节点 (示意)",
    "source": "ip-api.com",
}

RESULTS_DIRECT = [
    make_result("视频", "哔哩哔哩 (Bilibili)", "www.bilibili.com",
                dns_resolved="203.107.1.1", tcp_latency_ms=285.4, http_status=200, overall_ok=True),
    make_result("视频", "爱奇艺 (iQIYI)", "www.iqiyi.com",
                dns_resolved="101.227.131.55", tcp_latency_ms=468.2, http_status=403, overall_ok=False),
    make_result("视频", "腾讯视频", "v.qq.com",
                dns_resolved="111.30.131.30", tcp_latency_ms=512.7, http_status=200, overall_ok=True),
    make_result("视频", "优酷", "www.youku.com",
                dns_resolved="106.11.62.117", tcp_latency_ms=445.1, http_status=451, overall_ok=False),
    make_result("音乐", "网易云音乐", "music.163.com",
                dns_resolved="59.111.181.38", tcp_latency_ms=698.1, http_status=460, overall_ok=False),
    make_result("社交", "微博", "weibo.com",
                dns_resolved="121.51.111.111", tcp_latency_ms=320.5, http_status=302, overall_ok=True),
    make_result("社交", "小红书", "www.xiaohongshu.com",
                dns_resolved=None, dns_error="DNS 解析超时", overall_ok=False),
    make_result("游戏", "王者荣耀 官网", "pvp.qq.com",
                dns_resolved="111.30.131.99", tcp_latency_ms=620.3, http_status=200, overall_ok=True),
    make_result("游戏", "原神 米哈游", "ys.mihoyo.com",
                dns_resolved="49.51.6.18", tcp_latency_ms=755.8, http_status=200, overall_ok=True),
    make_result("电商", "淘宝", "www.taobao.com",
                dns_resolved="124.115.4.193", tcp_latency_ms=387.2, http_status=200, overall_ok=True),
    make_result("支付", "支付宝", "www.alipay.com",
                dns_resolved="110.75.184.146", tcp_latency_ms=412.6, http_status=200, overall_ok=True),
    make_result("支付", "微信支付", "pay.weixin.qq.com",
                dns_resolved=None, dns_error="DNS 解析失败", overall_ok=False),
]

RESULTS_VPN = [
    make_result("视频", "哔哩哔哩 (Bilibili)", "www.bilibili.com",
                dns_resolved="203.107.1.1", tcp_latency_ms=3.4, http_status=200, overall_ok=True),
    make_result("视频", "爱奇艺 (iQIYI)", "www.iqiyi.com",
                dns_resolved="101.227.131.55", tcp_latency_ms=9.1, http_status=200, overall_ok=True),
    make_result("视频", "腾讯视频", "v.qq.com",
                dns_resolved="111.30.131.30", tcp_latency_ms=6.5, http_status=200, overall_ok=True),
    make_result("视频", "优酷", "www.youku.com",
                dns_resolved="106.11.62.117", tcp_latency_ms=7.3, http_status=200, overall_ok=True),
    make_result("音乐", "网易云音乐", "music.163.com",
                dns_resolved="59.111.181.38", tcp_latency_ms=11.2, http_status=200, overall_ok=True),
    make_result("社交", "微博", "weibo.com",
                dns_resolved="121.51.111.111", tcp_latency_ms=8.7, http_status=302, overall_ok=True),
    make_result("社交", "小红书", "www.xiaohongshu.com",
                dns_resolved="106.11.45.123", tcp_latency_ms=3.5, http_status=404, overall_ok=True),
    make_result("游戏", "王者荣耀 官网", "pvp.qq.com",
                dns_resolved="111.30.131.99", tcp_latency_ms=3.2, http_status=200, overall_ok=True),
    make_result("游戏", "原神 米哈游", "ys.mihoyo.com",
                dns_resolved="49.51.6.18", tcp_latency_ms=1.4, http_status=200, overall_ok=True),
    make_result("电商", "淘宝", "www.taobao.com",
                dns_resolved="124.115.4.193", tcp_latency_ms=2.1, http_status=200, overall_ok=True),
    make_result("支付", "支付宝", "www.alipay.com",
                dns_resolved="110.75.184.146", tcp_latency_ms=1.8, http_status=200, overall_ok=True),
    make_result("支付", "微信支付", "pay.weixin.qq.com",
                dns_resolved="58.247.206.142", tcp_latency_ms=5.3, http_status=200, overall_ok=True),
]


def main() -> None:
    out_dir = os.path.join(_ROOT, "docs")
    os.makedirs(out_dir, exist_ok=True)

    render_scenario(
        "cn-probe · 海外直连国内服务（未使用加速）",
        GEO_DIRECT, RESULTS_DIRECT,
        os.path.join(out_dir, "screenshot-no-vpn.svg"),
    )
    render_scenario(
        "cn-probe · 使用回国加速器后",
        GEO_VPN, RESULTS_VPN,
        os.path.join(out_dir, "screenshot-with-vpn.svg"),
    )


if __name__ == "__main__":
    main()
