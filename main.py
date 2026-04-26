import discord
from discord.ext import commands
import random
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True      # ←必須
intents.presences = True    # ←これないとSpotify無理
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")

TARGET_ROLE_ID = 1495420804819845301  # ←ロールID

# =========================
# 起動
# =========================
@bot.event
async def on_ready():
    print("ログインしました！")
    await bot.change_presence(activity=discord.Game(name="V1.25"))

# =========================
# 投票View
# =========================
class VoteView(discord.ui.View):
    def __init__(self, target_user, message):
        super().__init__(timeout=60)
        self.target_user = target_user
        self.message = message

        self.yes = 0
        self.no = 0
        self.voters = set()

    def make_bar(self):
        total = self.yes + self.no
        if total == 0:
            return "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜"

        ratio = self.yes / total
        filled = int(ratio * 10)
        return "🟩" * filled + "⬜" * (10 - filled)

    def update_labels(self):
        self.yes_button.label = f"はい ({self.yes})"
        self.no_button.label = f"いいえ ({self.no})"

    async def update_message(self, interaction):
        self.update_labels()
        bar = self.make_bar()

        content = (
            f"{self.target_user.mention} に汚い名誉を与えますか？\n"
            f"{bar}\n"
            f"はい: {self.yes} / いいえ: {self.no}"
        )

        await interaction.response.edit_message(content=content, view=self)

    @discord.ui.button(label="はい (0)", style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id in self.voters:
            await interaction.response.send_message("どんだけ嫌ってるんｗｗｗ", ephemeral=True)
            return

        self.voters.add(interaction.user.id)
        self.yes += 1
        await self.update_message(interaction)

    @discord.ui.button(label="いいえ (0)", style=discord.ButtonStyle.red)
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id in self.voters:
            await interaction.response.send_message("どんだけ嫌ってるんｗｗｗ", ephemeral=True)
            return

        self.voters.add(interaction.user.id)
        self.no += 1
        await self.update_message(interaction)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        bar = self.make_bar()

        result_text = (
            f"投票終了！\n"
            f"{bar}\n"
            f"はい: {self.yes} / いいえ: {self.no}"
        )

        await self.message.edit(content=result_text, view=self)

        guild = self.target_user.guild
        role = guild.get_role(TARGET_ROLE_ID)

        await self.message.channel.send(
            f"📊 投票結果\n対象: {self.target_user.mention}\nはい: {self.yes}\nいいえ: {self.no}"
        )

        if self.yes > self.no:
            await self.target_user.add_roles(role)
            await self.message.channel.send(
                f"{self.target_user.mention} に汚い名誉を与えたよ！（24時間後に削除）"
            )

            await asyncio.sleep(86400)
            await self.target_user.remove_roles(role)

        else:
            await self.message.channel.send("ロールは付与されなかった。しょうもな")

# =========================
# メッセージ処理
# =========================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 🔹 ランダム煽り
    if random.random() < 0.01:
        await message.channel.send("陰キャやんｗｗｗｗｗ🫵😂🫵😂🫵😂←陽キャたち")

    # 🔹 特定ユーザー
    if message.author.id == 1344954155353243650:
        if random.random() < 0.1:
            responses = [
                "おまえちんこやんｗｗｗｗ😂😂😂😂",
                "静かにしろ😡",
                "くかぁ🫵😂🫵😂🫵😂",
                "おい😂それはだめだろ🫵😂",
                "お、おう😅😅😅😅"
            ]
            await message.channel.send(f"{message.author.mention} {random.choice(responses)}")

    # 🔹 ワード反応
    if any(word in message.content for word in ["お、おう","わたあめ","ばこぴょん","ほね"]):
        await message.channel.send(random.choice([
            "お、おう","あ、うん、","なにいってん","は？",
            "https://youtu.be/J5Z7tIq7bco"
        ]))

    elif any(word in message.content for word in ["ばこん","バコン","997951321237893130"]):
        await message.channel.send(random.choice([
            "どうした","ん？","要件をいえ",
            "えろ"
        ]))

    elif any(word in message.content for word in ["アベル","アテネ","あべる","あてね"]):
        await message.channel.send(random.choice([
            "https://www.youtube.com/@ABELLandATENE",
            "https://www.youtube.com/watch?v=zP7qRsknFxs",
            "https://www.youtube.com/watch?v=zTCvaySiWYY",
            "https://www.youtube.com/watch?v=8DBRSuzHPxw",
            "https://www.youtube.com/watch?v=I7HuIlFUx44"
        ]))

    # 投票トリガー
    if any(word in message.content for word in ["スカトロ","児ポ","腸内洗浄"]):
        msg = await message.channel.send("投票開始…")
        view = VoteView(message.author, msg)

        await msg.edit(
            content=f"{message.author.mention} に汚名誉を付けますか？（1人1票・60秒）",
            view=view
        )

    await bot.process_commands(message)

games = {}

@bot.command()
async def core(ctx):
    if ctx.author.id in games:
        return await ctx.send("すでに実験中だぞ")

    games[ctx.author.id] = {
        "danger": 0,
        "turn": 0
    }

    view = CoreView(ctx.author)
    msg = await ctx.send(
        "☢️ 日本への核爆弾を投下するために核爆弾を作ろう！！\nボタンで操作しろ\n🙂 安定\n危険度: 0% / ターン: 0",
        view=view
    )

    view.message = msg  # ←これ重要


class CoreView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=60)
        self.user = user
        self.message = None  # ←追加

    def get_status(self):
        g = games.get(self.user.id)
        if not g:
            return "ゲーム終了"

        if g["danger"] > 70:
            state = "😨 やばい"
        elif g["danger"] > 40:
            state = "😐 微妙"
        else:
            state = "🙂 安定"

        return f"{state}\n☢️ 危険度: {g['danger']}% / ターン: {g['turn']}"

    async def process(self, interaction, change):
        if interaction.user != self.user:
            return await interaction.response.send_message("お前の実験じゃない", ephemeral=True)

        g = games.get(self.user.id)
        if not g:
            return await interaction.response.send_message("ゲーム終わってる", ephemeral=True)

        difficulty = 1 + (g["turn"] // 5)

        if isinstance(change, tuple):
            g["danger"] = max(0, g["danger"] + random.randint(change[0], change[1]))
        else:
            g["danger"] = max(0, g["danger"] + change * difficulty)

        g["turn"] += 1

        # 事故
        if random.random() < 0.08:
            await interaction.response.edit_message(
                content=f"💀 助手がうんこを漏らしてしまって、あなたはその悪臭に耐え切れずしんだ\nターン: {g['turn']}",
                view=None
            )
            del games[self.user.id]
            return

        # ゲームオーバー
        if g["danger"] >= 100:
            await interaction.response.edit_message(
                content=f"💥 あなたは今朝素手でトマトスパゲティを食べたことを忘れて、ドライバーを滑らせ、落とした瞬間、部屋に眩い綺麗な青色と共に致死量の放射能を浴び\nターン: {g['turn']}",
                view=None
            )
            del games[self.user.id]
            return

        # クリア
        if g["turn"] >= 15:
            await interaction.response.edit_message(
                content=f"🎉 あなたは核爆弾「オレオットセイ」を作り上げたことにより生涯使い切れないほどの金と名誉を手に入れた！\n危険度: {g['danger']}%\nターン: {g['turn']}",
                view=None
            )
            del games[self.user.id]
            return

        await interaction.response.edit_message(
            content=self.get_status(),
            view=self
        )

    @discord.ui.button(label="安定", style=discord.ButtonStyle.green)
    async def stable(self, interaction, button):
        await self.process(interaction, -10)

    @discord.ui.button(label="観測", style=discord.ButtonStyle.blurple)
    async def observe(self, interaction, button):
        await self.process(interaction, +15)

    @discord.ui.button(label="テスト", style=discord.ButtonStyle.red)
    async def test(self, interaction, button):
        await self.process(interaction, +20)

    @discord.ui.button(label="冷却", style=discord.ButtonStyle.gray)
    async def cool(self, interaction, button):
        await self.process(interaction, (-10, 30))  # ←修正

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        if self.user.id in games:
            del games[self.user.id]

        if self.message:
            await self.message.edit(content="⌛ 時間切れで終了", view=self)

bot.run(os.environ["TOKEN"])
