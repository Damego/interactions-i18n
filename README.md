# interactions-i18n
Add localization support to your interactions.py bot

## Installation

`pip install --upgrade interactions-i18n`

## Usage

```py
import interactions

client = interactions.Client(...)

# Load an i18n extension
i18n = client.load("interactions.ext.i18n")
# Load a folder with locales
# Also you can load json file only
i18n.load("./locales/")

...

client.start()
```

## Creating a locale file

1. Choose a language you want and find their code in the [Discord Locales Docs](https://discord.com/developers/docs/reference#locales)
2. Create a `[CODE].json` file with found code in the folder with locales.

## Getting and setting keys

Let's create a command with name `info` with some subcommands

```py
@client.command()
async def info(ctx: interactions.CommandContext):
    ...
    # Key for command name will be `INFO_NAME`
    # Key for command description will be `INFO_DESCRIPTION`


@info.group()
async def my_group(ctx: interactions.CommandContext):
    ...
    # Keys are `MY_GROUP_NAME` for name and `MY_GROUP_DESCRIPTION` for description


@my_group.subcommand()
@interactions.option(key="info_member_opt")  # `key` is optional. Keys for this option you can get from option name
async def user(ctx: interactions.CommandContext, member: interactions.Member):
    ...
    # Keys for subcommand are `USER_NAME` for name and `USER_DESCRIPTION` for description
    # Keys for option are `INFO_MEMBER_OPT_NAME` for name and `INFO_MEMBER_OPT_DESCRIPTION` for description
```

How will look our json file

`locales/de.json`

```json
{
  "INFO_NAME": "...",
  "INFO_DESCRIPTION": "...",
  "MY_GROUP_NAME": "...",
  "MY_GROUP_DESCRIPTION": "...",
  "MEMBER_NAME": "...",
  "MEMBER_DESCRIPTION": "...",
  "INFO_MEMBER_OPT_NAME": "...",
  "INFO_MEMBER_OPT_DESCRIPTION": "..."
}
```
