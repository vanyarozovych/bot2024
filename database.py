# Import dependencies
import sqlite3
import disnake
from disnake.ext import commands
import json
import time


# Create connection to database and create tables
def initialize_database():
    conn = sqlite3.connect('discord.db')
    c = conn.cursor()

    # User table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        discriminator INTEGER,
        avatar TEXT,
        bot INTEGER,
        system INTEGER,
        messages_sent INTEGER DEFAULT 0,
        reactions_sent INTEGER DEFAULT 0,
        time_spent_in_voice_channels INTEGER DEFAULT 0,
        coins INTEGER DEFAULT 0
    )''')

    # Message table
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY,
        channel_id INTEGER,
        author_id INTEGER,
        content TEXT,
        timestamp INTEGER,
        edited_timestamp INTEGER
    )''')

    # Reaction table
    c.execute('''CREATE TABLE IF NOT EXISTS reactions (
        reaction_id INTEGER PRIMARY KEY,
        emoji_id TEXT,
        message_id INTEGER,
        user_id INTEGER,
        emoji TEXT
    )''')

    # Voice channels table
    c.execute('''CREATE TABLE IF NOT EXISTS voice_channels (
        voice_channel_id INTEGER PRIMARY KEY,
        name TEXT,
        bitrate INTEGER,
        user_limit INTEGER,
        time_spent_in_channel INTEGER DEFAULT 0
    )''')

    # Role changes table
    c.execute('''CREATE TABLE IF NOT EXISTS role_changes (
        user_id INTEGER,
        old_roles TEXT,
        new_roles TEXT,
        timestamp INTEGER
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS shop (
        role_id INTEGER,
        price INTEGER
    )''')

    # Commit changes to database
    conn.commit()
    conn.close()


# Initialize the database
initialize_database()

# Create a dictionary to track voice states
voice_states = {}

# Create bot with specified prefix and intents
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


def setup(bot):
    try:
        with open('config.json') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Файл 'config.json' не найден.")
        return
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON в файле 'config.json'.")
        return

    myserver = config['guild']

    @bot.event
    async def on_ready():
        print('Бот запущен!')
        try:
            print('Вношу данные о пользователях в базу данных')
            guild = await bot.fetch_guild(myserver)
            if guild:
                members = await guild.fetch_members().flatten()
                for member in members:
                    if not member.bot:
                        with sqlite3.connect('discord.db') as conn:
                            c = conn.cursor()
                            c.execute(
                                "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?, 0, 0, 0, 0)",
                                (member.id, member.name, member.discriminator, str(member.avatar),
                                 member.bot, member.system)
                            )
                print('База данных заполнена, и работает исправно')
            else:
                print(f'Не удалось найти гильдию с ID {myserver}.')
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        with sqlite3.connect('discord.db') as conn:
            c = conn.cursor()
            c.execute(
                "UPDATE users SET messages_sent = messages_sent + 1 WHERE user_id = ?",
                (message.author.id,)
            )
            c.execute(
                "INSERT INTO messages (message_id, channel_id, author_id, content, timestamp) VALUES (?, ?, ?, ?, ?)",
                (message.id, message.channel.id, message.author.id, message.content,
                 int(message.created_at.timestamp()))
            )
        await bot.process_commands(message)


    role_multipliers = {
        "760998034850709535": 2,  # Роль 1: 2x монеты
        "1291461515467296808": 2,  # Роль 2: 2x монеты
        # Добавьте больше ролей по мере необходимости
    }

    @bot.event
    async def on_voice_state_update(member, before, after):
        with sqlite3.connect('discord.db') as conn:
            c = conn.cursor()
            if before.channel is None and after.channel is not None:
                print(f"{member.name} присоединился к голосовому каналу {after.channel.name}")
                voice_states[member.id] = int(time.time())
                c.execute(
                    "INSERT OR IGNORE INTO voice_channels (voice_channel_id, name, bitrate, user_limit, "
                    "time_spent_in_channel) VALUES (?, ?, ?, ?, 0)",
                    (after.channel.id, after.channel.name, after.channel.bitrate,
                     after.channel.user_limit)
                )
            elif before.channel is not None and after.channel is None:
                print(f"{member.name} покинул голосовой канал {before.channel.name}")
                joined_at = voice_states.get(member.id)
                if joined_at:
                    time_spent = int(time.time()) - joined_at

                    # Начисление монет (10 монет за 1 минуту)
                    base_coins = time_spent // 60 * 10  # 10 монет за каждую полную минуту

                    # Проверяем, есть ли у пользователя специальные роли
                    multiplier = 1  # По умолчанию
                    for role_id in role_multipliers.keys():
                        if disnake.utils.get(member.roles, id=int(role_id)):
                            multiplier = role_multipliers[role_id]
                            break  # Если роль найдена, выходим из цикла

                    coins_earned = base_coins * multiplier  # Увеличиваем монеты в зависимости от роли

                    c.execute(
                        'UPDATE users SET coins = coins + ? WHERE user_id = ?',
                        (coins_earned, member.id)
                    )

                    # Обновление времени, проведенного в голосовом канале
                    c.execute(
                        'UPDATE users SET time_spent_in_voice_channels = time_spent_in_voice_channels + ? WHERE '
                        'user_id = ?',
                        (time_spent, member.id)
                    )
                    c.execute(
                        "UPDATE voice_channels SET time_spent_in_channel = time_spent_in_channel + ? WHERE "
                        "voice_channel_id = ?",
                        (time_spent, before.channel.id)
                    )
                    del voice_states[member.id]

    @bot.event
    async def on_raw_reaction_add(payload):
        with sqlite3.connect('discord.db') as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO reactions (reaction_id, message_id, user_id, emoji_id) VALUES (NULL, ?, ?, ?)",
                (payload.message_id, payload.user_id, payload.emoji.name)
            )
            c.execute(
                "UPDATE users SET reactions_sent = reactions_sent + 1 WHERE user_id = ?",
                (payload.user_id,)
            )

    @bot.event
    async def on_member_update(before, after):
        # Проверяем, изменились ли роли
        if before.roles != after.roles:
            with sqlite3.connect('discord.db') as conn:
                c = conn.cursor()
                # Вставка информации об изменении ролей в базу данных
                c.execute(
                    "INSERT INTO role_changes (user_id, old_roles, new_roles, timestamp) VALUES (?, ?, ?, ?)",
                    (after.id, str([role.id for role in before.roles]), str([role.id for role in after.roles]),
                     int(time.time()))
                )
                print(f"{after.name} изменил роли: {before.roles} -> {after.roles}")
