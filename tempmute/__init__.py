from .tempmute import TempMute


async def setup(bot):
    cog = Mod(bot)
    bot.add_cog(cog)
    await cog.initialize()
