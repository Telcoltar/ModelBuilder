from Option import OptionNone, Option
from pydantic import BaseModel, constr, conint, confloat


class Example(BaseModel):
    string_prop: constr(min_length=5) = ""
    int_with_mod_prop: conint(gt=10)
    int_prop: int
    boolean_prop: bool
    option_string_prop: Option[str]
