from pathlib import Path

base_path = Path(".")

print("현재 실행 위치:", base_path.resolve())

common_structure = {
    "01_기본정보": [
        "기본정보.md",
        "공통요구역량.md",
        "준비로드맵.md",
    ],
    "02_산업군": [],
    "03_기술도구": [],
    "04_학습자료": [
        "도서.md",
        "강의.md",
        "공식문서.md",
        "실습프로젝트.md",
    ],
}

created_count = 0
skipped_count = 0
job_folder_count = 0

for first_level_folder in base_path.iterdir():
    if not first_level_folder.is_dir():
        continue

    for second_level_folder in first_level_folder.iterdir():
        if not second_level_folder.is_dir():
            continue

        job_folder_count += 1
        print(f"처리 중: {second_level_folder}")

        for folder_name, file_names in common_structure.items():
            target_folder = second_level_folder / folder_name
            target_folder.mkdir(parents=True, exist_ok=True)

            if file_names:
                for file_name in file_names:
                    file_path = target_folder / file_name

                    if file_path.exists():
                        skipped_count += 1
                        continue

                    title = file_name.replace(".md", "")
                    file_path.write_text(f"# {title}\n\n", encoding="utf-8")
                    created_count += 1
            else:
                gitkeep_path = target_folder / ".gitkeep"

                if gitkeep_path.exists():
                    skipped_count += 1
                    continue

                gitkeep_path.write_text("", encoding="utf-8")
                created_count += 1

print("\n전체 작업 완료")
print("처리한 중분류 폴더 수:", job_folder_count)
print("새로 생성한 파일 수:", created_count)
print("이미 존재해서 건너뛴 파일 수:", skipped_count)

if job_folder_count == 0:
    print("중분류 폴더를 찾지 못했습니다. 현재 위치와 폴더 구조를 확인하세요.")