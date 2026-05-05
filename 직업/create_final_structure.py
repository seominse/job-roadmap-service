from pathlib import Path
import shutil

# job-roadmap-service에서 실행하면 "직업" 폴더를 기준으로 사용
# 직업 폴더 안에서 실행하면 현재 위치를 기준으로 사용
base_path = Path("직업") if Path("직업").exists() else Path(".")

print("기준 폴더:", base_path.resolve())

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
moved_count = 0
skipped_count = 0

for category_path in base_path.iterdir():
    # 대분류 폴더만 처리
    if not category_path.is_dir():
        continue

    print(f"\n대분류 확인: {category_path.name}")

    for job_path in category_path.iterdir():
        # 중분류 또는 직업명 폴더만 처리
        if not job_path.is_dir():
            continue

        print(f"  처리 중: {job_path.name}")

        old_description_path = job_path / "설명.md"

        for folder_name, file_names in common_structure.items():
            folder_path = job_path / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)

            if file_names:
                for file_name in file_names:
                    file_path = folder_path / file_name

                    # 기존 설명.md를 01_기본정보/기본정보.md로 이동
                    if folder_name == "01_기본정보" and file_name == "기본정보.md":
                        if old_description_path.exists():
                            if file_path.exists():
                                backup_path = folder_path / "기존_설명.md"

                                if backup_path.exists():
                                    skipped_count += 1
                                else:
                                    shutil.move(str(old_description_path), str(backup_path))
                                    moved_count += 1

                                continue

                            shutil.move(str(old_description_path), str(file_path))
                            moved_count += 1
                            continue

                    # 나머지 파일 생성
                    if file_path.exists():
                        skipped_count += 1
                        continue

                    title = file_name.replace(".md", "")
                    file_path.write_text(f"# {title}\n\n", encoding="utf-8")
                    created_count += 1

            else:
                # GitHub는 빈 폴더를 저장하지 않기 때문에 .gitkeep 생성
                gitkeep_path = folder_path / ".gitkeep"

                if gitkeep_path.exists():
                    skipped_count += 1
                    continue

                gitkeep_path.write_text("", encoding="utf-8")
                created_count += 1

        # 설명.md가 없었고 기본정보.md도 없으면 새로 생성
        basic_info_path = job_path / "01_기본정보" / "기본정보.md"

        if not basic_info_path.exists():
            basic_info_path.write_text(f"# 기본정보\n\n", encoding="utf-8")
            created_count += 1

print("\n전체 작업 완료")
print("설명.md 이동 수:", moved_count)
print("새로 생성한 파일 수:", created_count)
print("이미 존재해서 건너뛴 수:", skipped_count)