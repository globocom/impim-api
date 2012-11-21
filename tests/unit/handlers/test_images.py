#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from tapioca.request import ParamRequiredError
from unittest import TestCase

from impim_api.handlers.images import ImageCreationSchema


class ImageCreationSchemaTestCase(TestCase):

    def test_image_creation_schema(self):
        schema = ImageCreationSchema()
        event_date = datetime.now()
        values = {
            'title': u'title',
            'credits': u'credits',
            'tags': u'tag1, tag2',
            'event_date': event_date.isoformat()
        }

        validated_values = schema.validate_querystring(values=values)

        assert validated_values['title'] == u'title'
        assert isinstance(validated_values['title'], unicode)
        assert validated_values['credits'] == u'credits'
        assert isinstance(validated_values['credits'], unicode)
        assert validated_values['tags'] == [u'tag1', u'tag2']
        assert validated_values['event_date'] == event_date
