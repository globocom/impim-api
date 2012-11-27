#!/usr/bin/env python
# -*- coding: utf-8 -*-


def import_class(name, get_module=False):
    module_name = get_module and name or '.'.join(name.split('.')[:-1])
    klass = name.split('.')[-1]

    module = get_module and __import__(name) or __import__(module_name)
    if '.' in module_name:
        module = reduce(getattr, module_name.split('.')[1:], module)

    return get_module and module or getattr(module, klass)
