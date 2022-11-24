from typing import List, Union

from interactions.client.decor import command

from interactions import MISSING, Command, Option

from .extension import Localization
from .localization import CommandLocalization, OptionLocalization


def _command(self: Command):
    return command(
        type=self.type,
        name=self.name,
        description=self.description if self.type == 1 else MISSING,
        options=self.options if self.type == 1 else MISSING,
        scope=self.scope,
        name_localizations=self.name_localizations,
        description_localizations=self.description_localizations,
        default_member_permissions=self.default_member_permissions,
        dm_permission=self.dm_permission,
    )


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
            add_option_localization(option.options, localization.options[option.name])


def override():
    @property
    def full_data(self: Command) -> Union[dict, List[dict]]:
        i18n: Localization = self.client.i18n  # type: ignore
        command_localization: CommandLocalization = i18n.get_command_localization(self.name)

        if command_localization is None:
            return _command(self)

        self.name_localizations = command_localization.name
        self.description_localizations = command_localization.description

        if self.options:
            add_option_localization(self.options, command_localization)

        return _command(self)

    setattr(Command, "full_data", full_data)
