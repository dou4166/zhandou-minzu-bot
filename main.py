import discord
from discord.ext import commands
import os
import openai
import asyncio

# 讀取環境變數
openai.api_key = os.getenv("OPENAI_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

emotion = "normal"
voice_channel = None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.command()
async def set_emotion(ctx, emo):
    global emotion
    emotion = emo
    await ctx.send(f"情緒已設定為：{emotion}")

@bot.command()
async def voice_chat(ctx, *, text):
    global voice_channel
    voice_channel = ctx.author.voice.channel if ctx.author.voice else None
    if voice_channel is None:
        await ctx.send("你必須先加入語音頻道！")
        return

    vc = await voice_channel.connect()
    # 播放語音的邏輯寫這裡，這是示意
    # 播放嘎嘎叫音效
    if emotion == "angry":
        source = discord.FFmpegPCMAudio(
        "assets/gaga_angry.wav",
        executable="C:/ffmpeg/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"
        )

        vc.play(source)
        while vc.is_playing():
            await asyncio.sleep(1)
    await vc.disconnect()
    await ctx.send(f"我說：{text}")

bot.run(DISCORD_TOKEN)
