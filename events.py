import disnake
from disnake.ext import commands


def setup(bot):
    @bot.command()
    @commands.check_any(commands.has_role(1123262857614721104), commands.has_role(1123263812884234360),
                        commands.has_role(760998034850709540))
    async def event_among_us(ctx):
        # Получение объекта канала по ID
        channel_id = 1291935428227760210  # Замените на фактический ID текстового канала
        target_channel = bot.get_channel(channel_id)

        if target_channel is not None:
            # Создание embed сообщения
            embed = disnake.Embed(title="AMONG US!",
                                  description="<@&1291935144827031647> Начинается ивент по игре Among Us!\nЗаходите "
                                              "все в голосовой канал!",
                                  color=0x323232)
            embed.set_image(url="https://media.tenor.com/BGQHhBwbYNwAAAAC/among-us.gif")

            # Отправка embed сообщения в определенный канал
            await target_channel.send(embed=embed)
        else:
            await ctx.send("Канал не найден.")

    @bot.command()
    @commands.check_any(commands.has_role(1123262857614721104), commands.has_role(1123263812884234360),
                        commands.has_role(760998034850709540))
    async def event_puzzle(ctx):
        # Получение объекта канала по ID
        channel_id = 1291935428227760210  # Замените на фактический ID текстового канала
        target_channel = bot.get_channel(channel_id)

        if target_channel is not None:
            # Создание embed сообщения
            embed = disnake.Embed(title="Puzzle!",
                                  description="<@&1291935144827031647> Начинается ивент по игре Puzzle!\nЗаходите все "
                                              "в голосовой канал!",
                                  color=0x323232)
            embed.set_image(url="https://i.gifer.com/BgeK.gif")

            # Отправка embed сообщения в определенный канал
            await target_channel.send(embed=embed)
        else:
            await ctx.send("Канал не найден.")

    @bot.command()
    @commands.check_any(commands.has_role(1123262857614721104), commands.has_role(1123263812884234360),
                        commands.has_role(760998034850709540))
    async def event_film(ctx):
        # Получение объекта канала по ID
        channel_id = 1291935428227760210  # Замените на фактический ID текстового канала
        target_channel = bot.get_channel(channel_id)

        if target_channel is not None:
            # Создание embed сообщения
            embed = disnake.Embed(title="Film!",
                                  description="<@&1291935144827031647> Начинается ивент по просмотру "
                                              "Кино-фильмов!\nЗаходите все в голосовой канал!",
                                  color=0x323232)
            embed.set_image(url="https://i.gifer.com/7FAC.gif")

            # Отправка embed сообщения в определенный канал
            await target_channel.send(embed=embed)
        else:
            await ctx.send("Канал не найден.")

    @bot.command()
    @commands.check_any(commands.has_role(1123262857614721104), commands.has_role(1123263812884234360),
                        commands.has_role(760998034850709540))
    async def event_minecraft(ctx):
        # Получение объекта канала по ID
        channel_id = 1291935428227760210  # Замените на фактический ID текстового канала
        target_channel = bot.get_channel(channel_id)

        if target_channel is not None:
            # Создание embed сообщения
            embed = disnake.Embed(
                title="MINECRAFT!",
                description="<@&1291935144827031647> Начинается ивент по игре Minecraft! \n\n- IP: "
                            "vanyarozovych.aternos.me:56613\n- Version: 1.16.5 \n- Режим игры: выживание\n- Давайте "
                            "развиваться вместе!\n\n- (Если вы впервые заходите на сервер, попросите одного из "
                            "ивентёров добавить вас в whitelist, чтобы у вас был доступ к заходу на сервер)",
                color=0x323232
            )
            embed.set_image(url="https://media.tenor.com/c8zAMfdwlDgAAAAC/dwdsd.gif")

            # Отправка embed сообщения в определенный канал
            await target_channel.send(embed=embed)
        else:
            await ctx.send("Канал не найден.")

    @bot.command()
    @commands.check_any(commands.has_role(1123262857614721104), commands.has_role(1123263812884234360),
                        commands.has_role(760998034850709540))
    async def event_brawlstars(ctx):
        # Получение объекта канала по ID
        channel_id = 1291935428227760210  # Замените на фактический ID текстового канала
        target_channel = bot.get_channel(channel_id)

        if target_channel is not None:
            # Создание embed сообщения
            embed = disnake.Embed(
                title="BRAWLSTARS!",
                description="<@&1291935144827031647> Начинается ивент по игре BrawlStars!",
                color=0x323232
            )
            embed.set_image(url="https://media.tenor.com/7-endVMZbCoAAAAi/eshkere-edgar.gif")

            # Отправка embed сообщения в определенный канал
            await target_channel.send(embed=embed)
        else:
            await ctx.send("Канал не найден.")

    @bot.command()
    @commands.check_any(commands.has_role(1123262857614721104), commands.has_role(1123263812884234360),
                        commands.has_role(760998034850709540))
    async def event_mafia(ctx):
        # Получение объекта канала по ID
        channel_id = 1291935428227760210  # Замените на фактический ID текстового канала
        target_channel = bot.get_channel(channel_id)

        if target_channel is not None:
            # Создание embed сообщения
            embed = disnake.Embed(
                title="MAFIA!",
                description="<@&1291935144827031647> Начинается ивент по игре Mafia!",
                color=0x323232
            )
            embed.set_image(url="https://media1.tenor.com/m/DHR-LGMxXqYAAAAC/mafia.gif")

            # Отправка embed сообщения в определенный канал
            await target_channel.send(embed=embed)
        else:
            await ctx.send("Канал не найден.")

    @bot.command()
    @commands.check_any(commands.has_role(1123262857614721104), commands.has_role(1123263812884234360),
                        commands.has_role(760998034850709540))
    async def event_alias(ctx):
        # Получение объекта канала по ID
        channel_id = 1291935428227760210  # Замените на фактический ID текстового канала
        target_channel = bot.get_channel(channel_id)

        if target_channel is not None:
            # Создание embed сообщения
            embed = disnake.Embed(
                title="ALIAS!",
                description="<@&1291935144827031647> Начинается ивент по игре Alias!",
                color=0x323232
            )
            embed.set_image(url="https://media1.tenor.com/m/gWT2QqylI7gAAAAC/word-funny.gif")

            # Отправка embed сообщения в определенный канал
            await target_channel.send(embed=embed)
        else:
            await ctx.send("Канал не найден.")

    @bot.command()
    @commands.check_any(commands.has_role(1123262857614721104), commands.has_role(1123263812884234360),
                        commands.has_role(760998034850709540))
    async def event_gartic(ctx):
        # Получение объекта канала по ID
        channel_id = 1291935428227760210  # Замените на фактический ID текстового канала
        target_channel = bot.get_channel(channel_id)

        if target_channel is not None:
            # Создание embed сообщения
            embed = disnake.Embed(
                title="GARTIC PHONE!",
                description="<@&1291935144827031647> Начинается ивент по игре Gartic Phone!",
                color=0x323232
            )
            embed.set_image(url="https://media1.tenor.com/m/9u4aLvK2ZDcAAAAC/garticphone.gif")

            # Отправка embed сообщения в определенный канал
            await target_channel.send(embed=embed)
        else:
            await ctx.send("Канал не найден.")
