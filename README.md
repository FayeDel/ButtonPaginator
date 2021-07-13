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


## License
This project is under the MIT License.

## Contribute
Anyone can contribute to this by forking the repository, making a change, and create a pull request!

Make sure you run it under the black formatter first :)

## Credits to:

+ [decave27](https://github.com/decave27/ButtonPaginator/) for the README layout
+ [toxicrecker](https://github.com/toxicrecker/DiscordUtils) for the basis of this paginator
+ Everyone that maintains the [discord-py-interactions](https://github.com/discord-py-slash-commands/discord-py-interactions) lib.