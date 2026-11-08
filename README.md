# MatryoshkaLJY · 项目与笔记

个人静态展示站：<https://matryoshkaljy.github.io/>

## 内容

- `index.html`：五个项目的介绍、分类筛选、GitHub 链接与笔记入口。
- `assets/`：样式、少量交互与本地静态资源。
- `notes/say-halo-training-guide.html`：单文件 say “Halo” 中文育成手册，保留原有工具与来源。

## 本地预览

无需安装依赖或构建，在仓库根目录运行：

```bash
python3 -m http.server 8000
```

打开 <http://localhost:8000/>。

## 更新与发布

向 `main` 推送后，GitHub Actions 会校验站内链接和 JavaScript 语法，仅将页面与资源复制到 `_site/` 并发布到 GitHub Pages。仓库的 **Settings → Pages → Source** 应选择 **GitHub Actions**。工作流也支持手动运行。

项目介绍直接编辑 `index.html`；新增页面后，记得更新 `sitemap.xml` 和 `scripts/check_site.py` 中的发布文件清单。没有构建依赖、外部字体或分析脚本。

## 内容与来源

- 项目介绍按各公开仓库于 2026-11-08 的 README / 源码整理，不代表实时状态。
- IIDX 记分板为本站原创 SVG 界面示意，使用虚构队伍与占位数据，并非项目实际运行截图。
- ShinyColors 是 [biuuu/ShinyColors](https://github.com/biuuu/ShinyColors) 的个人增强 fork，主页保留上游署名。相关代码与数据以原仓库许可证为准。
- Pebble、ShinyColors、VFD 和 Pico 画面为本站绘制的示意，并非实物照片或实际运行截图。音源切换按钮仅演示原理，不连接硬件。
- 育成手册保留原文来源及版本说明；正文与计算工具可离线使用，原文链接需联网。
