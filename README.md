<p align="center">
  <strong>Clean Code Reviewer</strong>
</p>

<p align="center">
  <em>格式交给机器，逻辑留给人类。</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/rules-350%2B-green.svg" alt="350+ 条规则">
  <img src="https://img.shields.io/badge/levels-L1%E2%80%93L5-orange.svg" alt="L1–L5 严格度">
</p>

把《Clean Code》《Clean Architecture》《The Pragmatic Programmer》三本书的 350 多条规则，装进 Claude Code 的代码审查。审查前先问你三个问题，决定这条代码配得上多严格的标准，然后按 15 点清单走查，最后给一份只含结论的报告。

不检查格式。那属于 linter 和 formatter 的活。这里只看逻辑、设计与架构。

## 为什么用它

- **每条结论都能溯源。** 报告里的问题都标注规则编号（CC-## / CA-## / PP-##），对应参考文档里的原文。
- **严格度可以调。** 3+4+2 问卷把标准从 L1（实验室脚本）校准到 L5（金融、医疗级）。同一个 skill，审玩具项目不小题大做，审核心依赖不放水。
- **懂语言差异。** 书里规则大多是 Java 场景。skill 按范式调整：Java/C# 全量适用，TypeScript、Python、Kotlin 做适配，Rust、Go 和函数式语言另有一套。
- **结论有优先级。** 每个 Critical/Important 问题附带 Effort（改起来多费劲）和 Benefit（改了值多少），团队照此排修复顺序。
- **报告里没有废话。** 不夸优点，不写"整体不错"。只有问题清单加一个最终裁决。

## 对比

普通 `"review this code"` 得到的往往是一段泛泛的点评：

> 代码整体不错，但有些函数偏长，命名可以更好，建议考虑抽象……

Clean Code Reviewer 的输出是：

> **L3 Team** · Critical 1 / Important 1 / Minor 1
>
> - **[user.ts:45] SQL 查询用字符串拼接构造** — Critical · PP-72 · 注入风险 · Effort Low / Benefit High
> - **[helpers.ts:120] 函数 8 个参数** — Important · CC-26 · 超出 L3 阈值（≤5）· Effort Medium / Benefit Low
> - **[helpers.ts:42] 魔法数字 86400 未命名** — Minor · CC-175
>
> 裁决：⚠️ Needs fixes

## 工作方式

审查前先校准严格度，回答三个问题：

1. 谁用这份代码？自己 / 团队内部 / 外部用户
2. 想要什么标准？能跑就行 / 基本质量 / 仔细审查 / 最高标准
3. （条件触发）多关键？普通功能 / 核心依赖，坏了就出事故

组合出 L1–L5 五档。跳过校准也行，默认按 L3（团队）审查。

校准之后走 15 点清单：正确性与错误路径、命名与注释、职责与依赖方向、测试，以及 L3 以上的进阶项（并发安全、安全验证、资源释放、算法复杂度）。发现的问题按严重度分级，Critical/Important 附带 Effort/Benefit，最后按裁决标准收尾。

## 安装

需要 Node.js（用来跑 npx）。安装工具是 Vercel Labs 的 [skills](https://github.com/vercel-labs/skills) CLI，它从仓库读取 `skills/clean-code-reviewer/`，放进对应 agent 的目录。

```bash
# 安装到当前项目（自动识别你的 agent）
npx skills add R-jed/clean-code-reviewer

# 全局安装，所有项目可用
npx skills add R-jed/clean-code-reviewer -g

# 指定某个 agent
npx skills add R-jed/clean-code-reviewer --agent claude-code
```

skill 统一装到 `.agents/skills/`（universal，适配 20+ 种 agent），Claude Code、Cursor、Codex 等通过符号链接接入（如 `.claude/skills/`）。加 `-g` 装到用户级目录（`~/.agents/skills/`，Claude Code 链接到 `~/.claude/skills/`）。

## 更新

```bash
# 更新（CLI 会询问安装范围）
npx skills update clean-code-reviewer

# 更新全局安装
npx skills update clean-code-reviewer -g
```

## 使用

安装后直接说需求即可触发：

- "review this PR" / "review this code" / "check code quality"
- "这段代码能上线吗" / "检查一下有没有 bug"
- "ready to merge?" / "technical debt"

也可以指定范围：整个仓库、单个文件、或某次提交的 diff。审查对象超过该级别允许的规模时，skill 会把它标出来。

## 目录结构

```
.
├── skills/
│   └── clean-code-reviewer/   # skill 本体
│       ├── SKILL.md           # 主文件：工作流、清单、报告模板
│       ├── docs/              # 功能说明、度量阈值、定位系统、规则来源
│       ├── references/        # 三本书规则原文、语言调整、快速查询
│       └── scripts/           # 校验脚本
├── LICENSE
└── README.md
```

## 开发

校验 skill 结构是否合法：

```bash
python3 skills/clean-code-reviewer/scripts/validate_skill.py skills/clean-code-reviewer
```

## FAQ

**和 linter 有什么区别？** linter 管格式、命名、未用变量。这个 skill 只看机器看不出来的东西：逻辑正确性、设计决策、架构对齐。

**支持哪些语言？** 按范式调整。Java/C# 全量适用；TypeScript、Python、Kotlin 做适配；Rust、Go 和函数式语言各有调整。详见 `references/language-adjustments.md`。

**审查会不会太严格？** 3+4+2 问卷把标准压到 L1 时，只关心"能不能跑"。同一个 skill，两种用法。

**需要联网吗？** 不需要。安装后所有规则和参考都在本地文件里。

**零问题算通过吗？** 算。没有问题就报告零问题，这是合法结果，不为了凑数硬挑毛病。

## License

MIT，见 [LICENSE](LICENSE)。
