#!/usr/bin/python
# -*- coding: utf-8 -*-


import re


class BaseHandlerMixin(object):
    
    def extract_arguments(self, accepted_arguments):
        arguments = {}
        for argument_tuple in accepted_arguments:
            argument = argument_tuple[0]
            default = argument_tuple[1]
            arguments[self._to_underscore(argument)] = self.get_argument(argument, default)
        return arguments
    
    def _to_underscore(self, string):
        return re.sub(r'([A-Z]){1}', lambda match: '_' + match.group(1).lower(), string)
