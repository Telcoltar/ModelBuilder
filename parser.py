from typing import Optional, Union

from yaml import load, Loader
from jinja2 import FileSystemLoader, Environment, select_autoescape
from pathlib import Path

primitives = ["string", "number", "boolean", "integer", "int", "url", "HttpUrl"]


def parse_modifier_to_z_modifier(modifier: str, modifier_value: str):
    if modifier == "min":
        return f".min({int(modifier_value)})"
    if modifier == "max":
        return f".max({int(modifier_value)})"
    if modifier == "length":
        return f".length({int(modifier_value)})"
    if modifier == "uuid":
        return f".uuid()"
    if modifier == "starts_with":
        return f'.startsWith("{modifier_value}")'
    if modifier == "gt":
        return f".gt({modifier_value})"
    if modifier == "gte":
        return f".gte({modifier_value})"
    if modifier == "lt":
        return f".lt({modifier_value})"
    if modifier == "lte":
        return f".lte({modifier_value})"
    if modifier == "int":
        return f".int()"
    if modifier == "optional":
        return ".optional()"
    if modifier == "trim":
        return ".trim()"
    if modifier in ["url", "HttpUrl"]:
        return ".url()"
    if modifier == "array":
        return ".array()"


def get_z_type(input_type: str):
    if input_type == "string":
        return "z.string()"
    if input_type == "number":
        return "z.number()"
    if input_type == "boolean":
        return "z.boolean()"
    if input_type in ["int", "integer"]:
        return "z.number().int()"
    if input_type in ["url", "HttpUrl"]:
        return "z.string().url()"


def get_ts_primitive_type(input_type: str):
    if input_type == "string":
        return "string"
    if input_type == "number":
        return "number"
    if input_type == "boolean":
        return "boolean"
    if input_type in ["int", "integer"]:
        return "number"
    if input_type in ["url", "HttpUrl"]:
        return "string"


def get_primitive_py_type(input_type: str):
    if input_type == "string":
        return "str"
    if input_type == "number":
        return "float"
    if input_type == "boolean":
        return "bool"
    if input_type in ["integer", "int"]:
        return "int"
    if input_type == "url":
        return "AnyUrl"
    if input_type == "HttpUrl":
        return "HttpUrl"


def get_py_mod_type(input_type: str):
    if input_type == "string":
        return "constr"
    if input_type == "number":
        return "confloat"
    if input_type == "boolean":
        return "conbool"
    if input_type == "integer":
        return "conint"


def parse_modifier_to_py_modifier(modifier: str, modifier_value: str):
    if modifier == "min":
        return f"min_length={modifier_value}"
    if modifier == "max":
        return f"max_length={modifier_value}"
    if modifier == "gt":
        return f"gt={modifier_value}"
    if modifier == "gte":
        return f"ge={modifier_value}"
    if modifier == "lt":
        return f"lt={modifier_value}"
    if modifier == "lte":
        return f"le={modifier_value}"


def parse_modifiers_to_z_string(modifiers: dict[str, str]):
    current_z_string = ""
    for mod, mod_value in modifiers.items():
        current_z_string += parse_modifier_to_z_modifier(mod, mod_value)
    return current_z_string


def get_ts_boolean(input_boolean: bool):
    return "true" if input_boolean else "false"


def parse_ts_generic(current_z_string, current_class_dict, prop):
    generic_type = prop['generic']['type']
    current_class_dict["type"] = f"{prop['type']}<{generic_type}>"

    if generic_type not in primitives:
        current_class_dict["creation"] = lambda data: f"create{prop['type']}({data}, true, {generic_type})"
        current_z_string += f"{generic_type}Schema)"
    else:
        option_z_string = get_z_type(generic_type)
        if "modifiers" in prop["generic"]:
            option_z_string += parse_modifiers_to_z_string(prop["generic"]["modifiers"])
        current_z_string += f"create{prop['type']}Schema({option_z_string})"
        current_class_dict["creation"] = lambda data: f"create{prop['type']}({data}, false, {option_z_string})"
    return current_z_string, current_class_dict


def parse_ts_primitive(current_z_string, current_class_dict, prop):
    current_class_dict["type"] = get_ts_primitive_type(prop["type"])
    current_z_string += get_z_type(prop["type"])

    if "modifiers" in prop:
        modifiers = prop["modifiers"]
        current_z_string += parse_modifiers_to_z_string(modifiers)
    return current_z_string, current_class_dict


