#!/usr/bin/python
# -*- coding: utf-8 -*-


import dateutil.parser
import re


class ExtractArgumentsMixin(object):

    def extract_arguments(self, accepted_arguments):
        arguments = {}
        for argument_tuple in accepted_arguments:
            argument_key = argument_tuple[0]
            default = argument_tuple[2]
            argument_value = self._parse(self.get_argument(argument_key, default), argument_tuple[1])
            arguments[argument_key] = argument_value
        return arguments

    def _parse(self, argument, argument_type):
        if argument == None: return None
        if argument_type == 'datetime': return dateutil.parser.parse(argument)
        return argument_type(argument)
