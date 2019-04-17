import config
import discord
from modules.splatoon_rotation import SplatoonRotation, ModeTypes
from modules.splatoon_splatfest import SplatoonSplatfest, SplatfestWinner
from datetime import datetime, timedelta
from dateutil.parser import parse
from discord.ext import commands
from misc_date_utilities.date_difference import DateDifference


class Splatfest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(case_insensitive=True, invoke_without_command=True, aliases=["sf", "fest", "splatfests"])
    async def splatfest(self, ctx, *args):
        await ctx.send(":warning: Command in alpha test")

    @rotation.group(case_insensitive=True, invoke_without_command=True, aliases=["turf", "t", "reg"])
    async def regular(self, ctx, *args):
        await self.make_single_rotation(ModeTypes.REGULAR, ctx, *args)

    @rotation.group(case_insensitive=True, invoke_without_command=True, aliases=["rank", "rk"])
    async def ranked(self, ctx, *args):
        await self.make_single_rotation(ModeTypes.RANKED, ctx, *args)

    @rotation.group(case_insensitive=True, invoke_without_command=True, aliases=["l"])
    async def league(self, ctx, *args):
        await self.make_single_rotation(ModeTypes.LEAGUE, ctx, *args)

    @rotation.group(case_insensitive=True, invoke_without_command=True, aliases=["sr", "s"])
    async def salmon(self, ctx, *args):
        await self.make_single_rotation(ModeTypes.SALMON, ctx, *args)

    @salmon.command(name="upcoming")
    async def salmon_upcoming(self, ctx, *args):
        await self.make_upcoming_rotations(ModeTypes.SALMON, ctx)

    @ranked.command(name="upcoming")
    async def ranked_upcoming(self, ctx, *args):
        await self.make_upcoming_rotations(ModeTypes.RANKED, ctx)

    @league.command(name="upcoming")
    async def league_upcoming(self, ctx, *args):
        await self.make_upcoming_rotations(ModeTypes.LEAGUE, ctx)

    @regular.command(name="upcoming")
    async def turf_upcoming(self, ctx, *args):
        await self.make_upcoming_rotations(ModeTypes.REGULAR, ctx)

    async def make_single_rotation_time(self, ctx, *args):
        time = datetime.now()

        if len(args) > 0:
            try:
                time = parse(args[0])
                # if the time has already happened, delay the lobby start time to the next day
                if DateDifference.subtract_datetimes(time, datetime.now()) <= DateDifference(0):
                    time = time + timedelta(days=1)
            except ValueError as e:
                await ctx.send(":x: You gave an invalid time.")
                return

        splatfest = SplatoonSplatfest(datetime=time, session=self.bot.session)
        success = await rotation.populate_data()

        if success:
            title = "Splatfest Information - " + splatfest.alpha_name + " vs. " + splatfest.bravo_name
            thumbnail = config.images["regular"]

            embed = discord.Embed(title=title, color=config.embed_color)
            embed.set_thumbnail(url=thumbnail)

            embed.add_field(name="Start Time", value=splatfest.start_time)
            embed.add_field(name="End Time", value=splatfest.end_time)


            # custom stuff for salmon run
            if schedule_type is ModeTypes.SALMON:
                # Checking if full rotation has been released yet for salmon
                if rotation.stage_a is None:
                    # use special formatting because salmon run can occur between two separate days
                    embed.add_field(name="Stage", value="*Not released yet*")
                    embed.add_field(name="Rotation Time",
                                    value=SplatoonRotation.format_time_sr(rotation.start_time) + " - "
                                          + SplatoonRotation.format_time_sr(rotation.end_time))
                    embed.add_field(name="Weapons", value="*Not released yet*")
                else:
                    embed.set_image(url=rotation.stage_a_image)
                    embed.add_field(name="Stage", value=rotation.stage_a)
                    # use special formatting because salmon run can occur between two separate days
                    embed.add_field(name="Rotation Time",
                                    value=SplatoonRotation.format_time_sr(rotation.start_time) + " - "
                                          + SplatoonRotation.format_time_sr(rotation.end_time))
                    embed.add_field(name="Weapons", value=rotation.weapons_array[0] + "\n" +
                                    rotation.weapons_array[1] + "\n" +
                                    rotation.weapons_array[2] + "\n" +
                                    rotation.weapons_array[3])

            else:
                embed.set_image(url=rotation.stage_a_image)
                embed.add_field(name="Stages", value=rotation.stage_a + "\n" + rotation.stage_b)
                embed.add_field(name="Rotation Time", value=SplatoonRotation.format_time(rotation.start_time) + " - " +
                                                            SplatoonRotation.format_time(rotation.end_time))

            await ctx.send(embed=embed)
        else:
            await ctx.send(":x: No rotation information was found for the given time.")

    async def make_upcoming_rotations(self, schedule_type: ModeTypes, ctx):
        schedule_array = await SplatoonRotation.get_all_rotations(time=datetime.now(), mode_type=schedule_type,
                                                                  session=self.bot.session)

        next_rot_val = 0  # Array val to access the next rotation
        title = "Upcoming Rotation Information - "
        thumbnail = ""
        if schedule_type is ModeTypes.REGULAR:
            title += "Regular Battle"
            thumbnail = config.images["regular"]
        elif schedule_type is ModeTypes.RANKED:
            title += "Ranked Battle"
            thumbnail = config.images["ranked"]
        elif schedule_type is ModeTypes.LEAGUE:
            title += "League Battle"
            thumbnail = config.images["league"]
        elif schedule_type is ModeTypes.SALMON:
            title += "Salmon Run"
            thumbnail = config.images["salmon"]

        embed = discord.Embed(title=title, color=config.embed_color)
        embed.set_thumbnail(url=thumbnail)

        # custom stuff for salmon run
        if schedule_type is ModeTypes.SALMON:
            embed.add_field(name="Mode", value=schedule_array[0].mode)
            value = ""
            for element in schedule_array:
                value = value + SplatoonRotation.format_time_sr(element.start_time) + " - " + \
                        SplatoonRotation.format_time_sr(element.end_time) + "\n"
            embed.add_field(name="Rotation Times", value=value)
        else:
            next_rot_val = 1
            for element in schedule_array:
                fmt_time = SplatoonRotation.format_time_sch(element.start_time) + " - " \
                           + SplatoonRotation.format_time_sch(element.end_time)
                embed.add_field(name="Rotation Time", value=fmt_time, inline=True)
                embed.add_field(name="Mode", value=element.mode, inline=True)

        # Calculates the amount of time until the next rotation
        time = schedule_array[next_rot_val].start_time
        time_diff = DateDifference.subtract_datetimes(time, datetime.now())
        time_str = str(time_diff)
        # For Salmon Run only: print if the rotation is happening right now
        if schedule_type is ModeTypes.SALMON and time_diff <= DateDifference(0):
            time_str = "Rotation is happening now!"

        embed.add_field(name="Time Until Next Rotation", value=time_str)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Splatfest(bot))