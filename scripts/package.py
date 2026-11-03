#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT.parent / f"{ROOT.name}.zip"
EXCLUDED_DIRS = {".git", "build", "__pycache__", "__MACOSX"}


def included(path):
    relative = path.relative_to(ROOT)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if path.name in {".DS_Store", "毕业论文.previous.pdf"}:
        return False
    return path.is_file()


with ZipFile(ARCHIVE, "w", ZIP_DEFLATED) as zf:
    files = [path for path in ROOT.rglob("*") if included(path)]
    for path in sorted(files):
        zf.write(path, (Path(ROOT.name) / path.relative_to(ROOT)).as_posix())

with ZipFile(ARCHIVE) as zf:
    if zf.testzip() is not None:
        raise SystemExit("ZIP 校验失败。")
    names = zf.namelist()
    if any("__MACOSX" in name or ".DS_Store" in name for name in names):
        raise SystemExit("ZIP 中包含系统杂项文件。")
    print(f"已生成：{ARCHIVE}")
    print(f"文件数：{len(names)}")
