# interactions-i18n
Add localization support to your interactions.py bot

## Installation

1. `pip uninstall discord-py-interactions`
2. `pip install git+https://github.com/interactions-py/library.git@4.4.0-beta.1`
3. `pip install --upgrade interactions-i18n`


## Usage

```py
import interactions
from interactions.ext.i18n import setup

client = interactions.Client(...)

# Load an i18n extension
i18n = setup(client)

...  # your cool commands and cogs loads

# Load a folder with localization
i18n.load("./locales/de")
client.start()
```

### Usage in Extension

```py
from interactions import Extension
from interactions.ext.i18n import Localization


class MyExt(Extension):
    def __init__(self, client):
        self.client = client

        self.i18n: Localization = self.client.i18n
```

## Creating localization files

1. Choose a language you want and find their code in the [Discord Locales Docs](https://discord.com/developers/docs/reference#locales)
2. Create a `[CODE]` folder with found code and put it in the folder with locales.
3. Create two files. First is `commands.json` for your commands and second is `custom.json` for anything you want

## Example

Let's create a command with name `info` with some subcommands

```py
@client.command()
async def info(ctx: interactions.CommandContext):
    ...

@info.group()
async def my_group(ctx: interactions.CommandContext):
    ...

@my_group.subcommand()
@interactions.option()
async def user(ctx: interactions.CommandContext, member: interactions.Member):
    loc = i18n.get_translate("some_key", ctx.locale)
    await ctx.send(loc)
```

### Structure of json files

`locales/de/commands.json`

This file will contain localizations for your commands

```json
{
    "info": { // command name
        "name": "...", // localized name
        "description": "...", // localized description
        "options": { // options of command. Command groups and subcommands are options btw
            "my_group": {
                "name": "...",
                "description": "...",
                "options": {
                    "user": {
                        "name": "...",
                        "description": "...",
                        "options": {
                            "member": {
                                "name": "...",
                                "description": "...",
                                // if your option have choices you can do:
                                "choices": {
                                    "choice_name": "..."
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

`locales/de/custom.json`

This file will contain your custom localizations for anything

```json
{
  "SOME_KEY": "Some value"
}
```

## Automatic file generation

It seems difficult to write every command in the json, so you can generate file with your commands.
You need to only fill empty strings with your language

```python
from interactions import Client, Locale
from interactions.ext.i18n import setup

bot = Client(...)
i18n = setup(bot)
# i18n.load("./locales/de")

...  # your cool commands

# call this function in the end of main file
i18n.generate_files(Locale.GERMAN, "./locales/")
# bot.start()  # comment line where starts your bot

```
