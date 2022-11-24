try:
    from orjson import loads
except ImportError:
    from json import loads

from collections import defaultdict
from logging import getLogger
from os import PathLike
from pathlib import Path
from typing import Dict, Optional, Union

from interactions.client.context import _Context

from interactions import Locale

from .localization import CommandLocalization

__all__ = ("Localization",)

log = getLogger("i18n")

# TODO:
#   Implement way to add/update json files


class Localization:
    def __init__(self):
        self._commands: Dict[str, CommandLocalization] = defaultdict(CommandLocalization)
        self._custom: Dict[str, Dict[Union[Locale, str], str]] = defaultdict(dict)

    def load(self, path: PathLike):
        """
        Loads file/files with localization

        :param PathLike path: The path to file or to folder
        """
        _path = Path(path)

        if not _path.is_dir():
            raise ValueError("Should be a folder")  # TODO: !

        for folder in _path.iterdir():
            for file in folder.iterdir():
                file_name = file.name.removesuffix(".json")
                if file_name not in {"commands", "custom"}:
                    continue  # TODO: raise an error

                locale_data = loads(file.read_text("utf-8"))
                if not locale_data:
                    continue

                self._add_localization(folder.name, file_name, locale_data)

    def _add_localization(self, locale_name: str, type: str, locale_data: dict):
        locale = Locale(locale_name) if locale_name != "default" else "default"
        self._process_localization(locale, locale_data)
        if type == "commands":
            for command_name, command_data in locale_data.items():
                self._commands[command_name].add_localization(command_data)

        elif type == "custom":
            for key, value in locale_data.items():
                if previous := self._custom.get(key):
                    previous |= value
                else:
                    self._custom[key] = value

    def _process_localization(self, locale: Union[Locale, str], locale_data: dict):
        for key, value in locale_data.items():
            if isinstance(value, dict):
                self._process_localization(locale, value)
            else:
                locale_data[key] = {locale: value}

    def get(self, key: str) -> Optional[Dict[Union[Locale, str], str]]:
        """
        Gets dict with localized value.

        :param str key: The key to get value.
        :return: Dict with Locale as key and string as value
        """
        return self._custom.get(key.upper())

    def get_translate(self, key: str, locale: Optional[Locale] = None):
        localized_value = self.get(key.upper())
        if localized_value is None:
            return

        if locale is None:
            return localized_value["default"]
        try:
            return localized_value[locale]
        except KeyError:
            return localized_value["default"]

    def get_command_localization(self, command: str) -> Optional[CommandLocalization]:
        return self._commands.get(command)

    # TODO: Remove these methods after 4.4.0 release

    @staticmethod
    def get_locale(ctx: _Context) -> Optional[Locale]:
        """
        Hack to get locale from ctx.

        :param ctx:
        :return:
        """
        if hasattr(ctx, "locale"):
            return ctx.locale

        _locale: str = ctx._extras.get("locale")
        return Locale(_locale) if _locale else None

    @staticmethod
    def get_guild_locale(ctx: _Context) -> Optional[Locale]:
        """
        Hack to get guild locale from ctx.

        :param ctx:
        :return:
        """
        if hasattr(ctx, "guild_locale"):
            return ctx.guild_locale

        _guild_locale: str = ctx._extras.get("guild_locale")
        return Locale(_guild_locale) if _guild_locale else None
