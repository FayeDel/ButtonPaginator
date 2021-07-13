import asyncio
from typing import Union

import discord
from discord.ext import commands
from discord_slash import ComponentContext, SlashContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (
    create_actionrow,
    create_button,
    wait_for_component,
)


class AutoSlashEmbedPaginator(object):
    def __init__(self, ctx, **kwargs):
        self.embeds = None
        self.ctx: SlashContext = ctx
        self.bot: Union[
            discord.Client,
            discord.AutoShardedClient,
            commands.Bot,
            commands.AutoShardedBot,
        ] = ctx.bot
        self.current_page = 0
        self.auto_footer = kwargs.get("auto_footer", False)
        self.remove_reactions = kwargs.get("remove_reactions", False)
        self.control_emojis = ("⏪", "⬅", "🔐", "➡", "⏩")
        self.timeout = int(kwargs.get("timeout", 60))

    async def run(self, embeds, send_to=None):
        if not send_to:
            send_to = self.ctx
        wait_for = self.ctx.author if send_to == self.ctx else send_to

        def check(_button_ctx: ComponentContext):
            return _button_ctx.author == wait_for

        if not self.embeds:
            self.embeds = embeds
        if self.auto_footer:
            self.embeds[0].set_footer(
                text=f"({self.current_page + 1}/{len(self.embeds)})"
            )

        if len(self.control_emojis) > 5:  # because only one row.
            raise Exception("Because of Discord limitations, max emojis are 5.")
        buttons = [
            create_button(ButtonStyle.blue, emoji=emoji, custom_id=str(i))
            for i, emoji in enumerate(self.control_emojis)
        ]

        action_row = create_actionrow(*buttons)

        if len(self.embeds) > 1:
            msg = await send_to.send(embed=self.embeds[0], components=[action_row])
            while True:

                if self.timeout > 0:
                    try:
                        button_ctx: ComponentContext = await wait_for_component(
                            self.bot,
                            msg,
                            components=action_row,
                            check=check,
                            timeout=self.timeout,
                        )
                    except asyncio.TimeoutError:
                        await msg.edit(components=[])
                        break
                else:
                    button_ctx: ComponentContext = await wait_for_component(
                        self.bot, msg, check=check, components=action_row
                    )  # no timeout

                if button_ctx.custom_id == "0":
                    self.current_page = 0
                    if self.remove_reactions:
                        try:
                            await button_ctx.edit_origin(components=[])
                        except:
                            pass
                    if self.auto_footer:
                        self.embeds[0].set_footer(
                            text=f"({self.current_page + 1}/{len(self.embeds)})"
                        )
                    await button_ctx.edit_origin(embed=self.embeds[0])
                elif button_ctx.custom_id == "1":
                    self.current_page = self.current_page - 1
                    self.current_page = (
                        0 if self.current_page < 0 else self.current_page
                    )
                    if self.remove_reactions:
                        try:
                            await button_ctx.edit_origin(components=[])
                        except:
                            pass
                    if self.auto_footer:
                        self.embeds[self.current_page].set_footer(
                            text=f"({self.current_page + 1}/{len(self.embeds)})"
                        )
                    await button_ctx.edit_origin(embed=self.embeds[self.current_page])
                elif button_ctx.custom_id == "2":
                    self.current_page = 0
                    await button_ctx.edit_origin(components=[])
                    break
                elif button_ctx.custom_id == "3":
                    self.current_page = self.current_page + 1
                    self.current_page = (
                        len(self.embeds) - 1
                        if self.current_page > len(self.embeds) - 1
                        else self.current_page
                    )
                    if self.remove_reactions:
                        try:
                            await button_ctx.edit_origin(components=[])
                        except:
                            pass
                    if self.auto_footer:
                        self.embeds[self.current_page].set_footer(
                            text=f"({self.current_page + 1}/{len(self.embeds)})"
                        )
                    await button_ctx.edit_origin(embed=self.embeds[self.current_page])
                elif button_ctx.custom_id == "4":
                    self.current_page = len(self.embeds) - 1
                    if self.remove_reactions:
                        try:
                            await msg.edit(components=[])
                        except:
                            pass
                    if self.auto_footer:
                        self.embeds[len(self.embeds) - 1].set_footer(
                            text=f"({self.current_page + 1}/{len(self.embeds)})"
                        )
                    await button_ctx.edit_origin(
                        embed=self.embeds[len(self.embeds) - 1]
                    )
        else:
            await send_to.send(embed=self.embeds[0])  # There's no pages to scroll to.
