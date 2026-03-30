
import os
import subprocess
from datetime import datetime, timedelta

def get_project_folders(base_path):
    """
    取得指定資料夾下的所有子資料夾名稱
    """
    return [name for name in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, name))]

def has_git_folder(folder_path):
    """
    判斷資料夾是否包含.git資料夾
    """
    return os.path.isdir(os.path.join(folder_path, '.git'))

def get_git_log(folder_path, since_days=30):
    """
    取得指定資料夾本月的git log
    """
    since_date = datetime.now().strftime('%Y-%m-01')
    try:
        # git log --since="2026-03-01" --pretty=format:"%B" -p
        result = subprocess.run(
            ["git", "log", f"--since={since_date}", "--pretty=format:%B", "-p"],
            cwd=folder_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"[Error] {e.stderr.strip()}"


def get_all_git_logs(base_path, since_days=30):
    """
    取得 base_path 下所有有 .git 的資料夾的 git log，回傳 dict: {資料夾名稱: log內容}
    """
    if not os.path.isdir(base_path):
        raise ValueError("指定的路徑不存在或不是資料夾。")
    result = {}
    projects = get_project_folders(base_path)
    for project in projects:
        project_path = os.path.join(base_path, project)
        if has_git_folder(project_path):
            log = get_git_log(project_path, since_days)
            result[project] = log if log else None
    return result

def main():
    base_path = input("請輸入工作資料夾路徑: ").strip()
    try:
        logs = get_all_git_logs(base_path)
        for project, log in logs.items():
            print(f"\n=== {project} ===")
            print(log if log else "(無本月的git log)")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()