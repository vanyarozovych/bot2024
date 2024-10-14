import disnake


def setup(bot):
    @bot.command()
    async def post_verification(ctx):
        # Получение объекта канала по ID
        channel_id = 1289128378800013413  # Замените на фактический ID текстового канала
        target_channel = bot.get_channel(channel_id)

        if target_channel is not None:
            # Создание embed сообщения
            embed = disnake.Embed(
                title="Верификация на сервере 💞",
                description=(
                    "_Для того чтобы получить доступ к серверу,_\n_пройдите верификацию "
                    "через голосовой канал:_\n\n<#1288810425475006524>\n<#1289649187742547969>\n"
                    "<#1289657190822445089>"
                ),
                color=0x323232
            )
            embed.set_image(url=(
                "https://cdn.discordapp.com/attachments/900316761520500756/"
                "1291821952494731387/image.png?ex67017e72&is=67002cf2&"
                "hm=bb424102c1823707210ab7616f6e85d4412cc9cd0679a51f26669c3f9f803026&"
            ))

            # Отправка embed сообщения в определенный канал
            await target_channel.send(embed=embed)
        else:
            await ctx.send("Канал не найден.")  # Отправить сообщение в канал, где была вызвана команда

    @bot.command()
    async def post_navigation(ctx):
        # Получение объекта канала по ID
        channel_id = 900316761520500756  # Замените на фактический ID текстового канала
        target_channel = bot.get_channel(channel_id)

        if target_channel is not None:
            # Создание embed сообщения
            embed = disnake.Embed(
                title="Добро пожаловать на fam!",
                description=(
                    "Приветствую! Зайди в голосовой канал <#760998035018088489>, там тебя "
                    "\nвстретит **Администрация Сервера**, и поможет тебе пройти "
                    "\nверификацию. Мы все ждём тебя, удачи!"
                ),
                color=0x323232
            )
            embed.set_image(url="https://media.giphy.com/media/c1NcxJX9Us3P9sRSHC/giphy.gif")

            # Отправка embed сообщения в определенный канал
            await target_channel.send(embed=embed)
        else:
            await ctx.send("Канал не найден.")  # Отправить сообщение в канал, где была вызвана команда

    @bot.command()
    async def post_available_roles(ctx):
        channel_id = 900316761520500756  # Замените на фактический ID текстового канала
        target_channel = bot.get_channel(channel_id)

        if target_channel is not None:
            # Создание embed сообщения
            embed = disnake.Embed(title="**Доступные роли**", color=0x323232)

            embed.add_field(
                name="Гендерная роль",
                value=(
                    "<@&760998034845728780> гендерная роль, позволяющая пользоваться "
                    "голосовыми каналами и чатами. Получить можно при прохождении "
                    "адаптации сервера."
                ),
                inline=False
            )
            embed.add_field(
                name="Гендерная роль 2",
                value=(
                    "<@&760998034792251411> гендерная роль, позволяющая пользоваться "
                    "голосовыми каналами и чатами. Получить можно при прохождении "
                    "адаптации сервера."
                ),
                inline=False
            )
            embed.add_field(
                name="Ивент-роль Minecraft",
                value=(
                    "<@&1123987922308313158> ивент-роль, позволяющая участвовать "
                    "в ивенте minecraft. Получить можно при прохождении адаптации "
                    "сервера."
                ),
                inline=False
            )
            embed.add_field(
                name="Ивент-роль Among Us",
                value=(
                    "<@&1124470731988807690> ивент-роль, позволяющая участвовать "
                    "в ивенте among-us. Получить можно при прохождении адаптации "
                    "сервера."
                ),
                inline=False
            )
            embed.add_field(
                name="Ивент-роль Puzzle",
                value=(
                    "<@&1125317036839538760> ивент-роль, позволяющая участвовать "
                    "в ивенте puzzle. Получить можно при прохождении адаптации "
                    "сервера."
                ),
                inline=False
            )
            embed.add_field(
                name="Ивент-роль 2",
                value=(
                    "<@&1121843791926657114> ивент-роль, позволяющая участвовать "
                    "в ивенте puzzle. Получить можно при прохождении адаптации "
                    "сервера."
                ),
                inline=False
            )

            # Загрузка изображения с файла на компьютере
            with open("D:/Downloads/Telegram Desktop/ДОСТУПНЫЕ РОЛИ.png", "rb") as image_file:
                image = disnake.File(image_file, filename="ДОСТУПНЫЕ РОЛИ.png")
                embed.set_thumbnail(url="attachment://ДОСТУПНЫЕ РОЛИ.png")

            await target_channel.send(embed=embed, file=image)
        else:
            await ctx.send("Канал не найден.")  # Отправить сообщение в канал, где была вызвана команда
