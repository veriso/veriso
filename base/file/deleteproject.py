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
from veriso.base.utils.doLoadProjectsDatabase import LoadProjectsDatabase

class DeleteProjectDialog(QDialog, Ui_DeleteProject):
  
    projectsDatabaseHasChanged = pyqtSignal()

    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.okButton.setText("Delete")
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)
        
        self.settings = QSettings("CatAIS","VeriSO")
        self.projects_database = self.settings.value("options/general/projectsdatabase") 

    def initGui(self):     
        d = LoadProjectsDatabase()
        projects = d.read()
        
        if not projects:
            self.cBoxProject.clear()    
            return
        
        self.projects = projects
        sortedProjects = sorted(self.projects, key=lambda k: k['displayname']) 
    
        self.cBoxProject.clear()    
        for project in sortedProjects:
            self.cBoxProject.addItem(unicode(project["displayname"]), project["dbschema"])

        self.cBoxProject.insertItem(0, "", None)
        self.cBoxProject.setCurrentIndex(0)

        return True

    def accept(self):
        currIdx = self.cBoxProject.currentIndex()
        if currIdx == 0:
            return
        
        dbschema = str(self.cBoxProject.itemData(currIdx))
        
        i = 0
        for project in self.projects:
            if dbschema ==  str(project["dbschema"]):                
                self.dbhost = str(project["dbhost"])
                self.dbname = str(project["dbname"])
                self.dbport = str(project["dbport"])
                self.dbschema = dbschema
                self.dbadmin = str(project["dbadmin"])
                self.dbadminpwd = str(project["dbadminpwd"])
                self.projectIndex = i
            i += 1
                 
        # Delete geodata in database.
        db = QSqlDatabase.addDatabase("QPSQL", "PostgreSQL")
        db.setHostName(self.dbhost)
        db.setDatabaseName(self.dbname)
        db.setUserName(self.dbadmin)
        db.setPassword(self.dbadminpwd)
        
        try:
            db.setPort(int(self.dbport))
        
            if not db.open():
                QMessageBox.critical(None, "VeriSO", self.tr("Could not open geodatabase."))                                    
                return
            
            sql = "BEGIN;"
            sql += "DROP SCHEMA IF EXISTS " + self.dbschema + " CASCADE;"
            sql += "COMMIT;"
            
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.buttonBox.setEnabled(False)      
        
            query = db.exec_(sql)
            
            if query.isActive() == False:
                QMessageBox.critical(None, "VeriSO", self.tr("Error occured while deleting project in geodatabase."))                                                    
                return
            
            db.close()
                
            # Delete project entry in project database.
            pdb = QSqlDatabase.addDatabase("QSQLITE")
            pdb.setDatabaseName(self.projects_database) 

            if not pdb.open():
                QMessageBox.critical(None, "VeriSO", self.tr("Could not open projects database."))                                    
                return 
                
            sql = "DELETE FROM projects WHERE dbschema = '" + self.dbschema + "';"

            query = pdb.exec_(sql)
            
            if not query.isActive():
                QMessageBox.critical(None, "VeriSO", self.tr("Error occured while deleting project in projects database."))                                                    
                return 
            
            pdb.close()
            self.projectsDatabaseHasChanged.emit()
            self.initGui()
            
        except Exception:
            QApplication.restoreOverrideCursor()        
            self.buttonBox.setEnabled(True)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", self.tr("Something went wrong while deleting project: ") + str(traceback.format_exc(exc_traceback)))                                    
            return

        QApplication.restoreOverrideCursor()        
        self.buttonBox.setEnabled(True)
        QMessageBox.information(None, "VeriSO", self.tr("Project deleted. Please remove project directory manually."))                                    

    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('VeriSO', message)
