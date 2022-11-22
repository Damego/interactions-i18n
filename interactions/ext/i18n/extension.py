import json
from collections import defaultdict
from logging import getLogger
from os import PathLike
from pathlib import Path
from typing import Dict, Optional

from interactions.client.context import _Context

from interactions import MISSING, Client, Locale

__all__ = ("Localization",)

log = getLogger("i18n")

# TODO:
#   Implement way to add/update json files


class Localization:
    def __init__(self, client: Client):
        self.client: Client = client
        self._locales: Dict[str, Dict[Locale, str]] = defaultdict(dict)

    @property
    def locales(self) -> Dict[str, Dict[Locale, str]]:
        """
        Returns dict of loaded localizations
        """
        return self._locales

    def load(self, path: PathLike):
        """
        Loads file/files with localization

        :param PathLike path: The path to file or to folder
        """
        _path = Path(path)

        if _path.is_file():
            locale_data = self.__load_file(_path)
            if not locale_data:
                return
            self.__load_localization(_path, locale_data)

        for file in _path.iterdir():
            locale_data = self.__load_file(file)
            if not locale_data:
                continue

            self.__load_localization(file, locale_data)

    def __load_file(self, file: Path) -> Optional[dict]:
        """
        Serializes file into dict
        """
        if file.suffix != ".json":
            log.debug(f"File {file} is not json format. Skipping...")
            return

        with open(file, "r", encoding="utf-8") as _file:
            try:
                return json.load(_file)
            except json.JSONDecodeError:
                log.exception(f"Couldn't load file {file}!")

    def __load_localization(self, file: Path, locale_data: dict):
        """
        Serializes dict to locale dict
        """
        locale = Locale(file.name.removesuffix(".json"))
        for key, value in locale_data.items():
            self._locales[key] |= {locale: value}

    def get(self, key: str) -> Optional[Dict[Locale, str]]:
        """
        Gets dict with localized value.

        :param str key: The key to get value.
        :return: Dict with Locale as key and string as value
        """
        return self.locales.get(key.upper())

    def get_translate(self, locale: Locale, key: str) -> Optional[str]:
        """
        Gets a translation from locale code and key.

        :param Locale locale: The locale code.
        :param str key: The key to get localization
        :return: localized string, if any.
        """

        _localizations: Dict[Locale, str] = self.get(key)
        return _localizations.get(locale) if _localizations else None

    def _get_name(self, key: str) -> Optional[Dict[Locale, str]]:
        """
        Gets dict with localized names to command/option name.

        :param str key: The key to get value.
        :return: Dict with Locale as key and string as value
        """
        _key: str = f"{key}_NAME"
        value = self.get(_key)
        return value if value is not None else MISSING

    def _get_description(self, key: str) -> Optional[Dict[Locale, str]]:
        """
        Gets dict with localized description to command/option name.

        :param str key: The key to get value.
        :return: Dict with Locale as key and string as value
        """
        _key: str = f"{key}_DESCRIPTION"
        value = self.get(_key)
        return value if value is not None else MISSING

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

        _locale = ctx._extras.get("locale")
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

        _guild_locale = ctx._extras.get("guild_locale")
        return Locale(_guild_locale) if _guild_locale else None
