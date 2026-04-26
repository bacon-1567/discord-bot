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

SPOTIFY_ROLE_ID = 1493255008807026748

# =========================
# 起動
# =========================
@bot.event
async def on_ready():
    print("ログインしました！")
    await bot.change_presence(activity=discord.Game(name="V1.2"))

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

@bot.command()
async def spotify(ctx):
    embed = discord.Embed(title="🎧 Spotify再生中", color=0x1DB954)

    found = False

    for member in ctx.guild.members:

        if not any(role.id == SPOTIFY_ROLE_ID for role in member.roles):
            continue

        if not member.activities:
            continue

        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                found = True

                embed.add_field(
                    name=f"🎧 {member.name}",
                    value=(
                        f"**曲名:** {activity.title}\n"
                        f"**アーティスト:** {', '.join(activity.artists)}\n"
                        f"**アルバム:** {activity.album}"
                    ),
                    inline=False
                )

    if not found:
        await ctx.send("誰も聴いてない😅")
    else:
        await ctx.send(embed=embed)

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

    # コマンド処理（必ず最後）
    await bot.process_commands(message)

games = {}

@bot.command()
async def core(ctx):
    games[ctx.author.id] = {
        "danger": 0,
        "turn": 0
    }
    await ctx.send("日本に落とす第3の核爆弾を作ろう！\n危険度: 0%")

@bot.command()
async def action(ctx, act):
    if ctx.author.id not in games:
        return await ctx.send("先に !core しろ")

    g = games[ctx.author.id]

    if act == "ドライバーを固定する":
        g["danger"] = max(0, g["danger"] - 15)
    elif act == "ドライバーを少し動かす":
        g["danger"] += 10
    elif act == "ドライバーを下に向ける":
        g["danger"] += 25
    elif act == "冷却":
        g["danger"] = max(0, g["danger"] - random.randint(10, 30))
    else:
        return await ctx.send("コマンド: ドライバーを固定する / ドライバーを少し動かす / ドライバーを下に向ける / 冷却")

    g["turn"] += 1

    # 💥 ゲームオーバー
    if g["danger"] >= 100:
        await ctx.send(f"💥 助手がドライバーを落とした瞬間、眩い青い光に包まれ致死量の放射能を浴びた\nターン: {g['turn']}")
        del games[ctx.author.id]
        return

    await ctx.send(f"☢️ 危険度: {g['danger']}% / ターン: {g['turn']}")

# =========================
bot.run(os.environ["TOKEN"])
