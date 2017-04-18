#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw.api.rest import ModuleResource
from flask import jsonify
from flask_restful import reqparse
from entropyfw.common import get_utc_ts
from .logger import log
"""
resources
Created by otger on 18/04/17.
All rights reserved.
"""


class EnableOutput(ModuleResource):
    url = 'enable_output'
    description = "Enables an output of the power supply"

    def __init__(self, module):
        super(EnableOutput, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('output', type=int, required=True, location='json')

    def post(self):
        args = self.reqparse.parse_args()
        output = args['output']
        output_1 = output == 1
        output_2 = output == 2
        try:
            self.module.enable_output(output_1=output_1, output_2=output_2)
        except Exception as ex:
            log.exception('Something went wrong when enabling output with arguments: {0}'.format(args))

        return jsonify({'args': args,
                        'utc_ts': get_utc_ts(),
                        'result': 'done'})

def get_api_resources():
    return [EnableOutput]
