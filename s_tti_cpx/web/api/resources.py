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


class Connect(ModuleResource):
    url = 'connect'
    description = "Connect to device"

    def __init__(self, module):
        super(Connect, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('ip', type=str, required=True, default=False, location='json')
        self.reqparse.add_argument('port', type=int, required=True, location='json')

    def post(self):
        args = self.reqparse.parse_args()
        ip = args['ip']
        port = args['port']
        try:
            self.module.connect(ip, port)
        except Exception as ex:
            log.exception('Something went wrong when connecting (arguments: {0})'.format(args))

        return jsonify({'args': args,
                        'utc_ts': get_utc_ts(),
                        'result': 'done'})


class Disconnect(ModuleResource):
    url = 'disconnect'
    description = "Connect to device"


    def post(self):
        try:
            self.module.disconnect()
        except Exception as ex:
            log.exception('Something went wrong when disconnecting')

        return jsonify({'utc_ts': get_utc_ts(),
                        'result': 'done'})


class EnableOutput(ModuleResource):
    url = 'enable_output'
    description = "Enables an output of the power supply"

    def __init__(self, module):
        super(EnableOutput, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('output_1', type=bool, required=False, default=False, location='json')
        self.reqparse.add_argument('output_2', type=bool, required=False, default=False, location='json')

    def post(self):
        args = self.reqparse.parse_args()
        output_1 = args['output_1']
        output_2 = args['output_2']
        try:
            self.module.enable_output(output_1=output_1, output_2=output_2)
        except Exception as ex:
            log.exception('Something went wrong when enabling output with arguments: {0}'.format(args))

        return jsonify({'args': args,
                        'utc_ts': get_utc_ts(),
                        'result': 'done'})


class DisableOutput(ModuleResource):
    url = 'disable_output'
    description = "Disable an output of the power supply"
    version = "0.1"

    def __init__(self, module):
        super(DisableOutput, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('output_1', type=bool, required=False, default=False, location='json')
        self.reqparse.add_argument('output_2', type=bool, required=False, default=False, location='json')

    def post(self):
        args = self.reqparse.parse_args()
        output_1 = args['output_1']
        output_2 = args['output_2']
        try:
            self.module.disable_output(output_1=output_1, output_2=output_2)
        except:
            log.exception('Exception on disable output callback')

        return jsonify({'args': args,
                        'utc_ts': get_utc_ts(),
                        'result': 'done'})


class UpdateI(ModuleResource):
    name = 'update_curr_limit'
    description = "update current limit of an output"
    version = "0.1"

    def __init__(self, module):
        super(UpdateI, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('output', type=int, required=True, location='json')
        self.reqparse.add_argument('current_limit', type=float, required=True, location='json')

    def post(self):
        args = self.reqparse.parse_args()
        output = args['output']
        amps = args['current_limit']
        self.module.set_current_limit(output=output, amps=amps)


class UpdateV(ModuleResource):
    name = 'update_voltage'
    description = "update voltage of an output"
    version = "0.1"

    def __init__(self, module):
        super(UpdateV, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('output', type=int, required=True, location='json')
        self.reqparse.add_argument('voltage', type=float, required=True, location='json')

    def post(self):
        args = self.reqparse.parse_args()
        output = args['output']
        volts = args['voltage']
        self.module.set_voltage(output=output, volts=volts)


class UpdateVI(ModuleResource):
    name = 'update_vi'
    description = "update applied voltage and current limit of an output"
    version = "0.1"

    def __init__(self, module):
        super(UpdateVI, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('output', type=int, required=True, location='json')
        self.reqparse.add_argument('current_limit', type=float, required=True, location='json')
        self.reqparse.add_argument('voltage', type=float, required=True, location='json')

    def post(self):
        args = self.reqparse.parse_args()
        output = args['output']
        volts = args['voltage']
        amps = args['current_limit']
        self.module.set_current_limit(output=output, amps=amps)
        self.module.set_voltage(output=output, volts=volts)


def get_api_resources():
    return [Connect, Disconnect, EnableOutput, DisableOutput, UpdateV, UpdateI, UpdateVI]
