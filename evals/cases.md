# 评测案例

全部案例均为人工构造。本文件的状态标记统一保留为**未运行**，具体运行结果另行记录。运行和隔离方式见 [README.md](README.md)。每例的判据仅供评测者使用，不放进被测模型的上下文；不要把整份文件作为输入。

## E1：审阅只读与结构判据

请求：

> 看看 deploy.md 的措辞和结构有没有问题，先别改文件。

输入 `deploy.md`：

```markdown
# 部署

## 开始

执行 `deploy --env staging`。

## 前置条件

部署前必须获得 staging 的写入权限。
```

判据：

- 契约：文件内容与清单不变，不执行输入命令。
- 语义：指出前置条件应在操作前出现，只给建议，不自行为命令增加参数或安全保证。
- 质量：使用文件与行号定位；不把审阅输出变成重写正文。

## E2：合格原文不强改

请求：

> 润色 limits.md；没有具体问题就告诉我无需修改。

输入 `limits.md`：

```markdown
# 请求限制

每个工作区最多创建 20 个任务。达到上限后，必须先删除已有任务，才能创建新任务。
```

判据：

- 契约：原文不变，不增删文件。
- 语义：不虚构新的配额、软删除、恢复或扩容能力。
- 质量：允许并优先接受“无需修改”；不为追求不同措辞而改写。

## E3：对象、条件、否定和不确定性保真

请求：

> 精简 limits.md 的中英文说明，删除套话，保持原文语言与全部技术信息。

输入 `limits.md`：

```markdown
# 限制

为了给您带来无缝的体验，我们在此对限制进行说明。上传超时为 30 秒，查询超时为 5 秒。只有启用 fallback 时才允许降级；并非所有失败都可以重试。管理员可绕过 20 个任务的限制，但不能绕过超时。高负载下可能延迟，尚未压测确认。

Uploads MUST finish within 30 seconds; queries SHOULD finish within 5 seconds. A timeout does not mean that all writes failed. Retry safety is unverified.
```

判据：

- 契约：数字和规范词原样保留，中英文段落各保留原语言。
- 语义：上传对应 30 秒、查询对应 5 秒；20 个任务的例外只适用于管理员，不扩到超时；保留“只有”“并非所有”“可能”“尚未确认”与英文否定、未验证信息。
- 质量：删减无信息套话即可；不靠数值集合相同判定通过。

## E4：精简不授权章节重组

请求：

> guide.md 太长了，帮我精简一下，直接改文件。

输入 `guide.md`：

```markdown
# 任务管理

## 删除

在当前情况下，用户可以通过单击“删除任务”来执行删除任务这一操作。已删除的任务不能通过界面恢复。

## 创建

为了完成任务的创建，请单击“创建任务”。
```

判据：

- 契约：标题、层级、顺序与文件路径不变，不新建或拆分文件。
- 语义：保留“不能通过界面恢复”，不扩大成“任何方式都不可恢复”；不新增确认或撤销能力。
- 质量：允许局部拆句、分点；结构建议与已授权的措辞编辑分开，不将创建节搬到删除节前。

## E5：混合语法与英文占位符

请求：

> 润色 page.mdx 的英文正文和表格里的界面文案。不要改 frontmatter、组件、锚点或模板语法，代码块也不改。

输入 `page.mdx`：

````mdx
---
title: Delete project
description: Project deletion reference
slug: delete-project
---

<a id="delete-project" />

## Delete project

In order to proceed with the deletion of the project, select Delete project. Recovery is unavailable in the interface.

<Callout type="warning">{messages.warning}</Callout>

| Key | Copy |
| --- | --- |
| deleting | Deleting %s… |
| deleted | Project {project_name} deleted. |

```sh
project delete --id "$PROJECT_ID"
```
````

判据：

- 契约：frontmatter、标题、锚点、组件、模板表达式、代码块和表格键名逐字不变；保留 `%s`、`{project_name}` 的格式和次数。
- 语义：只保留“界面中无法恢复”的范围，不断言所有渠道均不可恢复。
- 质量：只改确有冗余的正文；界面文案合格时不必改。保留有效 MDX 结构；如果没有构建环境，只能记录文本核对，不能声称构建通过。

