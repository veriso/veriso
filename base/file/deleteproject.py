# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from PyQt4 import uic
from qgis.core import *
from qgis.gui import *
import os
import json
import sys
import tempfile
import time
import traceback

from Ui_deleteproject import Ui_DeleteProject
from veriso.base.utils.loadprojectsdatabase import LoadProjectsDatabase

class DeleteProjectDialog(QDialog, Ui_DeleteProject):
  
    projectsDatabaseHasChanged = pyqtSignal()

    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.okButton.setText("Delete")
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)
        
        self.settings = QSettings("CatAIS","VeriSO")
        self.projects_database = self.settings.value("options/general/projects_database") 

    def initGui(self):
        d = LoadProjectsDatabase()
        projects = d.read()

        if not projects:
            self.cBoxProject.clear()    
            return

        self.projects = projects
        sorted_projects = sorted(self.projects, key=lambda k: k['displayname']) 
    
        self.cBoxProject.clear()    
        for project in sorted_projects:
            self.cBoxProject.addItem(unicode(project["displayname"]), project["dbschema"])

        self.cBoxProject.insertItem(0, "", None)
        self.cBoxProject.setCurrentIndex(0)

        return True

    def accept(self):            
        current_index = self.cBoxProject.currentIndex()
        if current_index == 0:
            return
        
        db_schema = str(self.cBoxProject.itemData(current_index))
        
        # Get the connections parameters from the projects list we created in the initGui method.
        i = 0
        for project in self.projects:
            if db_schema ==  str(project["dbschema"]):                
                self.db_host = str(project["dbhost"])
                self.db_name = str(project["dbname"])
                self.db_port = str(project["dbport"])
                self.db_schema = db_schema
                self.db_admin = str(project["dbadmin"])
                self.db_admin_pwd = str(project["dbadminpwd"])
                self.project_index = i
            i += 1
                 
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.buttonBox.setEnabled(False)      

        deleted = self.delete_data_in_database()
        if not deleted:
            self.restore_cursor()
            message = "Something went wrong while deleting data in database."
            QMessageBox.critical(None, "VeriSO", self.tr(message))
            return
        
        updated = self.update_project_database()
        if not updated:
            self.restore_cursor()
            message = "Something went wrong while updating projects database."
            QMessageBox.critical(None, "VeriSO", self.tr(message))
            return

        self.restore_cursor()

        self.projectsDatabaseHasChanged.emit()
        self.initGui()
        
        message = "Project deleted. Please remove project directory manually."
        QMessageBox.information(None, "VeriSO", self.tr(message))                                    

    def update_project_database(self):
        """Deletes the deleted project from the sqlite project database.
        
        Returns:
          False: If something went wrong. Otherwise True.
        """
        try:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(self.projects_database) 

            if not db.open():
                message = "Could not open projects database."
                QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)            
                QgsMessageLog.logMessage(str(db.lastError().text()), "VeriSO", QgsMessageLog.CRITICAL)            
                return  
                
            sql = "DELETE FROM projects WHERE dbschema = '" + self.db_schema + "';"

            query = db.exec_(sql)
            
            if not query.isActive():
                message = "Error while reading from projects database."
                QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)            
                QgsMessageLog.logMessage(str(QSqlQuery.lastError(query).text()), "VeriSO", QgsMessageLog.CRITICAL)      
                return 
            
            db.close()
            del db
            
            return True
            
        except Exception, e:
            message = "Error while reading projects database."
            QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)            
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)      
            return

    def delete_data_in_database(self):
        """Deletes the project (= database schema) in the database.
        
        Returns:
          False: If something went wrong with deleting in the database. Otherwise True.
        """
        try:
            db = QSqlDatabase.addDatabase("QPSQL")
            db.setHostName(self.db_host)
            db.setDatabaseName(self.db_name)
            db.setUserName(self.db_admin)
            db.setPassword(self.db_admin_pwd)
            db.setPort(int(self.db_port))
        
            if not db.open():
                message = "Could not open database."
                QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)            
                QgsMessageLog.logMessage(str(db.lastError().text()), "VeriSO", QgsMessageLog.CRITICAL)            
                return  
    
            sql = "BEGIN;"
            sql += "DROP SCHEMA IF EXISTS " + self.db_schema + " CASCADE;"
            sql += "COMMIT;"
            
            query = db.exec_(sql)
            
            if not query.isActive():
                message = "Error occured while deleting project in database."
                QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)            
                QgsMessageLog.logMessage(str(QSqlQuery.lastError(query).text()), "VeriSO", QgsMessageLog.CRITICAL)      
                return 
                
            db.close()
            del db
            
            return True
            
        except Exception, e:                
            message = "Something went wrong while deleting project."
            QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)            
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)      
            return

    def restore_cursor(self):
        QApplication.restoreOverrideCursor()        
        self.buttonBox.setEnabled(True)

    def tr(self, message):
        return QCoreApplication.translate('VeriSO', message)
