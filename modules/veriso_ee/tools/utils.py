 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import os
import json
import time
import sys
import traceback
import collections
from collections import OrderedDict

class Utils():
    @staticmethod
    def getCheckTopics():
        settings = QSettings("CatAIS","VeriSO")
        module_name = (settings.value("project/appmodule"))
        
        filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/"+module_name+"/checks/checks.json"))
        print filename
        
#        if not filename:
#            QMessageBox.critical(None, "VeriSO", self.tr("checks.json not found."))                                                    
#            return        
            
        try:
            checks = json.load(open(filename), object_pairs_hook=collections.OrderedDict) 
            print checks
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", Utils().tr("Failed to load checks.json. ") + str(traceback.format_exc(exc_traceback)))                                    
            return
            
        locale = QSettings().value('locale/userLocale')[0:2]

        try:
            topics = OrderedDict()
            for check in checks["checks"]:
                print "*************"
                print check
                topic = check["topic"]
                
                print topic
                
                # Test, ob checks.json multilingual ist.
                try:
                    if topics.has_key(topic):
                        continue
                    topics[topic] = check
                except:
                    print "MULTILINGUAL"
                    # Falls eingestellte Sprache nicht vorhanden,
                    # wird eine (1) Sprache verwendet (in diesem Fall
                    # die erste.
                    try:
                        my_topic = topic[locale]
                        my_check = OrderedDict()
                        my_check["topic"] = my_topic
                        my_check["file"] = check["file"]
                        topics[my_topic] = my_check
                        print "Sprache gefunden"
                    except:
                        print "Sprache nicht gefunden"
                        my_check = OrderedDict()
                        my_check["topic"] = topic.values()[0]
                        my_check["file"] = check["file"]
                        topics[my_check["topic"]] = my_check
                    
                
            return topics
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", Utils().tr("Error parsing json file. ") + str(traceback.format_exc(exc_traceback)))                                    
            return


    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('VeriSOModule', message)

