#!/usr/bin/python
# -*- coding: utf-8 -*-


import dateutil.parser


class ExtractArgumentsMixin(object):

    def extract_arguments(self, accepted_arguments):
        arguments = {}
        for argument_tuple in accepted_arguments:
            argument_key = argument_tuple[0]
            argument_type = argument_tuple[1]
            default = self._default(argument_tuple)
            
            argument_value = self._parse(self.get_argument(argument_key, default), argument_type)
            arguments[argument_key] = argument_value
        return arguments

    def _default(self, argument_tuple):
        try:
            return argument_tuple[2]
        except IndexError:
            if argument_tuple[1] == 'list':
                return []
            return None

    def _parse(self, argument, argument_type):
        if argument == None or argument == []:
            return argument
        if argument_type == 'datetime':
            return dateutil.parser.parse(argument)
        if argument_type == 'list':
            return [a.strip() for a in argument.split(',')]
        return argument_type(argument)
