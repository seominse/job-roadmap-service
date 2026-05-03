from pathlib import Path
import shutil

base_path = Path(".")

exclude_files = {"README.md", "설명.md"}

for category_path in base_path.iterdir():
    if not category_path.is_dir():
        continue

    for md_file in category_path.glob("*.md"):
        if md_file.name in exclude_files:
            continue

        folder_name = md_file.stem
        target_folder = category_path / folder_name
        target_file = target_folder / "설명.md"

        target_folder.mkdir(parents=True, exist_ok=True)

        if target_file.exists():
            print(f"이미 설명.md가 있어서 건너뜀: {target_file}")
            continue

        shutil.move(str(md_file), str(target_file))
        print(f"변환 완료: {md_file} -> {target_file}")

print("전체 변환 완료")