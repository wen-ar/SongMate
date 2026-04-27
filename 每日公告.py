from datetime import datetime, timedelta

def generate_announcement(gender, minutes, seconds):
    # 取得今天日期 +1 天
    tomorrow = datetime.today() + timedelta(days=1)
    weekday_map = {0:"一",1:"二",2:"三",3:"四",4:"五",5:"六",6:"日"}
    weekday = weekday_map[tomorrow.weekday()]

    # 播放時間固定
    play_time = "12：00～12：20"

    # 固定連結
    links = {
        "男生": "https://open.spotify.com/playlist/6ExD8QyzdVRpwfJt0zacHl?si=g7TvZMOrTcCVt0YM2kdyWQ",
        "女生": "https://open.spotify.com/playlist/3c0KHVbjKmlk2BqmcldeeA?si=J_c8EpssSD-vSvmZsQxLyA"
    }
    link = links.get(gender, "（未提供連結）")

    # 時長格式化
    duration = f"{minutes}分{seconds}秒"

    # 公告範本
    announcement = f"""
明{tomorrow.month}/{tomorrow.day}（{weekday}）為{gender}
播放時間為{play_time}
總時長：{duration}
公告欄
目前歌單連結：
{link}
"""
    return announcement.strip()

# 主程式互動
if __name__ == "__main__":
    gender = input("請輸入性別（男生/女生）：").strip()
    minutes = input("請輸入時長（分鐘）：").strip()
    seconds = input("請輸入時長（秒鐘）：").strip()

    print("\n=== 公告生成結果 ===")
    print(generate_announcement(gender, minutes, seconds))