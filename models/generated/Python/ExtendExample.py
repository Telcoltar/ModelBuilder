from Option import OptionNone, Option
from pydantic import BaseModel, constr, conint, confloat, AnyUrl, HttpUrl
from typing import Optional
from .Example import Example


class ExtendExample(Example):
    number_prop: confloat(le=5)
