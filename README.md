# Agent 操作手册

本仓库包含两个相互独立的 Markdown → PDF 模板。操作时先进入对应子目录，不要在上级目录直接运行 `scripts/build.py`。

## 1. 模板与输出

| 目录 | 内容 | 输出 |
| --- | --- | --- |
| `main-thesis-template/` | 主封面、总目录、承诺书、致谢、中西文摘要、正文目录、正文、参考文献、可选附录和作者简介 | `output/毕业论文.pdf` |
| `review-proposal-template/` | 文献综述封面、指导教师要求、文献综述、开题报告、外文翻译和外文原文 | `output/开题和文献综述.pdf` |

两个包均不含任务书、考核表和书脊。每个包有自己的 `论文.md`、`论文信息.md`、脚本、模板、图片和输出目录，可以单独复制或解压使用。

包内 PDF 是示例。正式使用前必须替换示例内容并重新生成。`build/` 是中间目录，不要手改。

## 2. 文件结构

每个子包的结构如下：

```text
模板目录/
├── README.md                 Agent 操作说明
├── 使用说明.md               人工操作说明
├── 论文信息.md               封面等字段
├── 论文.md                   全部可编辑正文
├── 生成论文.command          macOS 双击入口
├── 生成论文.bat              Windows 双击入口
├── images/                   插图
├── scripts/build.py          环境检查与完整构建
├── template/
│   ├── thesis-main.tex       页面装配顺序
│   ├── zju-thesis.sty        字体、页面、目录和图表格式
│   └── assets/               校名和校徽图片
├── output/                   生成的 PDF
└── 外文原文.pdf              仅开题包使用的可选附件
```

仓库根目录另有：

- `使用说明.md`：两个包的人工安装和使用说明。
- `scripts/package.py`：分别生成两个发布 ZIP。

不要用示例文件覆盖用户已经填写的论文内容。

## 3. 环境与检查

需要 Python 3、Pandoc、XeLaTeX、`ctex`/`xeCJK`/`fandol` 等 TeX 宏包和中英文字体，以及 Times New Roman。Typora 只是人工编辑器，不是构建依赖。

在对应模板目录运行：

```bash
# macOS
python3 scripts/build.py --check

# Windows
python scripts\build.py --check
```

该检查会执行一次真实的最小 XeLaTeX 编译。成功后仍需做一次完整示例构建。

macOS 直接调用脚本时，如找不到 TeX，可先执行：

```bash
export PATH="/Library/TeX/texbin:$HOME/Library/TinyTeX/bin/universal-darwin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
```

已验证环境：macOS arm64、Python 3.9.6、Pandoc 3.13、XeTeX 2026（TeX Live 2026）。Windows 入口和命令已实现，但 Windows + MiKTeX 尚未实机验证。

## 4. 完整构建

Agent 使用非交互命令，不要调用会等待回车的 `.command` 或 `.bat`。

```bash
# 主论文包
cd main-thesis-template
python3 scripts/build.py

# 开题和文献综述包
cd ../review-proposal-template
python3 scripts/build.py
```

Windows 使用 `python scripts\build.py`。

脚本依次检查依赖、校验字段和分区、用 Pandoc 转换 Markdown、替换模板字段，并连续运行三次 XeLaTeX。成功标志分别是：

```text
生成完成：output/毕业论文.pdf
生成完成：output/开题和文献综述.pdf
```

失败时返回非零退出码。旧 PDF 会改名为对应的 `.previous.pdf`，成功生成新文件后自动删除备份；不要仅凭 PDF 文件存在判断本次成功。

## 5. 输入规则

### 5.1 论文信息

两个包均使用 `字段名：字段值`，字段名不可修改且不能为空：

```text
西语题目：...
中文题目：...
姓名：...
学号：...
指导教师：...
年级与专业：...
所在学院：...
提交日期：...
论文性质：公开
```

开题包额外保留：

```text
起始页码：15
```

`论文性质`只能是`公开`或`涉密`。文件使用 UTF-8；支持中文或英文冒号，忽略空行、`#` 开头行和 HTML 注释。字段值中的 LaTeX 特殊字符由脚本转义。

### 5.2 主论文包分区

`main-thesis-template/论文.md` 必须按以下顺序保留 7 个独立行标记：

```text
【致谢】
【西文摘要】
【中文摘要】
【正文】
【参考文献】
【附录】
【作者简介】
```

不需要附录或作者简介时，保留标记并清空该标记下的示例内容。程序会跳过空部分。

前置部分使用罗马页码，正文从阿拉伯数字 1 开始。附录和作者简介不显示页眉页码，也不消耗正文页码。正文一级标题按双面排版规则从奇数物理页开始。

### 5.3 开题包分区

`review-proposal-template/论文.md` 必须按以下顺序保留 5 个独立行标记：

