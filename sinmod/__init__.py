from .mod import sinmod


async def setup(bot):
    cog = sinmod(bot)
    bot.add_cog(cog)
    await cog.initialize()
