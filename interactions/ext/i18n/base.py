from typing import Optional

from interactions.ext.base import Base
from interactions.ext.version import Version, VersionAuthor

from interactions import Client, Locale

from .extension import Localization
from .ipy_overrides import override

__all__ = ("version", "base", "setup")

__version__ = "0.0.2"

version = Version(
    version=__version__, author=VersionAuthor(name="Damego", email="damego.dev@gmail.com")
)
base = Base(
    name="interactions-i18n",
    version=version,
    link="https://github.com/Damego/interactions-i18n",
    description="Add localization support to your interactions.py bot",
    packages=["interactions.ext.i18n"],
    requirements=["discord-py-interactions>=4.3.2"],
)


def setup(client: Client, default_language: Optional[Locale] = None):
    override()
    client.i18n = Localization(client, default_language)
    return client.i18n
