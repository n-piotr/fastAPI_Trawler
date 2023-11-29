from typing import Annotated
from re import compile

from annotated_types import Predicate

__all__ = [
    "IsIdentifierStr",
    "IsAlphaStr",
    "PasswordStr",
    "SlugStr"
]


PASSWORD_PATTERN = compile(pattern=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,64}$")
SLUG_PATTERN = compile(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

IsIdentifierStr = Annotated[
    str,
    Predicate(func=str.isidentifier),
    Predicate(func=str.isascii)
]
IsAlphaStr = Annotated[
    str,
    Predicate(func=str.isalpha)
]
PasswordStr = Annotated[
    str,
    Predicate(
        func=lambda x: bool(PASSWORD_PATTERN.fullmatch(string=x))
    )
]
SlugStr = Annotated[
    str,
    Predicate(
        func=lambda x: bool(SLUG_PATTERN.fullmatch(string=x))
    )
]
