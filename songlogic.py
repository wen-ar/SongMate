import pandas as pd
import numpy as np
import datetime
import random
import os
from pathlib import Path

LIBRARY_FILE = "song_library.xlsx"
EXPORT_DIR = "/storage/emulated/0/SongMate/txt/" 

def time_to_seconds(t):
    if pd.isna(t): return 0
    if isinstance(t, (datetime.time, datetime.datetime)):
        return t.hour * 3600 + t.minute * 60 + t.second
    try:
        ts = str(t).strip().split(':')
        if len(ts) == 2:
            return int(ts[0]) * 60 + int(ts[1])
        if len(ts) == 3:
            return int(ts[0]) * 3600 + int(ts[1]) * 60 + int(ts[2])
    except:
        return 0
    return 0

def update_song_library(input_excel, output_excel=LIBRARY_FILE):
    try:
        new_df = pd.read_excel(input_excel)
        required_columns = ['姓名', '性別', '歌名', '歌曲連結', '歌曲時長']
        new_df = new_df[required_columns].copy()
        new_df = new_df.dropna(subset=['歌名'])

        new_df['duration_sec'] = new_df['歌曲時長'].apply(time_to_seconds)

        new_df['性別'] = new_df['性別'].str.strip().replace({
            '男': '男', '女': '女',
            'male': '男', 'female': '女'
        })

        if not Path(output_excel).exists():
            new_df['play_count'] = 0
            new_df['last_played'] = pd.NaT
            new_df['active'] = True

            new_df.to_excel(output_excel, index=False)
            return f"✅ 歌庫已建立，共 {len(new_df)} 首歌曲。"

        old_df = pd.read_excel(output_excel)

        old_df["last_played"] = pd.to_datetime(old_df["last_played"], errors="coerce")

        old_keys = set(zip(old_df['歌名'], old_df['性別']))

        filtered_rows = []
        added_count = 0

        for _, row in new_df.iterrows():
            key = (row['歌名'], row['性別'])

            if key not in old_keys:
                row['play_count'] = 0
                row['last_played'] = pd.NaT
                row['active'] = True

                filtered_rows.append(row)
                old_keys.add(key)
                added_count += 1

        if filtered_rows:
            add_df = pd.DataFrame(filtered_rows)
            final_df = pd.concat([old_df, add_df], ignore_index=True)
        else:
            final_df = old_df

        final_df.to_excel(output_excel, index=False)

        return f"✅ 更新完成，新增 {added_count} 首歌曲（已自動過濾重複）。"

    except Exception as e:
        return f"❌ 更新失敗：{str(e)}"
        
def draw_songs(num_songs=3, cooldown_days=5, auto_duration=False, target_min=20):
   
    if not Path(LIBRARY_FILE).exists():
        return "❌ 尚未建立歌庫，請先執行更新功能！"

    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(days=1)
    gender_today = "男" if tomorrow.day % 2 == 0 else "女"

    df = pd.read_excel(LIBRARY_FILE)
    df["last_played"] = pd.to_datetime(df["last_played"], errors="coerce")
    
    base_pool = df[(df["性別"] == gender_today) & (df["active"] == True)].copy()
   
    eligible_pool = base_pool[
        base_pool["last_played"].isna() | 
        (base_pool["last_played"] < today - datetime.timedelta(days=cooldown_days))
    ].copy()

    if len(eligible_pool) < num_songs:
        return f"⚠️ {gender_today}日歌曲不足（剩餘 {len(eligible_pool)} 首符合資格）"

    selected_indices = []
    
    if auto_duration:
        target_sec = target_min * 60
        best_diff = float('inf')
 
        for _ in range(1000):
            weights = 1 / (eligible_pool["play_count"] + 0.1)
            sample = eligible_pool.sample(n=num_songs, weights=weights)
            
            total_sec = sample['duration_sec'].sum()
            if total_sec <= target_sec:
                diff = target_sec - total_sec
                if diff < best_diff:
                    best_diff = diff
                    selected_indices = sample.index.tolist()
        
        if not selected_indices:
            selected_indices = eligible_pool.nsmallest(num_songs, 'duration_sec').index.tolist()
    else:
        weights = 1 / (eligible_pool["play_count"] + 0.1)
        selected_indices = np.random.choice(
            eligible_pool.index, size=num_songs, replace=False, 
            p=weights / weights.sum()
        )

    selected = df.loc[selected_indices]
    
    for idx in selected.index:
        df.loc[idx, "play_count"] += 1
        df.loc[idx, "last_played"] = pd.Timestamp(today)
    df.to_excel(LIBRARY_FILE, index=False)

    total_sec_sum = selected['duration_sec'].sum()
    min_sum, sec_sum = divmod(int(total_sec_sum), 60)
    
    result_lines = [f"🎶 播放清單（{gender_today}日）", f"總計時長：{min_sum:02d}:{sec_sum:02d} / {target_min}:00", "-"*20]
    for i, (_, r) in enumerate(selected.iterrows()):
        result_lines.append(f"{i+1}. {r.歌名} [{r.歌曲時長}] — {r.姓名}")
    
    result_text = "\n".join(result_lines)

    try:
        if not os.path.exists(EXPORT_DIR):
            os.makedirs(EXPORT_DIR)
        
        filename = f"playlist_{today.strftime('%Y%m%d')}_{gender_today}.txt"
        file_path = os.path.join(EXPORT_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result_text)
        return result_text + f"\n\n✅ 結果已存至：{filename}"
    except Exception as e:
        return result_text + f"\n\n⚠️ TXT 存檔失敗：{e}"

def delete_last_result():
   
    if not Path(LIBRARY_FILE).exists():
        return "❌ 歌庫不存在"
    
    df = pd.read_excel(LIBRARY_FILE)
    df["last_played"] = pd.to_datetime(df["last_played"])
    
    today = datetime.datetime.today().date()
    today_mask = df["last_played"].dt.date == today
    
    if not today_mask.any():
        return "ℹ️ 今天還沒有抽歌紀錄可以撤銷。"
    
    count = today_mask.sum()
    df.loc[today_mask, "play_count"] = df.loc[today_mask, "play_count"] - 1
    df.loc[today_mask, "last_played"] = pd.NaT
    
    df.to_excel(LIBRARY_FILE, index=False)
    return f"✅ 已成功撤銷今天的 {count} 首歌曲紀錄。"

def export_song_library(export_name="SongMate/export_song_library.xlsx"):
    
    if not Path(LIBRARY_FILE).exists(): return "❌ 歌庫不存在"
    
    df = pd.read_excel(LIBRARY_FILE)
    to_export = df[df["play_count"] == 0][['性別', '歌名', '歌曲連結', '歌曲時長']]
    
    os.makedirs(os.path.dirname(export_name), exist_ok=True)
    to_export.to_excel(export_name, index=False)
    return f"✅ 已匯出未播放歌單至：{export_name}"

def delete_song_library():
    if Path(LIBRARY_FILE).exists():
        os.remove(LIBRARY_FILE)
        return "🗑️ 歌庫檔案已刪除。"
    return "ℹ️ 找不到歌庫檔案。"
