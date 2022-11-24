try:
    from orjson import dumps
except ImportError:
    from json import dumps

from os import PathLike
from pathlib import Path
from typing import List, Union

from interactions import Command, Locale, Option


class JSONGenerator:
    def __init__(self, path: PathLike, commands: List[Command], custom: List[str]):
        self._path = Path(path)
        self._commands: List[Command] = commands
        self._custom: List[str] = custom

    def _get_json(self, command_or_option: Union[Command, Option]) -> dict:
        json = {
            "name": "",
            "description": "",
        }
        if command_or_option.options:
            json["options"] = {
                option.name: self._get_json(option) for option in command_or_option.options
            }
        if isinstance(command_or_option, Option) and command_or_option.choices:
            json["choices"] = {choice.name: "" for choice in command_or_option.choices}

        return json

    def generate(self, locale: Locale):
        commands_data = {}

        for command in self._commands:
            print(f"Generating `{command.name}`...")
            commands_data[command.name] = self._get_json(command)

        custom_data = {key: "" for key in self._custom}

        self._make_file(locale.value, commands_data, custom_data)

    def _make_file(self, folder_name: str, commands_data: dict, custom_data: dict):
        folder = self._path / folder_name
        folder.mkdir(exist_ok=True)

        commands_file = folder / "commands.json"
        commands_file.write_text(dumps(commands_data).decode("utf-8"))

        if custom_data:
            custom_file = folder / "custom.json"
            custom_file.write_text(dumps(custom_data).decode("utf-8"))
