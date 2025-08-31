import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from datetime import datetime
import random
import webserver

load_dotenv()
token = os.getenv("DISCORD_TOKEN")  

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="Cmd:", intents=intents)

bay = ("cặc", "lồn", "địt", "đị","djt","dm","cc","cl","vcl","vl","đm","đmẹ","đm mày","đm con mẹ mày","đm con mày","đm con đĩ","đĩ","dmm","dmn","dcmn","dcm","dcmẹ","dcmẹ mày","dcm con mày","dcm con mẹ mày")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Chào mừng {member.name} đã tham gia máy chủ này.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    content = message.content.lower()
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    words = content.split()

    if any(word in bay for word in words):
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} 🚫 Không dùng từ bậy trong server!")
        except discord.Forbidden:
            await message.channel.send(f"{message.author.mention} ⚠️ Bot không có quyền xóa tin nhắn.")
        return

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Xin chào!, {ctx.author.name}")

@bot.command()
async def list_player(ctx):
    members = ctx.guild.members
    member_names = [member.name for member in members if not member.bot]
    await ctx.send(f"Các thành viên trong server: {', '.join(member_names)}")

@bot.command()
async def poll_yes_no(ctx, *, question):
    await ctx.send(f"Bình chọn có/không: {question}")
    add_reaction = await ctx.send("Bình chọn 1 trong 2:✅,❌.")
    await add_reaction.add_reaction("✅")
    await add_reaction.add_reaction("❌")

@bot.command()
async def poll_luachon(ctx, question, *options):
    if len(options) < 2:
        await ctx.send("Vui lòng cung cấp ít nhất 2 lựa chọn.")
        return

    options_str = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(options)])
    await ctx.send(f"Bình chọn nhiều lựa chọn: {question}\n{options_str}")

@bot.command()
async def remind(ctx, time: int, *, message):
    await ctx.send(f"Đã đặt nhắc nhở sau {time} giây: {message}")
    await discord.utils.sleep_until(discord.utils.utcnow() + discord.timedelta(seconds=time))
    await ctx.send(f"{ctx.author.mention} Nhắc nhở: {message}")

@bot.command()
async def time(ctx):
    now = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    await ctx.send(f"Giờ hiện tại: {now}")

@bot.command()
async def random_number(ctx, start: int, end: int):
    num = random.randint(start, end)
    await ctx.send(f"Số ngẫu nhiên từ {start} đến {end}: {num}")

@bot.command()
async def roll_dice(ctx, sides: int = 6):
    result = random.randint(1, sides)
    await ctx.send(f"{ctx.author.mention} đã tung xúc xắc {sides} mặt và được: {result}")

@bot.command()
async def countdown(ctx, seconds: int):
    if seconds < 1:
        await ctx.send("Thời gian phải lớn hơn 0 giây.")
        return
    await ctx.send(f"Bắt đầu đếm ngược {seconds} giây!")
    while seconds > 0:
        await ctx.send(f"Còn lại: {seconds} giây")
        await discord.utils.sleep_until(discord.utils.utcnow() + discord.timedelta(seconds=1))
        seconds -= 1
    await ctx.send(f"@everyone Đếm ngược đã kết thúc! {ctx.author.mention}")


webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)


