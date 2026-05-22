# 贡献指南 / Contributing

感谢有兴趣为 **china-network-probe** 贡献！这份指南帮助你更高效地参与。

## 我可以贡献什么 / What can I contribute?

### 🎯 添加新的检测目标

如果你发现某个国内服务在海外访问经常有问题、值得加入默认检测列表，欢迎提 PR。

编辑 [`cn_probe/targets.py`](../cn_probe/targets.py)：

```python
{"category": "你的分类", "name": "服务展示名", "host": "域名", "port": 443, "scheme": "https"},
```

**评估标准：**
- 服务有一定知名度（海外华人 / 留学生群体常用）
- 域名在公开域名（非内部测试域名）
- 检测有意义（例如：能反映 IP 拦截、地区限制、CDN 覆盖问题）

### 🐛 修 bug

请先看 [Issues](https://github.com/999021-dev/china-network-probe/issues) 是否已经有人报告。如果没有，开一个新的。

### 📝 文档 / 翻译

欢迎补充：
- README 的英文 / 繁体中文版本
- FAQ 的实际案例
- GitHub Pages 上的指南内容

### ✨ 新功能

提 PR 前建议先开 Issue 讨论方向，避免做了之后方向不对。

## 开发流程 / Development workflow

```bash
# 1. Fork & clone
git clone https://github.com/YOUR_FORK/china-network-probe.git
cd china-network-probe

# 2. 创建分支
git checkout -b feat/your-feature

# 3. 装依赖
pip install -r requirements.txt

# 4. 改代码、本地测试
python -m cn_probe
python -m cn_probe --json | python -m json.tool

# 5. 提交
git add .
git commit -m "feat: 你的变更描述"
git push origin feat/your-feature

# 6. 在 GitHub 提 PR
```

## 代码风格 / Code style

- 遵循 PEP 8
- 函数命名 snake_case
- 类型注解可选但推荐
- 注释优先解释 **why**，不是 **what**
- 不引入不必要的第三方依赖（标准库够用就用标准库）

## 提交信息 / Commit message

建议使用 [Conventional Commits](https://www.conventionalcommits.org/) 风格：

```
feat: 添加 抖音 (douyin) 检测目标
fix: 修复 Windows 终端中文乱码问题
docs: 补充 FAQ 中关于 DNS 污染的解释
refactor: 抽离 HTTP 检测逻辑
```

## 行为准则 / Code of conduct

- 友好、尊重所有参与者
- 接受建设性批评
- 关注对项目和社区最有利的事

## License

提交 PR 即表示你同意你的贡献以 [MIT License](../LICENSE) 发布。
