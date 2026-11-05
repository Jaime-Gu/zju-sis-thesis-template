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
生成完成：output/开题和文献综述.pdf
```

失败返回非零退出码，旧文件移至 `output/开题和文献综述.previous.pdf`。成功后自动删除备份。

### 环境完成后告诉用户

用简洁中文告诉用户：只修改 `论文信息.md` 的冒号后字段，在 `论文.md` 中按原有分区替换示例内容；保留全部【分区标记】，标题用 `#`、`##` 且不写编号，普通段落之间空一行，图片放入 `images/` 并使用相对路径，文件保存为 UTF-8。文献综述和开题报告的参考文献序号及格式需要用户自己维护。

修改后 macOS 双击 `生成论文.command`，Windows 双击 `生成论文.bat`，在 `output/` 查看新 PDF。需要衔接主论文页码时修改`起始页码`；有现成原文时将附件命名为 `外文原文.pdf` 放在本目录。编辑器由用户自行选择，不需要安装 Typora，也不要编辑 `build/`。

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
