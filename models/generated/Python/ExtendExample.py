from Option import OptionNone, Option
from pydantic import BaseModel, constr, conint, confloat
from Example import Example


class ExtendExample(Example):
    number_prop: confloat(le=5)
