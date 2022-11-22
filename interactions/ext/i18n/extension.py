import json
from logging import getLogger
from os import PathLike
from pathlib import Path
from typing import Dict, Optional

from interactions import MISSING, Client, Locale

__all__ = ("Localization",)

log = getLogger("i18n")


class Localization:
    def __init__(self, client: Client):
        self.client: Client = client
        self._locales: Dict[str, Dict[Locale, str]] = {}

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
        for key in list(locale_data.keys()):
            _data = {locale: locale_data.pop(key)}

            if key not in self._locales:
                self._locales[key] = {}
            self._locales[key] |= _data

    def _get_value(self, key: str) -> Optional[Dict[Locale, str]]:
        """
        Gets dict with localized value. Returns interactions.MISSING if not exists

        :param str key: The key to get value.
        :return: Dict with Locale as key and string as value
        """
        return self.locales.get(key, MISSING)

    def get(self, key: str) -> Optional[Dict[Locale, str]]:
        """
        Gets dict with localized value.

        :param str key: The key to get value.
        :return: Dict with Locale as key and string as value
        """
        return self.locales.get(key.upper())

    def get_name(self, key: str) -> Optional[Dict[Locale, str]]:
        """
        Gets dict with localized names to command/option name.

        :param str key: The key to get value.
        :return: Dict with Locale as key and string as value
        """
        _key: str = f"{key.upper()}_NAME"
        return self._get_value(_key)

    def get_description(self, key: str) -> Optional[Dict[Locale, str]]:
        """
        Gets dict with localized description to command/option name.

        :param str key: The key to get value.
        :return: Dict with Locale as key and string as value
        """
        _key: str = f"{key.upper()}_DESCRIPTION"
        return self._get_value(_key)
