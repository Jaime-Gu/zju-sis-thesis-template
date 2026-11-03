#!/usr/bin/env python3
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
OUTPUT = ROOT / "output"
INFO_FILE = ROOT / "论文信息.md"
CONTENT_FILE = ROOT / "论文.md"

SECTIONS = {
    "致谢": "acknowledgements",
    "西文摘要": "abstract_es",
    "中文摘要": "abstract_zh",
    "正文": "body",
    "参考文献": "references",
    "附录": "appendix",
    "作者简介": "author",
    "任务书": "task",
    "指导教师要求": "requirements",
    "文献综述": "review",
    "开题报告": "proposal",
    "外文翻译": "translation",
    "外文原文": "original",
}

INFO_KEYS = {
    "西语题目": "TITLE_ES",
    "中文题目": "TITLE_ZH",
    "姓名": "AUTHOR",
    "学号": "STUDENT_ID",
    "指导教师": "ADVISOR",
    "年级与专业": "GRADE_MAJOR",
    "所在学院": "COLLEGE",
    "提交日期": "SUBMIT_DATE",
    "任务书起止日期": "TASK_DATES",
}


class BuildError(Exception):
    pass


def read_utf8(path):
    try:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        raise BuildError(f"缺少文件：{path.name}")
    except UnicodeDecodeError:
        raise BuildError(f"{path.name} 不是 UTF-8 编码。请在 Typora 中重新保存为 UTF-8。")


def parse_info():
    values = {}
    for raw_line in read_utf8(INFO_FILE).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("<!--"):
            continue
        match = re.match(r"^([^：:]+)[：:](.*)$", line)
        if not match:
            continue
        key = match.group(1).strip().replace("**", "")
        value = match.group(2).strip()
        if key in INFO_KEYS or key == "论文性质":
            values[key] = value
    missing = [key for key in list(INFO_KEYS) + ["论文性质"] if not values.get(key)]
    if missing:
        raise BuildError("论文信息.md 中以下项目为空：" + "、".join(missing))
    if values["论文性质"] not in {"公开", "涉密"}:
        raise BuildError("论文信息.md 的“论文性质”只能填写“公开”或“涉密”。")
    return values


def parse_content():
    text = re.sub(r"<!--.*?-->", "", read_utf8(CONTENT_FILE), flags=re.S)
    marker = re.compile(r"^【([^】]+)】\s*$", re.M)
    matches = list(marker.finditer(text))
    if not matches:
        raise BuildError("论文.md 中找不到【正文】等分区标记。请恢复模板中的分区标记。")
    sections = {name: "" for name in SECTIONS.values()}
    seen = []
    for index, match in enumerate(matches):
        label = match.group(1).strip()
        if label not in SECTIONS:
            raise BuildError(f"无法识别分区标记【{label}】。请检查是否写错了名称。")
        if label in seen:
            raise BuildError(f"分区标记【{label}】出现了两次。")
        seen.append(label)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[SECTIONS[label]] = text[match.end():end].strip()
    missing = [label for label in SECTIONS if label not in seen]
    if missing:
        raise BuildError("论文.md 缺少分区标记：" + "、".join(f"【{label}】" for label in missing))
    return sections


def latex_escape(value):
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def run_command(command, cwd=ROOT):
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        tail = "\n".join(result.stdout.splitlines()[-50:])
        raise BuildError(f"命令执行失败：{' '.join(map(str, command))}\n{tail}")
    return result.stdout


def preprocess_markdown(text, section):
    lines = []
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("Tabla:"):
            lines.append("\\zjuTableCaption{" + stripped[len("Tabla:"):].strip() + "}")
        elif stripped.startswith("Fuente:"):
            lines.append("\\zjuSource{" + stripped[len("Fuente:"):].strip() + "}")
        elif stripped.startswith("Palabras clave:"):
            lines.append("\\noindent\\textbf{Palabras clave:}" + stripped[len("Palabras clave:"):])
        elif stripped.startswith("关键词：") or stripped.startswith("关键词:"):
            value = re.sub(r"^关键词[：:]", "", stripped)
            lines.append("\\noindent\\textbf{关键词：}" + value)
        else:
            lines.append(raw_line)
    text = "\n".join(lines)
    if section == "references":
        entries = [line.strip() for line in text.splitlines() if line.strip()]
        text = "\n".join(f"{index}. {entry}" for index, entry in enumerate(entries, 1))
    return text + "\n"


def postprocess_latex(text):
    text = text.replace("{\\def\\LTcaptype{none} % do not increment counter", "{")
    text = text.replace("\\begin{figure}[htbp]", "\\begin{figure}[H]")
    text = re.sub(r"\\\[\s*", "\\\\begin{equation}\n", text)
    text = re.sub(r"\s*\\\]", "\n\\\\end{equation}", text)

    def wrap_table_columns(match):
        prefix, columns = match.group(1), match.group(2)
        count = sum(columns.count(column) for column in "lcr")
        if not count:
            return match.group(0)
        width = rf"\dimexpr\linewidth/{count}-2\tabcolsep\relax"
        wrapped = rf"@{{}}>{{\raggedright\arraybackslash}}p{{{width}}}" * count + "@{}"
        return prefix + "{" + wrapped + "}"

    text = re.sub(r"(\\begin\{longtable\}(?:\[[^\]]*\])?)\{@\{\}([lcr]+)@\{\}\}", wrap_table_columns, text)

    def keep_table_together(match):
        block = match.group(0)
        rows = max(4, block.count("\\\\") + 3)
        return f"\\Needspace{{{rows}\\baselineskip}}\n{block}"

    text = re.sub(r"\\begin\{longtable\}.*?\\end\{longtable\}", keep_table_together, text, flags=re.S)
    return text


