from typing import Optional, TypeVar, Generic

from pydantic import validator
from pydantic.generics import GenericModel

T = TypeVar("T")


class Option(GenericModel, Generic[T]):
    is_some: bool
    value: Optional[T]

    @validator("value", always=True)
    def check_consistency(cls, v, values):
        if v is None and values.get("is_some"):
            raise ValueError("value is None but is_some is true")
        if v is not None and not values.get("is_some"):
            raise ValueError("has value, bit is_some is false")
        return v

    def is_some(self):
        return self.is_some

    def unwrap(self):
        if not self.is_some:
            raise ValueError("Cant unwrap None value")

    def unwrap_or(self, default: T):
        if self.is_some:
            return self.value
        return default


OptionNone = Option(is_some=False)


def Some(value: T):
    if value is None:
        raise ValueError("value can't be None")
    return Option(value=value, is_some=True)
