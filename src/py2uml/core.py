"""
This requires to have the library (pkg) pre-installed.

Usage:
    $ python ./py2uml.py --pkg pandas
    $ python ./py2uml.py --pkg pandas --base-module pandas.core

"""
import inspect
import re
from itertools import filterfalse

CLS_TPL = """classDiagram

linkStyle default interpolate basis

{links}
"""

EXCLUDE_METH = [
    "_abc_",
    "__class__",
    "__delattr__",
    "__dict__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__gt__",
    "__hash__",
    "__init_subclass__",
    "__le__",
    "__lt__",
    "__module__",
    "__ne__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__setattr__",
    "__sizeof__",
    "__str__",
    "__subclasshook__",
    "__weakref__",
    "__abstractmethods__",
]


def class_name(cls):
    """Return a string representing the class"""
    # NOTE: can be changed to str(class) for more complete class info
    out = "%s.%s" % (cls.__module__, cls.__name__)
    return out


def classes_tree(module, base_module=None):

    if base_module is None:
        base_module = module.__name__

    module_classes = set()
    module_attrs = []
    inheritances = []

    def inspect_class(cls):

        if class_name(cls) not in module_classes:

            if cls.__module__.startswith(base_module):
                module_classes.add(class_name(cls))
                module_attrs.append(classes_attrs(cls))

                for base in cls.__bases__:
                    inheritances.append((class_name(base), class_name(cls)))
                    inspect_class(base)

    classes_list = [e for e in module.__dict__.values() if inspect.isclass(e)]

    for cls in classes_list:
        inspect_class(cls)

    return module_classes, inheritances, module_attrs


def get_attrs(module_classes, module_attrs):
    attrs_list = []
    for i, cls in enumerate(module_classes):
        mmd = ["%s: +%s" % (cls, attr) for attr in module_attrs[i]]
        attrs_list.append("\n".join(mmd))
    return attrs_list


def classes_tree_to_mermaid(module_classes, inheritances, module_attrs):
    attrs = get_attrs(module_classes, module_attrs)
    classes = list(module_classes)
    members = ["%s <|-- %s" % (a, b) for a, b in inheritances]
    out = CLS_TPL.format(links="\n".join(classes + members + attrs))
    return out


def classes_attrs(cls, exclude=EXCLUDE_METH):

    all_attr = dir(cls)

    def is_exclude(elem):
        for ex in exclude:
            if ex in elem:
                return True
        # return False

    def function_formatter(elem):
        if hasattr(getattr(cls, elem), "__call__"):
            return "%s()" % elem
        return elem

    out = filterfalse(is_exclude, all_attr)
    out = map(function_formatter, out)

    return list(out)


def remove_dots(mermaid_str):
    meth_regex = r"\.(\w)"

    def callback(pttn):
        return pttn.group(1).title()

    class_diagram_mod = re.sub(meth_regex, callback, mermaid_str)
    return class_diagram_mod


def cli():
    import argparse

    parse = argparse.ArgumentParser()
    parse.add_argument("--pkg", required=True)
    parse.add_argument("--base-module", default=None)
    parse.add_argument("--raw", action="store_true")
    args = parse.parse_args()

    _pkg = args.pkg
    base_module = args.base_module
    raw = args.raw

    pkg = __import__(_pkg)
    m_classes, inheritances, m_attrs = classes_tree(
            pkg, base_module=base_module
    )
    class_diagram = classes_tree_to_mermaid(m_classes, inheritances, m_attrs)

    if raw:
        print(class_diagram)
    else:
        print(remove_dots(class_diagram))
