# make.py from Strictdom by Ben Golightly

# This file itself is donated to the public domain, but the data it works on
# - and its output! - is copyright - see COPYING.md

import itertools
import json
import keyword
import textwrap

from util import *
from pathlib import Path


VERSION="1"
srcdir=Path("../html5spec/spec-json/")
destdir=Path("strictdom")


with (srcdir / "elements.json").open("r") as fp:
    g_elements = json.load(fp)

with (srcdir / "attributes.json").open("r") as fp:
    g_attributes = json.load(fp)

with (srcdir / "element-types.json").open("r") as fp:
    g_element_types = json.load(fp)


# Special options for pretty formatting
special_element_inline = ["br", "wbr"]
special_element_no_pretty = ["script", "style", "pre"]

# Translate names to avoid collisions with keywords
special_element_names = set(keyword.kwlist)


def docstring(x):
    """Format a string as a docstring with one indent"""
    if len(x) < 68:
        return "    \"\"\"%s\"\"\"\n" % x

    wx = textwrap.fill(x, width=75, initial_indent="    ", subsequent_indent="    ")
    return "    \"\"\"\n%s\n    \"\"\"\n" % wx


def get_attribute(element, attribute):
    attr = g_attributes.get(attribute)
    if not attr: return None
    if (element in attr["elements"]) or ("HTML" in attr["elements"]):
        return attr
    else:
        next_attribute = attr.get("next")
        if not next_attribute:
            return None
        return get_attribute(element, next_attribute)


def get_attributes(element, attribute_names):
    for attribute in attribute_names:
        if attribute == "aria":
            attr = {"value_type": None}
        elif attribute == "custom":
            attr = {"value_type": None}
        elif attribute == "events":
            attr = {"value_type": None}
        else:
            attr = get_attribute(element, attribute)

        if attr:
            attr["name"] = attribute
            yield attr
        else:
            print("Warning: missing attribute %s for element %s" % (repr(attribute), repr(element)))


def fmt_attribute_param(arg):
    """Formats an attribute as a single parameter definition for a function
       definition, e.g. for `__init__(...)` format a parameter such as
       `href: Optional[str] = None."""

    attr, last = arg
    k, v = attr["name"], attr
    orig_k = k
    cmt = ""
    value_type = v["value_type"]

    comma = "" if last else ","

    k = k.replace("-", "_") # http-equiv -> http_equiv
    if k in keyword.kwlist:
        k = k + "_" # e.g. del -> del_
        cmt = " # %s is a keyword" % repr(orig_k)

    if k == "aria":
        t = "Optional[Aria]"
        cmt = " # `aria-*` attributes"
    elif k == "custom":
        t = "Optional[Mapping[str, str]]"
        cmt = " # Custom `data-*` attributes"
    elif k == "events":
        t = "Optional[Events]"
        cmt = " # `on*` event attributes"
    elif value_type == "Boolean attribute":
        t = "Optional[bool]"
    elif value_type == "Keywords":
        t = "Optional[Literal["+(", ".join(map(repr, v["value_keywords"])))+"]]"
    else:
        t = "Optional[str]"

    lpad = (18 - len(k)) * ' '

    return "        %s: %s%s = None%s%s" % (k, lpad, t, comma, cmt)



def fmt_attribute_assign(arg):
    """Creates a dict assignment for a non-None keyword attribute"""

    attr, last = arg
    k, v = attr["name"], attr
    orig_k = k
    cmt = ""
    value_type = v["value_type"]

    comma = "" if last else ","

    k = k.replace("-", "_") # http-equiv -> http_equiv
    if k in keyword.kwlist:
        k = k + "_" # e.g. del -> del_

    kd = k # Dominate version of key
    if k == "class_":
        kd = "cls"
    elif k == "for_":
        kd = "html_for"
    elif k.endswith("_"):
        kd = "_" + k[:-1]

    if k == "aria":
        return "if aria is not None: optional.update({'aria-'+k: v for k, v in aria.kwargs.items()})"
    elif k == "custom":
        return "if custom is not None: optional.update({'data-'+k: v for k, v in custom.items()})"
    elif k == "events":
        return "if events is not None: optional.update({'on'+k: v for k, v in events.kwargs.items()})"
    else:
        return "if %s is not None: optional[%s] = %s" % (k, repr(kd), k)


