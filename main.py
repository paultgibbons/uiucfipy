#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# TODO
# - week 4 - least squares
#
import os
import numpy as np
import json

import webapp2
import jinja2

from fi import get_info, get_correlation_matrix
from stock import Stock
from predict import predict_change
# from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               extensions=['jinja2.ext.autoescape'],
                               autoescape=True)


class BaseHandler(webapp2.RequestHandler):
    def render(self, template_page, **template_values):
        template = jinja_env.get_template(template_page)
        self.response.write(template.render(template_values))


class MainHandler(BaseHandler):
    """
    Primary page = loads with default no information
    """
    def get(self):
        self.render('index.html')


class InfoHandler(BaseHandler):
    """
    Class returning json for desired data
    """
    def get(self):
        data = self.request.get('symbols').split(',')
        query = [str(word) for word in data]

        stocks = get_info(query)
        symbols = [s.symbol for s in stocks]
        matrix = get_correlation_matrix(stocks).tolist()

        self.response.headers['Content-Type'] = 'application/json'
        response = {
            'query': query,
            'symbols': symbols,
            'stocks': [s.__dict__ for s in stocks],
            'matrix': matrix
        }
        self.response.out.write(json.dumps(response))


class PredictHandler(BaseHandler):
    """
    Returns json giving prediction and actual for desired symbol
    """
    def get(self):
        symbol = self.request.get('symbol')
        data = predict_change(symbol)
        [guess, actual] = data
        response = {
            'guess_buy': (1 if guess > 0 else -1),
            'hit': (1 if actual*guess > 0 else -1),
            'guess': guess,
            'actual': actual
        }
        self.response.out.write(json.dumps(response))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/get_info', InfoHandler),
    ('/predict', PredictHandler)
], debug=True)
