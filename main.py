import songlogic
import os
print("目前執行位置:", os.getcwd())
print("資料夾內檔案:", os.listdir())
from pathlib import Path

CONFIG = {
    "auto_duration": False,
    "target_minutes": 20
}

def show_menu():
    status = "✅ 已開啟" if CONFIG["auto_duration"] else "❌ 已關閉"
    duration_info = f"({CONFIG['target_minutes']} 分鐘)" if CONFIG["auto_duration"] else ""
    
    print("\n" + "="*35)
    print(f"      🎵 SongMate 點歌系統")
    print(f"      自動配時：{status} {duration_info}")
    print("="*35)
    print(" 1. 🔄 更新歌庫 (從 Excel 匯入)")
    print(" 2. 🎲 隨機抽歌")
    print(" 3. 🔙 撤銷抽歌結果")
    print(" 4. 📂 歌庫管理 (匯出/刪除)")
    print(" 5. ⚙️ 系統設定 (配時開關/分鐘)")
    print(" 0. ❌ 退出程式")
    print("="*35)

def select_excel_file():
    files = [f for f in os.listdir('.') if f.endswith('.xlsx') and f != "song_library.xlsx"]
    
    print("\n--- 🔎 選擇點歌清單來源 ---")
    if not files:
        print("⚠️ 目錄下沒看到 .xlsx 檔案")
    else:
        for i, f in enumerate(files, 1):
            print(f" {i}. {f}")
    
    print(" m. 手動輸入完整路徑")
    print(" b. 返回主選單")
    
    choice = input("\n請選擇編號或輸入選項：").lower()
    
    if choice == 'b':
        return None
    elif choice == 'm':
        path = input("請輸入檔名 (含 .xlsx)：")
        return path if os.path.exists(path) else "FileNotFound"
    elif choice.isdigit() and 1 <= int(choice) <= len(files):
        return files[int(choice)-1]
    else:
        return "Invalid"

def settings_menu():
    while True:
        status = "開啟" if CONFIG["auto_duration"] else "關閉"
        print("\n--- ⚙️ 系統設定 ---")
        print(f" 1. 切換自動配時狀態 (目前：{status})")
        print(f" 2. 修改目標配時分鐘 (目前：{CONFIG['target_minutes']} 分鐘)")
        print(" 3. ⬅️ 返回主選單")
        
        choice = input("\n請選擇設定項目：")
        
        if choice == "1":
            CONFIG["auto_duration"] = not CONFIG["auto_duration"]
            new_status = "開啟" if CONFIG["auto_duration"] else "關閉"
            print(f"✅ 自動配時已設定為：{new_status}")
            
        elif choice == "2":
            new_min = input(f"請輸入新的目標分鐘數 (目前 {CONFIG['target_minutes']})：")
            if new_min.isdigit() and int(new_min) > 0:
                CONFIG["target_minutes"] = int(new_min)
                print(f"✅ 目標配時已修改為：{CONFIG['target_minutes']} 分鐘")
            else:
                print("⚠️ 請輸入正確的數字")
                
        elif choice == "3":
            break
        else:
            print("⚠️ 無效選項")

def main():
    while True:
        show_menu()
        choice = input("請選擇操作 (0-5)：")

        if choice == "1":
            file_path = select_excel_file()
            if file_path == "FileNotFound":
                print("❌ 找不到檔案，請確認名稱是否正確。")
            elif file_path == "Invalid":
                print("⚠️ 選項無效。")
            elif file_path:
                print(f"⌛ 正在從 '{file_path}' 更新資料...")
                try:
                    result = songlogic.update_song_library(file_path)
                    print(result)
                except Exception as e:
                    print(f"❌ 更新失敗：{e}")

        elif choice == "2":
            num = input("\n請輸入要抽幾首歌：")
            if num.isdigit():
                print("\n" + "="*20)
                result = songlogic.draw_songs(
                    num_songs=int(num), 
                    auto_duration=CONFIG["auto_duration"], 
                    target_min=CONFIG["target_minutes"]
                )
                print(result)
                print("="*20)
            else:
                print("⚠️ 請輸入數字")

        elif choice == "3":
            confirm = input("\n確定要撤銷今天的紀錄嗎？(y/n): ")
            if confirm.lower() == 'y':
                print(songlogic.delete_last_result())

        elif choice == "4":
            print("\n--- 📂 歌庫管理 ---")
            print("1. 📤 匯出歌庫 (不含姓名，僅限未播放)")
            print("2. 🗑️ 刪除主歌庫檔案")
            sub_choice = input("請選擇：")
            if sub_choice == "1":
                print(songlogic.export_song_library())
            elif sub_choice == "2":
                print(songlogic.delete_song_library())

        elif choice == "5":
            settings_menu()

        elif choice == "0":
            print("👋 再見！")
            break
        else:
            print("⚠️ 無效選項")

if __name__ == "__main__":
    main()