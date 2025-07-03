import discord
import asyncio
import json
import os
from datetime import datetime

DATA_FILE = "data/users.json"

voice_times = {}  # {user_id: join_time}

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def calculate_required_time(level):
    if level == 1:
        return 0
    total = 10  # Lv2 起始需要 10 分
    for i in range(2, level):
        total += (i - 1) * 3
    return total

def get_user_level(user_id):
    data = load_data()
    user = str(user_id)
    if user not in data:
        return 1
    total_minutes = data[user]["minutes"]
    level = 1
    while total_minutes >= calculate_required_time(level + 1):
        level += 1
    return level

def start_tracking(bot):
    @bot.event
    async def on_voice_state_update(member, before, after):
        user_id = str(member.id)
        data = load_data()

        # 進入語音
        if before.channel is None and after.channel is not None:
            voice_times[user_id] = datetime.utcnow()

        # 離開語音
        elif before.channel is not None and after.channel is None:
            if user_id in voice_times:
                join_time = voice_times.pop(user_id)
                now = datetime.utcnow()
                minutes = int((now - join_time).total_seconds() // 60)

                if user_id not in data:
                    data[user_id] = {"minutes": 0, "level": 1}

                data[user_id]["minutes"] += minutes
                old_level = data[user_id]["level"]
                new_level = get_user_level(user_id)

                if new_level > old_level:
                    data[user_id]["level"] = new_level
                    if new_level % 10 == 0:
                        channel = member.guild.system_channel
                        if channel:
                            await channel.send(f"🎉 {member.mention} 升到了 Lv{new_level}！嘎嘎嘎～🦆")

                save_data(data)
