import disnake
from disnake.ext import commands
from DataBaseAssistant import change
from config import settings
from os import remove


class AddProductCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    async def add_product(self, ctx: commands.Context , id):
        if ctx.message.author.id not in settings['admin_id']:
            await ctx.send(embed=disnake.Embed(description="Не достаточно прав!"))
            return
        await ctx.message.attachments[0].save(ctx.message.attachments[0].filename)
        with open(file=ctx.message.attachments[0].filename) as file:
            while True:
                line = file.readline()
                if not line:
                    await ctx.send(embed=disnake.Embed(description="**Успех!**"))
                    file.close()
                    remove(ctx.message.attachments[0].filename)
                    return
                await change("INSERT INTO tokens VALUES (?, ?)", (line, id))


def setup(bot: commands.Bot):
    bot.add_cog(AddProductCommand(bot))