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
        buttons_no_front = [
            create_button(
                ButtonStyle.blue, emoji=emoji, custom_id=str(i), disabled=i in range(2)
            )
            for i, emoji in enumerate(self.control_emojis)
        ]

        buttons_no_back = [
            create_button(
                ButtonStyle.blue,
                emoji=emoji,
                custom_id=str(i),
                disabled=i in range(3, 5),
            )
            for i, emoji in enumerate(self.control_emojis)
        ]
        _nofront = create_actionrow(
            *buttons_no_front
        )  # "default", first 2 buttons disabled
        _noback = create_actionrow(*buttons_no_back)  # last 2 buttons disabled

        action_row = create_actionrow(*buttons)  # no buttons disabled.

        if len(self.embeds) > 1:
            len_components = _nofront
            msg = await send_to.send(embed=self.embeds[0], components=[len_components])
            while True:

                if self.timeout > 0:
                    try:
                        button_ctx: ComponentContext = await wait_for_component(
                            self.bot,
                            msg,
                            components=len_components,
                            check=check,
                            timeout=self.timeout,
                        )
                    except asyncio.TimeoutError:
                        await msg.edit(components=[])
                        break
                else:
                    button_ctx: ComponentContext = await wait_for_component(
                        self.bot, msg, check=check, components=len_components
                    )  # no timeout

                if button_ctx.custom_id == "0":  # First page of iterator.
                    self.current_page = 0
                    if self.remove_reactions:
                        try:
                            await button_ctx.edit_origin(components=[])
                        except:
                            pass
                        else:
                            if self.auto_footer:
                                self.embeds[0].set_footer(
                                    text=f"({self.current_page + 1}/{len(self.embeds)})"
                                )
                            len_components = _nofront
                            await button_ctx.edit_origin(
                                embed=self.embeds[0], components=len_components
                            )
                elif button_ctx.custom_id == "1":  # page prior
                    self.current_page = self.current_page - 1
                    self.current_page = (
                        0 if self.current_page < 0 else self.current_page
                    )
                    if self.remove_reactions:
                        try:
                            await button_ctx.edit_origin(components=[])
                        except:
                            pass
                        else:
                            if self.auto_footer:
                                self.embeds[self.current_page].set_footer(
                                    text=f"({self.current_page + 1}/{len(self.embeds)})"
                                )
                            len_components = (
                                action_row if self.current_page != 0 else _nofront
                            )  # Every button is on if the page is not on the first.
                            await button_ctx.edit_origin(
                                embed=self.embeds[self.current_page],
                                components=len_components,
                            )
                elif button_ctx.custom_id == "2":  # Locks.
                    self.current_page = 0
                    await button_ctx.edit_origin(components=[])
                    break
                elif button_ctx.custom_id == "3":  # seeks page after.
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
                        else:
                            if self.auto_footer:
                                self.embeds[self.current_page].set_footer(
                                    text=f"({self.current_page + 1}/{len(self.embeds)})"
                                )
                            len_components = (
                                action_row
                                if self.current_page != len(self.embeds) - 1
                                else _noback
                            )  # Every button is on if the page is not on the last.
                            await button_ctx.edit_origin(
                                embed=self.embeds[self.current_page],
                                components=len_components,
                            )
                elif button_ctx.custom_id == "4":  # seeks last page.
                    self.current_page = len(self.embeds) - 1
                    if self.remove_reactions:
                        try:
                            await button_ctx.edit_origin(components=[])
                        except:
                            pass
                        else:
                            if self.auto_footer:
                                self.embeds[len(self.embeds) - 1].set_footer(
                                    text=f"({self.current_page + 1}/{len(self.embeds)})"
                                )
                            len_components = _noback
                            await button_ctx.edit_origin(
                                embed=self.embeds[len(self.embeds) - 1],
                                components=len_components,
                            )
        else:
            await send_to.send(embed=self.embeds[0])  # There's no pages to scroll to.


class CustomAutoSlashPaginator(AutoSlashEmbedPaginator):
    """
    A subclass of AutoSlashEmbedPaginator that lets you choose what emojis you want.

    To use this object,you **must** override the button actions, to customise which actions
    that you want to pick per emoji. With that said, you will have to implement stopping the
    Pagination loop if you set the timeout kwarg to 0.
    """

    def __init__(self, ctx, control_emojis, default_run: bool = False, **kwargs):
        super().__init__(ctx, **kwargs)
        self.control_emojis = control_emojis
        self.default_run = default_run

    # In the original paginator, the IDs go from 0 to 4.
    # In function implementation, the function nomenclature follows 1 through 5, per user implementation.
    # (and easier to use)

    async def button_1_action(self, button_ctx: ComponentContext):
        """The function that's called when button "0" is clicked"""
        raise NotImplementedError

    async def button_2_action(self, button_ctx: ComponentContext):
        """The function that's called when button "1" is clicked"""
        raise NotImplementedError

    async def button_3_action(self, button_ctx: ComponentContext):
        """The function that's called when button "2" is clicked"""
        raise NotImplementedError

    async def button_4_action(self, button_ctx: ComponentContext):
        """The function that's called when button "3" is clicked"""
        raise NotImplementedError

    async def button_5_action(self, button_ctx: ComponentContext):
        """The function that's called when button "4" is clicked"""
        raise NotImplementedError

    async def run(self, embeds, send_to=None):
        if self.default_run:
            return await super().run(embeds, send_to)

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
                    await self.button_1_action(button_ctx)
                elif button_ctx.custom_id == "1":
                    await self.button_2_action(button_ctx)
                elif button_ctx.custom_id == "2":
                    await self.button_3_action(button_ctx)
                elif button_ctx.custom_id == "3":
                    await self.button_4_action(button_ctx)
                elif button_ctx.custom_id == "4":
                    await self.button_5_action(button_ctx)
        else:
            await send_to.send(embed=self.embeds[0])  # There's no pages to scroll to.
