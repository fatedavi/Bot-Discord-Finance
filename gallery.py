import pathlib
import discord


class GalleryView(discord.ui.View):

    def __init__(self, images: list[pathlib.Path], title: str = "", description: str = ""):
        super().__init__(timeout=180)
        self.images = images
        self.title = title
        self.description = description
        self.index = 0
        self._update_buttons()

    def _update_buttons(self):
        self.prev_button.disabled = self.index == 0
        self.next_button.disabled = self.index == len(self.images) - 1

    def _build_embed(self):
        embed = discord.Embed(
            title=self.title,
            description=self.description,
            color=discord.Color.magenta()
        )
        embed.set_image(url="attachment://gallery.jpeg")
        embed.set_footer(text=f"{self.index + 1} / {len(self.images)}")
        return embed

    async def _render(self, interaction: discord.Interaction):
        path = self.images[self.index]
        file = discord.File(path, filename="gallery.jpeg")
        embed = self._build_embed()
        self._update_buttons()
        await interaction.response.edit_message(
            attachments=[file], embed=embed, view=self
        )

    @discord.ui.button(label="◀", style=discord.ButtonStyle.secondary)
    async def prev_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.index -= 1
        await self._render(interaction)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.secondary)
    async def next_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.index += 1
        await self._render(interaction)
