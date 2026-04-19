import discord
from discord.ext import commands
import random
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")

TARGET_ROLE_ID = 1495420804819845301  # ←ロールID

# =========================
# 起動
# =========================
@bot.event
async def on_ready():
    print("ログインしました！")
    await bot.change_presence(activity=discord.Game(name="V1.0"))

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
    if any(word in message.content for word in ["69","スカトロ","児ポ","腸内洗浄"):
        msg = await message.channel.send("投票開始…")
        view = VoteView(message.author, msg)

        await msg.edit(
            content=f"{message.author.mention} にロールを付けますか？（1人1票・60秒）",
            view=view
        )

    # コマンド処理（必ず最後）
    await bot.process_commands(message)

# =========================
bot.run(os.environ["TOKEN"])
