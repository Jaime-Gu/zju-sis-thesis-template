# 开题和文献综述模板：Agent 操作说明

在本文件所在目录执行命令。此目录可单独复制和解压，不依赖上级仓库。

## 文件与输出

```text
review-proposal-template/
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
├── output/开题和文献综述.pdf
└── 外文原文.pdf             可选，默认不存在
```

只编辑 `论文信息.md`、`论文.md`、`images/` 和可选的 `外文原文.pdf`。不要手改 `build/`。排版改动在 `template/`，构建逻辑在 `scripts/build.py`。

本包包含文献综述封面、指导教师要求、文献综述、开题报告、外文翻译和外文原文；不含主论文、任务书、考核表和书脊。

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
生成完成：output/开题和文献综述.pdf
```

失败返回非零退出码，旧文件移至 `output/开题和文献综述.previous.pdf`。成功后自动删除备份。

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
起始页码：15
```

`论文性质`只能为`公开`或`涉密`。`起始页码`是文献综述第一页的阿拉伯页码。支持中英文冒号；忽略空行、`#` 开头行和 HTML 注释。字段值中的 LaTeX 特殊字符会自动转义。

## 论文.md 分区

必须按顺序保留 5 个独立行标记，不能缺少、重复或改名：

```text
【指导教师要求】
【文献综述】
【开题报告】
【外文翻译】
【外文原文】
```

`<!-- ... -->` 不进入 PDF。文献综述从`起始页码`开始，开题报告、外文翻译和外文原文连续编号；封面和指导教师要求不显示页眉页码。各部分章节分别从 1 开始编号。

## Markdown 规则

标题使用 `#`、`##`、`###`、`####`，`#`后有空格，不写章节编号。正文直接书写，段落之间空一行，不用空格或空行控制缩进和分页。

文献综述和开题报告末尾的参考文献属于普通正文，`[1]`、`[2]` 和整条格式均由作者维护。脚本不会自动生成或整理这些参考文献格式。

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

【外文翻译】和【外文原文】的文章标题使用：

```text
Title: Apuntes sobre el valor económico del español
```

该标题居中、加粗且不编号。其内部章节仍使用 `#`、`##`。

根目录存在 `外文原文.pdf` 时，程序在 `Texto de origen` 标题页后插入整份 PDF，忽略【外文原文】的 Markdown 内容；插入页不额外添加模板页眉页码。不存在该文件时，排版【外文原文】中的文字。

内部链接使用 Markdown 锚点。跨分区链接使用 `review`、`proposal`、`translation`、`original` 等目标分区前缀，例如 `#review-introduction`。

## 验收与排错

每次修改后完整构建。检查输出 PDF 能打开，并检查日志：

```bash
# macOS；无输出表示未匹配到这些错误
grep -E "LaTeX Error|undefined|multiply defined|Overfull|LaTeX Font Warning" build/thesis.log || true

# Windows
findstr /C:"LaTeX Error" /C:"undefined" /C:"multiply defined" /C:"Overfull" /C:"LaTeX Font Warning" build\thesis.log
```

还需核对封面字段、起始页码、后续页码、图表公式和外文原文附件页序。模板改动后渲染查看封面、指导教师要求和各部分首页，不能只看退出码。

详细日志在 `build/xelatex-pass-N.txt`、`build/thesis.log`；最小编译失败时查看 `build/environment-check.txt`。

已验证环境：macOS arm64、Python 3.9.6、Pandoc 3.13、XeTeX 2026。Windows 入口已实现，尚未完成 Windows + MiKTeX 实机验证。
