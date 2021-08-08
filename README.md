<div align="center">
    <div>
        <h1>SlashPaginator</h1>
        <span> <a href="https://pypi.org/project/discord-py-slash-command/"><img src="https://raw.githubusercontent.com/discord-py-slash-commands/discord-py-interactions/goverfl0w-new-readme/.github/banner_transparent.png" alt="discord-py-interactions" height="128"></a></span>
    </div>
    <div>
    </div>
    <div>
        <h3>Button paginator using discord-py-interactions</h3>
    </div>
</div>

## Welcome!
It's a very simple paginator for discord-py-interactions!

This project is open source ⭐.

## Install
```
pip install --upgrade SlashPaginator
```

# Example

```py
@slash.slash(name="example")
async def _example(ctx):
    embed1 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 1")
    embed2 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 2")
    embed3 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 3")
    paginator = SlashPaginator.AutoSlashEmbedPaginator(ctx)
    embeds = [embed1, embed2, embed3]
    await paginator.run(embeds)

```

The `AutoSlashEmbedPaginator` uses the lib's buttons to scroll.
If given only one page, it just acts as a glorified ctx.send(embed=embeds) message.

The `CustomAutoSlashPaginator` is a subclass of `AutoSlashEmbedPaginator` that lets you:
  - Customise what buttons you want to use, instead of the default.
  - Customize what functions the buttons should use instead.

The caveat with the custom object is that it requires learning about how to use components in the lib.
You may refer [here](https://discord-py-slash-command.readthedocs.io/en/latest/components.html#responding-to-interactions) to learn more.

## Custom example (Reimplementing AutoSlashEmbedPaginator without the freeze page button):

```py
class MyOwnPaginator(SlashPaginator.CustomAutoSlashPaginator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def button_1_action(self, button_ctx):
        """Seeks to the first page."""
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
    async def button_2_action(self, button_ctx):
        """Seeks to the previous page."""
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
    async def button_3_action(self, button_ctx):
        """Seeks to the next page."""
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
    async def button_4_action(self, button_ctx):
        """Seeks to the last page."""
        self.current_page = len(self.embeds) - 1
        if self.remove_reactions:
            try:
                await button_ctx.edit_origin(components=[])
            except:
                pass
        if self.auto_footer:
            self.embeds[len(self.embeds) - 1].set_footer(
                text=f"({self.current_page + 1}/{len(self.embeds)})"
            )
        await button_ctx.edit_origin(
            embed=self.embeds[len(self.embeds) - 1]
        )
        

@slash.slash(name="example")
async def _example(ctx):
    embed1 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 1")
    embed2 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 2")
    embed3 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 3")
    emojis = ["⏮️", "◀", "▶", "⏭️"]  # first page, prev page, next page, last page
    embeds = [embed1, embed2, embed3]
    paginator = MyOwnPaginator(ctx, control_emojis=emojis)
    
    await paginator.run(embeds)

```

## Custom Example #2
(Redoing the look of the buttons, but keep the functionality intact.)

```py
@slash.slash(name="example")
async def _example(ctx):
    embed1 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 1")
    embed2 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 2")
    embed3 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 3")
    emojis = ["⏮️", "◀", "⏹️", "▶", "⏭️"]  # first page, prev page, stop, next page, last page
    embeds = [embed1, embed2, embed3]
    paginator = SlashPaginator.CustomAutoSlashPaginator(ctx, control_emojis=emojis, default_run=True)
    
    await paginator.run(embeds)


```






## License
This project is under the MIT License.

## Contribute
Anyone can contribute to this by forking the repository, making a change, and create a pull request!

Make sure you run it under the black formatter first :)

## Credits to:

+ [decave27](https://github.com/decave27/ButtonPaginator/) for the README layout
+ [toxicrecker](https://github.com/toxicrecker/DiscordUtils) for the basis of this paginator
+ Everyone that maintains the [discord-py-interactions](https://github.com/discord-py-slash-commands/discord-py-interactions) lib.