#!/usr/bin/env python
# -*- coding: utf-8 -*-


import copy
import dateutil.parser
from json import dumps, loads
from urllib import urlencode

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest

from .base import MetadataStorage
from impim_api.infrastructure.encoder import JsonDatetimeSerializer


class ElasticSearch(MetadataStorage):

    def __init__(self, config, http_client=AsyncHTTPClient()):
        self._http_client = http_client
        self._elastic_search_urls = Urls(config=config)
        self._elastic_search_parser = Parser()
        self._json_encoder = JsonDatetimeSerializer(camel_case_transform=False)

    @gen.engine
    def search(self, callback, **search_arguments):
        elastic_search_request = self._build_search_request(**search_arguments)
        elastic_search_response = yield gen.Task(self._http_client.fetch, elastic_search_request)
        images_dict = self._elastic_search_parser.parse_images_from_search(elastic_search_response.body)
        callback(images_dict)

    @gen.engine
    def fetch_meta_data(self, callback, image_id):
        url = self._elastic_search_urls.document_url(Urls.IMAGE_TYPE, image_id)
        elastic_search_response = yield gen.Task(self._http_client.fetch, url, method='GET')
        image_dict = self._elastic_search_parser.parse_image_from_document(elastic_search_response.body)
        callback(image_dict)

    @gen.engine
    def store_meta_data(self, callback, image_id, **meta_data):
        url = self._elastic_search_urls.document_url(Urls.IMAGE_TYPE, image_id)
        yield gen.Task(self._http_client.fetch, url, method='PUT', body=self._json_encoder.encode(meta_data))
        callback()

    def _build_search_request(self, **search_arguments):
        url = self._elastic_search_urls.search_url(Urls.IMAGE_TYPE)

        search_request_body = SearchRequestBody()
        search_request_body.from_index((search_arguments.get('page') - 1) * search_arguments.get('page_size'))
        search_request_body.size(search_arguments.get('page_size'))
        if search_arguments.get('q'):
            search_request_body.query_string(search_arguments.get('q'))
        if search_arguments.get('created_date_from'):
            search_request_body.range('created_date').gte(search_arguments.get('created_date_from').isoformat())
        if search_arguments.get('created_date_to'):
            search_request_body.range('created_date').lte(search_arguments.get('created_date_to').isoformat())
        if search_arguments.get('event_date_from'):
            search_request_body.range('event_date').gte(search_arguments.get('event_date_from').isoformat())
        if search_arguments.get('event_date_to'):
            search_request_body.range('event_date').lte(search_arguments.get('event_date_to').isoformat())
        search_request_body.sort([{'_score': 'desc'}, {'created_date': {'order': 'desc', 'ignore_unmapped': True}}])

        return HTTPRequest(url, body=search_request_body.as_json(), allow_nonstandard_methods=True)


class Parser(object):

    def parse_image_from_document(self, es_json):
        es_data = loads(es_json)

        if self._index_does_not_exist(es_data) or self._document_does_not_exist(es_data):
            return None

        parsed_image = {'id': es_data['_id']}
        parsed_image.update(self._parse_source(es_data['_source']))

        return parsed_image

    def parse_images_from_search(self, es_json):
        es_data = loads(es_json)

        total = 0
        images = []
        if self._index_exists(es_data):
            total = es_data['hits']['total']
            for hit in es_data['hits']['hits']:
                parsed_image = {'id': hit['_id']}
                parsed_image.update(self._parse_source(hit['_source']))
                images.append(parsed_image)

        return {
            'total': total,
            'items': images,
        }

    def _parse_source(self, source):
        date_fields = ['created_date', 'event_date']
        parsed_source = copy.copy(source)
        for key in source:
            if key in date_fields:
                parsed_source[key] = dateutil.parser.parse(parsed_source[key])
        return parsed_source

    def _index_exists(self, es_data):
        return not self._index_does_not_exist(es_data)

    def _index_does_not_exist(self, es_data):
        return es_data.get('status') == 404

    def _document_does_not_exist(self, es_data):
        return not es_data.get('exists')


class SearchRequestBody(object):

    def __init__(self):
        self._body_dict = {}
        self._ranges = {}

    def from_index(self, from_argument):
        self._body_dict['from'] = from_argument

    def size(self, size_argument):
        self._body_dict['size'] = size_argument

    def query_string(self, query_argument):
        self._initialize_query()
        self._body_dict['query']['bool']['must'].append({'query_string': {'query': query_argument}})

    def range(self, range_argument):
        self._initialize_query()

        if not self._ranges.get(range_argument):
            self._ranges[range_argument] = self.Range(range_argument)
            self._body_dict['query']['bool']['must'].append({'range': {range_argument: self._ranges[range_argument].range_dict}})

        return self._ranges[range_argument]

    def sort(self, sort_argument):
        self._body_dict['sort'] = sort_argument

    def as_json(self):
        return dumps(self._body_dict)

    def _initialize_query(self):
        if not self._body_dict.get('query'):
            self._body_dict['query'] = {'bool': {'must': []}}


    class Range(object):

        def __init__(self, range_argument):
            self._range_argument = range_argument
            self.range_dict = {}

        def gte(self, gte_argument):
            self.range_dict['gte'] = gte_argument
            return self

        def lte(self, lte_argument):
            self.range_dict['lte'] = lte_argument
            return self


class Urls(object):

    IMAGE_TYPE = 'image'

    def __init__(self, config):
        self._config = config

    def index_url(self):
        return '%s/%s' % (self._config.ELASTIC_SEARCH_BASE_URL, self._config.ELASTIC_SEARCH_INDEX)

    def type_url(self, document_type):
        return '%s/%s' % (self.index_url(), document_type)

    def document_url(self, document_type, image_id):
        return '%s/%s' % (self.type_url(document_type), image_id)

    def search_url(self, document_type, **kwargs):
        query_string = urlencode(kwargs)
        if query_string:
            query_string = '?%s' % query_string
        return self.type_url(document_type) + '/_search%s' % query_string

    def refresh_url(self):
        return "%s/_refresh" % self.index_url()
