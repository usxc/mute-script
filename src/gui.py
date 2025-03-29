import tkinter as tk
from tkinter import messagebox
import schedule
import time
import threading
import json
import os
import re
from datetime import datetime
from mute_control import mute, unmute

CONFIG_FILE = "src/config.json"

def save_schedule(times):
    """設定をJSONに保存"""
    with open(CONFIG_FILE, "w") as f:
        json.dump({"mute_times": times}, f)

def load_schedule():
    """JSONから設定を読み込む"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                data = json.load(f)
                return data.get("mute_times", [])
            except json.JSONDecodeError:
                return []
    return []

def is_valid_time_format(time_str):
    """ HH:MM のフォーマットチェック（先頭ゼロ必須）"""
    time_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"  # 00:00 ～ 23:59 のみ許可
    return re.fullmatch(time_pattern, time_str) is not None  # 厳密なチェック

def add_schedule():
    """時間帯をスケジュールに追加"""
    start_time = start_entry.get().strip()
    end_time = end_entry.get().strip()

    if start_time and end_time:
        try:
            # 時間フォーマットの確認
            start_time_obj = datetime.strptime(start_time, "%H:%M")
            end_time_obj = datetime.strptime(end_time, "%H:%M")
        except ValueError:
            messagebox.showerror("エラー", "時間のフォーマットは HH:MM の形式で入力してください！")
            return
        
        # ここでフォーマットチェックを追加
        if not is_valid_time_format(start_time) or not is_valid_time_format(end_time):
            messagebox.showerror("エラー", "時間のフォーマットは HH:MM の形式で入力してください！（例: 01:02）")
            return
    
        # 同じ時間の設定チェック
        if start_time == end_time:
            messagebox.showerror("エラー", "開始時間と終了時間は異なる時間に設定してください！")
            return
        
        # 時間の逆転チェック
        if start_time_obj > end_time_obj:
            messagebox.showerror("エラー", "終了時間は開始時間よりも後に設定してください！")
            return
        
        # 重複チェック
        for existing_time in mute_times:
            existing_start, existing_end = existing_time.split(' - ')
            existing_start_obj = datetime.strptime(existing_start, "%H:%M")
            existing_end_obj = datetime.strptime(existing_end, "%H:%M")

            # 新しい時間帯が既存の時間帯と重なっているか確認
            if (start_time_obj < existing_end_obj and end_time_obj > existing_start_obj):
                messagebox.showerror("エラー", "この時間帯は既存の時間と重複しています！")
                return
        
        # 重複がなければ時間帯を追加
        time_range = f"{start_time} - {end_time}"
        if time_range not in mute_times:
            mute_times.append(time_range)
            save_schedule(mute_times)

            # mute_times を開始時間で昇順ソート
            mute_times.sort(key=lambda x: datetime.strptime(x.split(' - ')[0], "%H:%M"))

            update_listbox()  # リストボックスを更新

            # スケジュールを登録
            schedule.every().day.at(start_time).do(mute)
            schedule.every().day.at(end_time).do(unmute)
            
            messagebox.showinfo("成功", f"{time_range} にミュートを設定しました！")
        else:
            messagebox.showwarning("警告", "既に登録済みの時間です！")
    else:
        messagebox.showerror("エラー", "開始時間と終了時間を入力してください！")

def remove_schedule():
    """選択したスケジュールを削除"""
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        mute_times.pop(index)
        save_schedule(mute_times)
        update_listbox()
    else:
        messagebox.showerror("エラー", "削除する時間を選択してください！")

def update_listbox():
    """リストボックスを更新"""
    listbox.delete(0, tk.END)
    for t in mute_times:
        listbox.insert(tk.END, t)

def schedule_checker():
    """バックグラウンドでスケジュールを監視"""
    while True:
        schedule.run_pending()
        time.sleep(1)

# 設定をロード
mute_times = load_schedule()

# GUIの作成
root = tk.Tk()
root.title("ミュート設定")
root.geometry("280x320")

tk.Label(root, text="開始時間 (HH:MM):").pack()
start_entry = tk.Entry(root)
start_entry.pack()

tk.Label(root, text="終了時間 (HH:MM):").pack()
end_entry = tk.Entry(root)
end_entry.pack()

tk.Button(root, text="設定", command=add_schedule).pack()

# 設定済みの時間を表示するリストボックス
tk.Label(root, text="設定済みの時間:").pack()
listbox = tk.Listbox(root)
listbox.pack()
update_listbox()

tk.Button(root, text="削除", command=remove_schedule).pack()

# スケジュール監視スレッドを開始
threading.Thread(target=schedule_checker, daemon=True).start()

# GUIを実行
root.mainloop()