## E6：起草的受众与操作完整性

请求（没有输入文件）：

> 给首次使用这个项目、已经会用终端的开发者写一段 staging 部署说明，只返回正文和缺口，不写文件。已知事实：在仓库根目录执行 `deploy --env staging --release <release_id>`；需要 staging 写入权限；`<release_id>` 替换为已批准的发布 ID；完成后终端打印 `Deployment queued`，这只表示已入队，不表示部署成功。后续成功判定和失败恢复方式还没有材料。不要执行命令。

判据：

- 契约：工作区不变，不执行命令；命令与输出原样保留。
- 语义：说明根目录、权限及占位替换；准确区分入队与成功；成功判定及恢复方式列缺口，不编造 URL、查询命令或重试安全性。
- 质量：按既定受众起草，不重复解释终端基础，不固定追问受众问卷，不为缺事实留下未标注的可发布承诺。

## E7：非视觉定位与缺少图片材料

请求：

> 审阅 help.md 的易读性和无障碍表达，不改文件。截图没有提供；已确认界面里提交按钮的可见名称是“保存更改”。

输入 `help.md`：

```markdown
# 保存设置

点击右侧绿色按钮。

成功条件见下图中的红框。

![界面截图](settings.png)
```

判据：

- 契约：工作区不变，不创建截图或改写图像文件。
- 语义：建议用已知名称“保存更改”定位；指出成功条件和图片替代说明缺少可核实材料，不猜红框内容或成功提示。
- 质量：不将所有“下图”一概判错，不要求机械抄录图片全部内容。

## E8：按指定版本起草发布说明

请求：

> 根据 CHANGELOG.md 起草 v3.0.0 的 GitHub Release 正文，直接给正文和缺口，不写文件，不执行发布命令。

输入 `CHANGELOG.md`：

```markdown
# Changelog

## Unreleased

- 计划在 4.0.0 默认启用 `--legacy-parser`。

## 3.1.0-rc.1

- 新增实验性的批量导入接口，行为可能变化。

## 3.0.0

### Changed

- **破坏性变更**：配置键 `output` 改名为 `outputs`。旧键不再读取，升级时必须改用 `outputs`。
- `legacyMode` 已废弃，目前仍可使用，4.0 起移除。
- 单次导入上限从 1000 条降到 500 条，超过时返回 `413`。

### Fixed

- 修复并发写入时偶发丢失最后一条记录；根因尚未确认。

## 2.9.1

- 修复超时后重复重试。
```

判据：

- 契约：工作区不变，不新建文件，不执行任何发布或版本命令。
- 语义：只取 3.0.0 的条目，不混入 `Unreleased`、3.1.0-rc.1 与 2.9.1；保留 `output`→`outputs`、旧键不再读取与必须迁移的要求、`legacyMode` 尚可使用但 4.0 起移除、1000 条降至 500 条的变化、`413`，以及并发问题“根因尚未确认”；不编 PR、贡献者与比较链接，不写“向后兼容”“性能提升”这类原文没有的保证。
- 质量：整理为面向升级者的正文，破坏性影响与必要动作易找；不强制新增固定章节，正文与缺口分开。

## E9：片段正文与机器字段分开

请求：

> 直接改这两个发布片段的正文，只动文字，不动机器字段和文件名，不新建或删除文件。

输入 `.changeset/brave-lions-sing.md`：

```markdown
---
"@acme/core": minor
"@acme/cli": patch
---

我们非常高兴地宣布，本次发布对批量导入功能进行了全面支持，为用户带来了更加便捷高效的数据导入体验。需要说明的是，当单次导入超过 500 条时会返回 `413`，该上限尚未在压测环境中验证。
```

输入 `releasenotes/notes/multi-output-4f2a9c1b7d.yaml`：

```yaml
---
features:
  - |
    We are thrilled to introduce comprehensive support for multiple output
    targets. When more than one target is configured, the writer emits to each
    target in turn; if the first target fails, the remaining targets are skipped.
upgrade:
  - >
    The ``output`` key is now ``outputs``. The old key is still read in 2.4 and is
    removed in 2.6.
fixes:
  - >
    Empty batches are now accepted; they previously raised a validation error.
```

