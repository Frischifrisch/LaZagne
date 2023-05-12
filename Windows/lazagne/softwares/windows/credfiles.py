# -*- coding: utf-8 -*-
from lazagne.config.module_info import ModuleInfo
from lazagne.config.constant import constant
import os


class CredFiles(ModuleInfo):
    def __init__(self):
        ModuleInfo.__init__(self, 'credfiles', 'windows', dpapi_used=True)

    def run(self):
        pwd_found = []
        if constant.user_dpapi and constant.user_dpapi.unlocked:
            creds_directory = os.path.join(constant.profile['APPDATA'], u'Microsoft', u'Credentials')
            if os.path.exists(creds_directory):
                for cred_file in os.listdir(creds_directory):
                    if cred := constant.user_dpapi.decrypt_cred(
                        os.path.join(creds_directory, cred_file)
                    ):
                        pwd_found.append(cred)

        return pwd_found