def pandoc_fragment(text, section):
    source = preprocess_markdown(text, section)
    command = [
        "pandoc",
        "--from=markdown+raw_tex+tex_math_dollars",
        "--to=latex",
        "--wrap=none",
        f"--resource-path={ROOT}",
    ]
    result = subprocess.run(
        command,
        cwd=ROOT,
        input=source,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise BuildError(f"Pandoc 无法转换“{section}”部分：\n{result.stderr}")
    latex = postprocess_latex(result.stdout)
    latex = re.sub(r"\\label\{([^}]+)\}", lambda match: rf"\label{{{section}-{match.group(1)}}}", latex)
    if section == "references":
        latex = latex.replace(r"\def\labelenumi{\arabic{enumi}.}", r"\def\labelenumi{[\arabic{enumi}]}")
    return latex


def check_dependencies():
    missing = []
    for name in ("pandoc", "xelatex"):
        if shutil.which(name) is None:
            missing.append(name)
    if missing:
        raise BuildError(
            "缺少排版程序：" + "、".join(missing) +
            "。请按照 README.md 安装 Pandoc 和 TeX 环境；安装后关闭并重新打开生成窗口。"
        )


def build(check_only=False):
    check_dependencies()
    if check_only:
        print("Pandoc：", run_command(["pandoc", "--version"]).splitlines()[0])
        print("XeLaTeX：", run_command(["xelatex", "--version"]).splitlines()[0])
        print("环境检查通过。")
        return

    info = parse_info()
    sections = parse_content()
    BUILD.mkdir(exist_ok=True)
    OUTPUT.mkdir(exist_ok=True)

    print("1/4 正在转换 Markdown……")
    for section in SECTIONS.values():
        (BUILD / f"{section}.tex").write_text(pandoc_fragment(sections[section], section), encoding="utf-8")

    appendix = ""
    if sections["appendix"].strip():
        appendix = "\\zjuPartTitle{Apéndice}{appendix}\n\\input{build/appendix.tex}"
    author = ""
    if sections["author"].strip():
        author = "\\zjuPartTitle{Breve resumen del autor}{author}\n\\input{build/author.tex}"
    original_pdf = ROOT / "外文原文.pdf"
    if original_pdf.exists():
        original = "\\clearpage\\includepdf[pages=-,pagecommand={\\thispagestyle{empty}}]{外文原文.pdf}"
    else:
        original = "\\input{build/original.tex}"

    replacements = {token: latex_escape(info[key]) for key, token in INFO_KEYS.items()}
    replacements.update({
        "SECRECY_MARK": r"$\boxtimes$" if info["论文性质"] == "涉密" else r"$\square$",
        "PUBLIC_MARK": r"$\boxtimes$" if info["论文性质"] == "公开" else r"$\square$",
        "APPENDIX": appendix,
        "AUTHOR_SECTION": author,
        "ORIGINAL": original,
    })
    template = (ROOT / "template" / "thesis-main.tex").read_text(encoding="utf-8")
    for token, value in replacements.items():
        template = template.replace(f"%%{token}%%", value)
    unresolved = re.findall(r"%%[A-Z_]+%%", template)
    if unresolved:
        raise BuildError("模板中存在未替换的标记：" + "、".join(unresolved))
    (BUILD / "thesis.tex").write_text(template, encoding="utf-8")

    print("2/4 正在进行第一次 XeLaTeX 排版……")
    for pass_number in range(1, 4):
        if pass_number > 1:
            print(f"{pass_number + 1}/4 正在更新目录、交叉引用和页码（第 {pass_number} 次）……")
        log = run_command([
            "xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            "-output-directory=build",
            "build/thesis.tex",
        ])
        (BUILD / f"xelatex-pass-{pass_number}.txt").write_text(log, encoding="utf-8")

    result_pdf = BUILD / "thesis.pdf"
    if not result_pdf.exists():
        raise BuildError("XeLaTeX 已结束，但没有生成 PDF。请查看 build/thesis.log。")
    shutil.copy2(result_pdf, OUTPUT / "毕业论文.pdf")
    print("生成完成：output/毕业论文.pdf")


def main():
    parser = argparse.ArgumentParser(description="将论文.md 生成符合模板的 PDF")
    parser.add_argument("--check", action="store_true", help="只检查 Pandoc 和 XeLaTeX 是否可用")
    args = parser.parse_args()
    try:
        build(check_only=args.check)
    except BuildError as error:
        print("\n生成失败：\n" + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
