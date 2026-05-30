"""
Commands Module.
Contains all Discord slash commands for the finance bot.
"""
import io
import pathlib
from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands

from sheets_service import get_sheets_service
from finance_service import get_finance_service
import config
from gallery import GalleryView


async def setup_commands(bot: commands.Bot) -> None:
    """
    Set up all slash commands for the bot.
    
    Args:
        bot: The Discord bot instance
    """
    @app_commands.command(
        name='masuk',
        description='Record income transaction'
    )
    @app_commands.describe(
        amount='Amount of income',
        description='Description of income'
    )
    async def masuk(
        interaction: discord.Interaction,
        amount: app_commands.Range[int, 1],
        description: str
    ) -> None:
        """Record an income transaction."""
        try:
            sheets = get_sheets_service()
            user_name = interaction.user.name

            result = sheets.add_transaction(
                transaction_type='Income',
                amount=amount,
                description=description,
                user_name=user_name
            )

            if result:
                embed = discord.Embed(
                    title='✅ Income Recorded',
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                embed.add_field(
                    name='Amount',
                    value=f'Rp {amount:,}',
                    inline=True
                )
                embed.add_field(
                    name='Description',
                    value=description,
                    inline=True
                )
                embed.set_footer(text=f'User: {user_name}')
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    '❌ Failed to record income. Please try again.',
                    ephemeral=True
                )

        except Exception as e:
            await interaction.response.send_message(
                f'❌ Error: {str(e)}',
                ephemeral=True
            )

    @app_commands.command(
        name='keluar',
        description='Record expense transaction'
    )
    @app_commands.describe(
        amount='Amount of expense',
        description='Description of expense'
    )
    async def keluar(
        interaction: discord.Interaction,
        amount: app_commands.Range[int, 1],
        description: str
    ) -> None:
        """Record an expense transaction."""
        try:
            sheets = get_sheets_service()
            user_name = interaction.user.name

            result = sheets.add_transaction(
                transaction_type='Expense',
                amount=amount,
                description=description,
                user_name=user_name
            )

            if result:
                embed = discord.Embed(
                    title='✅ Expense Recorded',
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                embed.add_field(
                    name='Amount',
                    value=f'Rp {amount:,}',
                    inline=True
                )
                embed.add_field(
                    name='Description',
                    value=description,
                    inline=True
                )
                embed.set_footer(text=f'User: {user_name}')
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    '❌ Failed to record expense. Please try again.',
                    ephemeral=True
                )

        except Exception as e:
            await interaction.response.send_message(
                f'❌ Error: {str(e)}',
                ephemeral=True
            )

    @app_commands.command(
        name='balance',
        description='Check current balance'
    )
    async def balance(interaction: discord.Interaction) -> None:
        """Check the current balance (total income, expense, and balance)."""
        try:
            sheets = get_sheets_service()
            finance = get_finance_service()

            if sheets.is_empty():
                embed = discord.Embed(
                    title='💰 Balance Report',
                    color=discord.Color.blue(),
                    description='No transactions recorded yet.'
                )
                await interaction.response.send_message(embed=embed)
                return

            total_income, total_expense, balance = finance.get_balance()

            embed = discord.Embed(
                title='💰 Balance Report',
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            embed.add_field(
                name='Total Income',
                value=f'Rp {total_income:,}',
                inline=True
            )
            embed.add_field(
                name='Total Expense',
                value=f'Rp {total_expense:,}',
                inline=True
            )
            embed.add_field(
                name='Balance',
                value=f'Rp {balance:,}',
                inline=False
            )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(
                f'❌ Error: {str(e)}',
                ephemeral=True
            )

    @app_commands.command(
        name='report',
        description='Show monthly financial report'
    )
    async def report(interaction: discord.Interaction) -> None:
        """Show the monthly financial report for the current month."""
        try:
            finance = get_finance_service()
            now = datetime.now()

            monthly_data = finance.get_monthly_report(now.year, now.month)

            embed = discord.Embed(
                title=f'📊 Monthly Report - {monthly_data["month_name"]}',
                color=discord.Color.gold(),
                timestamp=datetime.now()
            )
            embed.add_field(
                name='Income',
                value=f'Rp {monthly_data["income"]:,}',
                inline=True
            )
            embed.add_field(
                name='Expense',
                value=f'Rp {monthly_data["expense"]:,}',
                inline=True
            )
            embed.add_field(
                name='Net Profit',
                value=f'Rp {monthly_data["net_profit"]:,}',
                inline=False
            )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(
                f'❌ Error: {str(e)}',
                ephemeral=True
            )

    @app_commands.command(
        name='topuser',
        description='Show user with highest income'
    )
    async def topuser(interaction: discord.Interaction) -> None:
        """Show the user who contributed the most income."""
        try:
            finance = get_finance_service()

            top = finance.get_top_income_user()

            if top is None:
                embed = discord.Embed(
                    title='🏆 Top Income Contributor',
                    color=discord.Color.gold(),
                    description='No income recorded yet.'
                )
                await interaction.response.send_message(embed=embed)
                return

            embed = discord.Embed(
                title='🏆 Top Income Contributor',
                color=discord.Color.gold(),
                timestamp=datetime.now()
            )
            embed.add_field(
                name='User',
                value=top['user'],
                inline=True
            )
            embed.add_field(
                name='Total Income',
                value=f'Rp {top["amount"]:,}',
                inline=True
            )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(
                f'❌ Error: {str(e)}',
                ephemeral=True
            )

    @app_commands.command(
        name='recent',
        description='Show recent transactions'
    )
    @app_commands.describe(
        limit='Number of transactions to show (max 10)'
    )
    async def recent(
        interaction: discord.Interaction,
        limit: app_commands.Range[int, 1, 10] = 5
    ) -> None:
        """Show the most recent transactions."""
        try:
            sheets = get_sheets_service()

            recent_transactions = sheets.get_recent_transactions(limit)

            if not recent_transactions:
                embed = discord.Embed(
                    title='📋 Recent Transactions',
                    color=discord.Color.blue(),
                    description='No transactions recorded yet.'
                )
                await interaction.response.send_message(embed=embed)
                return

            embed = discord.Embed(
                title='📋 Recent Transactions',
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )

            for i, txn in enumerate(recent_transactions, 1):
                emoji = '💚' if txn['Type'] == 'Income' else '❤️'
                amount_str = f"Rp {txn['Amount']:,}"
                embed.add_field(
                    name=f'{i}. {emoji} {txn["Type"]}',
                    value=f'{amount_str} - {txn["Description"]}\n'
                          f'👤 {txn["User"]} | {txn["Tanggal"]}',
                    inline=False
                )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(
                f'❌ Error: {str(e)}',
                ephemeral=True
            )

    @app_commands.command(
        name='help',
        description='Show all available commands'
    )
    async def help_command(interaction: discord.Interaction) -> None:
        """Show help information about all commands."""
        embed = discord.Embed(
            title='📚 Finance Bot Commands',
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )

        commands_list = [
            ('/masuk', 'Record income', '!masuk 50000 desain logo'),
            ('/keluar', 'Record expense', '!keluar 25000 makan siang'),
            ('/balance', 'Check total balance', None),
            ('/report', 'Monthly financial report', None),
            ('/topuser', 'Top income contributor', None),
            ('/recent', 'Recent transactions', '!recent 5'),
            ('/pdf', 'Convert image to PDF', None),
        ]

        for cmd, desc, example in commands_list:
            value = desc
            if example:
                value += f'\nExample: `{example}`'
            embed.add_field(name=cmd, value=value, inline=False)

        embed.set_footer(
            text='Use / before each command | Cooldown: 3 seconds'
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name='pdf',
        description='Convert image to PDF'
    )
    @app_commands.describe(
        file='Image file to convert (.png, .jpg, .jpeg, .gif, .bmp, .webp)'
    )
    async def pdf_command(
        interaction: discord.Interaction,
        file: discord.Attachment
    ) -> None:
        """Convert an image to PDF."""
        try:
            ext = pathlib.Path(file.filename).suffix.lower()
            allowed_img = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')

            if ext not in allowed_img:
                await interaction.response.send_message(
                    '❌ File must be an image (.png, .jpg, .jpeg, .gif, .bmp, .webp)',
                    ephemeral=True
                )
                return

            await interaction.response.defer()

            import img2pdf
            file_bytes = await file.read()
            out_name = pathlib.Path(file.filename).stem + '.pdf'
            pdf_bytes = img2pdf.convert(file_bytes)

            await interaction.followup.send(
                file=discord.File(io.BytesIO(pdf_bytes), filename=out_name)
            )

        except Exception as e:
            await interaction.followup.send(
                f'❌ Error: {str(e)}',
                ephemeral=True
            )

    @app_commands.command(
        name='test-anniversary',
        description='Preview anniversary message (test only)'
    )
    async def test_anniversary(interaction: discord.Interaction) -> None:
        """Send anniversary preview to current channel."""
        await interaction.response.defer()

        images = sorted(config.ASSETS_DIR.iterdir())
        if not images:
            await interaction.followup.send("No images found.", ephemeral=True)
            return

        first = images[0]
        file = discord.File(first, filename="gallery.jpeg")
        view = GalleryView(images, title="🎉 Happy Anniversary ❤️", description=config.ANNIVERSARY_TEXT)
        embed = view._build_embed()
        await interaction.followup.send(file=file, embed=embed, view=view)

    bot.tree.add_command(masuk)
    bot.tree.add_command(keluar)
    bot.tree.add_command(balance)
    bot.tree.add_command(report)
    bot.tree.add_command(topuser)
    bot.tree.add_command(recent)
    bot.tree.add_command(help_command)
    bot.tree.add_command(pdf_command)
    bot.tree.add_command(test_anniversary)
