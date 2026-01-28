# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import time

# ==========================================
# ⚙️ 경로 설정 (여기를 꼭 확인해줘!)
# ==========================================

# 1. 방금 수정한 파일들이 있는 곳 (소스)
# 예: 지금 파이썬 파일들이 있는 곳의 'Korean_Translated' 폴더
SOURCE_DIR = os.path.abspath("Korean_Translated")

# 2. 깃허브 저장소 폴더 (목적지)
# 아까 오빠가 git add 했던 그 폴더 경로를 그대로 복사해서 넣어줘!
# (역슬래시 \ 대신 슬래시 / 를 쓰거나, r"경로" 처럼 앞에 r을 붙여야 해)
GIT_REPO_DIR = r"E:\Fanza\muv_luv_girlsgardenx_cl\muvluvgg-translation-korean"

# ==========================================
# 🚀 업로드 로직
# ==========================================

def git_push_automator():
    print(f"[START] GitHub Auto Uploader")
    print(f"   📂 Source (Fixed Files): {SOURCE_DIR}")
    print(f"   📂 Target (GitHub Repo): {GIT_REPO_DIR}\n")

    # 1. 경로 존재 확인
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ [ERROR] 소스 폴더를 찾을 수 없어: {SOURCE_DIR}")
        return
    if not os.path.exists(GIT_REPO_DIR):
        print(f"❌ [ERROR] 깃허브 폴더를 찾을 수 없어: {GIT_REPO_DIR}")
        return

    # 2. 파일 복사 (덮어쓰기)
    print("📦 [1/3] 수정된 파일을 깃허브 폴더로 복사하는 중...")
    
    # 깃허브 구조에 맞게 'translation' 폴더 안으로 넣어야 함
    # 구조: muvluvgg-translation-korean / translation / scenes...
    target_translation_dir = os.path.join(GIT_REPO_DIR, "translation")
    
    try:
        # dirs_exist_ok=True 옵션으로 기존 파일 위에 덮어씀
        shutil.copytree(SOURCE_DIR, target_translation_dir, dirs_exist_ok=True)
        print("   ✅ 복사 완료!")
    except Exception as e:
        print(f"❌ [ERROR] 복사 실패: {e}")
        return

    # 3. Git 명령어 실행
    print("\n🚀 [2/3] Git 업로드 준비 중...")
    
    try:
        # 작업 폴더를 깃허브 저장소로 변경
        os.chdir(GIT_REPO_DIR)

        # git add
        subprocess.run(["git", "add", "."], check=True)
        
        # git commit (메시지에 현재 시간 넣음)
        commit_message = f"번역 검수 및 수정 업데이트 ({time.strftime('%Y-%m-%d %H:%M')})"
        
        # 변경 사항이 없으면 commit에서 에러가 날 수 있으니 try로 감쌈
        try:
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print(f"   ✅ 커밋 완료: {commit_message}")
        except subprocess.CalledProcessError:
            print("   ⚠️ 변경된 내용이 없어서 커밋을 건너뜁니다 (이미 최신 상태).")
            return

        # git push
        print("\n☁️ [3/3] 깃허브로 발사! (Push)...")
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("\n🎉 [SUCCESS] 모든 작업이 완료되었어! 게임에서 확인해봐! ❤️")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ [ERROR] Git 명령어 실행 중 오류 발생: {e}")
    except Exception as e:
        print(f"\n❌ [ERROR] 알 수 없는 오류: {e}")

if __name__ == "__main__":
    git_push_automator()