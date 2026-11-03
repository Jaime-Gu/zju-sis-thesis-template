# Agent 操作手册

本文件供 CodeX、Claude Code、Kimi Code 等 Agent 阅读并执行。人工操作步骤见 `使用说明.md`。

## 1. 工作目录与结果

项目根目录为 `zju-thesis-markdown/`。以下命令默认都在该目录执行。

输入文件：

- `论文信息.md`：封面及任务书字段。
- `论文.md`：全部论文内容。
- `images/`：正文插图。
- `外文原文.pdf`：可选附件，放在项目根目录。

输出文件：

```text
output/毕业论文.pdf
```

构建中间文件位于 `build/`。不要手动编辑 `build/`，每次构建都会重新生成其中的文件。

## 2. 文件结构

```text
zju-thesis-markdown/
├── README.md                 Agent 操作手册
├── 使用说明.md               人工操作手册
├── 论文信息.md               必填字段
├── 论文.md                   论文内容
├── 生成论文.command          macOS 人工双击入口，会等待回车
├── 生成论文.bat              Windows 人工双击入口，会等待回车
├── images/
│   └── ejemplo.png           示例图片
├── scripts/
│   └── build.py              构建脚本
├── template/
│   ├── thesis-main.tex       页面顺序及各部分装配
│   ├── zju-thesis.sty        页面、字体、封面、目录、图表等格式
│   └── assets/
│       ├── zju-wordmark.png
│       └── zju-seal.png
├── output/
│   └── 毕业论文.pdf          已生成的示例
└── 外文原文.pdf              可选；默认不存在
```

修改内容时只编辑 `论文信息.md`、`论文.md`、`images/` 和可选的 `外文原文.pdf`。修改排版时编辑 `template/`。修改解析或构建逻辑时编辑 `scripts/build.py`。

不要用示例文件覆盖用户已经填写的论文内容。

## 3. 依赖

自动构建需要：

- Python 3；
- Pandoc；
- XeLaTeX，以及 `ctex`、`xeCJK`、`fandol` 等 TeX 宏包和字体；
- Times New Roman。

人工编辑推荐使用 Typora，但 Agent 执行构建不需要 Typora。

检查命令：

```bash
# macOS
python3 scripts/build.py --check

# Windows
python scripts\build.py --check
```

成功时输出 Pandoc 和 XeLaTeX 版本，最后显示“环境检查通过”。

如果缺少程序：

- Typora：<https://typora.io/#download>
- Python：<https://www.python.org/downloads/>
- Pandoc：<https://pandoc.org/installing.html>
- macOS 完整 MacTeX：<https://www.tug.org/mactex/>
- Windows MiKTeX：<https://miktex.org/download>

macOS 构建入口已把 `/Library/TeX/texbin`、`/opt/homebrew/bin` 和 `/usr/local/bin` 加入 PATH。直接调用 `scripts/build.py` 时，如果找不到 `xelatex`，先检查：

```bash
export PATH="/Library/TeX/texbin:/opt/homebrew/bin:/usr/local/bin:$PATH"
python3 scripts/build.py --check
```

Windows 安装 Python 时必须把 Python 加入 PATH。MiKTeX 必须允许安装缺少的宏包。

## 4. 执行构建

Agent 使用非交互命令，不要调用会等待用户按回车的 `.command` 或 `.bat` 文件。

```bash
# macOS
python3 scripts/build.py

# Windows
python scripts\build.py
```

构建顺序：

1. 检查 Pandoc 和 XeLaTeX。
2. 读取并校验 `论文信息.md`。
3. 读取 `论文.md`，按分区标记拆成 13 个部分。
4. 用 Pandoc 转换为 LaTeX 片段。
5. 处理标题锚点、参考文献编号、图表、公式和附件。
6. 将内容装入 `template/thesis-main.tex`。
7. 连续运行三次 XeLaTeX，更新目录、引用和页码。
8. 将结果复制到 `output/毕业论文.pdf`。

成功标志：

```text
生成完成：output/毕业论文.pdf
```

脚本失败时返回非零退出码。不要把“开始运行 XeLaTeX”当作成功。

## 5. 填写论文信息

`论文信息.md` 使用“字段名：字段值”格式。以下字段均不能为空，字段名不能修改：

