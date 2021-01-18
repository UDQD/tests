import nest_asyncio
import time
import discord
import math
from random import randint as rnd
from config import *

nest_asyncio.apply()
prefix = conf['PREFIX']

# role_price = {'1': 1200,
#               '2': 6500}
# role_id = {'1': 798142893759660042,
#            '2': 798142950419857418}

start_time = time.time()

client = discord.Client()

is_not_true = True
start_game = False
game_code = '00000'
numb_mess = 0
lim_mes = rnd(conf['MSG_INT_MIN'], conf['MSG_INT_MAX'])

intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
client = discord.Client(intents=intents)

main_ch = 0
# print("Chenel - ", main_ch)

import sqlite3 as sq

db = sq.connect('db_3.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS table_1 (
name TEXT,
id BIGINT,
bal BIGINT ,
rang INT
)""")
db.commit()


def chek_new(m):
    sql.execute("SELECT id FROM table_1 WHERE id = '{0}'".format(m.id))
    if sql.fetchone() is None:
        print(m.id)
        sql.execute("INSERT INTO table_1 VALUES (?,?,?,?)", (m.name, m.id, conf['START_BAL'], 100))
        db.commit()


async def try_pay(person, amount, message, idd):
    # print(type(person.id), "===", type(idd))
    # print(person.id==idd)
    if person.id != int(idd):

        if amount.isdigit() and int(amount) > 0:
            amount = int(amount)

            sql.execute("SELECT bal FROM table_1 WHERE id = '{0}'".format(idd))
            money_2 = sql.fetchone()
            if money_2 is None:
                await message.channel.send("Пользователь не найден")
                return False
            else:
                sql.execute("SELECT bal FROM table_1 WHERE id = '{0}'".format(person.id))
                money_1 = sql.fetchone()
                # print('Внутри try, money = ',money[0],'      amount = ',amount)
                if money_1[0] < amount:
                    await message.channel.send(person.mention + ', у вас недостаточно денег.')
                    return False
                else:
                    res = money_1[0] - amount
                    sql.execute(f"UPDATE table_1 SET bal = {res}  WHERE id = '{person.id}'")
                    # print("1 :",res)
                    db.commit()
                    res2 = money_2[0] + amount
                    sql.execute(f"UPDATE table_1 SET bal = {res2}  WHERE id = '{idd}'")
                    # print("2 :",res2)
                    db.commit()
                    # sm = ":drop_of_blood:" * amount
                    await message.channel.send(
                        f"Перевод от {message.author.mention} к <@!{idd}> прошел  успешно. Переведено {amount} {conf['VAL']}.")
                    return True
        else:
            await message.channel.send("Некорректная сумма")
            return False
    else:
        await message.channel.send("Нельзя отправить деньги самому себе")


# async def try_get(id, amount, message):
#     amount = int(amount)
#     # sql.execute("SELECT bal FROM table_1 WHERE id = '{0}'".format(id))
#     # money = sql.fetchone()
#     # if money is None:
#     #     await message.channel.send("Пользователь не найден")
#     # else:
#         # money = sql.fetchone()
#     # res = money[0] + amount
#     # sql.execute(f"UPDATE table_1 SET bal = {res}  WHERE id = '{id}'")
#     db.commit()
#     await message.channel.send(f"Перевод от {message.author.mention} к <@!{id}> прошел  успешно. Переведено {amount} :dollar:.")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    global main_ch
    main_ch = client.get_channel(chan['main'])
    # await client.send_message(mainChannel, "Starting countdown", tts=True)
    await main_ch.send("Начало работы")
    for m in client.get_all_members():
        chek_new(m)
        print(m)


@client.event
async def on_message(message):
    global numb_mess
    global game_code
    global is_not_true
    global start_game
    global lim_mes
    if message.channel == main_ch:
        numb_mess += 1
    if message.author == client.user:
        return

    # elif message.content.startswith(prefix + 'name'):
    #     await message.channel.send('Твое имя ' + str(message.author.mention))

    # elif message.content.startswith(prefix + 'саня'):
    #     await message.channel.send(':)')

    elif message.content.startswith(prefix + 'members'):
        if message.author.guild_permissions.administrator:
            await message.channel.send('члены:')

            for m in client.get_all_members():
                await message.channel.send(f'{m.name} - {m.id}')
        await message.channel.send("Недостаточно прав для данной команды")

    if message.content.startswith(prefix + 'role'):
        for role in message.guild.roles:
            await message.channel.send(f' роль - {role} - {role.id}')

    elif message.content.startswith(prefix + 'db'):
        if message.author.guild_permissions.administrator:
            for val in sql.execute("""SELECT * FROM table_1"""):
                await message.channel.send(val)
        else:
            await message.channel.send("Недостаточно прав для данной команды")

    elif message.content.startswith(prefix + 'fullbal'):
        if message.author.guild_permissions.administrator:
            for val in sql.execute("""SELECT * FROM table_1 ORDER BY bal DESC"""):
                await message.channel.send(str(val[0]) + " - " + str(val[2]) + f"{conf['VAL']}")
        else:
            await message.channel.send("Недостаточно прав для данной команды")

    elif message.content.startswith(prefix + 'pay'):
        list_content = message.content.split()
        id = ''.join(filter(str.isdigit, str(list_content[1])))
        amount = str(list_content[2])
        print(list_content)
        print(id)
        print(amount)
        await try_pay(message.author, amount, message, id)
        # await try_get(id, amount, message)

    elif message.content.startswith(prefix + 'ch'):
        print(message.channel.id)

    elif message.content.startswith(prefix + 'whoami'):
        if message.author.guild_permissions.administrator:
            await message.channel.send("ты Админ")
            s = str(f" ты - {message.author.guild_permissions}")
            await message.channel.send(s)
        else:
            await message.channel.send("ты НЕ Админ")
            s = str(f" ты - {message.author.guild_permissions}")
            await message.channel.send(s)

    # if message.content.startswith(prefix + ''):
    #     if  message.author.guild_permissions.administrator:
    #         pass
    #     else:
    #         await message.channel.send("Недостаточно прав для данной команды")

    elif message.content.startswith(prefix + 'setbal'):
        if message.author.guild_permissions.administrator:
            list_content = message.content.split()
            id = ''.join(filter(str.isdigit, str(list_content[1])))
            amount = str(list_content[2])
            if amount.isdigit() and int(amount) >= 0:
                amount = int(amount)

                sql.execute("SELECT bal FROM table_1 WHERE id = '{0}'".format(id))
                money = sql.fetchone()
                if money is None:
                    await message.channel.send("Пользователь не найден")
                else:
                    sql.execute(f"UPDATE table_1 SET bal = {amount}  WHERE id = '{id}'")
                    db.commit()
                    await message.channel.send(f"Балланс <@!{id}> установлен на {amount} {conf['VAL']}")

            else:
                await message.channel.send("Некорректная сумма")
        else:
            await message.channel.send("Недостаточно прав для данной команды")


    elif message.content.startswith(prefix + 'add'):
        if message.author.guild_permissions.administrator:
            list_content = message.content.split()
            id = ''.join(filter(str.isdigit, str(list_content[1])))
            amount = str(list_content[2])
            if amount.isdigit() and int(amount) > 0:
                amount = int(amount)

                sql.execute("SELECT bal FROM table_1 WHERE id = '{0}'".format(id))
                money = sql.fetchone()
                if money is None:
                    await message.channel.send("Пользователь не найден")
                else:
                    sql.execute(f"UPDATE table_1 SET bal = {money[0] + amount}  WHERE id = '{id}'")
                    db.commit()
                    await message.channel.send(f"На <@!{id}> с неба упало {amount} {conf['VAL']}")

            else:
                await message.channel.send("Некорректная сумма")
        else:
            await message.channel.send("Недостаточно прав для данной команды")

    elif message.content.startswith(prefix + 'pick'):
        if message.author.guild_permissions.administrator:
            list_content = message.content.split()
            id = ''.join(filter(str.isdigit, str(list_content[1])))
            amount = str(list_content[2])
            if amount.isdigit() and int(amount) > 0:
                amount = int(amount)

                sql.execute("SELECT bal FROM table_1 WHERE id = '{0}'".format(id))
                money = sql.fetchone()
                if money is None:
                    await message.channel.send("Пользователь не найден")
                else:
                    s = money[0] - amount
                    if s < 0:
                        await message.channel.send("Недостаточно денег")
                    else:
                        sql.execute(f"UPDATE table_1 SET bal = {money[0] - amount}  WHERE id = '{id}'")
                        db.commit()
                        await message.channel.send(f"У <@!{id}> неожиданно пропало {amount} {conf['VAL']}")

            else:
                await message.channel.send("Некорректная сумма")
        else:
            await message.channel.send("Недостаточно прав для данной команды")

    elif message.content.startswith(prefix + 'vipe'):
        if message.author.guild_permissions.administrator:
            sql.execute(f"UPDATE table_1 SET bal = {conf['START_BAL']}")
            db.commit()
            await message.channel.send("Возврат к исходному состоянию: успешно!")
        else:
            await message.channel.send("Недостаточно прав для данной команды")

    elif message.content.startswith(prefix + 'bal'):
        sql.execute(f"SELECT * FROM table_1 WHERE id = {message.author.id}")
        st = sql.fetchone()
        await message.channel.send(f"{message.author.mention}, твой баланс: {st[2]} {conf['VAL']}")

    elif message.content.startswith(prefix + 'voice'):
        voice_list = []
        for ch in message.guild.channels:
            # await message.channel.send(str(ch.name)+' - '+str(ch.id)+' - '+str(ch.type))
            # print(ch.type," --- ",'voice')
            if str(ch.type) == 'voice':
                voice_list.append(ch.id)
        await message.channel.send(voice_list)

    elif message.content.startswith(prefix + 'buyrole'):
        m = message.content.split()
        print(m)
        role_name = int(m[1])
        sql.execute(f"SELECT * FROM table_1 WHERE id = {message.author.id}")
        st = sql.fetchone()[2]

        for i in range(1, len(roles['id']) + 1):
            if role_name == i:
                role = discord.utils.get(message.guild.roles, id=roles['id'][str(i)])
                if not role in message.author.roles:
                    # print(role)
                    # print(message.author.roles)
                    if st < roles['price'][str(i)]:
                        await message.channel.send(f"Недостаточно денег для покупки роли '{role}'")
                    else:
                        sql.execute(
                            f"UPDATE table_1 SET bal = {st - roles['price']['1']}  WHERE id = '{message.author.id}'")
                        db.commit()
                        # role = discord.utils.get(message.guild.roles, id=role_id['1'])
                        await message.author.add_roles(role)
                        await message.channel.send(
                            f"<@!{message.author.id}> купил роль '{role}' за {roles['price'][str(i)]} {conf['VAL']}")
                else:
                    await message.channel.send("Роль уже куплена")
                break


    elif message.content.startswith(prefix + 'react'):
        pass

    elif message.content.startswith(prefix + 'code'):
        amount = rnd(conf['MIN_NAG'], conf['MAX_NAG'])
        start_game = False
        # global is_not_true
        # global game_code
        user_code = message.content.split()[1]
        print(user_code)
        print(game_code)
        print(is_not_true)
        if (is_not_true and user_code == game_code):
            is_not_true = False
            sql.execute("SELECT bal FROM table_1 WHERE id = '{0}'".format(message.author.id))
            money = sql.fetchone()
            sql.execute(f"UPDATE table_1 SET bal = {money[0] + amount}  WHERE id = '{message.author.id}'")
            db.commit()
            await message.channel.send(f"{message.author.mention} написал код первым, Награда: {amount} {conf['VAL']}")
        else:
            pass

    if numb_mess >= lim_mes:
        lim_mes = rnd(conf['MSG_INT_MIN'], conf['MSG_INT_MAX'])
        numb_mess = 0
        # global is_not_true
        is_not_true = True
        start_game = True
        # global game_code
        game_code = str(rnd(10000, 99999))
        await main_ch.send(f"Код - {game_code}. напиши первым и получи бабки. команда {prefix}code *****")


# @client.command(pass_context=True)
# async def joinvoice(ctx):
#     await main_ch.send('Кто-то зашел в войс')

@client.event
async def on_member_join(member):
    # await main_ch.send('Привет ' + str(member.mention))
    chek_new(member)


# t = [time.time(), 0]
global tdict
tdict = {}


@client.event
async def on_voice_state_update(member, before, after):
    mikro_off = False

    if before.channel is None and after.channel is not None:
        if not (after.mute or after.self_mute):
            print(member.name, 'Зашел с включеным')
            t1 = time.time()
            tdict[member.id] = t1
        else:
            print(member.name, 'Зашел с вЫключеным')
            mikro_off = True



    elif before.channel is not None and after.channel is None:
        if not member.id in tdict:
            print('not')
            if not (after.mute or after.self_mute):
                tdict[member.id] = start_time
                print('start_time')
            else:
                tdict[member.id] = time.time()
                print('time.time()')

        if (after.mute or after.self_mute):
            tdict[member.id] = time.time()
        print(member.name, 'Вышел')
        t2 = time.time()
        # print('0')
        print(t2 - tdict[member.id])
        dt = math.floor(t2 - tdict[member.id]) // 60
        nag = math.floor(dt * conf['VOICE_NAG'])
        # await main_ch.send(f"{member.mention} провел на канале {dt} минут. Награда - {nag} {conf['VAL']}")
        sql.execute("SELECT bal FROM table_1 WHERE id = '{0}'".format(member.id))
        money = sql.fetchone()
        sql.execute(f"UPDATE table_1 SET bal = {money[0] + nag}  WHERE id = '{member.id}'")
        db.commit()

    elif not (after.mute or after.self_mute):
        print(member.name, 'Включил микро')
        t1 = time.time()
        tdict[member.id] = t1

    elif after.mute or after.self_mute:
        print(member.name, 'Выключил микро')
        t2 = time.time()
        # print('0')
        print(t2 - tdict[member.id])
        dt = math.floor(t2 - tdict[member.id]) // 60
        nag = math.floor(dt * conf['VOICE_NAG'])
        # await main_ch.send(f"{member.mention} провел на канале {dt} минут. Награда - {nag} {conf['VAL']}")
        sql.execute("SELECT bal FROM table_1 WHERE id = '{0}'".format(member.id))
        money = sql.fetchone()
        sql.execute(f"UPDATE table_1 SET bal = {money[0] + nag}  WHERE id = '{member.id}'")
        db.commit()

    # # muted = False
    # if ((before.channel is None and after.channel is not None) and not (after.mute or after.self_mute)) or not (after.mute or after.self_mute):
    #     print('1')
    #     t1 = time.time()
    #     tdict[member.id] = t1
    # elif (before.channel is not None and after.channel is None) or (after.mute or after.self_mute):
    #     t2 = time.time()
    #     print('0')
    #     if member.id in tdict:
    #         # tdict[member.id] = start_time
    #     # if after.mute or after.self_mute:
    #     #     tdict[member.id] = time.time()
    #         print("dt = ", t2 - tdict[member.id])
    #         dt = math.floor(t2 - tdict[member.id])# // 60
    #         nag = math.floor(dt * conf['VOICE_NAG'])
    #         await main_ch.send(f"{member.mention} провел на канале {dt} минут. Награда - {nag} {conf['VAL']}")
    #         sql.execute("SELECT bal FROM table_1 WHERE id = '{0}'".format(member.id))
    #         money = sql.fetchone()
    #         sql.execute(f"UPDATE table_1 SET bal = {money[0] + nag}  WHERE id = '{member.id}'")
    #         db.commit()
    #
    #     # await message.channel.send(f"На <@!{id}> с неба упало {amount} :drop_of_blood:")
    # if after.mute or after.self_mute:
    #     # print('mute')
    #     await main_ch.send(f"{member.mention} в муте")
    # else:
    #     # print('unmute')
    #     await main_ch.send(f"{member.mention} НЕ в муте")

    # if (member.mute or member.self_mute) and not muted:
    #     await main_ch.send(f"{member.mention} в муте")
    #     muted = True
    # elif not (member.mute or member.self_mute) and muted:
    #     muted = False
    #     await main_ch.send(f"{member.mention} НЕ в муте")


#     if message.content.startswith('$money'):
#         await message.channel.send('Баланс '+str(message.author)+' = '+)

client.run(conf['TOKEN'])
