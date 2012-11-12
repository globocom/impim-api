#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from optparse import OptionParser

import tornado.ioloop
from tornado.httpserver import HTTPServer

from impim_api.app import ImagesApplication


def main():
    parser = OptionParser()
    parser.add_option('-p', '--port', type=int, dest='port', default='8080',
                      help='Port to start the server with.')
    parser.add_option('-i', '--ip', dest='ip', default='0.0.0.0',
                      help='Host ip to start the server in.')
    parser.add_option('-l', '--log-level', dest='log_level', default="warning",
                      help = 'The log level to be used. Possible values are: ' \
                             'debug, info, warning, error, critical or notset.'\
                             '[default: warning].')
    parser.add_option('-c', '--conf', dest='conf', default=None,
                      help='Configuration file to use for the server.')
    parser.add_option('-d', '--debug', action='store_true', dest='debug', default=False,
                      help='Debug flag.')

    (opt, args) = parser.parse_args()

    logging.basicConfig(level=getattr(logging, opt.log_level.upper()))

    main_loop = tornado.ioloop.IOLoop.instance()

    application = ImagesApplication(
        conf_file=opt.conf,
        debug=opt.debug
    )

    server = HTTPServer(application)
    server.bind(opt.port, opt.ip)
    server.start(1)

    logging.info('-- Impim API started listening in %s:%d --' % (opt.ip,
        opt.port))
    try:
        main_loop.start()
    except KeyboardInterrupt:
        logging.info('')
        logging.info('-- Impim API closed by user interruption --')

if __name__ == '__main__':
    main()