```text
西语题目：...
中文题目：...
姓名：...
学号：...
指导教师：...
年级与专业：...
所在学院：...
提交日期：...
任务书起止日期：...
论文性质：公开
```

`论文性质`只能为`公开`或`涉密`。

解析规则：

- 同时支持中文冒号和英文冒号。
- 忽略空行、以 `#` 开头的行和以 `<!--` 开头的行。
- 文件必须为 UTF-8；读取时也兼容带 BOM 的 UTF-8。
- 字段值中的 LaTeX 特殊字符会由构建脚本转义。

## 6. 编辑论文内容

### 6.1 分区

`论文.md` 必须包含以下独立行，名称和顺序固定，不能重复：

```text
【致谢】
【西文摘要】
【中文摘要】
【正文】
【参考文献】
【附录】
【作者简介】
【任务书】
【指导教师要求】
【文献综述】
【开题报告】
【外文翻译】
【外文原文】
```

只编辑标记之间的内容。

【附录】或【作者简介】不需要内容时，保留标记，删除标记到下一个分区之间的全部文字。构建脚本会跳过该部分。

`<!-- ... -->` 中的注释不会进入 PDF。

### 6.2 标题与段落

```markdown
# 一级标题

## 二级标题

### 三级标题

#### 四级标题
```

`#` 后必须有空格。不要手动写章节编号。正文、文献综述和开题报告分别从 1 开始编号。

普通正文直接书写，段落之间空一行。不要用段首空格控制缩进，也不要用连续空行控制分页。

### 6.3 摘要关键词

```text
Palabras clave: Español; chino mandarín; difusión internacional
```

```text
关键词：西班牙语；汉语普通话；国际传播
```

程序只自动加粗标签，不重写关键词内容。

### 6.4 正文参考文献

【参考文献】中每条文献单独一行，不写序号：

```text
Baker, M. Routledge Encyclopedia of Translation Studies[M]. Shanghai: Shanghai Foreign Language Education Press, 2010.
Cooper, R. L. A Framework for the Study of Language Spread[J]. Language Spread: Studies in Diffusion and Social Change, 1982, 5: 36.
```

程序生成`[1]`、`[2]`等编号和悬挂缩进。

【文献综述】和【开题报告】末尾的参考文献属于普通章节内容，其中的`[1]`、`[2]`需要自行维护。

### 6.5 引用、长引用和脚注

文内引用按普通文字书写：

```text
(Cooper 1982:13)
```

长引用：

```markdown
> 引用正文。
>
> （Autor 2020：25）
```

脚注：

```markdown
正文标记。[^1]

[^1]: 脚注说明。
```

### 6.6 图片

图片使用相对路径，放在 `images/` 中。图片单独占一个段落：

```markdown
![图题，不写图号](images/mi-figura.png){width=12cm}
```

图号自动生成，图题位于图片下方。可调整 `width`，不要超过正文宽度。

图片下一行可写：

```text
Fuente: Elaboración propia.
```

### 6.7 表格

```markdown
| Partes | Aspectos | Indicadores |
|:---|:---|:---|
| Tracción del mercado | General | Índice de Poder |
| Empuje del gobierno | Gobierno | Aportación |

Tabla: 表题，不写表号

Fuente: Elaboración propia.
```

表号自动生成，表题位于表格下方。长文本列会自动换行。大表需要在内容中手动拆分，不能保证超过一页的表格自动完整放入一页。

### 6.8 公式

独立公式：

```markdown
$$
U = 3X
$$
```

独立公式自动转为编号公式，按章节显示为`(3-1)`等。

行内公式：

```markdown
La variable $U$ representa ...
```

### 6.9 外文原文附件

存在根目录 `外文原文.pdf` 时：

- 在 `Texto de origen` 标题页后插入整份 PDF；
- 忽略【外文原文】中的文字；
- 插入页使用空白页面样式，不额外添加模板页眉和页码。

不存在该文件时，排版【外文原文】中的 Markdown 内容。

## 7. 修改模板

页面顺序在 `template/thesis-main.tex`：

