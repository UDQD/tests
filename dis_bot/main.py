import nest_asyncio
import time
nest_asyncio.apply()
import discord
import math

prefix = '!'



client = discord.Client()

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
        sql.execute("INSERT INTO table_1 VALUES (?,?,?,?)", (m.name, m.id, 1000, 100))
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
                    await message.channel.send(f"Перевод от {message.author.mention} к <@!{idd}> прошел  успешно. Переведено {amount} :drop_of_blood:.")
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
    main_ch = client.get_channel(795956162695790624)
    # await client.send_message(mainChannel, "Starting countdown", tts=True)
    await main_ch.send("Начало работы")
    for m in client.get_all_members():
        chek_new(m)
        print(m)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith(prefix + 'name'):
        await message.channel.send('Твое имя ' + str(message.author.mention))

    elif message.content.startswith(prefix + 'саня'):
        await message.channel.send(':)')

    elif message.content.startswith(prefix + 'members'):
        if  message.author.guild_permissions.administrator:
            await message.channel.send('члены:')

            for m in client.get_all_members():
                await message.channel.send(f'{m.name} - {m.id}')
        await message.channel.send("Недостаточно прав для данной команды")

    # if message.content.startswith(prefix + 'role'):
    #     await message.channel.send('твоя роль - ' + str(message.author.role))

    elif message.content.startswith(prefix + 'db'):
        if message.author.guild_permissions.administrator:
            for val in sql.execute("""SELECT * FROM table_1"""):
                await message.channel.send(val)
        else:
            await message.channel.send("Недостаточно прав для данной команды")

    elif message.content.startswith(prefix + 'fullbal'):
        if  message.author.guild_permissions.administrator:
            for val in sql.execute("""SELECT * FROM table_1 ORDER BY bal DESC"""):
                await message.channel.send(str(val[0]) + " - " + str(val[2]) + ":drop_of_blood:")
        else:
            await message.channel.send("Недостаточно прав для данной команды")

    elif message.content.startswith(prefix + 'pay'):
        list_content = message.content.split()
        id = ''.join(filter(str.isdigit,  str(list_content[1])))
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
            if amount.isdigit() and int(amount) > 0:
                amount = int(amount)

                sql.execute("SELECT bal FROM table_1 WHERE id = '{0}'".format(id))
                money = sql.fetchone()
                if money is None:
                    await message.channel.send("Пользователь не найден")
                else:
                    sql.execute(f"UPDATE table_1 SET bal = {amount}  WHERE id = '{id}'")
                    db.commit()
                    await message.channel.send(f"Балланс <@!{id}> установлен на {amount} :drop_of_blood:")

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
                    sql.execute(f"UPDATE table_1 SET bal = {money[0]+amount}  WHERE id = '{id}'")
                    db.commit()
                    await message.channel.send(f"На <@!{id}> с неба упало {amount} :drop_of_blood:")

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
                    s = money[0]-amount
                    if s<0:
                        await message.channel.send("Недостаточно денег")
                    else:
                        sql.execute(f"UPDATE table_1 SET bal = {money[0]-amount}  WHERE id = '{id}'")
                        db.commit()
                        await message.channel.send(f"У <@!{id}> неожиданно пропало {amount} :drop_of_blood:")

            else:
                await message.channel.send("Некорректная сумма")
        else:
            await message.channel.send("Недостаточно прав для данной команды")

    elif message.content.startswith(prefix + 'vipe'):
        if  message.author.guild_permissions.administrator:
            sql.execute(f"UPDATE table_1 SET bal = {1000}")
            db.commit()
            await message.channel.send("Возврат к исходному состоянию: успешно!")
        else:
            await message.channel.send("Недостаточно прав для данной команды")

    elif message.content.startswith(prefix + 'bal'):
        sql.execute(f"SELECT * FROM table_1 WHERE id = {message.author.id}")
        st = sql.fetchone()
        await message.channel.send(f"{message.author.mention}, твой баланс составляет {st[2]} :drop_of_blood:")

    elif message.content.startswith(prefix + 'voice'):
        voice_list = []
        for ch in message.guild.channels:
            # await message.channel.send(str(ch.name)+' - '+str(ch.id)+' - '+str(ch.type))
            # print(ch.type," --- ",'voice')
            if str(ch.type) == 'voice':
                voice_list.append(ch.id)
        await message.channel.send(voice_list)



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

    if before.channel is None and after.channel is not None:
        print('1')
        t1 = time.time()
        tdict[member.id] = t1
    elif before.channel is not None and after.channel is None:
        t2 = time.time()
        print('0')
        print(t2-tdict[member.id])
        dt = math.floor(t2-tdict[member.id])
        nag = math.floor(dt * 2.5)
        await main_ch.send(f"{member.mention} провел на канале {dt} секунд. Награда - {nag} :drop_of_blood:")
        sql.execute("SELECT bal FROM table_1 WHERE id = '{0}'".format(member.id))
        money = sql.fetchone()
        sql.execute(f"UPDATE table_1 SET bal = {money[0] + nag}  WHERE id = '{member.id}'")
        db.commit()
        # await message.channel.send(f"На <@!{id}> с неба упало {amount} :drop_of_blood:")


#     if message.content.startswith('$money'):
#         await message.channel.send('Баланс '+str(message.author)+' = '+)
client.run('')