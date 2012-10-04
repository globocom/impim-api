#!/usr/bin/python
# -*- coding: utf-8 -*-


import dateutil.parser
import re


class BaseHandlerMixin(object):
    
    def extract_arguments(self, accepted_arguments):
        arguments = {}
        for argument_tuple in accepted_arguments:
            argument_key = argument_tuple[0]
            default = argument_tuple[2]
            argument_value = self._parse(self.get_argument(argument_key, default), argument_tuple[1])
            arguments[self._to_underscore(argument_key)] = argument_value
        return arguments
    
    def _to_underscore(self, string):
        return re.sub(r'([A-Z]){1}', lambda match: '_' + match.group(1).lower(), string)

    def _parse(self, argument, argument_type):
        if argument == None: return None
        if argument_type == 'datetime': return dateutil.parser.parse(argument)
        return argument_type(argument)
