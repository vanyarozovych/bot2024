import sqlite3
import time

import disnake
from disnake.ext import commands

# Создание бота
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Список ролей и их цен
roles = {
    "760998034821349443": 20000,
    "760998034821349444": 20000,
    "760998034821349445": 20000,
    "760998034829344808": 20000,
}


def add_roles_to_shop():
    with sqlite3.connect('discord.db') as conn:
        c = conn.cursor()
        # Создаем таблицу, если ее нет
        c.execute("CREATE TABLE IF NOT EXISTS shop (role_id TEXT PRIMARY KEY, price INTEGER)")
        for role_id, price in roles.items():
            # Проверяем, существует ли запись для текущей роли
            c.execute("SELECT role_id FROM shop WHERE role_id = ?", (role_id,))
            result = c.fetchone()
            if not result:
                # Если роли нет в базе, добавляем её
                c.execute("INSERT INTO shop (role_id, price) VALUES (?, ?)", (role_id, price))
        conn.commit()


# Вызов функции для добавления ролей в магазин
add_roles_to_shop()


def setup(bot):
    def get_last_daily(user_id):
        with sqlite3.connect('discord.db') as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS daily_claims (user_id INTEGER PRIMARY KEY, last_claim INTEGER)")
            c.execute("SELECT last_claim FROM daily_claims WHERE user_id = ?", (user_id,))
            result = c.fetchone()
            return result[0] if result else None

    # Функция для обновления времени последнего выполнения команды
    def update_last_daily(user_id):
        with sqlite3.connect('discord.db') as conn:
            c = conn.cursor()
            current_time = int(time.time())
            c.execute("INSERT OR REPLACE INTO daily_claims (user_id, last_claim) VALUES (?, ?)",
                      (user_id, current_time))
            conn.commit()

    # Команда для получения монет
    @bot.command()
    async def daily(ctx):
        user_id = ctx.author.id
        last_claim = get_last_daily(user_id)
        current_time = int(time.time())

        # Проверяем, прошло ли 24 часа (86400 секунд)
        if last_claim is None or (current_time - last_claim) >= 86400:
            with sqlite3.connect('discord.db') as conn:
                c = conn.cursor()
                c.execute("UPDATE users SET coins = coins + 1000 WHERE user_id = ?", (user_id,))
                conn.commit()

            update_last_daily(user_id)  # Обновляем время последнего получения награды
            await ctx.send(f"Вы получили 1000 монет!")
        else:
            # Вычисляем оставшееся время до следующей возможности получения монет
            time_left = 86400 - (current_time - last_claim)
            hours, remainder = divmod(time_left, 3600)
            minutes, seconds = divmod(remainder, 60)
            await ctx.send(
                f"Вы уже получали монеты. \nПопробуйте снова через: **{int(hours)}ч {int(minutes)}м {int(seconds)}с.**")

    @bot.command()
    async def balance(ctx, member: disnake.Member = None):
        # Если участник не указан, показываем баланс отправителя команды
        if member is None:
            member = ctx.author

        user_id = member.id
        with sqlite3.connect('discord.db') as conn:
            c = conn.cursor()
            c.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
            result = c.fetchone()

        # Проверяем, существует ли пользователь в базе данных
        if result is not None:
            balance = result[0]
            # Упоминаем эмодзи рядом с балансом
            emoji = "<:famcoin:717105131619090513>"
            await ctx.send(f"Баланс участника {member.mention}: {balance} {emoji}")
        else:
            await ctx.send(f"{member.mention} не найден в базе данных.")

    def get_balance(user_id):
        with sqlite3.connect('discord.db') as conn:
            c = conn.cursor()
            c.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
            balance = c.fetchone()
            return balance[0] if balance else 0  # Возвращает 0, если пользователь не найден

    @bot.command()
    async def give_coins(ctx, member: disnake.Member, amount: int):
        if amount <= 0:
            await ctx.send("Количество монет должно быть положительным.")
            return

        # Получаем ID пользователя, которому будут даны монеты
        user_id = member.id

        with sqlite3.connect('discord.db') as conn:
            c = conn.cursor()
            # Обновляем баланс пользователя, добавляя указанное количество монет
            c.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (amount, user_id))
            conn.commit()

        # Получаем новый баланс после добавления монет
        new_balance = get_balance(user_id)
        await ctx.send(f"Участник {member.mention} получил {amount} монет!")

    @bot.command()
    async def shop(ctx):
        with sqlite3.connect('discord.db') as conn:
            c = conn.cursor()
            c.execute("SELECT role_id, price FROM shop")
            items = c.fetchall()

        if not items:
            await ctx.send("Магазин пуст.")
            return

        # Создание встраиваемого сообщения с черной боковой полоской
        embed = disnake.Embed(title="Магазин ролей", color=0x000000)

        # Установка изображения в эмбед (укажите ссылку на ваше изображение)
        embed.set_image(url="https://is.gd/Q1MaOD")  # Замените на вашу ссылку на изображение
        embed.set_footer(text="Для покупки товара, введите команду (!buy + номер позиции)")

        # Добавляем каждую роль в embed с нумерацией
        for index, item in enumerate(items, start=1):
            role_id = item[0]
            price = item[1]

            # Получаем объект роли по её ID
            role = ctx.guild.get_role(int(role_id))

            if role:
                role_name = role.name  # Получаем название роли
                embed.add_field(name=f"{index}. Роль: {role_name}", value=f"Цена: {price} монет", inline=False)

        # Отправляем встраиваемое сообщение
        await ctx.send(embed=embed)

    @bot.command()
    async def buy(ctx, position: int):
        with sqlite3.connect('discord.db') as conn:
            c = conn.cursor()
            c.execute("SELECT role_id, price FROM shop")
            items = c.fetchall()

        # Проверяем, существует ли позиция
        if position < 1 or position > len(items):
            await ctx.send("Некорректный номер позиции. Пожалуйста, введите правильный номер.")
            return

        # Получаем данные о роли
        role_id = items[position - 1][0]  # Позиция в списке (начиная с 0)
        price = items[position - 1][1]

        user_id = ctx.author.id
        # Получаем баланс пользователя
        c.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
        balance = c.fetchone()

        if not balance or balance[0] < price:
            await ctx.send("У вас недостаточно монет для покупки этой роли.")
            return

        # Снимаем деньги и добавляем роль
        new_balance = balance[0] - price
        c.execute("UPDATE users SET coins = ? WHERE user_id = ?", (new_balance, user_id))
        await ctx.author.add_roles(disnake.Object(id=role_id))  # Добавляем роль
        conn.commit()

        await ctx.send(f"Вы купили роль <@&{role_id}> за {price} монет! Остаток: {new_balance} монет.")

    @bot.command()
    async def top(ctx):
        with sqlite3.connect('discord.db') as conn:
            c = conn.cursor()
            # Извлекаем пользователей и их монеты, сортируем по убыванию
            c.execute("SELECT user_id, coins FROM users ORDER BY coins DESC LIMIT 10")
            top_users = c.fetchall()

        if not top_users:
            await ctx.send("Топ пользователей пуст.")
            return

        # Создание встраиваемого сообщения
        embed = disnake.Embed(title="Топ пользователей по монетам", color=0x000000)  # Чёрный цвет
        for index, (user_id, coins) in enumerate(top_users, start=1):
            user = ctx.guild.get_member(user_id)

            # Проверяем, найден ли пользователь
            if user is not None:
                user_mention = user.mention  # Упоминание пользователя
                user_nickname = user.nick if user.nick else user.name  # Ник или имя пользователя
            else:
                user_mention = "Неизвестный пользователь"
                user_nickname = "Неизвестен"  # Указание на то, что пользователя не найдено

            embed.add_field(name=f"{index}. {user_mention} ({user_nickname})", value=f"{coins} монет", inline=False)

        # Отправляем встраиваемое сообщение
        await ctx.send(embed=embed)



