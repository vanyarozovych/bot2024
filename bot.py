import asyncio
import io

import disnake
import requests as requests
from PIL import Image, ImageFont, ImageDraw
from disnake.ext import commands
import threading
import datetime
import sqlite3

import events
import posts
import database
import economy

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

posts.setup(bot)
events.setup(bot)
database.setup(bot)
economy.setup(bot)


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    msg = message.content.lower()
    greeting_words = ["hello", "hi", "привет", "хай"]
    censored_words = ["дурак", "дура", "придурок", "лох", "ублюдок", "хуесос,", " мудила", "пизда", "уебан", "пидарас",
                      "пиздец", "смегма"]

    if msg in greeting_words:
        await message.channel.send(f"{message.author.name}, приветствую тебя!")

    # Filter censored words
    for bad_content in msg.split(" "):
        if bad_content in censored_words:
            await message.channel.send(f"{message.author.mention}, Будьте вежливее человечишка!")


# на запас код приветствия
@bot.event
async def on_member_join(member):
    # Получаем канал приветствия по его ID
    channel = bot.get_channel(1117872265556676728)  # Замените ID на свой
    role = member.guild.get_role(760998034850709535)
    if role is not None:
        mention = role.mention  # Получение упоминания роли

    if channel is not None:
        await channel.send(f'{member.mention}, залетел на сервер!\n {role.mention}')


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1130597461304561724)  # Замените ID на свой

    if channel is not None:
        await channel.send(f'{member.mention}, вышел с сервера!')


@bot.command()
@commands.check_any(commands.has_role(760998034850709535))
async def give_boy(ctx, member: disnake.Member):
    role = disnake.utils.get(ctx.guild.roles, id=760998034845728780)  # Замените ID роли на фактический ID
    if role is None:
        await ctx.send("Роль не найдена.")
        return

    try:
        await member.add_roles(role)
        await ctx.send(f"Роль {role.name} успешно добавлена участнику {member.display_name}.")
    except disnake.Forbidden:
        await ctx.send("У меня недостаточно прав для выдачи этой роли.")
    except Exception as e:
        await ctx.send(f"Произошла ошибка при выдаче роли: {str(e)}")


@bot.command()
@commands.check_any(commands.has_role(760998034850709535))
async def give_girl(ctx, member: disnake.Member):
    role = disnake.utils.get(ctx.guild.roles, id=760998034792251411)  # Замените ID роли на фактический ID
    if role is None:
        await ctx.send("Роль не найдена.")
        return

    try:
        await member.add_roles(role)
        await ctx.send(f"Роль {role.name} успешно добавлена участнику {member.display_name}.")
    except disnake.Forbidden:
        await ctx.send("У меня недостаточно прав для выдачи этой роли.")
    except Exception as e:
        await ctx.send(f"Произошла ошибка при выдаче роли: {str(e)}")


@bot.command()
@commands.check_any(commands.has_role(760998034850709535))
async def remove_boy(ctx, member: disnake.Member):
    role = disnake.utils.get(ctx.guild.roles, id=760998034845728780)  # Замените ROLE_ID на фактический ID роли
    if role is None:
        await ctx.send("Роль не найдена.")
        return

    try:
        await member.remove_roles(role)
        await ctx.send(f"Роль {role.name} успешно удалена у участника {member.display_name}.")
    except disnake.Forbidden:
        await ctx.send("У меня недостаточно прав для удаления этой роли.")
    except Exception as e:
        await ctx.send(f"Произошла ошибка при удалении роли: {str(e)}")


@bot.command()
@commands.check_any(commands.has_role(760998034850709535))
async def remove_girl(ctx, member: disnake.Member):
    role = disnake.utils.get(ctx.guild.roles, id=760998034792251411)  # Замените ROLE_ID на фактический ID роли
    if role is None:
        await ctx.send("Роль не найдена.")
        return

    try:
        await member.remove_roles(role)
        await ctx.send(f"Роль {role.name} успешно удалена у участника {member.display_name}.")
    except disnake.Forbidden:
        await ctx.send("У меня недостаточно прав для удаления этой роли.")
    except Exception as e:
        await ctx.send(f"Произошла ошибка при удалении роли: {str(e)}")


