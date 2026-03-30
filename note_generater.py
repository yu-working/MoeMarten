from google import genai
import dotenv
import os

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
    if "python" in prompt:
        return "Python 是一種高級程式語言，適合用於資料分析、機器學習和網頁開發等領域。"
    elif "llm" in prompt:
        return "LLM（Large Language Model）是一種基於深度學習的自然語言處理模型，能夠理解和生成自然語言文本。"
    elif "agent" in prompt:
        return "Agent 是一種自主軟體實體，能夠感知環境並執行任務以達成特定目標。"
    else:
        return "hello world"
    
def start_note_generation(prompt=""):
    # 這裡可以選擇使用 LLM 或規則基礎的方法來生成筆記
    # 目前示例中直接使用 LLM 方法
    dotenv.load_dotenv()
    if "Gemini_API_KEY" in os.environ:
        return generate_by_llm(prompt)
    else:
        return generate_by_rule_based(prompt)

if __name__ == "__main__":
    prompt = input("請輸入關鍵字或Git log來生成筆記：")
    note = start_note_generation(prompt)
    print(note)