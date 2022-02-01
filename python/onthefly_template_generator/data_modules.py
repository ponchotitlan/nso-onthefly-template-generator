# -*- mode: python; python-indent: 4 -*-
__author__ = "Alfonso Sandoval,Cesar Alves"
__version__ = "2.1.0"
__maintainer__ = "Alfonso Sandoval,Cesar Alves"
__status__ = "Release"

from enum import Enum
from ncs.maagic import Container
import uuid

class Result(Enum):
    """Enumeration for the different action results
    - Success = 'SUCCESS'
    - Failed = 'FAILED'
    """
    Success = 'SUCCESS'
    Failed = 'FAILED'

class XMLTemplateName(Enum):
    """Enumeration for XML template names located in python/resource_templates
    """
    DeviceTemplateXML = 'packages/onthefly-template-generator/python/resource_templates/device_template.xml'

class ActionOutput():
    """ This class contains the results of any given operation with the try-Except decorator

    Inputs:
    - result:  -> Operation result (Result)
    - info:    -> Operation payload (str)

    Outputs:
    - ActionOutput instance
    """
    def __init__(self, result:Result , info:str) -> None:
        self.__result = result
        self.__info = info

    @property
    def result(self) -> Result:
        '''Returns result enum'''
        return self.__result

    @property
    def info(self) -> str:
        '''Returns info string'''
        return self.__info

class DeviceResources():
    """ This class contains all the data required for the operation of this action

    Inputs:
    - input: -> ncs.maagic.Container

    Outputs:
    - DeviceResources instance
    """
    def __init__(self, input:Container ) -> None:
        """Initialization of all class parameters under the following constraints:
            - ( DEVICE_TEMPLATE : str ) Initialized with YANG inputs
            - ( NED ID : const str ) Ned is delivered in a double format (ned_id:ned_id) by YANG. Hence, it needs to be trimmed
            - ( DUMMY_DEVICE_NAME : const str ) Dummy device for Native to XML parsing. Standard name initialization
            - ( NATIVE_CONFIGURATION : const str) Native configuration as specified in YANG inputs
        """
        self.__DEVICE_TEMPLATE = input.template_name
        self.__NATIVE_CONFIGURATION = input.native_configuration
        self.__DUMMY_DEVICE_NAME = f'{str(uuid.uuid4().hex)[0:5]}_device'
        self.__NED_ID = input.ned_id.split(':')[0]

    @property
    def deviceTemplate(self) -> str:
        '''Returns device template value'''
        return self.__DEVICE_TEMPLATE

    @property
    def dummy_device_name(self) -> str:
        '''Returns dummy device name value'''
        return self.__DUMMY_DEVICE_NAME

    @property
    def ned_id(self) -> str:
        '''Returns NED id value'''
        return self.__NED_ID

    @property
    def native_configuration(self) -> str:
        '''Returns native configuration value'''
        return self.__NATIVE_CONFIGURATION