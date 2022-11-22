from typing import Awaitable, Callable, Optional

from interactions.utils.attrs_utils import define, field

import interactions
from interactions import Option as _Option
from interactions import option as _option


@define()
class Option(_Option):
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
