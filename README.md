# git_log_to_note 使用說明

## 介紹

`git_log_to_note.py` 會自動讀取指定資料夾下所有有 `.git` 的專案的 git log，並用 LLM 產生繁體中文筆記，寫入 `notes/` 資料夾下以今天日期命名的 md 檔案。

## 安裝依賴

1. 建議使用虛擬環境：
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```
2. 安裝套件：
   ```
   pip install -r requirements.txt
   ```

## 使用方法

1. 執行主程式：
   ```
   python note_generater.py
   ```
2. 輸入你的專案根目錄路徑（例如 `C:\Users\User\repo_file`）。
3. 程式會自動抓取所有子資料夾的 git log，並產生筆記，寫入 `notes/` 資料夾。

## 產生的筆記
- 檔名格式：`YYYYMMDD.md`
- 每個專案一個區塊，區塊標題為專案資料夾名稱。

## 需要的 API Key
- 若要使用 Google Gemini LLM，請將 `Gemini_API_KEY` 設為環境變數或寫入 `.env` 檔案。

## 相關檔案
- `git_log_reader.py`：讀取 git log
- `note_generater.py`：產生筆記內容
- `notes/`：存放產生的 md 筆記

## 待新增功能
- 自動產生標題並避免重複
- 標記上次生成時間以避免內容重複
- git log較多時，保留部分內容用於下次生成筆記
- 添加 rule-based 正式生成規則(暫時直接貼上commit messege)