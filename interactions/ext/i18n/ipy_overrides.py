from typing import Awaitable, Callable, List, Optional, Union

from interactions.client.decor import command
from interactions.utils.attrs_utils import define, field

import interactions
from interactions import MISSING, Command
from interactions import option as _option

from .extension import Localization


def add_option_localizations(i18n: Localization, __option: interactions.Option):
    key = __option.name
    if locale_key := getattr(__option, "locale_key", None):
        key = locale_key

    _name = i18n._get_name(key)
    _description = i18n._get_description(key)

    if _name:
        __option.name_localizations = _name
        __option._json["name_localizations"] = _name  # TODO: Remove this after asdict pr
    if _description:
        __option.description_localizations = _description
        __option._json[
            "description_localizations"
        ] = _description  # TODO: Remove this after asdict pr


@property
def full_data(self) -> Union[dict, List[dict]]:
    i18n: Localization = self.client.i18n  # type: ignore

    self.name_localizations = i18n._get_name(self.name)
    self.description_localizations = i18n._get_description(self.name)

    for option in self.options:
        add_option_localizations(i18n, option)
        if option.options:
            for _option in option.options:  # noqa: F402
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


@define()
class Option(interactions.Option):
    locale_key: Optional[str] = field(default=None)


def option(
    description: str = "No description set",
    /,
    *,
    key: Optional[str] = None,
    **kwargs,
) -> Callable[[Callable[..., Awaitable]], Callable[..., Awaitable]]:
    def wrapper(coro: Callable[..., Awaitable]) -> Callable[..., Awaitable]:
        _coro = _option(description, **kwargs)(coro)

        # I'm getting AttributeError when trying to set attribute
        __option = Option(**_coro._options[0]._json)
        __option.locale_key = key
        _coro._options[0] = __option

        return _coro

    return wrapper


interactions.option = option
