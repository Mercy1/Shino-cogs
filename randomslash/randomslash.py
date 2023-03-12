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


from redbot.core import commands

class randomslash(commands.Cog):



    @commands.command(
    name="cat", 
    description="Get a random cat image",
    options = [
        interactions.Option(
            name="text",
            description="What you want the text to say on the image",
            type=interactions.OptionType.STRING,
            required=True,
        ),

        interactions.Option(
            name="mention",
            description="Mention a user",
            type=interactions.OptionType.USER,
            required=True,
        ),
    ],
    )
    async def cat(ctx: interactions.CommandContext, text: str, mention: discord.Member):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thecatapi.com/v1/images/search') as response:
                data = await response.json()
                image_url = data[0]['url']

        
        # Imgix credentials
        IMGIX_DOMAIN = 'sinon.imgix.net'
        IMGIX_TOKEN = 'BtuMAnze33zRPbQ8'
        IMGUR_CLIENT_ID = 'a803934c495300c'

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



        # Append file extension to force file format
        #url = urlmg + ".png"

        title = "A random Catto 😺"
        message = f"A random cat with '{text}' written on it 😺" if text else "A random cat 😺"
        message2 = "🦊"
        message3 = "Someone sent you a cat! 😺"
        embed = Embed(title=title, description=message, color=int(discord.Color.gold().value))

        if mention:
            mention_string = mention.mention
            embed.description = f"{mention_string} {message2}"
    


    
        embed.set_image(url=link) #url=url default 
        await ctx.send(embeds=[embed])
        await ctx.send(f"{mention_string} {message3}")
        #DEBUG await ctx.send(url) - This posts the non-preview RAW Imgix link 


    @commands.command(
    name="fox",
    description="Sends a random fox or 'floof' to your screen 🦊"
)

    async def fox(ctx: interactions.CommandContext):
        response = requests.get('https://randomfox.ca/floof/')
        image_url = response.json()['image']

        await ctx.send(f"Here is a random Fox! 🦊 : {image_url}")







