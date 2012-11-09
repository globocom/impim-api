#!/usr/bin/env python
# -*- coding: utf-8 -*-


import mimetypes
import urllib

from tornado.httpclient import AsyncHTTPClient as TornadoAsyncHTTPClient


class AsyncHTTPClient(object):
    
    def __init__(self, test_case):
        self._test_case = test_case
        self._http_client = getattr(self._test_case, 'http_client', TornadoAsyncHTTPClient(self._test_case.io_loop))
    
    def get(self, path, **querystring):
        url = self._test_case.get_url(path)
        if querystring:
            url = "%s?%s" % (url, urllib.urlencode(querystring))
        return self._fetch(url, 'GET')
    
    def post(self, url, data):
        return self._fetch(url, 'POST', body=data)
    
    def multipart_post(self, url, fields, files):
        content_type, body = self._encode_multipart_formdata(fields, files)
        return self._fetch(url, 'POST', body=body, headers={'Content-Type': content_type})
    
    def put(self, url, data):
        return self._fetch(url, 'PUT', body=data)
    
    def delete(self, url):
        return self._fetch(url, 'DELETE')
    
    def _fetch(self, url, method, **kwargs):
        self._http_client.fetch(url, self._test_case.stop, method=method, **kwargs)
        return self._test_case.wait()

    def _encode_multipart_formdata(self, fields, files):
        boundary = '----------ThIs_Is_tHe_bouNdaRY_$'
        crlf = '\r\n'
        lines = []
        for (key, value) in fields:
            lines.append('--' + boundary)
            lines.append('Content-Disposition: form-data; name="%s"' % key)
            lines.append('')
            lines.append(value.encode('utf-8'))
        for (key, filename, value) in files:
            lines.append('--' + boundary)
            lines.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            lines.append('Content-Type: %s' % self._get_content_type(filename))
            lines.append('')
            lines.append(value)
        lines.append('--' + boundary + '--')
        lines.append('')
        body = crlf.join(lines)
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return content_type, body

    def _get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
