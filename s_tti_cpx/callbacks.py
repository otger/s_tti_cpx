#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Callback
from .logger import log

"""
callbacks
Created by otger on 23/03/17.
All rights reserved.
"""


class EnableOutput(Callback):
    name = 'enable_output'
    description = "enable an output of the power supply"
    version = "0.1"

    def functionality(self):
        output = getattr(self.event.value, 'output', None)
        if output is None:
            log.warning("UpdateOutput has not valid output value")
            return
        try:
            self.module.enable_output(output_1=(output == 1), output_2=(output == 2))
        except:
            log.exception('Exception on enable output callback')


class UpdateI(Callback):
    name = 'updatei'
    description = "update applied current to thermoelectric"
    version = "0.1"

    def functionality(self):
        i = getattr(self.event.value, self.module.i_keyword, None)
        if i is None:
            log.warning("Updatei Callback event has no valid I value")
            return
        self.module.update_values(i=i)


class UpdateVI(Callback):
    name = 'updatevi'
    description = "update applied current and voltage to thermoelectric"
    version = "0.1"

    def functionality(self):
        i = getattr(self.event.value, self.module.i_keyword, None)
        v = getattr(self.event.value, self.module.v_keyword, None)
        if i is None or v is None:
            logger.log.warning("Updatevi Callback event has no valid I or V value")
        self.module.update_values(i=i, v=v)


