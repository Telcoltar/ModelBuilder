from Option import OptionNone, Option
from pydantic import BaseModel, constr, conint


class Example(BaseModel):
    string_prop: constr(min_length=5) = ""
    int_prop: conint(gt=10)
    boolean_prop: bool
    option_string_prop: Option[str]
