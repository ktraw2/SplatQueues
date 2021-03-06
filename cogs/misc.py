import asyncio
import math
import config
from discord.ext import commands
from modules.async_client import AsyncClient
from modules import embeds, checks

# Delete below when ac command is EOL-ed
from datetime import date, datetime
from dateutil.relativedelta import relativedelta



class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(case_insensitive=True, invoke_without_command=True, aliases=["commands"])
    async def help(self, ctx, *args):
        """default help message for SplatBot"""
        if len(args) == 0:
            help_embed = embeds.generate_base_help_embed(self.bot)
            help_embed.add_field(name=":question: **Help Categories**",
                                 value="To get help for the various parts of " + self.bot.user.name + ", "
                                       "use `s!help [page]` to view any of the pages listed below:\n\n"
                                       "1. Lobby Commands\n"
                                       "2. Rotation Commands\n"
                                       "3. Misc. Commands\n"
                                       "4. Command Syntax Help\n\n"
                                       "You can also type `s!help full` "
                                       "if you would like the view the full contents of the help in a DM.")
            embeds.add_help_embed_footer_links(help_embed, self.bot)
            await ctx.send(embed=help_embed)
        else:
            await ctx.send(":x: Sorry, that is not a valid help page. Type `s!help` to view the valid help pages.")

    @help.command(name="1", aliases=["Lobby"])
    async def lobby_commands(self, ctx):
        help_embed = embeds.generate_base_help_embed(self.bot)
        embeds.add_help_embed_field(help_embed, "lobby_commands")
        await ctx.send(embed=help_embed)

    @help.command(name="2", aliases=["Rotation", "Schedule"])
    async def rotation_commands(self, ctx):
        help_embed = embeds.generate_base_help_embed(self.bot)
        embeds.add_help_embed_field(help_embed, "rotation_commands")
        await ctx.send(embed=help_embed)

    @help.command(name="3", aliases=["Misc"])
    async def misc_commands(self, ctx):
        help_embed = embeds.generate_base_help_embed(self.bot)
        embeds.add_help_embed_field(help_embed, "misc_commands")
        await ctx.send(embed=help_embed)

    @help.command(name="4", aliases=["Command"])
    async def command_syntax(self, ctx):
        help_embed = embeds.generate_base_help_embed(self.bot)
        embeds.add_help_embed_field(help_embed, "command_syntax")
        await ctx.send(embed=help_embed)

    @help.command()
    async def full(self, ctx):
        help_embed = embeds.generate_base_help_embed(self.bot)
        for key, field in embeds.help_embed_fields.items():
            help_embed.add_field(name=field["title"], value=field["body"])
        embeds.add_help_embed_footer_links(help_embed, self.bot)
        await ctx.author.send(embed=help_embed)
        await ctx.send(":white_check_mark: " + ctx.author.mention +
                       ", the full help for " + self.bot.user.name + " has been DMed to you to prevent spam.")

    @commands.command()
    @commands.check(checks.user_is_developer)
    async def update(self, ctx, *args):
        self.bot.exit = 3  # exit code will be interpreted by bash to update bot
        await ctx.send(":white_check_mark: Updating and restarting " + self.bot.user.name + "...")
        if self.bot.session is not None:
            await self.bot.session.close()
        await self.bot.logout()

    @commands.command()
    async def hello(self, ctx, *args):
        await ctx.send("Hello, World!")

    @commands.command(aliases=["🍑"])
    @commands.guild_only()
    @checks.message_from_guild(config.ts_guild_id)
    @commands.check(checks.off_topic_commands_enabled)
    async def buttcheeks(self, ctx, *args):
        await ctx.message.add_reaction("🍑")
        await ctx.send("Who is buttcheeks???")

    @commands.command(aliases=["reminddavid"])
    @commands.guild_only()
    @checks.message_from_guild(config.ts_guild_id)
    @commands.check(checks.off_topic_commands_enabled)
    async def remind_david(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("<@283480526336163840> reminder to bring gcn to wgf kthxbai")
        else:
            david_reminder_str = ""
            for arg in args:
                david_reminder_str = david_reminder_str + arg + " "
            await ctx.send("<@283480526336163840> " + david_reminder_str)

    @commands.command(aliases=["tea", "🍵"])
    @commands.guild_only()
    @checks.message_from_guild(config.ts_guild_id)
    @commands.check(checks.off_topic_commands_enabled)
    async def david_tea(self, ctx, *args):
        await ctx.message.add_reaction("🍵")
        await ctx.send("<@283480526336163840>, you're missing out :tea:")

    @commands.command()
    @commands.check(checks.off_topic_commands_enabled)
    async def bruh(self, ctx, *args):

        is_silent = False
        for i in range(0, len(args)):
            if "-s" in args[i] or "--silent" in args[i] or "mute" in args[i]:
                is_silent = True

        # gets previous message and reacts to it
        channel = ctx.message.channel
        logs = channel.history(limit=2)
        # FIXME I'm guessing there's a better way of doing this but i can't think of it
        await logs.next()  # skips command message
        # adds reaction
        async for msg in logs:
            await msg.add_reaction("🇧")
            await msg.add_reaction("🇷")
            await msg.add_reaction("🇺")
            await msg.add_reaction("🇭")

        # sends out message, space separated due to stupid unicode
        if is_silent:
            if ctx.message.channel.permissions_for(ctx.message.channel.guild.me).manage_messages:
                await ctx.message.delete()
        else:
            await ctx.send(":regional_indicator_b: :regional_indicator_r: "
                           ":regional_indicator_u: :regional_indicator_h:")

    @commands.command()
    @commands.check(checks.off_topic_commands_enabled)
    async def g7(self, ctx, *args):
        g7_str = ":loudspeaker: MAY I HAVE YOUR ATTENTION PLEASE\n" \
                 ":loudspeaker: MAY I HAVE YOUR ATTENTION PLEASE\n" \
                 ":loudspeaker: THE BUILDING ALARM SYSTEM HAS BEEN ACTIVATED\n" \
                 ":loudspeaker: PLEASE EVACUATE IMMEDIATELY\n" \
                 ":loudspeaker: PLEASE DO NOT USE THE ELEVATORS"
        for i in range(0, 3):
            await ctx.send(g7_str)
            await asyncio.sleep(2)

    @commands.command(aliases=["ac", "nh", "acnh"])
    @commands.check(checks.off_topic_commands_enabled)
    async def animalcrossing(self, ctx, *args):
        curr_time = datetime.now()
        delta = relativedelta(datetime(year=2020, month=3, day=19, hour=21), curr_time)

        if delta.days < 0 or delta.hours < 0 or delta.minutes < 0:
            ac_str = "New Horizons is out! Why are you still using Splatbot?"
        else:
            ac_str = "Only " + str(delta.days) + " days, " + str(delta.hours) + " hours, and " + str(delta.minutes)\
                 + " minutes until New Horizons comes out!"

        await ctx.send(ac_str)

    @commands.command()
    @commands.guild_only()
    @checks.message_from_guild(config.ts_guild_id)
    @commands.check(checks.off_topic_commands_enabled)
    async def kevin(self, ctx, *args):
        await ctx.send(ctx.guild.get_role(config.ts_guild_id).mention + " KEVIN GANG KEVIN GANG KEVIN GANG")

    @commands.command(aliases=["vote", "upvote", "downvote", "karma"])
    @commands.check(checks.off_topic_commands_enabled)
    async def reddit(self, ctx, *args):
        # gets previous message and reacts to it, from the `bruh` command
        channel = ctx.message.channel
        logs = channel.history(limit=2)
        # FIXME I'm guessing there's a better way of doing this but i can't think of it
        await logs.next() # skips command message
        # adds reaction
        async for msg in logs:
            await msg.add_reaction("⬆️")
            await msg.add_reaction("⬇️")

        # deletes command that made it
        if ctx.message.channel.permissions_for(ctx.message.channel.guild.me).manage_messages:
            await ctx.message.delete()

    @commands.command()
    @commands.check(checks.off_topic_commands_enabled)
    async def boxie(self, ctx, *args):
        await ctx.send("#PreventBridgettAbuse :package:")

    @commands.command(aliases=["listkevins", "kevins"])
    @commands.guild_only()
    @checks.message_from_guild(config.ts_guild_id)
    @commands.check(checks.off_topic_commands_enabled)
    async def list_kevins(self, ctx, *args):
        kevin_str = "Kevin #1: <@394434644642103296>" + "\n" + \
                    "Kevin #2: " + "\n" + \
                    "Kevin #3: " + "\n" + \
                    "Kevin #4: " + "\n" + \
                    "Kevin #5: " + "\n" + \
                    "Kevin #6: " + "\n" + \
                    "Kevin # Rainmaker Main: <@192053720236818432>" + "\n" + \
                    "." + "\n" + \
                    "." + "\n" + \
                    "." + "\n" + \
                    "Worst Kevin: <@333435876275388426>" + "\n"
        await ctx.send(kevin_str)

    @commands.command()
    @commands.guild_only()
    @checks.message_from_guild(config.ts_guild_id)
    @commands.check(checks.off_topic_commands_enabled)
    async def list_uncool_people(self, ctx, *args):
        await ctx.send("Uncool People:\n"
                       "For being dum dum: <@333435876275388426>")

    @commands.command(case_insensitive=True, aliases=["f"])
    @commands.check(checks.off_topic_commands_enabled)
    async def eff(self, ctx, *args):
        # embedded function for small calculation
        def get_num_f(base_size):
            return int(math.ceil(base_size * size_mult))

        char_to_print = "F"
        str_to_send = ""
        size_mult = 1
        if len(args) > 0:
            char_to_print = args[0]

            # Blacklisting @everyone and @here to prevent pinging everyone
            if "@everyone" in char_to_print or "@here" in char_to_print:
                await ctx.send(":x: `@everyone` and `@here` have been blacklisted. Please try again.")
                return

            size_mult = 0.5

        # Builds the big F
        for x in range(get_num_f(3)):
            for y in range(get_num_f(19)):
                str_to_send = str_to_send + char_to_print
            str_to_send = str_to_send + "\n"

        for x in range(get_num_f(3)):
            for y in range(get_num_f(6)):
                str_to_send = str_to_send + char_to_print
            str_to_send = str_to_send + "\n"

        for x in range(get_num_f(3)):
            for y in range(get_num_f(12)):
                str_to_send = str_to_send + char_to_print
            str_to_send = str_to_send + "\n"

        for x in range(get_num_f(5)):
            for y in range(get_num_f(6)):
                str_to_send = str_to_send + char_to_print
            str_to_send = str_to_send + "\n"

        if len(str_to_send) > 2000:
            await ctx.send(":warning: Output exceeds Discord character limit. Please try a smaller input.")
        else:
            await ctx.send(str_to_send)

    @commands.command()
    @commands.is_owner()
    @commands.check(checks.off_topic_commands_enabled)
    async def getip(self, ctx, *args):
        ip_text = await AsyncClient(session=self.bot.session).send_request("http://checkip.dyndns.org/")
        # scrape page for body
        body = ip_text[ip_text.index("<body>") + len("<body>"):ip_text.index("</body>")]
        await ctx.send(body)


def setup(bot):
    # remove the default help command so the better one can be used
    bot.remove_command("help")
    bot.add_cog(Misc(bot))