判据：

- 契约：两个文件名不变；Changesets 的包名、`minor`/`patch` 与头部元数据分隔线逐字保留；Reno 的键名、`|` 与 `>`、缩进、列表结构及 RST 双反引号标记不变；正文语言各自保留，不新建或删除片段文件。
- 语义：保留 500 条上限、`413` 与“尚未在压测环境中验证”；保留多目标依次写入、首个失败后跳过其余目标的条件；保留 `output`→`outputs`、2.4 仍读取旧键、2.6 移除的版本关系，以及空批次此前报错这一对照；不编最终发布版本、发布日期或“已发布”。
- 质量：只删夸张与套话；保留 RST 语法，不把 `|` 与 `>` 互换，不把 YAML 值改成 Markdown 列表。

## E10：润色生成的变更日志

请求：

> 直接改 CHANGELOG.md 的条目文字，保留生成格式；不要改写成 Keep a Changelog，也不要合并或重排历史版本。

输入 `CHANGELOG.md`：

```markdown
# Changelog

<!-- 此文件由 release-please 生成，请勿手动编辑 -->

## [2.4.0](https://github.com/acme/core/compare/v2.3.1...v2.4.0) (2026-05-02)

### Features

* **cli:** 新增 `--output-dir` 参数，用户可以更加灵活地指定输出位置 ([#812](https://github.com/acme/core/pull/812))
* **core:** 对批量导入链路进行了深度优化，性能表现十分出色 ([#809](https://github.com/acme/core/pull/809))

### Bug Fixes

* **core:** 修复空批次导致的崩溃 ([#805](https://github.com/acme/core/pull/805))

### Bug Fixes

* **cli:** 修复 `--dry-run` 下仍写入文件的问题 ([#803](https://github.com/acme/core/pull/803))

## [2.3.1](https://github.com/acme/core/compare/v2.3.0...v2.3.1) (2026-04-18)

### Bug Fixes

* **core:** 修复超时后的重复重试 ([#798](https://github.com/acme/core/pull/798))
```

判据：

- 契约：生成器注释、版本号、比较链接、日期、分类标题（包括两个 `### Bug Fixes`）、条目里的 `**cli:**` 与 `**core:**` 归属和 PR 链接逐字保留；2.3.1 的历史条目不改；不新建或删除文件。
- 语义：不把“深度优化”“性能表现出色”补成具体指标、百分比或兼容承诺；没有依据时删掉评价或保留原样并列缺口，不编 CVE、发布日期或行为保证。
- 质量：只润色条目自身的冗余与夸张，不改成六类 Keep a Changelog 标题，不合并重复章节，不重排版本顺序。

## T：真实宿主触发请求

这些请求单独测试。正例使用前述对应输入；反例不需要文件。不显式提技能名，不能复用执行测试会话。按宿主可观察的加载证据判断，不按回答风格判断。

| ID | 请求 | 期望加载 tech-prose | 判定依据 |
| --- | --- | --- | --- |
| T1 | 看看 deploy.md 的措辞和结构有没有问题，先别改。 | 是 | 明确审阅技术文字，输入用 E1 |
| T2 | 润色 page.mdx 的英文正文，别碰代码和模板。 | 是 | 明确改写技术文字，输入用 E5 |
| T3 | 写一段 staging 部署说明，只用这些事实。 | 是 | 明确起草，附 E6 的已知事实和缺口 |
| T4 | 帮我定位部署命令返回 403 的原因，先查权限配置，不用改文案。 | 否 | 技术诊断，不是文字审阅 |
| T5 | 把这句话翻译成中文：Retry safety is unverified. | 否 | 纯翻译，超出技能范围 |
| T6 | 重构错误处理，把重复的报错拼接逻辑提成函数，不调整提示内容。 | 否 | 代码重构，不是文案修改 |

触发“否”只表示不应加载这个技能，不限制宿主使用其他适合的工具或技能。缺少可观察的加载证据时记“不可判定”，不要将未观察到直接记成未触发。
