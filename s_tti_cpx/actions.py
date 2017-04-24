#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
actions
Created by otger on 19/04/17.
All rights reserved.
"""

from entropyfw import Action
from .logger import log


class TTiCPXAction(Action):
    name = 'gen_action'
    description = "Generic callback"
    version = "0.1"

    def get_output(self):
        output = self.get_arg('output')
        if output is None:
            log.error("{} request has no valid 'output' value".format(self.__class__.__name__))
            raise Exception()
        return output

    def get_curr_limit(self):
        curr_lim = self.get_arg('current_limit')
        if curr_lim is None:
            log.error("{} request has no valid 'current_limit' value".format(self.__class__.__name__))
            raise Exception()
        return curr_lim

    def get_voltage(self):
        volts = self.get_arg('voltage')
        if volts is None:
            log.error("{} request has no valid 'voltage' value".format(self.__class__.__name__))
            raise Exception()
        return volts

    def functionality(self):
        pass


class EnableOutput(TTiCPXAction):
    name = 'enable_output'
    arguments = [('output', int)]
    description = "Enable an output of the power supply"
    version = "0.1"

    def functionality(self):
        output = self.get_output()
        try:
            self.module.enable_output(output_1=(output == 1), output_2=(output == 2))
            self.module.pub_status(output)
        except:
            log.exception('Exception on enable output callback')
            raise


class DisableOutput(TTiCPXAction):
    name = 'disable_output'
    arguments = [('output', int)]
    description = "Disable an output of the power supply"
    version = "0.1"

    def functionality(self):
        output = self.get_output()
        try:
            self.module.disable_output(output_1=(output == 1), output_2=(output == 2))
            self.module.pub_status(output)
        except:
            log.exception('Exception on disable output callback')
            raise


class UpdateI(TTiCPXAction):
    name = 'update_curr_limit'
    arguments = [('output', int), ('current_limit', float)]
    description = "update current limit of an output"
    version = "0.1"

    def functionality(self):
        output = self.get_output()
        amps = self.get_curr_limit()
        self.module.set_current_limit(output=output, amps=amps)
        self.module.pub_status(output)


class UpdateV(TTiCPXAction):
    name = 'update_voltage'
    arguments = [('output', int), ('voltage', float)]
    description = "update voltage of an output"
    version = "0.1"

    def functionality(self):
        output = self.get_output()
        volts = self.get_voltage()
        self.module.set_voltage(output=output, volts=volts)
        self.module.pub_status(output)


class UpdateVI(TTiCPXAction):
    name = 'update_vi'
    arguments = [('output', int), ('voltage', float), ('current_limit', float)]
    description = "update applied voltage and current limit of an output"
    version = "0.1"

    def functionality(self):
        log.debug('Updating V and I by request from {}'.format(self.request.source))
        output = self.get_output()
        volts = self.get_voltage()
        amps = self.get_curr_limit()
        self.module.set_current_limit(output=output, amps=amps)
        self.module.set_voltage(output=output, volts=volts)
        self.module.pub_status(output)


class Connect(TTiCPXAction):
    name = 'connect'
    arguments = [('output', int), ('voltage', float), ('current_limit', float)]
    description = "update applied voltage and current limit of an output"
    version = "0.1"

    def functionality(self):
        output = self.get_output()
        volts = self.get_voltage()
        amps = self.get_curr_limit()
        self.module.set_current_limit(output=output, amps=amps)
        self.module.set_voltage(output=output, volts=volts)
        self.module.pub_status(output)