def parse_ts_complex(current_z_string, current_class_dict, prop):
    current_class_dict["type"] = prop["type"]
    current_z_string += f"{prop['type']}Schema"
    return current_z_string, current_class_dict


def build_ts(dict_repr, output_dir):
    z_properties = []
    class_properties = []
    classes_to_import = set()

    baseclass = dict_repr.get("baseclass")
    if baseclass is not None:
        classes_to_import.add(baseclass)

    for prop in dict_repr["properties"]:
        current_z_string = f"{prop['name']}: "
        current_class_dict: dict[str, Union[str, bool]] = {"name": prop['name']}

        if "optional" in prop:
            current_class_dict["optional"] = True
        else:
            current_class_dict["optional"] = False

        if "default" in prop:
            if prop["default"] == "":
                prop["default"] = '""'
            current_class_dict["default"] = prop["default"]

        current_class_dict["complex"] = False

        if prop["type"] in primitives:
            current_z_string, current_class_dict = parse_ts_primitive(current_z_string, current_class_dict, prop)
        elif "generic" in prop:
            current_class_dict["complex"] = True
            if prop["generic"]["type"] not in primitives:
                classes_to_import.add(prop['type'])
            current_z_string, current_class_dict = parse_ts_generic(current_z_string, current_class_dict, prop)
        else:
            classes_to_import.add(prop['type'])
            current_z_string, current_class_dict = parse_ts_complex(current_z_string, current_class_dict, prop)

        if "array" in prop:
            current_z_string += ".array()"
            current_class_dict["type"] += "[]"
        if "optional" in prop:
            current_z_string += ".optional()"

        z_properties.append(current_z_string)
        class_properties.append(current_class_dict)

    env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
    template = env.get_template("class.ts.jinja2")

    imports = [
        "import { " + f"{t}, {t}Schema" " } from " + f'"./{t}"' for t in classes_to_import
    ]

    with open(Path(output_dir).joinpath(f"{dict_repr['name']}.ts"), "w") as f:
        f.write(template.render(
            {
                "z_properties": z_properties,
                "class_properties": class_properties, "name": dict_repr["name"],
                "imports": imports,
                "baseclass": baseclass
            }
        ))


def build_py(dict_repr, output_dir):
    properties = []
    classes_to_import = set()

    baseclass = dict_repr.get("baseclass")
    if baseclass is not None:
        classes_to_import.add(baseclass)

    for prop in dict_repr["properties"]:
        current_property = f"{prop['name']}: "

        if "optional" in prop:
            current_property += "Optional["

        if "array" in prop:
            current_property += "list["

        if prop["type"] in primitives:
            if "modifiers" in prop:
                ignored_modifiers = ["int"]
                modifiers = [parse_modifier_to_py_modifier(mod, value)
                             for mod, value in prop['modifiers'].items() if mod not in ignored_modifiers]
                if "array" in prop["modifiers"]:
                    current_property += "list["
                if "int" in prop["modifiers"] or prop["type"] in ["int", "integer"]:
                    if len(modifiers) > 0:
                        current_property += f"conint({','.join(modifiers)})"
                    else:
                        current_property += "int"
                else:
                    current_property += f"{get_py_mod_type(prop['type'])}({','.join(modifiers)})"
                if "array" in prop["modifiers"]:
                    current_property += "]"
            else:
                current_property += get_primitive_py_type(prop["type"])

        elif "generic" in prop:
            current_property += f"{prop['type']}[{get_primitive_py_type(prop['generic']['type'])}]"
            if prop["generic"]["type"] not in primitives:
                classes_to_import.add(prop["generic"]["type"])
        else:
            classes_to_import.add(prop["type"])
            current_property += prop["type"]

        if "array" in prop:
            current_property += "]"

        if "optional" in prop:
            current_property += "]"

        if "default" in prop:
            current_property += f" = {prop['default']}"

        properties.append(current_property)

    imports = [
        f"from .{t} import {t}" for t in classes_to_import
    ]

    env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
    template = env.get_template("class.py.jinja2")
    with open(Path(output_dir).joinpath(f"{dict_repr['name']}.py"), "w") as f:
        f.write(template.render(
            {
                "name": dict_repr["name"],
                "properties": properties,
                "imports": imports,
                "baseclass": baseclass
            }
        ))