```text
【指导教师要求】
【文献综述】
【开题报告】
【外文翻译】
【外文原文】
```

文献综述、开题报告和外文翻译分别从 1 开始章节编号。文献综述页码由`起始页码`决定，后续部分连续编号；封面和指导教师要求不显示页眉页码。

### 5.4 标题与正文

```markdown
# 一级标题

## 二级标题

### 三级标题

#### 四级标题
```

`#`后必须有空格。不要手写章节编号。普通文字直接书写，段落之间空一行；不要用段首空格控制缩进，也不要用连续空行控制分页。`<!-- ... -->` 不进入 PDF。

摘要关键词分别使用：

```text
Palabras clave: Español; chino mandarín; difusión internacional
关键词：西班牙语；汉语普通话；国际传播
```

### 5.5 参考文献

主论文包【参考文献】中每条单独一行，不写序号：

```text
Baker, M. Routledge Encyclopedia of Translation Studies[M]. Shanghai: Shanghai Foreign Language Education Press, 2010.
Cooper, R. L. A Framework for the Study of Language Spread[J]. Language Spread: Studies in Diffusion and Social Change, 1982, 5: 36.
```

脚本只自动生成 `[1]`、`[2]` 等编号和悬挂缩进，不自动判断文献类型或重排作者、年份、标点。学生必须按学院格式填写每条文献。

开题包的文献综述和开题报告参考文献属于普通正文，`[1]`、`[2]` 和整条格式均由作者维护。文内引用也按普通文字填写，例如 `(Cooper 1982:13)`。

### 5.6 图片、表格、公式和引用

图片：

```markdown
![图题，不写图号](images/mi-figura.png){width=12cm}

Fuente: Elaboración propia.
```

表格：

```markdown
| Partes | Aspectos |
|:---|:---|
| Tracción del mercado | General |

Tabla: 表题，不写表号

Fuente: Elaboración propia.
```

公式：

```markdown
$$
U = 3X
$$
```

行内公式使用 `$U$`。图号、表号和独立公式编号自动生成。大表需要人工拆分，不能保证超过一页的表格自动完整放入一页。

长引用使用 Markdown 引用块 `>`；脚注使用 `[^1]` 和 `[^1]: 脚注说明`。内部链接可使用 `[跳转到本章](#introduction)`；跨分区链接需使用目标分区前缀，例如 `#body-introduction`、`#review-introduction`。

表题、来源和关键词中的 `&`、`%`、`#`、`_`、`{`、`}` 按普通文字输入，不要自行添加反斜杠。

### 5.7 外文翻译与原文

【外文翻译】和【外文原文】的文章标题使用：

```text
Title: Apuntes sobre el valor económico del español
```

该标题居中、加粗且不编号。其内部章节仍用 `#`、`##`，但不会收入主论文目录。

开题包根目录存在 `外文原文.pdf` 时，程序在 `Texto de origen` 标题页后插入整份 PDF，忽略【外文原文】的 Markdown 内容；插入页不额外添加模板页眉页码。不存在该文件时，排版【外文原文】中的文字。

## 6. 修改模板与验收

页面装配在各自的 `template/thesis-main.tex`，格式在 `template/zju-thesis.sty`，解析和构建在 `scripts/build.py`。只输出 PDF，不输出 DOCX；不执行篇幅、文献数量、外文文献数量或文献比例检查。

每次改动后必须完整构建，并检查：

```bash
# macOS；无输出表示未匹配到这些错误
grep -E "LaTeX Error|undefined|multiply defined|Overfull|LaTeX Font Warning" build/thesis.log || true

# Windows
findstr /C:"LaTeX Error" /C:"undefined" /C:"multiply defined" /C:"Overfull" /C:"LaTeX Font Warning" build\thesis.log
```

还需检查输出 PDF 能打开、字段无示例残留、标题与页码正确、图表公式编号正确、图片未越界。模板改动后要渲染查看封面、目录、正文图表页及各部分首页，不能只看退出码。

失败日志依次查看：

1. 命令完整输出；
2. `build/xelatex-pass-N.txt`；
3. `build/thesis.log` 中第一个以 `!` 开头的错误；
4. 最小编译失败时的 `build/environment-check.txt`。

## 7. 发布打包

在仓库根目录运行：

```bash
python3 scripts/package.py
```

Windows 使用 `python scripts\package.py`。脚本在仓库同级目录生成：

```text
main-thesis-template.zip
review-proposal-template.zip
```

ZIP 内分别以对应模板目录为根目录。脚本排除 `.git/`、`build/`、`__pycache__/`、`.DS_Store`、`__MACOSX/` 和 `.previous.pdf`，并执行 CRC 和目录检查。中文文件名使用 UTF-8 标志。发布前应解压两个 ZIP，分别执行完整构建。
