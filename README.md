**简体中文** | [English](README.en.md)

# Tech Prose

审阅、润色、起草技术文字的 agent skill。覆盖文档、代码注释与 docstring、界面与 CLI 文案、提交信息与 PR 描述、AI 指令文件，中文和英文都处理。

默认只改表达，不动事实：数字、版本、限额、标识符、路径，以及 `必须`/`建议`/`允许` 这类规范强度逐字保留。结构调整只提建议，动手需要你明确要求。

## 安装

需要 Node.js 22.20 或更高版本。

```bash
npx skills add kuoruan/tech-prose           # 交互选择安装到哪些 agent
npx skills add kuoruan/tech-prose -g        # 全局安装，所有项目可用
npx skills add kuoruan/tech-prose --skill tech-prose -a claude-code
```

安装路径遵循 `skills` CLI 的约定：Claude Code 写入 `.claude/skills/`，Codex、Cursor、Pi 等写入 `.agents/skills/`；加 `-g` 则写入用户目录。其他 agent 的支持情况见 [skills CLI 的 agent 列表](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)。

不安装也可以试用：

```bash
npx skills use kuoruan/tech-prose@tech-prose
```

## 怎么用

装好后直接提要求，输出形式由请求决定。

审阅只列问题，不改文件：

```text
看看这份部署文档有没有问题，先别改。
```

输出是 `路径:行号`、问题、依据和建议。

润色返回改写后的文字：

```text
润色一下这段安装说明，数字和版本别动。
```

原文没有、要求起草时返回正文：

```text
按现有代码给这个接口写一段 API 参考。
```

`SKILL.md` 的 `description` 把适用范围限定为用户明确要求审阅、润色、精简或起草技术文字；普通编码、调试和重构不会触发它。是否自动触发取决于所用的 agent。

## 解决什么问题

| 问题 | 这个 skill 的做法 |
| --- | --- |
| AI 腔：铺垫开场、“不是 X 而是 Y”、排比三连、空泛评价、伪造重要性 | 删掉不含信息的部分，或换成具体的事实与条件 |
| 改措辞时把语义关系改坏：条件范围、否定范围、因果、指代 | 改写前先确认这几项还在原处 |
| 事实漂移：数字、版本、`MUST`/`SHOULD` 强度、不确定性被悄悄改成确定 | 逐字保留；可选脚本标出需要人工复核的项 |
| 越界：把“太长”“精简”“易读”当成搬动章节的授权 | 只改措辞，结构问题列成建议 |

## 改写示例

下面是人工构造的示意文本，不是模型运行记录。缺陷集中在框架句，承载技术事实的句子没有改动。

原文：

> 随着业务的发展，缓存层已经成为系统中不容忽视的关键环节。它不仅仅是缓存，更是稳定性的基石。为了提升可靠性，我们建议对现有的失效策略进行优化：当 fallback 未配置时，缓存失效会导致请求失败；只有在配置了 fallback 的情况下，服务才会降级。重试次数不能超过 3 次。

改写：

> 为了提升可靠性，我们建议优化现有的失效策略：当 fallback 未配置时，缓存失效会导致请求失败；只有在配置了 fallback 的情况下，服务才会降级。重试次数不能超过 3 次。

删掉的是两句框架句：一句是铺垫开场，连同 `不容忽视` 这类评价；另一句是“不只是缓存而是基石”的对偶。`进行优化` 改为 `优化`，删掉套壳后原意不变。

其余内容原样保留：目的、两个条件、“只有…才”的关系，以及 `不能超过 3 次` 的强度。

`check_rewrite.py` 对这对文本报 `RESULT: PASS`。它标出需要人工复核的项，不作语义等价的判决。

## 不做什么

- 不重构代码，不改公共 API 契约；精简注释不等于重构。
- 不擅自换语言。中英混排的文档，优化英文段落不等于把它译成中文。
- 不补材料里没有的细节：异常类型、并发保证、边界行为都标成缺口。
- 不删限制、前提、例外和回滚说明。
- 重排章节、拆分或合并文档要你明确要求。

## 结构

```
skills/tech-prose/
├── SKILL.md                    入口：动作判定、保护边界、按需加载、自检
├── references/
│   ├── carriers/               载体规则：文档 / 注释 / 界面文案 / AI 指令 / 提交信息
│   ├── languages/              语言规则：中文 / 英文
│   └── tasks/structure.md      结构调整（需明确要求）
└── scripts/check_rewrite.py    事实、规范强度、不确定性、代码一致性的复核脚本
```

载体决定写什么，语言决定怎么写，两者正交。`SKILL.md` 只放跨载体的判据，各载体文件只写差异。

## 更新

```bash
npx skills check    # 查看是否有新版本
npx skills update   # 更新已安装的技能
```

版本记录在 `SKILL.md` 的 `metadata.version`；`skills` CLI 按整个技能文件夹的内容哈希判断更新。

## 开发

```bash
python3 scripts/validate.py                    # 校验 frontmatter、引用路径、脚本可编译
python3 skills/tech-prose/scripts/check_rewrite.py <原文> <改写>
python3 -m unittest discover -s tests -v          # 两个检查脚本的回归测试
```

改动规则前先读 `skills/tech-prose/SKILL.md` 的“改动前的三个判断”，并保持 `references/` 内的路径相对 `SKILL.md`。CI 在每次 push 和 PR 上跑同一份校验。

## License

MIT
