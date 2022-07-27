import json
import logging
import pathlib
from collections import OrderedDict
from typing import Any, Dict

import yaml

logger = logging.getLogger(__name__)


class OASParser:
    @staticmethod
    def gettype(type):
        if type == "float":
            return "number"
        for i in ["string", "boolean", "integer"]:
            if type in i:
                return i
        return None

    @staticmethod
    def parse(json_data):
        d: Dict[str, Any] = {}
        if type(json_data) is dict:
            d["type"] = "object"
            d["properties"] = {}
            for k in json_data:
                c = OASParser.parse(json_data[k])
                if not c:
                    logger.warning(f"🚨 parsing type failed for key:{k}")
                    continue
                d["properties"][k] = c
            return d
        elif type(json_data) is list:
            if not json_data:
                return None
            d["type"] = "array"
            d["items"] = OASParser.parse(json_data[0])
            return d
        else:
            t = OASParser.gettype(type(json_data).__name__)
            if not t:
                return None
            d["type"] = t
            if d["type"] == "number":
                d["format"] = "float"
            return d


def make_ordered(d) -> Dict[str, Any]:
    if not isinstance(d, dict):
        return d
    keyorder = ["type", "properties", "items"]
    ordered = OrderedDict(
        sorted(
            d.items(),
            key=lambda i: keyorder.index(i[0]) if i[0] in keyorder else -1,
        )
    )
    r = dict(ordered)
    for k in r:
        r[k] = make_ordered(r[k])
    return r


def main():
    with open(pathlib.Path("input.json")) as f:
        data = json.load(f)

    parsed = OASParser.parse(data)
    ordered = make_ordered(parsed)
    yaml_str = yaml.dump(dict(ordered), sort_keys=False)

    dest = pathlib.Path("oas.yml")
    with open(dest, "w") as f:
        f.write(yaml_str)

    print("=" * 40)
    print(yaml_str)
    print("=" * 40)
    print(f"👉 check out {dest.absolute()}")


if __name__ == "__main__":
    main()
