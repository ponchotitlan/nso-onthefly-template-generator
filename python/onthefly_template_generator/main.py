# -*- mode: python; python-indent: 4 -*-
__author__ = "Alfonso Sandoval,Cesar Alves"
__version__ = "2.1.0"
__maintainer__ = "Alfonso Sandoval,Cesar Alves"
__status__ = "Release"

import ncs
from .ops_modules import *
from .data_modules import DeviceResources,XMLTemplateName,Result,ActionOutput
from ncs.dp import Action

class OnTheFlyTemplateGeneratorAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output, trans):
        self.log.info('action name: ', name)
        m = ncs.maapi.Maapi()
        with ncs.maapi.Session(m, 'admin', name):
            CREATE_DUMMY_DEVICE_RESULT  : ActionOutput
            PARSE_RESULT : ActionOutput
            PUSH_DP_RESULT : ActionOutput
            my_device_resources = DeviceResources(input)
            #Creation of dummy device in CDB
            CREATE_DUMMY_DEVICE_RESULT = create_dummy_device(
                self.log,
                m,
                my_device_resources.dummy_device_name,
                my_device_resources.ned_id
            )
            if CREATE_DUMMY_DEVICE_RESULT.result == Result.Failed:
                output.result = Result.Failed.value
                output.info = CREATE_DUMMY_DEVICE_RESULT.info
                return
            #Native configuration parsing
            PARSE_RESULT = device_load_native_config(
                self.log,
                m,
                my_device_resources.dummy_device_name,
                my_device_resources.native_configuration
            )
            if PARSE_RESULT.result == Result.Failed:
                flush_dummy_device(
                    self.log,
                    m,
                    my_device_resources.dummy_device_name
                )
                output.result = Result.Failed.value
                output.info = PARSE_RESULT.info
                return
            #Creation of the device template in CDB
            PUSH_DP_RESULT = push_device_template(
                self.log,
                m,
                XMLTemplateName.DeviceTemplateXML.value,
                my_device_resources.deviceTemplate,
                my_device_resources.ned_id,
                PARSE_RESULT.info
            )
            if PUSH_DP_RESULT.result == Result.Failed:
                flush_dummy_device(
                    self.log,
                    m,
                    my_device_resources.dummy_device_name
                )
                output.result = Result.Failed.value
                output.info = PUSH_DP_RESULT.info
                return
            #Dummy device is deleted from CDB
            flush_dummy_device(
                self.log,
                m,
                my_device_resources.dummy_device_name
            )
            #Success creation reporting into the action
            output.result = Result.Success.value
            output.info = PUSH_DP_RESULT.info

class Main(ncs.application.Application):
    def setup(self):
        self.log.info('Main RUNNING')
        self.register_action('onthefly-template-generator-action', OnTheFlyTemplateGeneratorAction)

    def teardown(self):
         self.log.info('Main FINISHED')