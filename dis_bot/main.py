import nest_asyncio

nest_asyncio.apply()
import discord

prefix = '!'



client = discord.Client()

intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
client = discord.Client(intents=intents)
main_ch = client.get_channel(795956162695790624)
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

                res2 = money_2[0] + amount
                sql.execute(f"UPDATE table_1 SET bal = {res2}  WHERE id = '{idd}'")
                db.commit()
                # sm = ":drop_of_blood:" * amount
                await message.channel.send(f"Перевод от {message.author.mention} к <@!{idd}> прошел  успешно. Переведено {amount} :drop_of_blood:.")
                return True
    else:
        await message.channel.send("Некорректная сумма")
        return False


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
    # await client.send_message(mainChannel, "Starting countdown", tts=True)
    # await main_ch.send("Начало работы")
    for m in client.get_all_members():
        chek_new(m)
        print(m)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix + 'name'):
        await message.channel.send('Твое имя ' + str(message.author.mention))

    if message.content.startswith(prefix + 'саня'):
        await message.channel.send(':)')

    if message.content.startswith(prefix + 'members'):
        await message.channel.send('члены:')

        for m in client.get_all_members():
            await message.channel.send(f'{m.name} - {m.id}')

    if message.content.startswith(prefix + 'role'):
        await message.channel.send('твоя роль - ' + str(message.author.role))

    if message.content.startswith(prefix + 'db'):
        for val in sql.execute("""SELECT * FROM table_1"""):
            await message.channel.send(val)

    if message.content.startswith(prefix + 'bal'):
        for val in sql.execute("""SELECT * FROM table_1"""):
            await message.channel.send(str(val[0]) + " - " + str(val[2]) + " монет")

    if message.content.startswith(prefix + 'pay'):
        list_content = message.content.split()
        id = ''.join(filter(str.isdigit,  str(list_content[1])))
        amount = str(list_content[2])
        print(list_content)
        print(id)
        print(amount)
        await try_pay(message.author, amount, message, id)
            # await try_get(id, amount, message)

    if message.content.startswith(prefix + 'ch'):
        print(message.channel.id)


# @client.command(pass_context=True)
# async def joinvoice(ctx):
#     await main_ch.send('Кто-то зашел в войс')

# @client.event
# async def on_member_join(member):
#     await main_ch.send('Привет ' + str(member.mention))
#     chek_new(member)


#     if message.content.startswith('$money'):
#         await message.channel.send('Баланс '+str(message.author)+' = '+)
client.run('Nzk1OTg0MzQxNDgyMjA5MzAy.X_RULw.bLVyhAK5A2qWBY17UxTTCthpuQk')