with Path("COPYING.md").open("w") as fp:
    fp.write("""\
COPYING Strictdom
================================================================================

Strictdom is by Ben Golightly (`ben@tawesoft.co.uk`) at Tawesoft Ltd
(`www.tawesoft.co.uk`) and also incorporates intellectual property from the
following sources:

""")

    # Write out copyright notice from JSON embedded __META__
    for i in g_elements["__META__"]["copyright"]:
        for j in textwrap.wrap(i, width=78):
            fp.write("%s\n" % j)
        fp.write("\n")
    fp.write("""\
Redistribution of Strictdom is permitted only in simultaneous accordance with
the above licenses, namely attribution to all authors under the Creative
Commons Attribution 4.0 International License, and attribution to all authors
under the W3C Document License and any additional terms specified.

Strictdom is available from `https://github.com/tawesoft/strictdom` and
`https://www.tawesoft.co.uk/products/open-source-software`. Strictdom also
relies on `https://github.com/tawesoft/html5spec.json` to download
and extract a machine-readable spec.

Strictdom is a wrapper around Dominate, available from
`https://github.com/Knio/dominate` and licensed under the
GNU Lesser General Public License v3.0: see
`https://raw.githubusercontent.com/Knio/dominate/master/LICENSE.txt`
""")


with (destdir / ("tags_" + VERSION + ".py")).open("w") as fp:

    # Write out copyright notice from JSON embedded __META__
    for i in g_elements["__META__"]["copyright"]:
        for j in textwrap.wrap(i, width=77):
            fp.write("# %s\n" % j)
        fp.write("#\n")

    fp.write("""\
# This file generated by free software by Tawesoft Ltd and/or contributor(s)
# available from `https://github.com/tawesoft` or
# `https://www.tawesoft.co.uk/products/open-source-software`
#
# This implementation of the above specifications is frozen as \
`tags_"""+VERSION+"""`.
# Only backwards-compatible changes to this file will be made.


import dominate
from enum import Enum
from typing import Mapping, Optional, Tuple, Union
from typing_extensions import Literal


class Aria:
    \"""
    Holder for all `aria-*` attribute arguments. May be typechecked in future.

    e.g. `button(aria=Aria(pressed="false"))`
    \"""
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class Events:
    \"""
    Holder for all `on*` event attribute arguments. May be typechecked in
    future.

    e.g. `button(events=Events(click="alert('Hello world');"))`
    \"""
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class ElementType(Enum):
    normal_elements = 0
    foreign_elements = 1
""")
    for i, element_type in enumerate(g_element_types):
        fp.write("    %s = %d\n" % (element_type.replace("-", "_"), i+2))

    fp.write("\n\n")

    # write out a class definition for each element
    for element, value in sorted(g_elements.items()):
        name = element

        # filter out "__META__", etc.
        if element.startswith("__"):
            continue

        # avoid keyword collisions
        if element in special_element_names:
            name = element + "_"
        else:
            name = element

        # Some elements, like <embed>, support any attribute. Others support
        # attributes from another spec e.g. SVG or MathML.
        any_kwargs = ("any" in value["attributes"]) \
            or any(attr.startswith("per [") for attr in value["attributes"])

        desc = value.get("desc")

        fp.write("class %s(dominate.tags.html_tag):\n" % name)
        fp.write(docstring(desc))

        # Get the "kind" of element, defaulting to normal, and normalise it
        # to an ElementType Enum value.
        kind="normal_elements"
        for element_type, elements in g_element_types.items():
            if element in elements:
                kind = element_type.replace("-", "_")
        is_single = (kind == "void_elements")

        fp.write("    name=%s\n" % repr(element))
        fp.write("    kind=ElementType.%s\n" % kind.replace("-", "_"))
        
        if is_single:
            fp.write("    is_single=True\n")
        if element in special_element_no_pretty:
            fp.write("    is_pretty=False\n")
        if element in special_element_inline:
            fp.write("    is_inline=True\n")

        fp.write("\n")

        special = ["aria", "custom", "events"] # special
        attributes = list(get_attributes(element, sorted(value["attributes"] + special)))

        fp.write("    def __init__(self,\n")

        if is_single:
            fp.write("        *args: None, # this is a void element\n")
        else:
            fp.write("        *args,\n")

        fp.write("\n".join(map(fmt_attribute_param, list_lastitems(attributes))))
        if any_kwargs:
            fp.write("\n        , **kwargs # any extra attributes")

        fp.write("\n    ) -> None:\n")
        fp.write("        optional = {}\n        ")
        fp.write("\n        ".join(map(fmt_attribute_assign, list_lastitems(attributes))))

        if any_kwargs:
            fp.write("""
        assert not (set(kwargs) & set(optional)) # collisions
        optional.update(kwargs)
""")

        if is_single:
            fp.write("\n        super().__init__(**optional)")
            fp.write("\n        assert args is None")
        else:
            fp.write("\n        super().__init__(*args, **optional)")

        fp.write("\n\n")












