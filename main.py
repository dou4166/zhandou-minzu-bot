import discord
from discord.ext import commands
import json
import level_system

# 載入設定檔
with open("config.json", "r") as f:
    config = json.load(f)

# 機器人初始化
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} 已上線！嘎嘎嘎")
    level_system.start_tracking(bot)

@bot.command()
async def 等級(ctx):
    level = level_system.get_user_level(ctx.author.id)
    await ctx.send(f"{ctx.author.mention} 你的鴨等是 Lv{level} 🦆")

# 啟動機器人
bot.run(config["TOKEN"])
