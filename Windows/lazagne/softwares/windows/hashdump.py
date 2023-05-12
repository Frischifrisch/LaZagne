# -*- coding: utf-8 -*- 
from .creddump7.win32.hashdump import dump_file_hashes
from lazagne.config.module_info import ModuleInfo
from lazagne.config.constant import constant


class Hashdump(ModuleInfo):
    def __init__(self):
        ModuleInfo.__init__(self, 'hashdump', 'windows', system_module=True)

    def run(self):
        if hashdump := dump_file_hashes(
            constant.hives['system'], constant.hives['sam']
        ):
            return ['__Hashdump__', hashdump]
