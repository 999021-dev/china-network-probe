"""检测结果的彩色终端输出。"""

from __future__ import annotations

from typing import List

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .checker import CheckResult

console = Console()


def _latency_color(latency_ms: float | None) -> str:
    if latency_ms is None:
        return "red"
    if latency_ms < 100:
        return "green"
    if latency_ms < 300:
        return "yellow"
    if latency_ms < 600:
        return "orange1"
    return "red"


def _latency_label(latency_ms: float | None) -> str:
    if latency_ms is None:
        return "—"
    if latency_ms < 100:
        return "优秀"
    if latency_ms < 300:
        return "良好"
    if latency_ms < 600:
        return "可用"
    return "差"


def print_geo(geo: dict) -> None:
    if "error" in geo:
        console.print(f"[red]✗ {geo['error']}[/red]\n")
        return

    cc = (geo.get("country_code") or "").upper()
    is_cn = cc == "CN"
    color = "green" if is_cn else "yellow"
    content = (
        f"[bold]出口 IP:[/bold] {geo.get('ip')}\n"
        f"[bold]归属地:[/bold] [{color}]{geo.get('country')} / {geo.get('region')} / {geo.get('city')}[/{color}]\n"
        f"[bold]运营商:[/bold] {geo.get('isp')}\n"
        f"[dim]数据来源: {geo.get('source')}[/dim]"
    )
    console.print(Panel(content, title="🌐 当前网络环境", border_style=color))
    if not is_cn:
        console.print(
            "[yellow]提示：你的出口 IP 不在中国大陆。访问国内服务可能遇到延迟高、地区版权拦截、风控等问题。[/yellow]\n"
        )


def print_results(results: List[CheckResult]) -> None:
    table = Table(
        title="🇨🇳 国内服务可达性与延迟检测",
        box=box.ROUNDED,
        show_lines=False,
        title_style="bold",
    )
    table.add_column("类别", style="cyan", no_wrap=True)
    table.add_column("服务", style="bold")
    table.add_column("主机", style="dim")
    table.add_column("DNS", justify="center")
    table.add_column("TCP 延迟", justify="right")
    table.add_column("评级", justify="center")
    table.add_column("HTTP", justify="center")
    table.add_column("综合", justify="center")

    for r in results:
        t = r.target
        dns_cell = "[green]✓[/green]" if r.dns_resolved else "[red]✗[/red]"

        if r.tcp_latency_ms is not None:
            tcp_color = _latency_color(r.tcp_latency_ms)
            tcp_cell = f"[{tcp_color}]{r.tcp_latency_ms:.0f} ms[/{tcp_color}]"
            grade_cell = f"[{tcp_color}]{_latency_label(r.tcp_latency_ms)}[/{tcp_color}]"
        else:
            tcp_cell = "[red]—[/red]"
            grade_cell = "[red]—[/red]"

        if r.http_status is not None:
            color = "green" if r.http_status < 400 else "yellow"
            http_cell = f"[{color}]{r.http_status}[/{color}]"
        else:
            http_cell = "[red]✗[/red]"

        overall = "[green]✓ 通[/green]" if r.overall_ok else "[red]✗ 异常[/red]"

        table.add_row(
            t["category"], t["name"], t["host"],
            dns_cell, tcp_cell, grade_cell, http_cell, overall,
        )

    console.print(table)

    total = len(results)
    ok_count = sum(1 for r in results if r.overall_ok)
    latencies = [r.tcp_latency_ms for r in results if r.tcp_latency_ms is not None]
    avg = sum(latencies) / len(latencies) if latencies else 0.0

    summary = (
        f"[bold]总计:[/bold] {total} 项    "
        f"[bold green]可达:[/bold green] {ok_count}    "
        f"[bold red]异常:[/bold red] {total - ok_count}    "
        f"[bold]平均延迟:[/bold] {avg:.0f} ms"
    )
    console.print(Panel(summary, title="📊 检测汇总", border_style="cyan"))

    failure_rate = (total - ok_count) / total if total else 0
    if avg > 400 or failure_rate > 0.3:
        console.print(
            "\n[yellow]⚠️  当前网络访问中国大陆服务延迟较高或部分服务异常。"
            "\n   如果你是海外华人/留学生，可参考 README 中『如果检测结果不理想怎么办?』章节获取改善方案。[/yellow]"
        )
