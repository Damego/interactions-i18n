from typing import Dict, Optional

from interactions.utils.attrs_utils import DictSerializerMixin, define, field
from interactions.utils.missing import MISSING

from interactions import Locale

__all__ = ("OptionLocalization", "CommandLocalization")


@define()
class BaseLocalization(DictSerializerMixin):
    name: Optional[Dict[Locale, str]] = field(default=MISSING)
    description: Optional[Dict[Locale, str]] = field(default=MISSING)
    options: Dict[str, "OptionLocalization"] = field(default=MISSING)

    def __attrs_post_init__(self):
        if self.options is not MISSING:
            self.options = {key: OptionLocalization(**value) for key, value in self.options.items()}


@define()
class OptionLocalization(BaseLocalization):
    choices: Dict[str, Dict[Locale, str]] = field(default=MISSING)

    def add_localization(self, data: dict):
        for key, value in data.items():
            if key == "options":
                if self.options is MISSING:
                    self.options = {}
                for opt_name, opt_value in value.items():
                    if option := self.options.get(opt_name):
                        option.add_localization(opt_value)
                    else:
                        self.options[opt_name] = OptionLocalization(**opt_value)
            elif key == "choices":
                if self.choices is MISSING:
                    self.choices = {}
                for choice_name, choice_value in value.items():
                    if choice := self.choices.get(choice_name):
                        choice |= choice_value
                    else:
                        self.choices[choice_name] = choice_value
            else:
                _current = getattr(self, key)
                if _current is MISSING:
                    setattr(self, key, value)
                else:
                    _current |= value


@define()
class CommandLocalization(BaseLocalization):
    def add_localization(self, data: dict):
        for key, value in data.items():
            if key == "options":
                if self.options is MISSING:
                    self.options = {}
                for opt_name, opt_value in value.items():
                    if option := self.options.get(opt_name):
                        option.add_localization(opt_value)
                    else:
                        self.options[opt_name] = OptionLocalization(**opt_value)
            else:
                _current = getattr(self, key)
                if _current is MISSING:
                    setattr(self, key, value)
                else:
                    _current |= value
