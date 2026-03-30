from datetime import datetime
import dotenv
import os
from google import genai
from git_log_reader import create_command_to_get_all_git_logs

NOTE_DIR = "notes"

def write_note(filename, content):
    os.makedirs(NOTE_DIR, exist_ok=True)
    path = os.path.join(NOTE_DIR, filename)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content + '\n')

def generate_by_llm(prompt):
    client = genai.Client()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
            ## 任務說明
            根據輸入的關鍵字或Git log，生成一份繁體中文筆記：
            
            ## 輸入
            {prompt}

            ## 限制
            1. 以繁體中文撰寫
            2. 只需要包含內文，不需要標題或其他說明
            3. 若有多項內容，請使用條列式呈現(使用符號 - )
            4. 不可出現 *、#、> 等特殊符號
            """
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"

def generate_by_rule_based(prompt):
    # 這裡可以根據具體的規則來生成筆記，以下是一個簡單的示例
    # if "python" in prompt:
    all_notes = []
    if prompt:
        for repo, log in prompt.items():
            all_notes.append(f"## Repo: {repo}\n{log}\n")
        return "\n".join(all_notes)
    #     return "Python 是一種高級程式語言，適合用於資料分析、機器學習和網頁開發等領域。"
    # elif "llm" in prompt:
    #     return "LLM（Large Language Model）是一種基於深度學習的自然語言處理模型，能夠理解和生成自然語言文本。"
    # elif "agent" in prompt:
    #     return "Agent 是一種自主軟體實體，能夠感知環境並執行任務以達成特定目標。"
    else:
        return "hello world"
    
def note_template(title, source, note):
    status = "未發佈"
    """
    產生標準化的筆記模板內容
    ---
    title: 標題
    source: 手動/rule-based/llm
    status: 未發佈/已發佈
    ---
    note
    """
    template = f'''---\ntitle: {title}\nsource: {source}\nstatus: {status}\n---\n{note}
    '''
    return template
    
def start_note_generation(base_path, since_date):
    dotenv.load_dotenv()
    if "Gemini_API_KEY" in os.environ:
        source = "llm"
        logs = create_command_to_get_all_git_logs(base_path, since_date=since_date, mode=source)
        note = generate_by_llm(logs)
    else:
        source = "rule-based"
        logs = create_command_to_get_all_git_logs(base_path, since_date=since_date, mode=source)
        note = generate_by_rule_based(logs)
    # 標題暫時固定為 "note"
    final_note = note_template(title="note", source=source, note=note)
    return final_note

if __name__ == "__main__":
    base_path = input("請輸入工作資料夾路徑: ").strip()
    # 以日期命名筆記存檔
    today = datetime.now().strftime('%Y%m%d')
    note_filename = f"{today}.md"

    # 先檢查key再查找git log
    since_date = datetime.now().strftime('%Y-%m-01')
    note = start_note_generation(base_path, since_date)
    write_note(note_filename, note)
    print(f"已寫入 {note_filename} 至 note/ 資料夾")