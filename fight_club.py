import disnake
from changing_balance import withdrawal_of_funds, replenishment_of_funds
from random import choice


class FightButton(disnake.ui.View):
    @disnake.ui.button(label="Удар в ноги", emoji="🦵", custom_id="legs_hit", style=disnake.ButtonStyle.primary)
    async def legs_button_callback(self, button, inter):
        await hit(inter, "удар в ноги")

    @disnake.ui.button(label="Удар в живот", emoji="👊", custom_id="torso_hit", style=disnake.ButtonStyle.primary)
    async def torso_button_callback(self, button, inter):
        await hit(inter, "удар в живот")

    @disnake.ui.button(label="Удар в голову", emoji="🤕", custom_id="head_hit", style=disnake.ButtonStyle.primary)
    async def head_button_callback(self, button, inter):
        await hit(inter, "удар в голову")

    @disnake.ui.button(label="Вернуться", emoji="👈", custom_id="Back", style=disnake.ButtonStyle.gray)
    async def back_button_callback(self, button, inter):
        pass

    async def on_error(self, error, item, inter):
        pass


async def hit(inter, body_part):
    await withdrawal_of_funds(inter, 10)
    if not choice(range(0, 2)):
        await replenishment_of_funds(inter, 15)
        await inter.response.send_message(embed=disnake.Embed(description=f"**Ты сделал {body_part} и отправил своего соперника в нокаут! Так держать, твой ты получаешь 15 монет на свой баланс!**"), ephemeral=True)
        return
    await inter.response.send_message(embed=disnake.Embed(description=f"Ты сделал {body_part}, но противник защитился и сделал удар. Ты остался без 5 зубов и 10 монет."), ephemeral=True)


async def show_fight_club_menu(inter):
    await inter.response.edit_message(embed=disnake.Embed(title="Бойцовский клуб", description="*Первое правило бойцовского клуба - никому не рассказывай про бойцовский клуб...* \n **Стоимость вступления в поединок - 10р. ** \n Тебе дают возможность сделать удар первым, если ты хорошо реализуешь его, то получишь 15 рублей, если противник защитится, соболезную тебе..."), view=FightButton())