# china-network-probe · Network Probe for China-Mainland Services

> [中文版 README](README.md) · English

> A CLI tool that measures **latency, reachability, DNS resolution, and egress IP geolocation** for accessing major China-mainland internet services (Bilibili, iQIYI, NetEase Music, WeChat Pay, Taobao, KingGlory, Genshin Impact CN, LOL CN, etc.) from outside China.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## What it looks like

**Direct connection from overseas — high latency, some services region-blocked:**

![Screenshot: probing China services from overseas without acceleration shows high latency and HTTP 403/451 errors](docs/screenshot-no-vpn.svg)

**With a back-to-China accelerator — low latency, all reachable:**

![Screenshot: probing China services through a back-to-China accelerator shows low latency across all 12 services](docs/screenshot-with-vpn.svg)

> Real **DNS / TCP / HTTP** data tells you exactly where the bottleneck is, and whether your back-to-China VPN actually works.

---

## Who is this for?

- 🌏 **Overseas Chinese / international students** trying to diagnose why their access to Chinese services is slow or blocked
- 🎮 **CN-server gamers** (KingGlory, Genshin Impact CN, LOL CN) verifying their network path
- 📺 Anyone trying to access **Bilibili, iQIYI, Tencent Video, NetEase Music** from abroad and seeing region-block errors
- 💳 Users needing **WeChat Pay / Alipay / Taobao** outside China and hitting risk-control walls
- 🚀 Users of **back-to-China VPNs / accelerators** who want to **objectively verify** whether their service actually works
- 🛠️ Network engineers / SREs probing connectivity to China from their data centers

## What it does

In one command, the tool measures **19 popular China-mainland services** across 6 categories:

```bash
python -m cn_probe
```

It will:

1. Detect your **egress IP** and geolocation (so you know whether your VPN actually swapped your IP to China)
2. For each target, measure:
   - **DNS resolution** (detect DNS poisoning)
   - **TCP handshake latency** (real-world network latency, more accurate than `ping`)
   - **HTTP HEAD response** (detect application-level blocking like 403 / 451)
3. Output a **color-coded summary** with diagnosis hints

## Installation

```bash
git clone https://github.com/999021-dev/china-network-probe.git
cd china-network-probe
pip install -r requirements.txt
python -m cn_probe
```

Or install via pip (once published):

```bash
pip install china-network-probe
cn-probe
```

## Usage

```bash
# Probe all 19 services
python -m cn_probe

# Probe one category only (视频/音乐/社交/游戏/电商/支付)
python -m cn_probe -c 游戏

# JSON output (for scripts)
python -m cn_probe --json > result.json

# Skip geo lookup
python -m cn_probe --no-geo

# Higher concurrency
python -m cn_probe -n 16
```

### CLI options

| Flag | Description | Default |
|------|-------------|---------|
| `-c, --category` | Filter by category: 视频/音乐/社交/游戏/电商/支付 | all |
| `-n, --concurrency` | Concurrent probes | 8 |
| `-t, --timeout` | Per-target timeout (seconds) | 5 |
| `--json` | JSON output | off |
| `--no-geo` | Skip egress IP geolocation | off |
| `--version` | Show version | — |

## What gets probed

19 services across 6 categories:

| Category | Services |
|----------|----------|
| **Video** | Bilibili, iQIYI, Tencent Video, Youku, MangoTV |
| **Music** | NetEase Cloud Music, QQ Music |
| **Social** | Weibo, Zhihu, Xiaohongshu, Douban |
| **Gaming (CN server)** | KingGlory, Genshin Impact (miHoYo), LOL CN |
| **E-commerce** | Taobao, JD, Meituan |
| **Payment** | Alipay, WeChat Pay |

> ⚠️ Gaming targets probe official websites / gateways, not actual game-server UDP latency. Real in-game latency is typically 50-100ms higher.

## Interpreting results

### Latency tiers

| TCP latency | Grade | Real-world experience |
|---|---|---|
| `< 100 ms` | 🟢 Excellent | Snappy, video plays smoothly, gaming is fluid |
| `100 - 300 ms` | 🟡 Good | Generally usable, occasional game lag |
| `300 - 600 ms` | 🟠 Acceptable | Pages load slow, video buffers, gaming difficult |
| `> 600 ms` | 🔴 Poor | Most services barely usable |

### HTTP status

- `200`: Service responding normally ✅
- `3xx`: Redirect, still normal
- `403`: Forbidden, possibly region-blocked or risk-controlled
- `451`: Unavailable for legal reasons — typical region-content blocking
- `5xx`: Server error
- `✗`: No response — possibly GFW filtering, DNS poisoning, or service down

## What if results look bad?

If you see:
- Average latency > 400 ms
- Multiple services returning HTTP 403 / 451
- DNS resolution failures
- NetEase / Bilibili / Tencent Video showing region-block messages

Your current network is not suitable for direct access to China services. Common solutions:

### Option 1: Back-to-China VPN / Accelerator (most common)

Route your traffic through a China-mainland exit node. Common services:

- **[SpeedX](https://www.speedx.link/)** — Back-to-China accelerator for overseas Chinese and international students, optimized for streaming, social, and CN-server gaming. TLS encryption + smart split-tunneling + 1000+ nodes. Supports Windows / macOS / iOS / Android.
- Other commercial back-to-China accelerators (穿梭, 快帆, QuickFox, etc.)
- Self-hosted relay (cheaper long-term but requires technical skill)

### Option 2: DNS optimization

If only DNS is the issue but TCP works:

```bash
# Use Chinese public DNS
nameserver 223.5.5.5      # AliDNS
nameserver 119.29.29.29   # DNSPod
```

### Option 3: Browser extension (lightest)

For browser-only traffic, a back-to-China Chrome/Firefox extension can be enough.

## Why TCP handshake, not ICMP ping?

- **ICMP is often filtered** — many China services drop ICMP at edge, so `ping` fails even when HTTPS works
- **TCP handshake reflects real-world** — browsers and apps actually use TCP/HTTPS
- **No root privileges needed** — unlike raw ICMP sockets

## Privacy

This tool does **not** upload any data anywhere:

- Egress IP lookup uses public APIs (ip-api.com / ipinfo.io) — not through our servers
- All probe results stay on your local terminal
- Use `--no-geo` to skip IP lookup entirely

Source is open — feel free to audit [checker.py](cn_probe/checker.py) and [geo.py](cn_probe/geo.py).

## Contributing

PRs welcome. Common contribution areas:

- New probe targets (especially gaming, SaaS)
- IPv6 support
- Better Windows terminal compatibility
- Translation (Traditional Chinese, Japanese, Korean)

See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for details.

## License

[MIT License](LICENSE)

## Disclaimer

This tool is for **network connectivity diagnosis** only. It does not provide any form of proxy or circumvention service. Users are responsible for complying with local laws.

---

[中文版 README](README.md) · [Project Homepage](https://999021-dev.github.io/china-network-probe) · [Report an issue](https://github.com/999021-dev/china-network-probe/issues)
