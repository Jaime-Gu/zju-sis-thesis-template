# 主论文模板：Agent 操作说明

在本文件所在目录执行命令。此目录可单独复制和解压，不依赖上级仓库。

## 文件与输出

```text
main-thesis-template/
├── 论文信息.md
├── 论文.md
├── images/
├── scripts/build.py
├── template/thesis-main.tex
├── template/zju-thesis.sty
├── template/assets/
├── 生成论文.command
├── 生成论文.bat
├── 使用说明.md
└── output/毕业论文.pdf
```

只编辑 `论文信息.md`、`论文.md` 和 `images/`。不要手改 `build/`。排版改动在 `template/`，构建逻辑在 `scripts/build.py`。

本包包含主封面、总目录、承诺书、致谢、中西文摘要、正文目录、正文、参考文献、可选附录和作者简介；不含任务书、考核表、文献综述、开题报告、外文翻译和书脊。

## 环境与构建

需要 Python 3、Pandoc、XeLaTeX、模板所用 TeX 宏包和中文字体、Times New Roman。Typora 不是构建依赖。

```bash
# macOS
python3 scripts/build.py --check
python3 scripts/build.py

# Windows
python scripts\build.py --check
python scripts\build.py
```

`--check` 会执行最小编译，完整命令会运行三次 XeLaTeX。Agent 不要调用会等待回车的 `.command` 或 `.bat`。

成功标志：

```text
生成完成：output/毕业论文.pdf
```

失败返回非零退出码，旧文件移至 `output/毕业论文.previous.pdf`。成功后自动删除备份。

## 论文信息

`论文信息.md` 使用 UTF-8 和 `字段名：字段值`。以下字段均必填，字段名不可改：

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

`论文性质`只能为`公开`或`涉密`。支持中英文冒号；忽略空行、`#` 开头行和 HTML 注释。字段值中的 LaTeX 特殊字符会自动转义。

## 论文.md 分区

必须按顺序保留 7 个独立行标记，不能缺少、重复或改名：

```text
【致谢】
【西文摘要】
【中文摘要】
【正文】
【参考文献】
【附录】
【作者简介】
```

不需要附录或作者简介时，保留标记并清空其下内容。`<!-- ... -->` 不进入 PDF。

前置部分使用罗马页码，正文从阿拉伯数字 1 开始。正文一级标题从奇数物理页开始。附录和作者简介不显示页眉页码，也不消耗正文页码。

## Markdown 规则

标题使用 `#`、`##`、`###`、`####`，`#`后有空格，不写章节编号。正文直接书写，段落之间空一行，不用空格或空行控制缩进和分页。

摘要关键词：

```text
Palabras clave: Español; chino mandarín; difusión internacional
关键词：西班牙语；汉语普通话；国际传播
```

【参考文献】每条单独一行，不写序号。脚本只生成 `[1]`、`[2]` 和悬挂缩进，不自动整理作者、年份、文献类型、卷期页码或标点；这些必须由作者按学院要求填写。

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

公式与行内变量：

```markdown
$$
U = 3X
$$

La variable $U$ representa ...
```

图表和独立公式自动编号。长引用使用 `>`，脚注使用 `[^1]` 与 `[^1]: 说明`。表题、来源和关键词中的 `&`、`%`、`#`、`_` 等直接输入，不要手动加反斜杠。

内部链接使用 Markdown 锚点，例如 `[查看本章](#introduction)`。跨分区链接使用分区前缀，例如 `#body-introduction`、`#references-entry`。

## 验收与排错

每次修改后完整构建。检查输出 PDF 能打开，并检查日志：

```bash
# macOS；无输出表示未匹配到这些错误
grep -E "LaTeX Error|undefined|multiply defined|Overfull|LaTeX Font Warning" build/thesis.log || true

# Windows
findstr /C:"LaTeX Error" /C:"undefined" /C:"multiply defined" /C:"Overfull" /C:"LaTeX Font Warning" build\thesis.log
```

还需核对封面字段、总目录和正文目录、页码、图表公式、附录和作者简介页眉页码。模板改动后渲染查看封面、目录和正文图表页，不能只看退出码。

详细日志在 `build/xelatex-pass-N.txt`、`build/thesis.log`；最小编译失败时查看 `build/environment-check.txt`。

已验证环境：macOS arm64、Python 3.9.6、Pandoc 3.13、XeTeX 2026。Windows 入口已实现，尚未完成 Windows + MiKTeX 实机验证。
