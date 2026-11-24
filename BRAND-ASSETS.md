# 品牌资产清单

本表记录自有项目和组织的**现役标识**。多个项目共用同一标识时，直接引用同一份素材。品牌条目以 `brand/*.json` 为准，画廊、评审页与 README 均由它生成。

## GitHub 组织

| 组织 | 现役标识 |
|---|---|
| [cortexos-dev](https://github.com/cortexos-dev) | `cortexos-dev/logo.svg` |
| [museav-ai](https://github.com/museav-ai) | `museav-ai/logo.svg` |
| [supercli-site](https://github.com/supercli-site) | `supercli/mark-v3.svg` + `supercli/mark-v3-dark.svg` |
| [xianling-music](https://github.com/xianling-music) | `xianling-music/logo-light.svg` + `xianling-music/logo-dark.svg` |

## 项目标识

| 项目 | 现役标识 | 状态 |
|---|---|---|
| chat-mood-gen | `chat-mood-gen/mark-v3.svg` + `chat-mood-gen/mark-v3-dark.svg` | 定稿 |
| claude-usage-statusline | `claude-usage-statusline/mark-v3.svg` + `claude-usage-statusline/mark-v3-dark.svg` | 定稿 |
| device-passport | `device-passport/mark-v3.svg` + `device-passport/mark-v3-dark.svg` | 定稿 |
| dsh-llm-hub | `dsh-llm-hub/mark-v3.svg` + `dsh-llm-hub/mark-v3-dark.svg` | 定稿 |
| dsh-museav-assets | `dsh-museav-assets/mark-v3.svg` + `dsh-museav-assets/mark-v3-dark.svg` | 待评审 |
| facet | `facet/mark-v3.svg` + `facet/mark-v3-dark.svg` | 定稿 |
| free-imgbed | `free-imgbed/mark-v3.svg` | 定稿 |
| jianpu-editor | `xianling-music/logo-light.svg` + `xianling-music/logo-dark.svg` | 复用仙灵音乐组织标识 |
| lite-browser | `lite-browser/mark-v3.svg` + `lite-browser/mark-v3-dark.svg` | 待评审 |
| logo-brand-designer | `logo-brand-designer/mark-v3.svg` + `logo-brand-designer/mark-v3-dark.svg` | 待评审 |
| meridian | `meridian/mark-v3.svg` + `meridian/mark-v3-dark.svg` | 待评审 |
| museav-cli | `museav-cli/mark-v3.svg` + `museav-cli/mark-v3-dark.svg` | 待评审 |
| plugins | `plugins/mark-v3.svg` + `plugins/mark-v3-dark.svg` | 待评审 |
| pr-contributor-skill | `pr-contributor-skill/mark-v3.svg` + `pr-contributor-skill/mark-v3-dark.svg` | 待评审 |
| reel-kit | `reel-kit/mark-v3.svg` + `reel-kit/mark-v3-dark.svg` | 定稿 |
| scorecard | `scorecard/mark-v3.svg` + `scorecard/mark-v3-dark.svg` | 定稿 |
| supercli | `supercli/mark-v3.svg` + `supercli/mark-v3-dark.svg` | 定稿 |
| typora-bloom-theme | `typora-Bloom-theme/mark-v3.svg` + `typora-Bloom-theme/mark-v3-dark.svg` | 待评审 |
| vite-plugin-agent-eyes | `vite-plugin-agent-eyes/mark-v3.svg` + `vite-plugin-agent-eyes/mark-v3-dark.svg` | 定稿 |
| voxflow | `voxflow/mark-v3.svg` + `voxflow/mark-v3-dark.svg` | 定稿 |
| wallpaper-generator | `wallpaper-generator/mark-v3.svg` + `wallpaper-generator/mark-v3-dark.svg` | 定稿 |
| webkubor | `webkubor/mark-v3.svg` + `webkubor/mark-v3-dark.svg` | 待评审 |

## 版本策略

- 图床只保留每项目的现役 logo；替换完成后清理弃用的旧版、过渡版和草稿。
- 替换标识时**先迁移使用方**（各项目 README、站点、博客数据），确认无引用后再移除旧文件。
- 深浅主题成对的文件（`mark-v3.svg` + `mark-v3-dark.svg`）视为同一版本，成对保留。
- banner、截图、favicon、OG 图不属于 logo，不在此表；也不自动冒充 logo。

## 评审与待设计

[现役标识评审](/design/logo-review.html)可查看每项的浅底/深底版本与 hex；[交付说明](design/DELIVERY.md)记录色板建议、检查范围与限制。

真实待设计项目见 [18 项设计任务](design/logo-briefs.html)；其中色板均标为待评审建议。`path-guard` 的定位以生产 README 的命令副本诊断为准，`release-sync-skill` 为版本台账同步；`ego-lite-ref` 为上游参照实现，不列入自有品牌委托。

## 待设计或核验

- **Bloom for Typora**：项目仅有花形 favicon；README 目前展示 banner，需按主题品牌另行确定正式字标或 logo。
- **Kyvault / xiaobai-kanban / boiling-snow**：README 顶部现有 banner/宣传图，不能仅凭文件名或 alt 文本认定它们是 logo。
- **有 banner、缺独立 logo**：Kyvault、xiaobai-kanban、Boiling Snow、Bloom for Typora、dsh-bloom-theme、ego-lite-ref。先保留现有 banner；在各项目确定专属视觉后再增补 logo。
- **未在 README 展示标识**：ai-orb、device-passport（已入库，README 仍使用 banner）、dsh-llm-hub（已入库，README 仍使用 R2 banner）。应用内部 favicon 不等同于 README 品牌图。
- **无可确认源图的自有项目**：ai-sse-kit、cs-mcp、ui-craft、im-notify-kit、mlx-vlm-kit、path-guard、charmoji-sticker-skill、deadcode-reaper-skill、release-sync-skill、writing-standard-skills、suno-publisher、vite-plugin-refresh-guard 等。先保留文本标题，不自动生成相同模板的占位 logo。

后续新增：先核对项目源文件、视觉用途及名称；优先用合格 SVG。新增后写入 `brand/*.json` 并在本表登记，迁移使用方引用，最后刷新画廊与评审页。U 盘原始素材不动。
