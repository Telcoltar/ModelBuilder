from Option import OptionNone, Option
from pydantic import BaseModel, constr, conint, confloat, AnyUrl, HttpUrl
from typing import Optional
from datetime import datetime
from .ExampleSubType import ExampleSubType


class Example(BaseModel):
    string_prop: Optional[constr(min_length=5)] = ""
    string_optional_prop: Optional[str]
    int_with_mod_prop: Optional[conint(gt=10)]
    int_prop: int
    boolean_prop: bool
    option_string_prop: Option[str]
    url_prop: AnyUrl
    http_url_prop: HttpUrl
    float_prop: confloat(le=12)
    string_array_prop: list[str]
    int_array_1_prop: list[int]
    int_array_2_prop: list[int]
    complex_array: list[ExampleSubType]
    date_prop: datetime
    optional_complex_prop: Optional[ExampleSubType]
