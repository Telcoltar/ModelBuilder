from Option import OptionNone, Option
from pydantic import BaseModel, constr, conint, confloat, AnyUrl, HttpUrl
from typing import Optional


class Example(BaseModel):
    string_prop: Optional[constr(min_length=5)] = ""
    int_with_mod_prop: Optional[conint(gt=10)]
    int_prop: int
    boolean_prop: bool
    option_string_prop: Option[str]
    url_prop: AnyUrl
    http_url_prop: HttpUrl
    float_prop: confloat(le=12)
