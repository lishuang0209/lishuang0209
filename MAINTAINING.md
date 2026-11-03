# 个人主页维护

此目录对应公开的 GitHub 个人主页仓库 `lishuang0209/lishuang0209`，与个人网站仓库独立。

- `README.md`：GitHub 个人主页展示内容。顶部改为浅色静态个人名片，名字为李爽，不再展示网站横幅或动画。
- `assets/profile-card.svg`：浅色圆角名片、蓝紫渐变线、姓名和介绍。
- `assets/nav-projects.svg`、`nav-about.svg`、`nav-writing.svg`：蓝、紫、绿导航按钮，链接到现有项目、关于和文章板块。
- `assets/profile-particles.gif`：保留的旧动画，当前 README 不再引用。
- `assets/profile-banner-clear.gif`：保留的上一版含文字横幅。
- `assets/profile-banner-animated.gif`：保留的上一版动画横幅。
- `scripts/render-banner.py`：使用 NumPy 和 Pillow 生成纯粒子动画；逐帧清除并验证解码帧与源帧一致。
- `assets/profile-banner-index.svg`：保留的静态粒子横幅。
- `assets/profile-banner.svg`：保留的旧版横幅。
- 仅展示公开项目；不要把私有仓库、登录态参数或公众号后台地址加入内容。
- 技能以公开项目 README 和实际依赖为依据，不使用虚构的熟练度。
- 微信文章仅保存公开阅读链接；后续有新文章时，在 README 的文章区增加标题、主题与链接。

## 依据

- 小红书 Skill：项目 README，包含 Python、Skills、MCP、Pillow 和内容创作流程。
- Blender 展示页：README 和 package.json，包含 React、TypeScript、Vite、Three.js、GSAP、Lenis、Web Audio。
- 个人网站：HTML、CSS、JavaScript、SVG，以及 GitHub Actions / Pages 配置。
- 三篇公众号文章的公开链接和完整标题由用户提供；微信返回验证页，未获取正文。文章分类仅根据标题整理，不对正文作未经核验的摘要。
- Obsidian + Codex 知识管理方向来自用户提供的第二篇文章标题。

后续新增公开项目时，同步更新 README 的项目目录。此版本没有设置定时任务。
