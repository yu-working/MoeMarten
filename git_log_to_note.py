import os
from datetime import datetime
from git_log_reader import get_all_git_logs
from note_generater import start_note_generation

NOTE_DIR = "notes"

def write_note(filename, content):
    os.makedirs(NOTE_DIR, exist_ok=True)
    path = os.path.join(NOTE_DIR, filename)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content + '\n')

def main():
    base_path = input("請輸入工作資料夾路徑: ").strip()
    logs = get_all_git_logs(base_path)
    today = datetime.now().strftime('%Y%m%d')
    note_filename = f"{today}.md"
    if logs:
        note = start_note_generation(logs.items())
        write_note(note_filename, note)
        print(f"已寫入 {note_filename} 至 note/ 資料夾")
    else:
        print("沒有可用的 git log 或產生內容。")

if __name__ == "__main__":
    main()
