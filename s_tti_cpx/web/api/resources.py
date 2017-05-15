#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw.api.rest import ModuleResource, REST_STATUS
from flask_restful import reqparse
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
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex), args=args)
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=None, args=args)


class Disconnect(ModuleResource):
    url = 'disconnect'
    description = "Connect to device"


    def post(self):
        try:
            self.module.disconnect()
        except Exception as ex:
            log.exception('Something went wrong when disconnecting')
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex))
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=None)


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
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex), args=args)
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=None, args=args)


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
        except Exception as ex:
            log.exception('Exception on disable output callback')
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex), args=args)
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=None, args=args)


class StartPubLoop(ModuleResource):
    url = 'start_status_loop'
    description = "Start a loop to publish tti cpx status periodically"
    version = "0.1"

    def __init__(self, module):
        super(StartPubLoop, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('interval', type=int, required=True, location='json')

    def post(self):
        args = self.reqparse.parse_args()
        interval = args['interval']

        try:
            self.module.start_timer(interval=interval)
        except Exception as ex:
            log.exception('Exception when starting status publication loop')
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex), args=args)
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=None, args=args)


class StopPubLoop(ModuleResource):
    url = 'stop_status_loop'
    description = "Start a loop to publish tti cpx status periodically"
    version = "0.1"

    def post(self):
        try:
            self.module.stop_timer()
        except Exception as ex:
            log.exception('Exception when stopping status publication loop')
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex))
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=None)


class UpdateI(ModuleResource):
    url = 'update_curr_limit'
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
        try:
            self.module.set_current_limit(output=output, amps=amps)
        except Exception as ex:
            log.exception('Exception while setting current limit')
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex), args=args)
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=None, args=args)


class UpdateV(ModuleResource):
    url = 'update_voltage'
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
        try:
            self.module.set_voltage(output=output, volts=volts)
        except Exception as ex:
            log.exception('Exception while setting voltage')
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex), args=args)
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=None, args=args)


class UpdateVI(ModuleResource):
    url = 'update_vi'
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
        try:
            self.module.set_current_limit(output=output, amps=amps)
            self.module.set_voltage(output=output, volts=volts)
        except Exception as ex:
            log.exception('Exception while setting current limit and voltage')
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex), args=args)
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=None, args=args)


class Status(ModuleResource):
    url = 'get_status'
    description = "Status of power supply outputs"

    def __init__(self, module):
        super(Status, self).__init__(module)

    def post(self):
        outputs = {}
        try:
            outputs['output_1'] = self.module.get_output(1)
            outputs['output_2'] = self.module.get_output(2)
        except Exception as ex:
            log.exception('Something went wrong when receiving output status')
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex))
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=None)


def get_api_resources():
    return [Connect, Disconnect, EnableOutput, DisableOutput, UpdateV, UpdateI, UpdateVI, StartPubLoop, StopPubLoop, Status]
