"""命令行入口。"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from . import __version__
from .checker import CheckResult, check_target
from .geo import get_public_ip_info
from .reporter import console, print_geo, print_results
from .targets import CATEGORIES, TARGETS


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="cn-probe",
        description=(
            "海外回国网络访问检测工具 — 检测当前网络访问中国大陆主流服务的延迟与可达性。\n"
            "适用于海外华人、留学生排查回国访问问题。"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-c", "--category",
        choices=CATEGORIES,
        help="只检测指定类别（默认全部）",
    )
    parser.add_argument(
        "-n", "--concurrency",
        type=int, default=8,
        help="并发检测数 (默认 8)",
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float, default=5.0,
        help="单项超时秒数 (默认 5)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出（便于脚本消费）",
    )
    parser.add_argument(
        "--no-geo",
        action="store_true",
        help="跳过出口 IP 归属地检测",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"cn-network-probe {__version__}",
    )
    return parser.parse_args()


def _filter_targets(category: str | None) -> list:
    if not category:
        return list(TARGETS)
    return [t for t in TARGETS if t["category"] == category]


def _run_checks(targets: list, concurrency: int, timeout: float) -> List[CheckResult]:
    results: List[CheckResult] = []
    target_index = {id(t): i for i, t in enumerate(targets)}
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(check_target, t, timeout): t for t in targets}
        with console.status("[cyan]检测中...[/cyan]", spinner="dots"):
            for fut in as_completed(futures):
                results.append(fut.result())
    results.sort(key=lambda r: target_index.get(id(r.target), 0))
    return results


def _to_json(results: List[CheckResult], geo: dict) -> None:
    payload = {
        "version": __version__,
        "geo": geo,
        "results": [
            {
                "category": r.target["category"],
                "name": r.target["name"],
                "host": r.target["host"],
                "dns_ip": r.dns_resolved,
                "dns_error": r.dns_error,
                "tcp_latency_ms": round(r.tcp_latency_ms, 2) if r.tcp_latency_ms is not None else None,
                "tcp_error": r.tcp_error,
                "http_status": r.http_status,
                "http_error": r.http_error,
                "ok": r.overall_ok,
            }
            for r in results
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> None:
    args = _parse_args()
    targets = _filter_targets(args.category)
    if not targets:
        console.print(f"[red]没有匹配类别 '{args.category}' 的检测目标[/red]")
        sys.exit(1)

    geo: dict = {}
    if not args.no_geo:
        if not args.json:
            console.print("[cyan]正在检测出口 IP 归属地...[/cyan]")
        geo = get_public_ip_info()

    results = _run_checks(targets, args.concurrency, args.timeout)

    if args.json:
        _to_json(results, geo)
    else:
        if geo:
            print_geo(geo)
        print_results(results)
        console.print(
            "\n[dim]检测仅反映网络层连通性，不代表业务层完全可用。"
            "完整使用方法见 README.md。[/dim]"
        )


if __name__ == "__main__":
    main()
