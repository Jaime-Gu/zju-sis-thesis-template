#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent
PACKAGES = ("main-thesis-template", "review-proposal-template")
EXCLUDED_DIRS = {".git", "build", "__pycache__", "__MACOSX"}
EXCLUDED_FILES = {
    ".DS_Store",
    "毕业论文.previous.pdf",
    "开题和文献综述.previous.pdf",
}


def included(path, package_root):
    relative = path.relative_to(package_root)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    return path.is_file() and path.name not in EXCLUDED_FILES


for package in PACKAGES:
    package_root = ROOT / package
    archive = ROOT.parent / f"{package}.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as zf:
        files = [path for path in package_root.rglob("*") if included(path, package_root)]
        for path in sorted(files):
            archive_name = (Path(package) / path.relative_to(package_root)).as_posix()
            zf.write(path, archive_name)
            if path.suffix == ".command":
                info = zf.getinfo(archive_name)
                info.external_attr |= 0o111 << 16

    with ZipFile(archive) as zf:
        damaged = zf.testzip()
        if damaged is not None:
            raise SystemExit(f"{archive.name} 校验失败：{damaged}")
        names = zf.namelist()
        if not names or any(not name.startswith(f"{package}/") for name in names):
            raise SystemExit(f"{archive.name} 的目录结构不正确。")
        if any("__MACOSX" in name or ".DS_Store" in name for name in names):
            raise SystemExit(f"{archive.name} 包含系统杂项文件。")
        for name in names:
            if name.endswith(".command") and (zf.getinfo(name).external_attr >> 16) & 0o111 != 0o111:
                raise SystemExit(f"{archive.name} 中的 .command 缺少执行权限。")
        print(f"已生成：{archive}")
        print(f"文件数：{len(names)}；CRC 校验通过")
