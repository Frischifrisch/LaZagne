# -*- coding: utf-8 -*- 

import base64

from xml.etree.cElementTree import ElementTree

from lazagne.config.module_info import ModuleInfo
from lazagne.config.constant import constant
from lazagne.config.winstructure import string_to_unicode

import os


class Unattended(ModuleInfo):
    def __init__(self):
        ModuleInfo.__init__(self, 'unattended', 'sysadmin', system_module=True)

    # Password should be encoded in b64
    def try_b64_decode(self, message):
        try:
            return base64.b64decode(message)
        except Exception:
            return message

    def run(self):

        windir = os.path.join(constant.profile['HOMEDRIVE'], string_to_unicode(os.sep), u'Windows')
        files = [
            'Panther\\Unattend.xml',
            'Panther\\Unattended.xml',
            'Panther\\Unattend\\Unattended.xml',
            'Panther\\Unattend\\Unattend.xml',
            'System32\\Sysprep\\unattend.xml',
            'System32\\Sysprep\\Panther\\unattend.xml'
        ]

        pwd_found = []
        xmlns = '{urn:schemas-microsoft-com:unattend}'
        for file in files:
            path = os.path.join(windir, string_to_unicode(file))
            if os.path.exists(path):
                self.debug(f'Unattended file found: {path}')
                tree = ElementTree(file=path)
                root = tree.getroot()

                for setting in root.findall(f'{xmlns}settings'):
                    component = setting.find(f'{xmlns}component')

                    if auto_logon := component.find(f'{xmlns}auto_logon'):
                        username = auto_logon.find(f'{xmlns}Username')
                        password = auto_logon.find(f'{xmlns}Password')
                        if all((username, password)):
                            # Remove false positive (with following message on password => *SENSITIVE*DATA*DELETED*)
                            if 'deleted' not in password.text.lower():
                                pwd_found.append({
                                    'Login': username.text,
                                    'Password': self.try_b64_decode(password.text)
                                })

                    if user_accounts := component.find(f'{xmlns}user_accounts'):
                        if local_accounts := user_accounts.find(
                            f'{xmlns}local_accounts'
                        ):
                            for local_account in local_accounts.findall(f'{xmlns}local_account'):
                                username = local_account.find(f'{xmlns}Name')
                                password = local_account.find(f'{xmlns}Password')
                                if all((username, password)):
                                    if 'deleted' not in password.text.lower():
                                        pwd_found.append({
                                            'Login': username.text,
                                            'Password': self.try_b64_decode(password.text)
                                        })

        return pwd_found
