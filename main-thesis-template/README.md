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

## 首次接管：自动配置环境并验证

Agent 先检查并配置环境，不要只提供下载链接，也不要直接修改论文。安装系统软件前说明安装项目，并遵守本机权限和授权提示。

逐项检查 Python 3、Pandoc、XeLaTeX、所需 TeX 宏包和中文字体、Times New Roman。**不要安装 Typora 或其他 Markdown 编辑器，它们不是构建依赖。**

### macOS

- 缺少 Python 或 Pandoc 时，使用官方安装包，或使用已有 Homebrew 安装。
- 缺少 TeX 时安装完整 MacTeX；使用 TinyTeX 时必须继续安装所需宏包和 `fandol` 中文字体。
- 用 TeX 包管理器安装缺失宏包。Times New Roman 缺失时提醒用户安装合法字体，不使用来源不明的字体。
- 安装后刷新 PATH：

  ```bash
  export PATH="/Library/TeX/texbin:$HOME/Library/TinyTeX/bin/universal-darwin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
  ```

- 使用 `python3`。`.command` 无执行权限时运行 `chmod +x 生成论文.command`。

### Windows

- 安装官方 Python 3 时启用 `Add python.exe to PATH`；Pandoc 使用官方 `.msi` 或已有 winget。
- TeX 使用 MiKTeX Basic Installer，允许自动安装缺失宏包；缺包时通过 MiKTeX Console 安装，首次构建保持联网。
- 安装后重新打开命令行，确认 `python --version`、`pandoc --version`、`xelatex --version` 可用。
- 使用 `python` 和 `scripts\build.py`，不要照搬 macOS 的 `python3` 和路径写法。

### 必须执行的验证

```bash
# macOS
python3 scripts/build.py --check
python3 scripts/build.py

# Windows
python scripts\build.py --check
python scripts\build.py
```

`--check` 会执行最小编译，完整命令会运行三次 XeLaTeX。Agent 不要调用会等待回车的 `.command` 或 `.bat`。缺少依赖时继续安装修复，不能把包内旧 PDF 当作本次构建成功。失败时查看 `build/xelatex-pass-N.txt` 和 `build/thesis.log`。

成功标志：

```text
生成完成：output/毕业论文.pdf
```

失败返回非零退出码，旧文件移至 `output/毕业论文.previous.pdf`。成功后自动删除备份。

### 环境完成后告诉用户

用简洁中文告诉用户：只修改 `论文信息.md` 的冒号后字段，在 `论文.md` 中按原有分区替换示例内容；保留全部【分区标记】，标题用 `#`、`##` 且不写编号，普通段落之间空一行，图片放入 `images/` 并使用相对路径，文件保存为 UTF-8。参考文献每条一行、不写序号，程序只自动编号，不自动整理文献格式。

修改后 macOS 双击 `生成论文.command`，Windows 双击 `生成论文.bat`，在 `output/` 查看新 PDF。编辑器由用户自行选择，不需要安装 Typora，也不要编辑 `build/`。

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