@bot.command()
@commands.check_any(commands.has_role(1123262857614721104))
async def mute_event(ctx, member: disnake.Member):
    role = disnake.utils.get(ctx.guild.roles, id=760998034792251402)  # Замените ID роли на фактический ID
    if role is None:
        await ctx.send("Роль не найдена.")
        return

    try:
        await member.add_roles(role)
        await ctx.send(f"Роль {role.name} успешно добавлена участнику {member.display_name}.")
    except disnake.Forbidden:
        await ctx.send("У меня недостаточно прав для выдачи этой роли.")
    except Exception as e:
        await ctx.send(f"Произошла ошибка при выдаче роли: {str(e)}")


@bot.command()
@commands.check_any(commands.has_role(1123262857614721104))
async def unmute_event(ctx, member: disnake.Member):
    role = disnake.utils.get(ctx.guild.roles, id=760998034792251402)  # Замените ROLE_ID на фактический ID роли
    if role is None:
        await ctx.send("Роль не найдена.")
        return

    try:
        await member.remove_roles(role)
        await ctx.send(f"Роль {role.name} успешно удалена у участника {member.display_name}.")
    except disnake.Forbidden:
        await ctx.send("У меня недостаточно прав для удаления этой роли.")
    except Exception as e:
        await ctx.send(f"Произошла ошибка при удалении роли: {str(e)}")


@bot.command()
@commands.check_any(commands.has_role(1123262857614721104))
async def mute_voice(ctx, member: disnake.Member):
    role = disnake.utils.get(ctx.guild.roles, id=760998034792251403)  # Замените ID роли на фактический ID
    if role is None:
        await ctx.send("Роль не найдена.")
        return

    try:
        await member.add_roles(role)
        await ctx.send(f"Роль {role.name} успешно добавлена участнику {member.display_name}.")
    except disnake.Forbidden:
        await ctx.send("У меня недостаточно прав для выдачи этой роли.")
    except Exception as e:
        await ctx.send(f"Произошла ошибка при выдаче роли: {str(e)}")


@bot.command()
@commands.check_any(commands.has_role(1123262857614721104))
async def unmute_voice(ctx, member: disnake.Member):
    role = disnake.utils.get(ctx.guild.roles, id=760998034792251403)  # Замените ROLE_ID на фактический ID роли
    if role is None:
        await ctx.send("Роль не найдена.")
        return

    try:
        await member.remove_roles(role)
        await ctx.send(f"Роль {role.name} успешно удалена у участника {member.display_name}.")
    except disnake.Forbidden:
        await ctx.send("У меня недостаточно прав для удаления этой роли.")
    except Exception as e:
        await ctx.send(f"Произошла ошибка при удалении роли: {str(e)}")


@bot.command()
async def report(ctx, member: disnake.Member, *, reason):
    # Получение объекта канала по ID
    channel_id = 760998035018088492  # Замените на фактический ID текстового канала
    target_channel = bot.get_channel(channel_id)

    if target_channel is not None:
        # Создание embed сообщения
        embed = disnake.Embed(
            title="Репорт",
            description=(
                f"Автор: {ctx.author.mention}\n"
                f"Нарушитель: {member.mention}\n"
                f"Причина: {reason}"
            ),
            color=0xFF0000,
        )

        # Отправка embed сообщения в определенный канал
        await target_channel.send(embed=embed)
    else:
        print("Канал не найден.")


@bot.command()
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount)
    message = await ctx.send(f"Было удалено {amount} сообщений...")
    await asyncio.sleep(15)
    await message.delete()


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: disnake
               .Member, *, reason=None):
    await ctx.message.delete(delay=1)  # Если желаете удалять сообщение после отправки с задержкой

    await member.send(f"Вы были кикнуты с сервера!")  # Отправить личное сообщение пользователю
    await ctx.send(f"Участник {member.mention} был кикнут с сервера!")
    await member.kick(reason=reason)


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: disnake
              .Member, *, reason=None):
    await member.send(f"You was banned on server")  # Отправить личное сообщение пользователю
    await ctx.send(f"Member **{member.mention}** was banned on this server")
    await member.ban(reason=reason)


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)


@bot.command()
async def mute_user(ctx, member: disnake.Member):
    mute_role = disnake.utils.get(ctx.guild.roles, name="role name")

    if mute_role is not None:
        await member.add_roles(mute_role)
        await ctx.send(f"**{ctx.author}** выдал мут для **{member}**")
    else:
        await ctx.send("Мут-роль не найдена")


