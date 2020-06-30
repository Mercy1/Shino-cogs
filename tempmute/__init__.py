from .tempmute import TempMute


async def setup(bot):
    cog = TempMute(bot)
    bot.add_cog(cog)
    await cog.initialize()
