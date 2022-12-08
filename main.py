from parser import build_py, build_ts
from yaml import load, Loader
import os

for tmpl in os.listdir("models/templates/"):
    with open(f"models/templates/{tmpl}") as f:
        dict_repr = load(f.read(), Loader)
        build_ts(dict_repr, "models/generated/TS")
        build_py(dict_repr, "models/generated/Python")