@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды!")

    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=disnake.Embed(
            description=(
                f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` "
                f"({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"
            )
        ))


@bot.command()
async def bot_help(ctx):
    embed = disnake.Embed(
        title="Меню",
        description="Здесь вы можете просмотреть доступные команды:"
    )
    commands_list = ["clear", "kick", "ban", "unban"]
    descriptions_for_commands = ["Чистит чат", "Кикает участника", "Банит участника", "Разбанивает участника"]

    for command_name, description_command in zip(commands_list, descriptions_for_commands):
        embed.add_field(
            name=command_name,
            value=description_command,
            inline=False  # Будет выводиться в столбик, если True - в строчку
        )

    await ctx.send(embed=embed)


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command(aliases=['профиль', 'profile'])
async def card_user(ctx, member: disnake.Member = None):
    # Если участник не указан, используем автора команды
    if member is None:
        member = ctx.author

    # Создание изображения для карточки пользователя
    img = Image.new('RGBA', (400, 200), '#232529')

    # Получение URL аватара
    avatar_url = str(member.avatar)

    # Проверяем, существует ли аватар
    if avatar_url is not None:
        response = requests.get(avatar_url, stream=True)
        response = Image.open(io.BytesIO(response.content))
        response = response.convert('RGBA')
        response = response.resize((100, 100), Image.Resampling.LANCZOS)

        img.paste(response, (15, 15, 115, 115))
    else:
        print("Пользователь не имеет аватара. Используем стандартное изображение.")

    idraw = ImageDraw.Draw(img)
    name = member.name
    tag = member.discriminator

    headline = ImageFont.truetype('arial.ttf', size=20)
    undertext = ImageFont.truetype('arial.ttf', size=12)

    idraw.text((145, 15), f'{name}#{tag}', font=headline)
    idraw.text((145, 50), f'ID: {member.id}', font=undertext)

    # Получение данных о времени, проведенном в голосовом канале
    with sqlite3.connect('discord.db') as conn:
        c = conn.cursor()
        # Получаем время, проведенное в голосовых каналах
        c.execute("SELECT time_spent_in_voice_channels FROM users WHERE user_id = ?", (member.id,))
        result = c.fetchone()
        time_spent = result[0] if result else 0
        hours, remainder = divmod(time_spent, 3600)
        minutes, _ = divmod(remainder, 60)
        idraw.text((145, 85), f'Время в голосе: {hours} ч, {minutes} мин', font=undertext)

        # Получаем количество монет
        c.execute("SELECT coins FROM users WHERE user_id = ?", (member.id,))
        coins_result = c.fetchone()
        coins = coins_result[0] if coins_result else 0
        idraw.text((145, 115), f'Монеты: {coins}', font=undertext)

    img.save('user_card.png')

    await ctx.send(file=disnake.File(fp='user_card.png'))




@bot.command()
async def minecraft_server(ctx):
    server = 'vanyarozovych.aternos.me:56613'
    response = requests.get(f'https://api.mcsrvstat.us/2/{server}')
    data = response.json()

    if data['online']:
        message = (
            f"✅ - Сервер `{server}` - онлайн. "
            f"На сервере `{data['players']['online']}`/`{data['players']['max']}` игроков онлайн."
        )
    else:
        message = f"❌ - Сервер `{server}` - оффлайн."

    await ctx.send(message)


@bot.command()
async def massrole(ctx, role: disnake
                   .Role):
    for member in ctx.guild.members:
        if role not in member.roles:
            await member.add_roles(role)


def console_input_loop():
    channel_id = int(
        input("Введите ID канала для отправки сообщений: "))  # ID канала, куда бот будет отправлять сообщения
    channel = bot.get_channel(channel_id)
    if channel is None:
        print("Канал не найден!")
        return
    while True:
        message = input("Введите сообщение для отправки (или 'exit' для выхода): ")
        if message.lower() == 'exit':
            break
        asyncio.run_coroutine_threadsafe(channel.send(message), bot.loop)


# Запуск потока для консоли
thread = threading.Thread(target=console_input_loop)
thread.start()


@bot.command()
async def timestamp(ctx, ts: int):
    """Конвертирует Unix timestamp в читаемый формат даты и времени."""
    dt_object = datetime.datetime.fromtimestamp(ts)
    readable_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    await ctx.send(f"Unix timestamp {ts} соответствует: {readable_time} (UTC)")


bot.run("MTExODUwMzk1NzAzMjA3NTMxNA.Go5nn9.sva36MopQ041RBYuZWUfG41o5f1q279uD3TE3k")
