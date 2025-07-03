import discord
from discord.ext import commands
import asyncio
import openai
import pyttsx3
import random

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = "你的OpenAI_API_Key"
tts_engine = pyttsx3.init()

emotion_state = "normal"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def set_emotion(ctx, emo: str):
    global emotion_state
    emo = emo.lower()
    if emo in ["normal", "angry", "happy"]:
        emotion_state = emo
        await ctx.send(f"情緒狀態已切換為：{emotion_state}")
    else:
        await ctx.send("無效的情緒，請輸入 normal、angry 或 happy")

async def play_audio(ctx, file_path):
    if not ctx.author.voice:
        await ctx.send("請先加入語音頻道")
        return None
    channel = ctx.author.voice.channel
    voice_client = ctx.voice_client
    if not voice_client:
        voice_client = await channel.connect()

    source = discord.FFmpegPCMAudio(file_path)
    voice_client.play(source)
    while voice_client.is_playing():
        await asyncio.sleep(0.5)
    return voice_client

@bot.command()
async def angry(ctx):
    voice_client = await play_audio(ctx, "assets/gaga_angry.wav")
    if voice_client:
        await voice_client.disconnect()

@bot.command()
async def voice_chat(ctx, *, question: str):
    global emotion_state
    if not ctx.author.voice:
        await ctx.send("請先加入語音頻道")
        return

    prompt = question
    if emotion_state == "angry":
        prompt = f"請用生氣且帶有嘎嘎叫情緒的口吻回答：{question}"
    elif emotion_state == "happy":
        prompt = f"請用開心的語氣回答：{question}"
    else:
        prompt = question

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content

    await ctx.send(f"機器人回答：{answer}")

    tts_engine.save_to_file(answer, "reply.mp3")
    tts_engine.runAndWait()

    voice_client = ctx.voice_client
    if not voice_client:
        voice_client = await ctx.author.voice.channel.connect()

    source = discord.FFmpegPCMAudio("reply.mp3")
    voice_client.play(source)

    if emotion_state == "angry" and random.random() < 0.5:
        while voice_client.is_playing():
            await asyncio.sleep(0.5)
        source2 = discord.FFmpegPCMAudio("assets/gaga_angry.wav")
        voice_client.play(source2)

    while voice_client.is_playing():
        await asyncio.sleep(1)

    await voice_client.disconnect()

bot.run("你的Discord_Bot_Token")
