# CI 与红线

`assets-check` 在每次 push / PR 跑 `tools/check.sh`，三道闸：

1. **尺寸红线**：图片 ≤2MB、视频 ≤10MB（jsDelivr 单文件上限 20MB，留余量）
2. **全仓重复检测**：MD5 相同的文件即失败 —— 同一素材全仓只留一份
3. **索引新鲜度**：INDEX.md 与实际目录不一致即失败（本地 `tools/index.sh` 重生成）

## UI 检查

`deploy-docs` 对涉及文档、图标包或构建工具的 PR 运行浏览器检查。推送到 `main` 后相同检查通过才发布到 Pages。

目前覆盖首页图标包入口、图片加载、品牌色和单色切换、Discord 直链复制、ZIP 下载，以及 390px 暗色布局。桌面和手机截图下载自 Actions 的 `ui-check` 产物。失败时还会保留浏览器追踪记录。

本地运行同一检查：

```bash
pnpm --dir docs install --frozen-lockfile
pnpm --dir docs exec playwright install --only-shell chromium
pnpm --dir docs build
pnpm --dir docs ui:check
```

检查使用本次构建的页面和素材。截图用于人工复查对齐、层级和视觉效果。
