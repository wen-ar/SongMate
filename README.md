# 🎵 SongMate 點歌系統

一個簡單的 **命令列互動式點歌系統**，支援歌庫管理、隨機抽歌、撤銷紀錄、匯出歌單等功能。  
專案以 **Python + Pandas** 為基礎，並搭配 Excel 檔案作為歌庫來源。

---

## 📂 專案結構
├── main.py              # 主程式入口，提供選單操作

├── songlogic.py         # 核心邏輯：更新、抽歌、刪除、匯出等功能

├── update_library.py    # 單獨更新歌庫

├── draw_songs.py        # 單獨抽歌

├── delete_result.py     # 單獨撤銷抽歌紀錄

├── manage_library.py    # 單獨管理歌庫（匯出/刪除）

└── song_library.xlsx    # 歌庫檔案（執行後生成）

---

## ⚙️ 功能介紹

- **歌庫更新**：從 Excel 匯入，並自動過濾重複歌曲  
- **隨機抽歌**：依照性別日規則，並支援「自動配時」功能  
- **撤銷抽歌**：可撤銷當天抽歌紀錄，恢復歌庫狀態  
- **歌庫管理**：
  - 匯出未播放歌曲清單
  - 刪除主歌庫檔案  
- **系統設定**：
  - 切換自動配時開關
  - 修改目標分鐘數  

---

## ▶️ 使用方式

### 1. 執行主程式
python main.py

### 2. 單獨執行功能
 - 更新歌庫：
 python update_library.py

 - 抽歌：
 python draw_songs.py

 - 撤銷抽歌紀錄：
 python delete_result.py

 - 管理歌庫：
 python manage_library.py

---

### 🛠️ 環境需求

 - Python 3.8+
 - 套件：
   - pandas
  - numpy
   - openpyxl

 - 安裝方式：
 pip install pandas numpy openpyxl

---

### 📌 注意事項

 - 抽歌時會依照「性別日」規則：
   - 偶數日 → 男
   - 奇數日 → 女
 - 自動配時功能會嘗試讓抽歌總時長接近設定的目標分鐘數  
 - 若歌庫不足，系統會提示剩餘可抽歌曲數量  

---
