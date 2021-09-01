
from dotenv import load_dotenv
import discord
import re

from UserMeetTimeClass import UserMeetTime
from DatabaseConnectionModule import DatabaseWrapper
from Utils import TOKEN

# 接続に必要なオブジェクトを生成

client = discord.Client()

def checkTime(startTime, endTime, secondStartTime, secondEndTime):
    first = set(range(startTime, endTime))
    second = set(range(secondStartTime, secondEndTime))
    inter = first & second
    if len(inter) == 0:
        return 0
    else:
        inter = list(inter)
        inter.sort()
        return inter[0], inter[-1] + 1

def match(id):
    sql = "SELECT name, timezone, lang, startTime, endTime, firstDate, secondDate  from USERS WHERE id=%s" % id
    con, cur = executioner(sql)
    myData = cur.fetchone()
    exitConnection(con, cur)
    sql = "SELECT name, timezone, lang, startTime, endTime, firstDate, secondDate, id from USERS WHERE NOT (id=%s)" % id
    con, cur = executioner(sql)
    otherDatas = cur.fetchall()
    exitConnection(con, cur)
    if len(otherDatas) > 0:
        for d in otherDatas:
            if not(myData[2] == d[2]): 
                if myData[5] == d[6] or myData[6] == d[5] or myData[5] == d[5] or myData[6] == d[6]:
                    x = checkTime(int(myData[3]), int(myData[4]), int(d[3]), int(d[4]))
                    print(x)
                    if not(x == 0):
                        s = timeDecoder(x[0], x[1], myData[1], myData[5])
                        t = timeDecoder(x[0], x[1], d[1], d[5])
                        mes = [myData[0], s, d[0], t]
                        sql = "DELETE FROM USERS WHERE id=%s OR id=%s" %(id, d[7])
                        exitConnection(*executioner(sql))
                        return mes 
    return "No one was matched to you for now."


@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    if message.content.startswith('/match'):
        # /match jp(en) 09/22 21:00-22:00 9
        userInput = UserMeetTime(message)
        if userInput.isValidInput:
            dbConn = DatabaseWrapper()
            dbConn.register(userInput)
            # id = checkID(message.author.mention)
            # await message.channel.send('Registered ' + message.author.display_name + " Your ID is " + str(id))
    #         m = match(id)
    #         if "No one" in m:
    #             await message.channel.send(m)
    #         else:
    #             print(m)
    #             mes = m[0] + " Your language exchange starts at " + formStringTime(m[1][0]) + " , and ends at " + formStringTime(m[1][1]) + " on " + m[1][2]
    #             await message.channel.send(mes)
    #             mes = m[2] + " Your language exchange starts at " + formStringTime(m[3][0]) + " , and ends at " + formStringTime(m[3][1]) + " on " + m[3][2]
    #             await message.channel.send(mes)
    #             guild = client.get_guild(message.guild.id)
    #             await message.channel.send(showChannels(guild) + "are voice channels that you can use.")
    #     else:
    #         await message.channel.send('Wrong Command. Please check your command)')
    # elif message.content.startswith('/cancel'):
    #     id = re.split(' ', message.content)[1]
    #     await message.channel.send(cancel(message.author.mention, id))
    # elif message.content.startswith('/init'):
    #     init()
    #     await message.channel.send('Initialized Database')
    # elif message.content.startswith('/users'):
    #     await message.channel.send(showAllUsers())
    # elif message.content.startswith('/channels'):
    #     guild = client.get_guild(message.guild.id)
    #     await message.channel.send(showChannels(guild) + "are voice channels that you can use.")


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
 
'''
        TODO:
                Continue clean-up
                Get Timestamps working
                Change postgresql creation query to store timestamps
                Create class for all sql commands
                Re-create match functionality to work again
'''