import discord
import requests
import interactions
import io
import aiohttp
from io import BytesIO
from PIL import Image
from interactions.api.models.message import Embed
from imgix import UrlBuilder
from discord import File
from redbot.core import commands, Config, checks

class CatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)

    @commands.command(
        name="cat", 
        description="Get a random cat image",
    )
    async def cat_command(self, ctx: commands.Context, text: str, mention: discord.Member):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thecatapi.com/v1/images/search') as response:
                data = await response.json()
                image_url = data[0]['url']

        # Build the Imgix URL with text overlay
        builder = UrlBuilder(domain=IMGIX_DOMAIN, sign_key=IMGIX_TOKEN)
        params = {"txt": text, "txtalign": "center,bottom", "txtsize": 48, "txtfont": "Arial"}

        if text:
            url = builder.create_url(image_url, params)
        else:
            url = builder.create_url(image_url)

        async with session.get(url) as img_response:
            # Load image from the response
            img = Image.open(BytesIO(await img_response.read()))

            # Save image as bytes to be sent as attachment
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            file = File(img_bytes, filename='cat.jpg')

        # Convert Imgix URL to Imgur link
        headers = {'Authorization': 'Client-ID ' + IMGUR_CLIENT_ID}
        data = {'image': url}
        response = requests.post('https://api.imgur.com/3/image', headers=headers, data=data)
        link = response.json()['data']['link']

        title = "A random Catto 😺"
        message = f"A random cat with '{text}' written on it 😺" if text else "A random cat 😺"
        message2 = "🦊"
        message3 = "Someone sent you a cat! 😺"
        embed = Embed(title=title, description=message, color=int(discord.Color.gold().value))

        if mention:
            mention_string = mention.mention
            embed.description = f"{mention_string} {message2}"

        embed.set_image(url=link)
        await ctx.send(embed=embed)
        await ctx.send(f"{mention_string} {message3}")

    @commands.command(
        name="fox",
        description="Sends a random fox or 'floof' to your screen 🦊"
    )
    async def fox_command(self, ctx: commands.Context):
        response = requests.get('https://randomfox.ca/floof/')
        image_url = response.json()['image']

        await ctx.send(f"Here is a random Fox! 🦊 : {image_url}")

def setup(bot):
    bot.add_cog(CatCog(bot))
