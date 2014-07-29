 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from qgis.gui import *
import os


class LoadProjectsDatabase(QObject):
    
    def __init__(self):
        pass

    def read(self):                
        settings = QSettings("CatAIS","VeriSO")
        filename = settings.value("options/general/projectsdatabase")
        
        if filename == "" or filename is None:
            # does not work on qgis startup...
            #self.bar.pushMessage("Warning",  QCoreApplication.translate("Qcadastre", "No project database found.") + str(db.lastError().driverText()) , level=QgsMessageBar.WARNING, duration=5)                                        
            return
            
        projects = []
        
        try:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(filename) 

            if  not db.open():
                # does not work on qgis startup...                
                #self.bar.pushMessage("Error",  QCoreApplication.translate("Qcadastre", "Could not open database.") + str(db.lastError().driverText()) , level=QgsMessageBar.CRITICAL, duration=5)                            
                return 

            sql = "SELECT * FROM projects;"

            query = db.exec_(sql)
            
            if not query.isActive():
                # does not work on qgis startup...                
                #self.bar.pushMessage("Error",  QCoreApplication.translate("Qcadastre", "Error occured while fetching projects informations.") , level=QgsMessageBar.CRITICAL, duration=5)                            
                return 

            record = query.record()
            while query.next():
                project = {}
                project["id"] = str(query.value(record.indexOf("id")))
                project["displayname"] = str(query.value(record.indexOf("displayname")))
                project["dbhost"] = str(query.value(record.indexOf("dbhost")))
                project["dbname"] = str(query.value(record.indexOf("dbname")))
                project["dbport"] = str(query.value(record.indexOf("dbport")))
                project["dbschema"] = str(query.value(record.indexOf("dbschema")))                
                project["dbuser"] = str(query.value(record.indexOf("dbuser")))
                project["dbpwd"] = str(query.value(record.indexOf("dbpwd")))
                project["dbadmin"] = str(query.value(record.indexOf("dbadmin")))
                project["dbadminpwd"] = str(query.value(record.indexOf("dbadminpwd")))
                project["provider"] = str(query.value(record.indexOf("provider")))
                project["epsg"] = str(query.value(record.indexOf("epsg")))
                project["ilimodelname"] = str(query.value(record.indexOf("ilimodelname")))
                project["appmodule"] = str(query.value(record.indexOf("appmodule")))
                project["appmodulename"] = unicode(query.value(record.indexOf("appmodulename")))
                project["projectrootdir"] = str(query.value(record.indexOf("projectrootdir")))
                project["projectdir"] = str(query.value(record.indexOf("projectdir")))
                project["datadate"] = str(query.value(record.indexOf("datadate")))
                project["importdate"] = str(query.value(record.indexOf("importdate")))
                
                projects.append(project)

            db.close()

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", self.tr("Error while reading projects database.") + str(traceback.format_exc(exc_traceback)))                                    
            return

        return projects

    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('VeriSO', message)
