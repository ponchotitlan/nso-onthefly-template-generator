# -*- mode: python; python-indent: 4 -*-
__author__ = "Alfonso Sandoval,Cesar Alves"
__version__ = "2.1.0"
__maintainer__ = "Alfonso Sandoval,Cesar Alves"
__status__ = "Release"

import ncs
from .data_modules import ActionOutput, Result

def action_reporting( method:any ):
    """This is a decorator function for try/Exception catching and NSO default logging
    Inputs
    - Method

    Outputs
    - ActionOutput
    """
    def method_exec(*args):
        try:
            result_payload = method(*args)
            args[0].info(result_payload)
            return ActionOutput(
                Result.Success,
                result_payload
                )
        except Exception as ex:
            args[0].error(f'Error: {str(ex)}')
            return ActionOutput(
                Result.Failed,
                {str(ex)}
                )
    return method_exec

@action_reporting
def create_dummy_device(logger:ncs.log.Log, m:ncs.maapi.Maapi , DUMMY_DEVICE_NAME:str ,NED_ID:str ):
    """ This function creates a dummy device with the specified name and NED ID
    This device is not commited in this function

    Inputs:
    - logger -> ncs.log.Log 
    - m -> ncs.maapi.Maapi
    - DUMMY_DEVICE_NAME -> str
    - NED_ID -> str

    Output:
    - str: Device name
    """
    with m.start_write_trans() as t:
        root = ncs.maagic.get_root(t)
        dummy_device = root.devices.device.create(DUMMY_DEVICE_NAME)
        dummy_device.address = '1.1.1.1'
        dummy_device.authgroup = 'default'
        dev_type = dummy_device.device_type.cli
        dev_type.ned_id = NED_ID
        t.apply()
        return f'Dummy Device ({DUMMY_DEVICE_NAME}) created!'

@action_reporting
def device_load_native_config(logger:ncs.log.Log, m:ncs.maapi.Maapi , DUMMY_DEVICE_NAME:str , NATIVE_CONFIG:str):
    """This function issues the XML parsing of native config via *load_native_config* and *commit dry-run* in the dummy device

    Inputs
    - logger -> ncs.log.Log 
    - m -> ncs.maapi.Maapi
    - DUMMY_DEVICE_NAME -> str
    - NATIVE_CONFIG -> str

    Output
    - str : String is the parsed XML configuration
    - str : String is the Exception error raised during the operation
    """
    with m.start_write_trans() as t:
        root = ncs.maagic.get_root(t)
        dummy_device = root.devices.device[DUMMY_DEVICE_NAME]
        service_input = dummy_device.load_native_config.get_input()
        service_input.data = NATIVE_CONFIG
        dummy_device.load_native_config.request(service_input)
        dryRun = root.services.commit_dry_run
        drInput = dryRun.get_input()
        drInput.outformat = 'xml'
        return dryRun.request(drInput).result_xml.local_node.data.split("<config>")[1].split("</config>")[0].split("</tailfned>")[1]

@action_reporting
def push_device_template(logger:ncs.log.Log, m:ncs.maapi.Maapi , TEMPLATE_FILE_NAME:str , DEVICE_TEMPLATE_NAME:str , NED_ID:str , TEMPLATE_CONFIG:str):
    """This function opens a XML file with the contents of the device template, performs a simple string replacement with the data provided, and pushes the new configuration via *load merge terminal* to CDB using the transaction instance. This operation is commited

    Inputs
    - logger -> ncs.log.Log 
    - m -> ncs.maapi.Maapi
    - TEMPLATE_FILE_NAME -> str : The XML file must be located in the /templates folder of this package
    - DEVICE_TEMPLATE_NAME -> str
    - NED_ID -> str
    - TEMPLATE_CONFIG -> str: XML configuration to put into the new template

    Outputs
    - str : Parsed XML of the new device template which was pushed to CDB
    """
    with m.start_write_trans() as t:
        with open(TEMPLATE_FILE_NAME, 'r') as XML_FILE:
            template_config = XML_FILE.read().replace('{/name}', DEVICE_TEMPLATE_NAME).replace('{/ned_id}',NED_ID).replace('{/config_template}',TEMPLATE_CONFIG)
            t.load_config_cmds(ncs.maapi.CONFIG_MERGE | ncs.maapi.CONFIG_XML, template_config, '/')
            t.apply()
            return f'Device template ({DEVICE_TEMPLATE_NAME}) created!\n{template_config}'

@action_reporting
def flush_dummy_device(logger:ncs.log.Log, m:ncs.maapi.Maapi , DEVICE_NAME:str):
    '''This function deletes the dummy device generated as part of the template creation process.

    Inputs:
    - logger -> ncs.log.Log 
    - m -> ncs.maapi.Maapi
    - DEVICE_NAME -> str      

    Outputs:

    - bool: Operation status
    '''
    with m.start_write_trans() as t:
        root = ncs.maagic.get_root(t)
        del root.devices.device[DEVICE_NAME]
        t.apply()
        return f'Dummy device deleted: {DEVICE_NAME}'