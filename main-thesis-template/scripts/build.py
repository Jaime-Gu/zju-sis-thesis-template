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
    if seen != list(SECTIONS):
        raise BuildError("论文.md 的分区顺序不正确。正确顺序为：" + " → ".join(f"【{label}】" for label in SECTIONS))
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


def latex_raw_block(content):
    return "```{=latex}\n" + content + "\n```"


def run_command(command, cwd=ROOT, log_path=None):
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
    )
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(result.stdout, encoding="utf-8")
    if result.returncode != 0:
        tail = "\n".join(result.stdout.splitlines()[-50:])
        message = f"命令执行失败：{' '.join(map(str, command))}\n{tail}"
        if log_path is not None:
            try:
                display_path = log_path.relative_to(ROOT)
            except ValueError:
                display_path = log_path
            message += f"\n完整日志：{display_path}"
        raise BuildError(message)
    return result.stdout


def preprocess_markdown(text, section):
    lines = []
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("Title:"):
            value = latex_escape(stripped[len("Title:"):].strip())
            lines.append(latex_raw_block("\\zjuArticleTitle{" + value + "}"))
        elif stripped.startswith("Tabla:"):
            value = latex_escape(stripped[len("Tabla:"):].strip())
            lines.append(latex_raw_block("\\zjuTableCaption{" + value + "}"))
        elif stripped.startswith("Fuente:"):
            value = latex_escape(stripped[len("Fuente:"):].strip())
            lines.append(latex_raw_block("\\zjuSource{" + value + "}"))
        elif stripped.startswith("Palabras clave:"):
            value = latex_escape(stripped[len("Palabras clave:"):].strip())
            lines.append(latex_raw_block("\\noindent\\textbf{Palabras clave:} " + value))
        elif stripped.startswith("关键词：") or stripped.startswith("关键词:"):
            value = re.sub(r"^关键词[：:]", "", stripped)
            lines.append(latex_raw_block("\\noindent\\textbf{关键词：}" + latex_escape(value)))
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

    def prefixed_target(target):
        if any(target.startswith(f"{name}-") for name in SECTIONS.values()):
            return target
        return f"{section}-{target}"

    latex = re.sub(
        r"\\label\{([^}]+)\}",
        lambda match: "\\label{" + prefixed_target(match.group(1)) + "}",
        latex,
    )
    latex = re.sub(
        r"\\hyperref\[([^\]]+)\]",
        lambda match: "\\hyperref[" + prefixed_target(match.group(1)) + "]",
        latex,
    )
    for macro in ("ref", "autoref", "pageref", "eqref"):
        latex = re.sub(
            rf"\\{macro}\{{([^}}]+)\}}",
            lambda match: "\\" + macro + "{" + prefixed_target(match.group(1)) + "}",
            latex,
        )
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
            "。请按照 使用说明.md 安装 Pandoc 和 TeX 环境；安装后关闭并重新打开生成窗口。"
        )


def check_template_environment():
    BUILD.mkdir(exist_ok=True)
    check_file = BUILD / "environment-check.tex"
    check_file.write_text(
        "\\documentclass[12pt,a4paper,fontset=none]{ctexart}\n"
        "\\usepackage{template/zju-thesis}\n"
        "\\usepackage{hyperref}\n"
        "\\begin{document}\nEnvironment check\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    run_command([
        "xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        "-output-directory=build",
        "build/environment-check.tex",
    ], log_path=BUILD / "environment-check.txt")


def build(check_only=False):
    check_dependencies()
    if check_only:
        print("Pandoc：", run_command(["pandoc", "--version"]).splitlines()[0])
        print("XeLaTeX：", run_command(["xelatex", "--version"]).splitlines()[0])
        check_template_environment()
        print("基础程序、TeX 宏包和字体检查通过。请继续执行一次完整示例构建。")
        return

    OUTPUT.mkdir(exist_ok=True)
    final_pdf = OUTPUT / "毕业论文.pdf"
    previous_pdf = OUTPUT / "毕业论文.previous.pdf"
    if previous_pdf.exists():
        previous_pdf.unlink()
    if final_pdf.exists():
        final_pdf.replace(previous_pdf)

    info = parse_info()
    sections = parse_content()
    BUILD.mkdir(exist_ok=True)
    auxiliary_files = [BUILD / f"thesis.{suffix}" for suffix in ("aux", "toc", "out", "log", "pdf", "lof", "lot")]
    for stale_file in list(BUILD.glob("xelatex-pass-*.txt")) + auxiliary_files:
        if stale_file.exists():
            stale_file.unlink()

    print("1/4 正在转换 Markdown……")
    for section in SECTIONS.values():
        (BUILD / f"{section}.tex").write_text(pandoc_fragment(sections[section], section), encoding="utf-8")

    appendix = ""
    if sections["appendix"].strip():
        appendix = "\\zjuUnnumberedPartTitle{Apéndice}{appendix}\n\\input{build/appendix.tex}"
    author = ""
    if sections["author"].strip():
        author = "\\zjuUnnumberedPartTitle{Breve resumen del autor}{author}\n\\input{build/author.tex}"
    original_pdf = ROOT / "外文原文.pdf"
    if original_pdf.exists():
        original = "\\clearpage\\includepdf[pages=-,pagecommand={\\thispagestyle{empty}}]{外文原文.pdf}"
    else:
        original = "\\zjuSuppressNextSectionBreaktrue\n\\input{build/original.tex}"

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
        run_command([
            "xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            "-output-directory=build",
            "build/thesis.tex",
        ], log_path=BUILD / f"xelatex-pass-{pass_number}.txt")

    result_pdf = BUILD / "thesis.pdf"
    if not result_pdf.exists():
        raise BuildError("XeLaTeX 已结束，但没有生成 PDF。请查看 build/thesis.log。")
    shutil.copy2(result_pdf, final_pdf)
    if previous_pdf.exists():
        previous_pdf.unlink()
    print("生成完成：output/毕业论文.pdf")


def main():
    parser = argparse.ArgumentParser(description="将论文.md 生成符合模板的 PDF")
    parser.add_argument("--check", action="store_true", help="检查程序、TeX 宏包和字体，并执行最小编译")
    args = parser.parse_args()
    try:
        build(check_only=args.check)
    except BuildError as error:
        print("\n生成失败：\n" + str(error), file=sys.stderr)
        if (OUTPUT / "毕业论文.previous.pdf").exists():
            print("上一份 PDF 保存在：output/毕业论文.previous.pdf", file=sys.stderr)
        return 1
    except OSError as error:
        print("\n文件读写失败：" + str(error), file=sys.stderr)
        print("请检查文件权限，并关闭正在占用 PDF 的阅读器。", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
