import discord
import re
import psycopg2
TOKEN = 'ODgxNDMxNTY5NTQ4NTgyOTEz.YSsvHg.8P8t-ws9Zb7oZFfsS-y_zEPKybM'
# 接続に必要なオブジェクトを生成

client = discord.Client()
def connect():
    con = psycopg2.connect("postgres://ogscmjrvhrudqo:8b640667ddf8d36c3913cd8a6e53d817c248a54aa2d65174ed5f73c9f9a22bcb@ec2-54-147-93-73.compute-1.amazonaws.com:5432/d8l3no5ghmat9c", sslmode='require')
    return con
def exitConnection(con, cur):
    cur.close()
    con.close()
def executioner(sql):
    con = connect()
    cur = con.cursor()
    cur.execute("BEGIN")
    cur.execute(sql)
    if not(re.split(' ', sql)[0] == "SELECT"):
        con.commit()
    return (con, cur)
def timeEncoder(s, tz, dt):
    a = re.split('[:：]', s)
    i = int(a[0]) * 60 + int(a[1]) - int(tz) * 60
    if i < 0:
        i = 60 * 24 + i
        s = re.split('[/／]', dt)
        s[1] = str(int(s[1]) - 1)
        realDt = s[0] + '/' + s[1]
        return i, realDt
    elif i >= 60 * 24:
        i = i - 60 * 24
        s = re.split('[/／]', dt)
        s[1] = str(int(s[1]) + 1)
        realDt = s[0] + '/' + s[1]
        return i, realDt
    return i, dt
def timeDecoder(x, y, tz, dt):
    a = x + 60 * tz
    b = y + 60 * tz
    realDt = dt
    s = re.split('[/／]', dt)
    if a >= 60 * 24:
        a = a - 60 * 24
        s[1] = str(int(s[1]) + 1)
    elif a < 0:
        a = 60 * 24 + a
        s[1] = str(int(s[1]) - 1)
    if b >= 60 * 24:
        b = b - 60 * 24
    elif b < 0:
        b = 60 * 24 + b
    realDt = s[0] + '/' + s[1]
    start = str(a // 60) + ':' + str(a % 60)
    end = str(b // 60) + ':' + str(b % 60)
    return start, end, realDt
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
def register(s):
    dt = s[2]
    start, end = re.split('[-ー]', s[3])
    x = timeEncoder(start, s[4], dt)
    y = timeEncoder(end, s[4], dt)
    print(x)
    print(y)

    sql = "INSERT INTO USERS (name, timezone, lang, startTime, endTime, firstDate, secondDate) VALUES ('%s', %s, '%s', '%s', '%s', '%s', '%s')" % (s[0], s[4], s[1], x[0], y[0], x[1], y[1])
    exitConnection(*executioner(sql))
    print("Registered")

def init():
    sql = "CREATE TABLE USERS (id SERIAL, name text, timezone integer, lang text, startTime text, endTime text, firstDate text, secondDate text)"
    exitConnection(*executioner(sql))
    print("Initialized")
def checkString(s):
    if s[1] == 'jp' or s[1] == 'en':
        if '/' in s[2] or '／' in s[2]:
            t = re.split('[-ー]', s[3])
            if (':' in t[0] and ':' in t[1]) or ('：' in t[0] and '：' in t[1]):
                if -12 <= int(s[4]) and int(s[4]) <= 12:
                    return True
def checkID(name):
    sql = "SELECT id from USERS WHERE name='%s'" % name
    con, cur = executioner(sql)
    id = cur.fetchone()[0]
    exitConnection(con, cur)
    return id
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
def cancel(name, id):
    sql = "SELECT name FROM USERS WHERE id=%s" % id
    con, cur = executioner(sql)
    try:
        if cur.fetchone()[0] == name:
            exitConnection(con, cur)
            sql = "DELETE FROM USERS WHERE id=%s" % id
            exitConnection(*executioner(sql))
            return "Canceled"
        else:
            return "You can't cancel other's reservation"
    except TypeError:
        return "You don't have any reservation"
def formString(s):
    st = re.split(':', s)
    if int(st[0]) < 10:
        st[0] = '0' + st[0]
    if int(st[1]) < 10:
        st[1] = '0' + st[1]
    return st[0] + ':' + st[1] 
def showAllUsers():
    sql = "SELECT * FROM USERS"
    con, cur = executioner(sql)
    rows = cur.fetchall()
    s = ""
    for r in rows:
        print(r)
    exitConnection(con, cur)
def showChannels(g):
    s = ""
    for v in g.voice_channels:
        s += (v.name + "\n")
    return s
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
        # /join jp(en) 09/22 21:00-22:00 9
        s = re.split(' ', message.content)
        s[0] = message.author.mention
        if checkString(s):
            register(s)
            id = checkID(message.author.mention)
            await message.channel.send('Registered ' + message.author.display_name + " Your ID is " + str(id))
            m = match(id)
            if "No one" in m:
                await message.channel.send(m)
            else:
                print(m)
                mes = m[0] + " Your language exchange starts at " + formString(m[1][0]) + " , and ends at " + formString(m[1][1]) + " on " + m[1][2]
                await message.channel.send(mes)
                mes = m[2] + " Your language exchange starts at " + formString(m[3][0]) + " , and ends at " + formString(m[3][1]) + " on " + m[3][2]
                await message.channel.send(mes)
                guild = client.get_guild(message.guild.id)
                await message.channel.send(showChannels(guild) + "are voice channels that you can use.")
        else:
            await message.channel.send('Wrong Command. Please check your command)')
    elif message.content.startswith('/cancel'):
        id = re.split(' ', message.content)[1]
        await message.channel.send(cancel(message.author.mention, id))
    elif message.content.startswith('/init'):
        init()
        await message.channel.send('Initialized Database')
    elif message.content.startswith('/users'):
        await message.channel.send(showAllUsers())
    elif message.content.startswith('/channels'):
        guild = client.get_guild(message.guild.id)
        await message.channel.send(showChannels(guild) + "are voice channels that you can use.")
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)