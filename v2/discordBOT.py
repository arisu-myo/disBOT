
from CeVioceCreate import CeVioAiCreateAudio, ReText
import discord
from discord.ext import commands  # , tasks
import datetime
import tracemalloc
import os

tracemalloc.start()


def event_time():
    now = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%m:%S : "))
    return now


data = {}
white_channel = []
cv = CeVioAiCreateAudio(
    str(os.path.join("C:\\", "Program Files", "CeVIO", "CeVIO AI")))


def get_casts():
    cast_list = []
    for cast in cv.get_active_cast():
        cast_list.append(cast)
    return cast_list


def get_emotions(cast):
    emotion_list = []
    for emotion in cv.get_emotions(cast):
        emotion_list.append(emotion.Name)
    return emotion_list


class VioceBot(commands.Cog, name="ボイスボッド"):
    @commands.command()
    async def join(self, ctx):
        """現在いるボイスチャンネルにBOTを接続します。"""
        if ctx.author.voice is None:
            await ctx.send("コマンド実行者がVOICEチャンネルに参加していません")
            return

        white_channel.append(ctx.message.channel.id)
        try:

            await ctx.author.voice.channel.connect()
            await ctx.send("接続に成功しました。")
            return
        except Exception as e:
            print(e)
            await ctx.message.guild.voice_client.disconnect()
            await ctx.author.voice.channel.connect()

            await ctx.send("すでにボイスチャンネルに入ってため再度接続しました。")
            return

    @commands.command()
    async def unjoin(self, ctx):
        """ボイスチャンネルとの接続を解除します。"""
        white_channel.clear()
        try:
            await ctx.message.guild.voice_client.disconnect()
            await ctx.send("ボイスチャンネルへの接続解除しました")
            return
        except Exception as e:
            print(str(e))

            await ctx.send("ボイスチャンネルへの接続を正常解除できません。")
            return


class RootUserSystem(commands.Cog, name="開発者向け機能"):
    """開発者向けのシステムです
    この以下のコマンド郡は、システム管理者に許可を得てください
    """

    @commands.command()
    async def logout(self, ctx):
        await ctx.message.delete()
        end()
        # await client.close()
        # client.loop.stop()
        # print("logout")
        return

    @commands.command()
    async def set_channel(self, ctx):
        await ctx.message.delete()
        white_channel.append(ctx.message.channel.id)
        return


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="$",
                      intents=intents)
client.add_cog(RootUserSystem(client))
client.add_cog(VioceBot(client))


@client.event
async def on_ready():
    print(f"{event_time()}BOT起動しました...")


@client.event
async def on_message(message):

    if message.author.bot:
        return

    if client.command_prefix in message.content:
        pass

    # voice_bot 本体
    elif message.guild.voice_client:

        # 許可が出ていないチャンネルでの発言は禁止
        if message.channel.id not in white_channel:
            return

        # cevio setting
        cv.cast = data["cast"]
        cv.volume = data["volume"]
        cv.tonescale = data["tonescale"]
        cv.tone = data["tone"]
        cv.alpha = data["alpha"]
        cv.speed = data["speed"]

        # audio setting
        cv.file_name = data["file_name"]
        cv.file_path = data["file_path"]

        # text replace
        text = ReText().new_remove_all(data, message.content)

        # info:メッセージの割り込みを可能とする

        if message.guild.voice_client.is_playing() is True:
            print(message.guild.voice_client.is_playing())
            message.guild.voice_client.stop()

        file = cv.output_wav(text)
        message.guild.voice_client.play(discord.FFmpegPCMAudio(file))

        return
    else:
        pass
    await client.process_commands(message)


@ client.event
async def on_command_error(ctx, error):
    await ctx.send("エラーコマンド実行者:{}\n エラー詳細:{}"
                   .format(ctx.message.author.name, error))


def start(userdata=None):

    if userdata is None:
        raise ValueError("dict to None")

    for key in userdata.datas:
        data[key] = userdata[key]

    client.command_prefix = userdata["command_prefix"]

    client.loop.create_task(client.start(userdata["token"]))

    try:
        client.loop.run_forever()
    finally:
        client.loop.close()
        print(f"{event_time()}終了が実行されました!")


def change_data(p: dict):
    for key in p:
        data[key] = p[key]
    print(f"{event_time()}パラメーターの変更が完了いたしました。")


def end():
    client.loop.stop()
