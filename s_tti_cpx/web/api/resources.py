#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw.api.rest import ModuleResource
from flask import jsonify
from flask_restful import reqparse
from entropyfw.common import get_utc_ts
from PicoController.common.definitions import THERMOCOUPLES, UNITS
from .logger import log
"""
resources
Created by otger on 18/04/17.
All rights reserved.
"""

# Connect
# Disconnect


class StartTempLoop(ModuleResource):
    url = 'start_temp_loop'
    description = "Configures tc08 to read and publish enabled channels every 'interval' seconds"

    def __init__(self, module):
        super(StartTempLoop, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('interval', type=float, required=True, location='json')

    def post(self):
        args = self.reqparse.parse_args()
        self.module.start_timer(args['interval'])

        return jsonify({'args': args,
                        'utc_ts': get_utc_ts(),
                        'result': 'done'})


class StopTempLoop(ModuleResource):
    url = 'stop_temp_loop'
    description = "Stop get temperature values loop"

    def __init__(self, module):
        super(StopTempLoop, self).__init__(module)

    def post(self):
        self.module.stop_timer()

        return jsonify({'utc_ts': get_utc_ts(),
                        'result': 'done'})


TC_TYPES = ('B', 'E', 'J', 'K', 'N', 'R', 'S', 'T')  # if modified, update web template
T_UNITS = ('Centigrade', 'Fahrenheit', 'Kelvin', 'Rankine')  # if modified, update web template


class EnableChannel(ModuleResource):
    url = 'enable_channel'
    description = "Enables a channel of TC08 with configured thermocouple type and units"

    def __init__(self, module):
        super(EnableChannel, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('channel', type=int, required=True, location='json')
        self.reqparse.add_argument('tc_type', type=str,
                                   choices=TC_TYPES,
                                   location='json')
        self.reqparse.add_argument('units', type=str,
                                   choices=T_UNITS,
                                   location='json')

    def post(self):
        args = self.reqparse.parse_args()

        tc_type = args.get('tc_type')
        if tc_type:
            tc_type = getattr(THERMOCOUPLES, tc_type.upper())

        units = args.get('units')
        if units:
            units = getattr(UNITS.TEMPERATURE, units.upper())
        try:
            self.module.enable(args['channel'], tc_type=tc_type, units=units)
        except Exception as ex:
            log.exception('Something went wrong when enabling module with arguments: {0}'.format(args))

        return jsonify({'args': args,
                        'utc_ts': get_utc_ts(),
                        'result': 'done'})


class DisableChannel(ModuleResource):
    url = 'disable_channel'
    description = "Disables a channel of TC08"

    def __init__(self, module):
        super(DisableChannel, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('channel', type=int, required=True, location='json')

    def post(self):
        args = self.reqparse.parse_args()

        self.module.disable(args['channel'])

        return jsonify({'args': args,
                        'utc_ts': get_utc_ts(),
                        'result': 'done'})


class ReadChannels(ModuleResource):
    url = 'read_channels'
    description = "Reads all enabled channels and return its read values"

    def get(self):
        return jsonify(self.module.tc.get_channels_values())


def get_api_resources():
    return [StartTempLoop, StopTempLoop, EnableChannel, DisableChannel, ReadChannels]
