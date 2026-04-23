import songlogic

# 程式執行時詢問使用者要抽幾首歌
num = int(input("請輸入要抽幾首歌： "))

print("\n抽歌結果：")
print(songlogic.draw_songs(num))