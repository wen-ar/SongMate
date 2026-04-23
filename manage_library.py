import songlogic

print("請選擇操作：")
print("1. 刪除歌庫")
print("2. 匯出歌庫")

choice = input("輸入選項 (1/2)： ")

if choice == "1":
    print(songlogic.delete_song_library())
elif choice == "2":
    print(songlogic.export_song_library("SongMate/export_song_library.xlsx"))
else:
    print("⚠️ 無效選項")