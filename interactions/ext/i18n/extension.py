try:
    from orjson import loads
except ImportError:
    from json import loads

from collections import defaultdict
from logging import getLogger
from os import PathLike
from pathlib import Path
from typing import Dict, List, Optional, Union

from interactions.client.context import _Context

from interactions import Client, Locale

from .json_generator import JSONGenerator
from .models import CommandLocalization
from .utils import add_command_localizations

__all__ = ("Localization",)

log = getLogger("i18n")


class Localization:
    def __init__(self, client: Client, default_language: Optional[Locale] = None):
        self.client: Client = client
        self.default_language: Locale = default_language

        self._commands_localizations: Dict[str, CommandLocalization] = defaultdict(
            CommandLocalization
        )
        self._custom_localizations: Dict[str, Dict[Union[Locale, str], str]] = defaultdict(dict)

        self._paths: List[Path] = []

    def load(self, path: Union[PathLike, str]):
        """
        Loads folder with localization

        :param Union[PathLike, str] path: The path to the folder with localization
        """
        self._load_file(Path(path))
        print(self._commands_localizations)
        add_command_localizations(self.client._commands, self._commands_localizations)

    def _load_file(self, path: Path):
        if not path.is_dir():
            raise ValueError("Path should be a directory")
        if path.name in [_.name for _ in self._paths]:
            raise RuntimeError("You already loaded directory with this localization!")

        for file in path.iterdir():
            file_name = file.name.removesuffix(".json")
            if file_name not in {"commands", "custom"}:
                continue

            locale_data = loads(file.read_text("utf-8"))
            if not locale_data:
                continue

            self._add_localization(path.name, file_name, locale_data)

        self._paths.append(path)

    def _add_localization(self, locale_name: str, type: str, locale_data: dict):  # noqa
        locale = Locale(locale_name) if locale_name != "default" else "default"
        self._process_localization(locale, locale_data)

        if type == "commands" and locale != "default":
            for command_name, command_data in locale_data.items():
                self._commands_localizations[command_name].add_localization(command_data)

        elif type == "custom":
            for key, value in locale_data.items():
                if previous := self._custom_localizations.get(key):
                    previous |= value
                else:
                    self._custom_localizations[key] = value

    def _process_localization(self, locale: Union[Locale, str], locale_data: dict):
        for key, value in locale_data.items():
            if isinstance(value, dict):
                self._process_localization(locale, value)
            elif value:
                locale_data[key] = {locale: value}

    def get(self, key: str) -> Optional[Dict[Union[Locale, str], str]]:
        """
        Gets dict with localized value.

        :param str key: The key to get value.
        """
        return self._custom_localizations.get(key.upper())

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
        return self._commands_localizations.get(command)

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

    def generate_files(self, locale: Locale, path: Path):
        """
        Generates files with empty string values for localization

        :param locale: The language
        :param path: The path to create files
        """
        JSONGenerator(
            path, self.client._commands, list(self._custom_localizations.keys())
        ).generate(
            locale
        )  # noqa
