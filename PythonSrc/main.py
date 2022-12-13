from PythonSrc.ModelParser.main import build_py, build_ts
from yaml import load, Loader
import os

for tmpl in os.listdir("../model_templates/"):
    with open(f"../model_templates/{tmpl}") as f:
        dict_repr = load(f.read(), Loader)
        build_ts(dict_repr, "../src/models/generated/", "templates")
        build_py(dict_repr, "models/generated/", "templates")
