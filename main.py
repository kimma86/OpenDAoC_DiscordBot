import discord
import requests
import json
import logging
from class_colors import get_color
from rank_titles import get_title

# config -->
token = "token goes here"
site = "https://example.com/api"
guilds = 123456789101112134
# <-- config

bot = discord.Bot()


logging.basicConfig(filename='aria_bot.log', level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')


@bot.event
async def on_ready():
    print(f"Bot is online, we have logged in as {bot.user}")
    logging.info(f'Bot is ready: {bot.user}')
    r = requests.get(f'{site}/stats')
    if r.status_code == 200:
        print('api is online')
    else:
        print('api seems to be offline')


@bot.slash_command(guild_ids=[guilds], description="Fetch player information from the Herald.")
async def who(ctx, player_name):
    command_name = ctx.command.name
    user_name = ctx.author.name
    logging.info(f'Command used: {command_name} {player_name} by {user_name}')
    player_name = player_name.capitalize()

    try:
        r = requests.get(f"{site}/player/{player_name}")
        # we could to /getAll here maybe, and then get rank all, rank realm, rank class as well, performance?

        if r.status_code == 200:
            res = r.json()

            player_class = res['class']
            player_rank = res['realmRank']
            player_rank_value = int(player_rank.split('L')[0])
            realm = res['realm']
            # emoji = ':' + realm[:3].lower() + ':'         # for :hib: :alb: :mid: emoji

            color = get_color(realm, player_class)
            title = get_title(realm, player_rank_value)

            embed_var = discord.Embed(
                title=f"Player Information: {player_name}",
                color=color
            )
            embed_var.add_field(
                name="Name",
                value=f"{res['name']} {res['lastname'] or ''}",
                inline=True
            )
            embed_var.add_field(
                name="Race",
                value=res['race'],
                inline=True
            )
            embed_var.add_field(
                name="Class",
                value=res['class'],
                inline=True
            )
            embed_var.add_field(
                name="Guild",
                value=f"<{res['guild']}>",
                inline=True
            )
            embed_var.add_field(
                name="Level",
                value=f"L{res['level']}",
                inline=True
            )
            embed_var.add_field(
                name="Realm Rank",
                value=res['realmRank'],
                inline=True
            )
            embed_var.add_field(
                name="Realm Points",
                value=res['realmPoints'],
                inline=True
            )
            embed_var.add_field(
                name="Title",
                value=title,
                inline=True
            )
            await ctx.respond(embed=embed_var)
        else:
            logging.info(f"Player {player_name} not found. Command by {user_name}")
            await ctx.respond(f"Player {player_name} not found.")

    except Exception as e:
        logging.info(f'An error occurred: {e}')


@bot.slash_command(guild_ids=[guilds], description="Show top 10 players")
async def top(ctx):
    command_name = ctx.command.name
    user_name = ctx.author.name
    logging.info(f'Command used: {command_name} by {user_name}')
    try:
        r = requests.get(f"{site}/stats/rp")
        res = json.loads(r.text)

        embed_var = discord.Embed(
            title="Top Players by Realm Points",
            color=0x00FF00  # green
        )

        # top players in the embed
        for i, player_info in enumerate(res[:10], start=1):
            embed_var.add_field(
                name=f"#{i}: {player_info['name']}",
                value=f"Realm Rank: {player_info['realmRank']}"
                      f"\nRP: {player_info['realmPoints']}"
                      f"\nClass: {player_info['class']}",
                inline=False
            )

        await ctx.respond(embed=embed_var)

    except Exception as e:
        logging.info(f'An error occurred: {e}')


@bot.slash_command(guild_ids=[guilds], description="Show top 10 by class")
async def get_class(ctx, player_class):
    command_name = ctx.command.name
    user_name = ctx.author.name
    logging.info(f'Command used: {command_name} by {user_name}')
    try:
        r = requests.get(f"{site}/player/getAll")
        res = json.loads(r.text)
        player_class = player_class.capitalize()

        filtered_players = sorted([player_info for player_info in res if player_info['class'] == player_class],
                                  key=lambda x: x['realmPoints'],
                                  reverse=True)[:10]

        embed_var = discord.Embed(
            title=f"Top {player_class} players by RPs",
            color=0x00FF00  # green
        )

        # top players in the embed
        for i, player_info in enumerate(filtered_players, start=1):
            player_rank = player_info['realmRank']
            player_rank_value = int(player_rank.split('L')[0])
            realm = player_info['realm']
            title = get_title(realm, player_rank_value)

            embed_var.add_field(
                name=f"#{i}: {player_info['name']}",
                value=f"Realm Rank: {player_info['realmRank']}"
                      f"\nRP: {player_info['realmPoints']}"
                      f"\nTitle: {title}",
                inline=False
            )

        await ctx.respond(embed=embed_var)

    except Exception as e:
        logging.info(f'An error occurred: {e}')


@bot.slash_command(guild_ids=[guilds], description="Show server stats/players online")
async def stats(ctx):
    command_name = ctx.command.name
    user_name = ctx.author.name
    logging.info(f'Command used: {command_name} by {user_name}')
    try:
        r = requests.get(f"{site}/stats/")
        r2 = requests.get(f"{site}/stats/uptime")
        res = json.loads(r.text)
        res2 = json.loads(r2.text)

        # realm statistics (logged in) & full uptime
        albion = res['Albion']
        hibernia = res['Hibernia']
        midgard = res['Midgard']
        total = res['Total']
        uptime = res2['uptime']

        embed_var = discord.Embed(
            title="Realm Statistics",
            color=0x00FF00  # green
        )

        embed_var.add_field(
            name="Albion",
            value=str(albion),
            inline=True
        )
        embed_var.add_field(
            name="Hibernia",
            value=str(hibernia),
            inline=True
        )
        embed_var.add_field(
            name="Midgard",
            value=str(midgard),
            inline=True
        )
        embed_var.add_field(
            name="Total",
            value=str(total),
            inline=True
        )
        embed_var.add_field(
            name="Uptime",
            value=str(uptime),
            inline=True
        )

        await ctx.respond(embed=embed_var)

    except Exception as e:
        logging.info(f'An error occurred: {e}')


@bot.slash_command(guild_ids=[guilds], description="Show players realm abilities")
async def ra(ctx, player_name):
    command_name = ctx.command.name
    user_name = ctx.author.name
    logging.info(f'Command used: {command_name} {player_name} by {user_name}')
    try:

        url = f"{site}/player/{player_name}/specs"

        r = requests.get(url)
        res = json.loads(r.text)

        if res:
            player_info = res[0]

            player_class = player_info['class']
            race = player_info['race']
            realm_abilities = player_info['realmAbilities']

            # nicely formatted string for realm abilities
            formatted_abilities = "\n".join([f"{ability}: {level}" for ability, level in realm_abilities.items()])

            embed_var = discord.Embed(
                title=f"Realm Abilities for {player_name}",
                color=0x00FF00  # green
            )

            embed_var.add_field(
                name="Class",
                value=player_class,
                inline=True
            )
            embed_var.add_field(
                name="Race",
                value=race,
                inline=True
            )
            embed_var.add_field(
                name="Realm Abilities",
                value=f"```{formatted_abilities}```",  # show specs in code block
                inline=False
            )

            await ctx.respond(embed=embed_var)
        else:
            await ctx.respond(f"Player {player_name} not found or hiding RAs.")

    except Exception as e:
        logging.info(f'An error occurred: {e}')


@bot.slash_command(guild_ids=[guilds], description="Show players specializations")
async def spec(ctx, player_name):
    command_name = ctx.command.name
    user_name = ctx.author.name
    logging.info(f'Command used: {command_name} {player_name} by {user_name}')
    try:
        url = f"{site}/player/{player_name}/specs"

        r = requests.get(url)
        res = json.loads(r.text)

        if res:
            player_info = res[0]
            player_class = player_info['class']
            race = player_info['race']

            specializations = player_info.get('specializations', {})

            formatted_specializations = "\n".join([f"{specs}: {level}" for specs, level in specializations.items()])

            embed_var = discord.Embed(
                title=f"Specializations for {player_name}",
                color=0x00FF00  # green
            )
            embed_var.add_field(
                name="Class",
                value=player_class,
                inline=True
            )
            embed_var.add_field(
                name="Race",
                value=race,
                inline=True
            )
            embed_var.add_field(
                name="Specializations",
                value=f"```{formatted_specializations}```",  # show specs in code block
                inline=False
            )

            await ctx.respond(embed=embed_var)
        else:
            await ctx.respond(f"Player {player_name} not found or hiding specializations.")

    except Exception as e:
        logging.warning(f'An error occurred: {e}')


bot.run(token)
