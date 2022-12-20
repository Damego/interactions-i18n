from typing import Dict, List, Union

from interactions import Command, Option

from .models import CommandLocalization, OptionLocalization

__all__ = ("add_option_localization", "add_command_localizations")


def add_option_localization(
    options: List[Option], localization: Union[CommandLocalization, OptionLocalization]
):
    for option in options:
        if not (option_localization := localization.options.get(option.name)):
            continue
        option.name_localizations = option_localization.name
        option.description_localizations = option_localization.description

        if option.choices:
            for choice in option.choices:
                if choice_localization := localization.choices.get(choice.name):
                    choice.name_localizations = choice_localization

        if option.options:
            add_option_localization(option.options, option_localization)


def add_command_localizations(
    commands: List[Command], localizations: Dict[str, CommandLocalization]
):
    for command in commands:  # noqa
        command_localization = localizations.get(command.name)

        if command_localization is None:
            continue

        command.name_localizations = command_localization.name
        command.description_localizations = command_localization.description

        if command.options:
            add_option_localization(command.options, command_localization)