- 主封面、总目录、承诺书；
- 致谢、西文摘要、中文摘要、目录；
- 正文、参考文献、可选附录和作者简介；
- 任务书、考核表、文献综述封面、教师要求；
- 文献综述、开题报告、外文翻译、外文原文；
- 文献综述考核表和书脊。

格式在 `template/zju-thesis.sty`：

- A4，上下边距 2.54 cm，左右约 3.17 cm；
- 正文 12 磅，18 磅行距，首行缩进两个字符；
- 西文 Times New Roman；
- 中文依次选择 STFangsong、FangSong、FandolFang；
- 标题、页眉、目录、图表、引用和固定表格样式；
- 表题位于表格下方；
- 前置部分罗马数字页码，正文阿拉伯数字页码；
- 一级标题奇数页起页。

只输出 PDF，不输出 DOCX。

不执行篇幅、参考文献数量、外文文献数量或未出版学位论文比例检查。

## 8. 验收

每次修改内容、脚本或模板后，都要重新执行完整构建，不能只检查 Python 语法或 LaTeX 文件是否存在。

检查输出：

```bash
# macOS
ls -lh output/毕业论文.pdf

# Windows
dir output\毕业论文.pdf
```

检查关键错误：

```bash
# macOS；无输出表示没有发现这些错误
grep -E "LaTeX Error|undefined|multiply defined|Overfull|LaTeX Font Warning" build/thesis.log || true

# Windows
findstr /C:"LaTeX Error" /C:"undefined" /C:"multiply defined" /C:"Overfull" build\thesis.log
```

需要进一步核对：

1. PDF 能正常打开，页数大于 0。
2. 封面字段没有示例残留。
3. 总目录和正文目录页码正确。
4. 前置页码连续，正文从 1 开始。
5. 一级标题位于奇数物理页。
6. 页眉随正文、文献综述、开题报告、外文翻译和外文原文切换。
7. 图、表和公式编号正确。
8. 固定表格和签名页没有被正文挤出额外页面。
9. 如果存在 `外文原文.pdf`，附件页数、顺序和方向正确。
10. 书脊题目和姓名正确。

修改模板后，应渲染并查看封面、目录、正文图表页、任务书、考核表、文献综述封面和书脊，不能仅以编译退出码判断排版合格。

## 9. 故障处理

### 找不到 `pandoc` 或 `xelatex`

先执行环境检查。确认安装后重新打开终端，并检查 PATH。macOS 可直接检查：

```bash
/Library/TeX/texbin/xelatex --version
```

### Windows 找不到 `python`

重新安装 Python 并启用 `Add python.exe to PATH`，然后打开新的命令行窗口。

### 缺少 `.sty` 文件

这是 TeX 宏包缺失。允许 MiKTeX 安装宏包，或在 macOS 的 TeX Live 中安装错误提示的宏包。完整 MacTeX 通常已经包含所需文件。

### 缺少字体

安装 Times New Roman。中文可使用系统仿宋、宋体、黑体，或安装 TeX 的 `fandol` 字体包。

### 分区错误

检查 `论文.md` 是否包含全部 13 个分区标记，是否使用中文方括号，是否有拼写变化或重复。

### 图片错误

检查 `images/` 中的实际文件名、扩展名和 Markdown 相对路径。不要使用原电脑绝对路径。

### 目录或页码未更新

让三次 XeLaTeX 全部完成。不要中途终止。必要时再执行一次完整构建。

### 无法写入 PDF

关闭占用 `output/毕业论文.pdf` 的阅读器，确认目录可写。

### 查看详细日志

依次检查：

1. 构建命令的标准输出和错误输出；
2. `build/xelatex-pass-1.txt`；
3. `build/thesis.log` 中第一个以 `!` 开头的错误。

修复第一个实质性错误后再构建，不要连续重复同一失败命令。

## 10. Agent 执行清单

1. 定位项目根目录。
2. 阅读现有输入，保留用户已填写内容。
3. 执行 `scripts/build.py --check`。
4. 按要求编辑输入或模板。
5. 执行完整构建。
6. 检查退出码和 `output/毕业论文.pdf`。
7. 检查日志中的引用、字体和版面错误。
8. 模板有改动时，渲染并检查代表性页面。
9. 报告生成文件路径、验证结果和仍未解决的问题。
