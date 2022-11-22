from typing import List, Union

from interactions.client.decor import command

from interactions import MISSING, Command, Option

from ..extension import Localization


def add_option_localizations(i18n: Localization, option: Option):
    key = option.name
    if locale_key := getattr(option, "locale_key", None):
        key = locale_key

    _name = i18n.get_name(key)
    _description = i18n.get_description(key)

    if _name:
        option.name_localizations = _name
        option._json["name_localizations"] = _name  # TODO: Remove this after asdict pr
    if _description:
        option.description_localizations = _description
        option._json[
            "description_localizations"
        ] = _description  # TODO: Remove this after asdict pr


@property
def full_data(self) -> Union[dict, List[dict]]:
    i18n: Localization = self.client.i18n  # type: ignore

    self.name_localizations = i18n.get_name(self.name)
    self.description_localizations = i18n.get_description(self.name)

    for option in self.options:
        add_option_localizations(i18n, option)
        if option.options:
            for _option in option.options:
                add_option_localizations(i18n, _option)
                if _option.options:
                    for __option in _option.options:
                        add_option_localizations(i18n, __option)

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


setattr(Command, "full_data", full_data)
