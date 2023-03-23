import disnake
from disnake.ext import commands
from config import settings
from PaymentSystemRuKassa import while_deletion_bill


intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, )


@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.online, activity=disnake.Game(name="/start for start", type=3))
    await while_deletion_bill(60)


# Add cogs
bot.load_extension("start_cog")
bot.load_extension("event")
bot.load_extension("balance_management")
bot.load_extension("add_product_cog")

bot.run(settings['token'])
