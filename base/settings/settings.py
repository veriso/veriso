# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
import os

class Settings(QObject):
    def __init__(self):
        settings = QSettings("CatAIS","VeriSO")

        self.db_params = {}
        self.db_params['db_host'] = settings.value("options/db/host")
        self.db_params['db_name'] =  settings.value("options/db/name")
        self.db_params['db_port'] = settings.value("options/db/port")
        self.db_params['db_admin'] = settings.value("options/db/admin")
        self.db_params['db_adminpwd'] = settings.value("options/db/adminpwd")
        self.db_params['db_user'] = settings.value("options/db/user")
        self.db_params['db_pwd'] =  settings.value("options/db/pwd")

        self.projects_database = settings.value("options/general/projects_database") 
        self.projects_root_directory = settings.value("options/general/projects_root_directory") 
        
        self.import_jar = settings.value("options/import/jar") 
        self.import_vm_arguments = settings.value("options/import/vm_arguments") 
