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

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Utils():
    @staticmethod
    def getCheckTopics():
        settings = QSettings("CatAIS","VeriSO")
        module_name = settings.value("project/appmodule")
        
        filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/"+module_name+"/checks/checks.json"))
           
        try:
            checks = json.load(open(filename), object_pairs_hook=collections.OrderedDict) 
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO",  _translate("VeriSO_EE_Utils", "Failed to load checks.json. ", None) + str(traceback.format_exc(exc_traceback)))                                    
            return
            
        locale = QSettings().value('locale/userLocale')[0:2]

        try:
            topics = OrderedDict()
            for check in checks["checks"]:
                topic = check["topic"]
                
                # Test, ob checks.json multilingual ist.
                try:
                    if topics.has_key(topic):
                        continue
                    topics[topic] = check
                    # Json ist NICHT multilingual.
                except:
                    # Json ist multilingual.
                    
                    # Falls eingestellte Sprache nicht vorhanden ist,
                    # wird eine (1) Sprache verwendet (in diesem Fall
                    # die erste.
                    try:
                        my_topic = topic[locale]
                        my_check = OrderedDict()
                        my_check["topic"] = my_topic
                        my_check["file"] = check["file"]
                        topics[my_topic] = my_check
                        # Sprache gefunden
                    except:
                        # Sprache nicht gefunden
                        my_check = OrderedDict()
                        my_check["topic"] = topic.values()[0]
                        my_check["file"] = check["file"]
                        topics[my_check["topic"]] = my_check
            return topics
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", _translate("VeriSO_EE_Utils", "Error parsing json file. ", None) + str(traceback.format_exc(exc_traceback)))                                    
            return
    
    @staticmethod
    def getChecks(checkfile):
        settings = QSettings("CatAIS","VeriSO")
        module_name = settings.value("project/appmodule")
        
        filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/"+module_name+"/checks/"+checkfile+".json"))
   
        try:
            checks = json.load(open(filename), object_pairs_hook=collections.OrderedDict) 
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", _translate("VeriSO_EE_Utils", "Failed to load checks file. ", None) + str(traceback.format_exc(exc_traceback)))                                                
            return
    
        try:
            topic_checks = []
            for check in checks["checks"]:
                topic_checks.append(check)
            return topic_checks
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", _translate("VeriSO_EE_Utils", "Error parsing json file. ", None) + str(traceback.format_exc(exc_traceback)))                                                            
            return
            
    @staticmethod
    def getBaselayers():
        settings = QSettings("CatAIS","VeriSO")
        module_name = (settings.value("project/appmodule"))
        
        filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/"+module_name+"/baselayer/baselayer.json"))
    
        try:
            baselayers = json.load(open(filename), object_pairs_hook=collections.OrderedDict) 
            return baselayers
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", _translate("VeriSO_EE_Utils", "Failed to load baselayer.json. ", None) + str(traceback.format_exc(exc_traceback)))                                                            
            return
    
    @staticmethod
    def getTopicsTables():
        settings = QSettings("CatAIS","VeriSO")
        module_name = settings.value("project/appmodule")
        ili_model_name =  settings.value("project/ilimodelname")

        filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/"+module_name+"/tables/"+ili_model_name.lower()+"/tables.json"))
        
        try:
            topics_json = json.load(open(filename), object_pairs_hook=collections.OrderedDict) 
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", _translate("VeriSO_EE_Utils", "Failed to load tables.json. ", None) + str(traceback.format_exc(exc_traceback)))                                                            
            return

        locale = QSettings().value('locale/userLocale')[0:2]

        try:
            topics = OrderedDict()
            for topic in topics_json["topics"]:
                topicName = topic["topic"]
                try:
                    keys =  topicName.keys()
                    try:
                        topicName = unicode(topicName[locale])
                    except:
                        topicName = unicode(topicName.values()[0])
                except:
                    topicName = unicode(topicName)
                
                topic["topic"] = topicName
                topics[topicName] = topic
            return topics
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", _translate("VeriSO_EE_Utils", "FaError parsing json file. ", None) + str(traceback.format_exc(exc_traceback)))                                                            
            return
