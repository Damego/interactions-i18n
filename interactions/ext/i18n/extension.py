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

from interactions import Client, Locale

from .json_generator import JSONGenerator
from .models import CommandLocalization

__all__ = ("Localization",)

log = getLogger("i18n")


class Localization:
    def __init__(self, client: Client, default_language: Optional[Locale] = None):
        self.client: Client = client
        self.default_language: Locale = default_language

        self._commands: Dict[str, CommandLocalization] = defaultdict(CommandLocalization)
        self._custom: Dict[str, Dict[Union[Locale, str], str]] = defaultdict(dict)

        self._path: Path = None

    def load(self, path: PathLike):
        """
        Loads file/files with localization

        :param PathLike path: The path to file or to folder
        """
        if self._path:
            raise RuntimeError("You already loaded directory with localizations!")

        _path = Path(path)

        if not _path.is_dir():
            raise ValueError("Path should be a directory")

        self._path = _path

        for folder in _path.iterdir():
            for file in folder.iterdir():
                file_name = file.name.removesuffix(".json")
                if file_name not in {"commands", "custom"}:
                    continue

                locale_data = loads(file.read_text("utf-8"))
                if not locale_data:
                    continue

                self._add_localization(folder.name, file_name, locale_data)

    def _add_localization(self, locale_name: str, type: str, locale_data: dict):  # noqa
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
        """
        return self._custom.get(key.upper())

    def get_translate(self, key: str, locale: Optional[Locale] = None) -> Optional[str]:
        """
        Returns localized value for given key and locale.

        :param str key: The key to lookup
        :param Optional[Locale] locale: The language to lookup.
        """
        localized_value = self.get(key.upper())
        if localized_value is None:
            return

        if locale is None:
            return localized_value.get(self.default_language)

        try:
            return localized_value[locale]
        except KeyError:
            return localized_value.get(self.default_language)

    def get_command_localization(self, command: str) -> Optional[CommandLocalization]:
        """
        Returns localization data for command.

        :param str command: The name of command.
        """
        return self._commands.get(command)

    # TODO: Remove these methods after 4.4.0 release

    @staticmethod
    def get_locale(ctx: _Context) -> Optional[Locale]:
        """
        Hack to get locale from ctx.

        :param _Context ctx: The context from command or component callback
        :return: The user's selected language.
        """
        if hasattr(ctx, "locale"):
            return ctx.locale

        _locale: str = ctx._extras.get("locale")  # noqa
        return Locale(_locale) if _locale else None

    @staticmethod
    def get_guild_locale(ctx: _Context) -> Optional[Locale]:
        """
        Hack to get guild locale from ctx.

        :param _Context ctx: The context from command or component callback
        :return: The guild's preferred language.
        """
        if hasattr(ctx, "guild_locale"):
            return ctx.guild_locale

        _guild_locale: str = ctx._extras.get("guild_locale")  # noqa
        return Locale(_guild_locale) if _guild_locale else None

    def generate_files(self, locale: Locale, path: Optional[str] = None):
        """
        Generates files with empty string values for localization

        :param locale: The language
        :param path: The path to create files
        """
        JSONGenerator(
            path or self._path, self.client._commands, list(self._custom.keys())
        ).generate(
            locale
        )  # noqa
