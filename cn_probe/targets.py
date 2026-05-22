"""国内主流服务检测目标清单。

涵盖海外用户访问中国大陆时最常遇到问题的几大场景：
视频流媒体、音乐、社交、国服游戏、电商、支付/政务。
"""

TARGETS = [
    # ─── 视频流媒体 ─────────────────────────────────────────
    {"category": "视频", "name": "哔哩哔哩 (Bilibili)", "host": "www.bilibili.com", "port": 443, "scheme": "https"},
    {"category": "视频", "name": "爱奇艺 (iQIYI)",      "host": "www.iqiyi.com",    "port": 443, "scheme": "https"},
    {"category": "视频", "name": "腾讯视频",             "host": "v.qq.com",         "port": 443, "scheme": "https"},
    {"category": "视频", "name": "优酷",                 "host": "www.youku.com",    "port": 443, "scheme": "https"},
    {"category": "视频", "name": "芒果TV",               "host": "www.mgtv.com",     "port": 443, "scheme": "https"},

    # ─── 音乐 ────────────────────────────────────────────
    {"category": "音乐", "name": "网易云音乐", "host": "music.163.com", "port": 443, "scheme": "https"},
    {"category": "音乐", "name": "QQ 音乐",    "host": "y.qq.com",      "port": 443, "scheme": "https"},

    # ─── 社交 ────────────────────────────────────────────
    {"category": "社交", "name": "微博",   "host": "weibo.com",            "port": 443, "scheme": "https"},
    {"category": "社交", "name": "知乎",   "host": "www.zhihu.com",        "port": 443, "scheme": "https"},
    {"category": "社交", "name": "小红书", "host": "www.xiaohongshu.com",  "port": 443, "scheme": "https"},
    {"category": "社交", "name": "豆瓣",   "host": "www.douban.com",       "port": 443, "scheme": "https"},

    # ─── 国服游戏（仅检测官网/网关连通性，非真实游戏服务器延迟）────
    {"category": "游戏", "name": "王者荣耀 官网",   "host": "pvp.qq.com",      "port": 443, "scheme": "https"},
    {"category": "游戏", "name": "原神 米哈游",     "host": "ys.mihoyo.com",   "port": 443, "scheme": "https"},
    {"category": "游戏", "name": "英雄联盟 国服",   "host": "lol.qq.com",      "port": 443, "scheme": "https"},

    # ─── 电商/生活 ───────────────────────────────────────
    {"category": "电商", "name": "淘宝", "host": "www.taobao.com",   "port": 443, "scheme": "https"},
    {"category": "电商", "name": "京东", "host": "www.jd.com",       "port": 443, "scheme": "https"},
    {"category": "电商", "name": "美团", "host": "www.meituan.com",  "port": 443, "scheme": "https"},

    # ─── 支付/政务 ───────────────────────────────────────
    {"category": "支付", "name": "支付宝",   "host": "www.alipay.com",      "port": 443, "scheme": "https"},
    {"category": "支付", "name": "微信支付", "host": "pay.weixin.qq.com",   "port": 443, "scheme": "https"},
]

CATEGORIES = sorted({t["category"] for t in TARGETS})
