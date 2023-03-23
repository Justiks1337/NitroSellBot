import disnake
from case import CaseButtons
from coin import show_coin
from fight_club import show_fight_club_menu


coin_game_menu = disnake.Embed(description="Сделай ставку и сделай свой выбор!")


class CasinoView(disnake.ui.View):
    @disnake.ui.button(label="Монетка", emoji="🪙", custom_id="coin", style=disnake.ButtonStyle.primary)
    async def coin_button_callback(self, button, inter):
        await show_coin(inter)

    @disnake.ui.button(label="Кейсы", emoji="📦", custom_id="case", style=disnake.ButtonStyle.primary)
    async def case_button_callback(self, button, inter):
        await inter.response.edit_message(embed=disnake.Embed(description="Для открытия кейса нажми на \"Открыть кейс\" \n **В кейсах большие шансы на выигрыш!**"), view=CaseButtons())

    @disnake.ui.button(label="Бойцовский клуб", emoji="👊", custom_id="BK", style=disnake.ButtonStyle.primary)
    async def bk_button_callback(self, button, inter):
        await show_fight_club_menu(inter)

    @disnake.ui.button(label="Вернуться", emoji="👈", custom_id="Back", style=disnake.ButtonStyle.gray)
    async def back_button_callback(self, button, inter):
        pass

