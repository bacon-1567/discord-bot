import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print("ログインしました！")
    await bot.change_presence(activity=discord.Game(name="てすとちゅー"))

@bot.command()
async def ping(ctx):
    raw_ping = bot.latency
    ping = round(raw_ping * 1000)
    await ctx.reply(f"しかたねぇな\nBotのPing値は{ping}msやカス🫵😒")

@bot.command()
async def このサーバーの情報を教えろカス(ctx):
  guild = ctx.message.guild
  roles =[role for role in guild.roles]
  text_channels = [text_channels for text_channels in guild.text_channels]
  embed = discord.Embed(title=f"{guild.name}info",color=0x3683ff)
  embed.add_field(name="管理者",value=f"{ctx.guild.owner}",inline=False)
  embed.add_field(name="ID",value=f"{ctx.guild.id}",inline=False)
  embed.add_field(name="チャンネル数",value=f"{len(text_channels)}",inline=False)
  embed.add_field(name="ロール数",value=f"{len(roles)}",inline=False)
  embed.add_field(name="サーバーブースター",value=f"{guild.premium_subscription_count}",inline=False)
  embed.add_field(name="メンバー数",value=f"{guild.member_count}",inline=False)
  embed.add_field(name="サーバー設立日",value=f"{guild.created_at}",inline=False)
  embed.set_footer(text=f"実行者 : {ctx.author} ")
  await ctx.send(embed=embed)

@bot.command()
async def 自分情報(ctx):
  embed = discord.Embed(title=f"user {ctx.author.name}",description="これがおめぇの情報だカス🫵😒",color=0x3683ff)
  embed.add_field(name="名前",value=f"{ctx.author.mention}",inline=False)
  embed.add_field(name="ID",value=f"{ctx.author.id}",inline=False)
  embed.add_field(name="ACTIVITY",value=f"{ctx.author.activity}",inline=False)
  embed.add_field(name="TOP_ROLE",value=f"{ctx.author.top_role}",inline=False)
  embed.add_field(name="discriminator",value=f"#{ctx.author.discriminator}",inline=False)
  embed.add_field(name="サーバー参加",value=f"{ctx.author.joined_at.strftime('%d.%m.%Y, %H:%M Uhr')}",inline=False)
  embed.add_field(name="アカウント作成",value=f"{ctx.author.created_at.strftime('%d.%m.%Y, %H:%M Uhr')}",inline=False)
  embed.set_thumbnail(url=f"{ctx.author.avatar.url}")
  embed.set_footer(text=f"実行者 : {ctx.author} ")
  await ctx.send(embed=embed)

class Button(discord.ui.View):
    def __init__(self, author):
        super().__init__()
        self.author = author  # コマンド実行者を保存

    async def disable_all_buttons(self):
        for item in self.children:
            item.disabled = True

    async def handle_interaction(self, interaction, message):
        # 押せる人を制限
        if interaction.user != self.author:
            await interaction.response.send_message("あなたは押せません", ephemeral=True)
            return

        # ボタン無効化
        await self.disable_all_buttons()

        # メッセージ更新（これが重要）
        await interaction.response.edit_message(content=message, view=self)

    @discord.ui.button(label="すぴきでるじばぜよ", style=discord.ButtonStyle.grey)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_interaction(interaction, "ｳﾜｧ!ﾊﾞｺﾝﾃﾞﾙｼﾞﾊﾞｾﾞﾖ!!")

    @discord.ui.button(label="アイスティー", style=discord.ButtonStyle.blurple)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_interaction(interaction, "淫夢でくさなんよww🫵😂")

    @discord.ui.button(label="１１４５１４", style=discord.ButtonStyle.green)
    async def button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_interaction(interaction, "淫夢でくさなんよww🫵😂")

    @discord.ui.button(label="８１０", style=discord.ButtonStyle.red)
    async def button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_interaction(interaction, "淫夢でくさなんよww🫵😂")


@bot.command()
async def button(ctx):
    view = Button(ctx.author)  # ←ここで実行者を渡す
    await ctx.send("淫夢診断", view=view)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if random.random() < 0.01:
        await message.channel.send("陰キャやんｗｗｗｗｗ🫵😂🫵😂🫵😂←陽キャたち")

    await bot.process_commands(message)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.id == 1344954155353243650:
        if random.random() < 0.2:
            responses = [
                "おまえちんこやんｗｗｗｗ😂😂😂😂",
                "静かにしろ😡",
                "くかぁ🫵😂🫵😂🫵😂",
                "おい😂それはだめだろ🫵😂",
                "お、おう😅😅😅😅"
            ]
            await message.channel.send(f"{message.author.mention} {random.choice(responses)}")

    await bot.process_commands(message)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 🔹 最初の反応
    words = ["お、おう", "わたあめ", "殺す", "イク","<@1490045435824308234>"]

    if any(word in message.content for word in words):
        responses = [
            "お、おう",
            "あ、うん、",
            "なにいってん",
            "は？",
            "https://youtu.be/J5Z7tIq7bco?si=-xNHR18ELy-nGoxF"
        ]
        sent = await message.channel.send(random.choice(responses))

    # 🔹 Botのメッセージに返信したかチェック
    if message.reference:  # 返信かどうか
        replied_msg = await message.channel.fetch_message(message.reference.message_id)

        if replied_msg.author == bot.user:
            await message.channel.send("ところでパンツ見せて")

    await bot.process_commands(message)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 🔹 最初の反応
    words = ["ばこん","バコン","997951321237893130"]

    if any(word in message.content for word in words):
        responses = [
            "どうした",
            "ん？",
            "ちんこ！！",
            "要件をいえ",
            "https://youtu.be/yegBF2yoTDo?si=CJAbwRgAJqUVAj03"
        ]
        sent = await message.channel.send(random.choice(responses))

bot.run(os.environ["TOKEN"])
