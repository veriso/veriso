# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from qgis.core import *
from qgis.gui import *
import os

from Ui_options import Ui_Options

class OptionsDialog(QDialog, Ui_Options):
    
    projectsDatabaseHasChanged = pyqtSignal()
  
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)
        
        self.settings = QSettings("CatAIS","VeriSO")
        self.projects_database = self.settings.value("options/general/projects_database")
        self.projects_database_path = QFileInfo(self.projects_database).absolutePath()
        self.projects_root_directory = self.settings.value("options/general/projects_root_directory")
        self.import_jar = self.settings.value("options/import/jar")
        self.import_jar_path = QFileInfo(self.import_jar).absolutePath()

    def initGui(self):  
        self.lineEditDbPort.setValidator(QRegExpValidator(QRegExp("[0-9]+"), self.lineEditDbPort))        
        
        self.lineEditProjectsDatabase.setText(self.settings.value("options/general/projects_database")) 
        self.lineEditProjectsRootDir.setText(self.settings.value("options/general/projects_root_directory")) 
        
        self.lineEditImportJar.setText(self.settings.value("options/import/jar"))
        vm_arguments = self.settings.value("options/import/vm_arguments")
        if vm_arguments == "" or not vm_arguments or vm_arguments is None:
            self.plainTextEditImportVMArguments.insertPlainText("-Xms128m -Xmx1024m")
        else:
            self.plainTextEditImportVMArguments.insertPlainText(vm_arguments)
    
        self.lineEditDbHost.setText(self.settings.value("options/db/host")) 
        self.lineEditDbDatabase.setText(self.settings.value("options/db/name")) 
        self.lineEditDbPort.setText(self.settings.value("options/db/port")) 
        self.lineEditDbUser.setText(self.settings.value("options/db/user")) 
        self.lineEditDbUserPwd.setText(self.settings.value("options/db/pwd"))  
        self.lineEditDbAdmin.setText(self.settings.value("options/db/admin")) 
        self.lineEditDbAdminPwd.setText(self.settings.value("options/db/adminpwd")) 

        QWidget.setTabOrder(self.lineEditDbHost, self.lineEditDbDatabase)
        QWidget.setTabOrder(self.lineEditDbDatabase, self.lineEditDbPort)
        QWidget.setTabOrder(self.lineEditDbPort, self.lineEditDbUser)
        QWidget.setTabOrder(self.lineEditDbUser, self.lineEditDbUserPwd)
        QWidget.setTabOrder(self.lineEditDbUserPwd, self.lineEditDbAdmin)
        QWidget.setTabOrder(self.lineEditDbAdmin, self.lineEditDbAdminPwd)

    @pyqtSignature("on_btnBrowseImportJar_clicked()")    
    def on_btnBrowseImportJar_clicked(self):
        file = QFileDialog.getOpenFileName(self, self.tr("Open import jar file"), self.import_jar_path, "jar (*.jar *.JAR)")
        file_info = QFileInfo(file)
        self.lineEditImportJar.setText(file_info.absoluteFilePath())

    @pyqtSignature("on_btnBrowseProjectsDatabase_clicked()")    
    def on_btnBrowseProjectsDatabase_clicked(self):
        file = QFileDialog.getOpenFileName(self, self.tr("Choose projects definitions database"), self.projects_database_path,  "SQLite (*.sqlite *.db *.DB)")
        file_info = QFileInfo(file)
        self.lineEditProjectsDatabase.setText(file_info.absoluteFilePath())

    @pyqtSignature("on_btnBrowseProjectsRootDir_clicked()")    
    def on_btnBrowseProjectsRootDir_clicked(self):
        dir = QFileDialog.getExistingDirectory(self, self.tr("Choose projects root directory"), self.projects_root_directory)
        dir_info = QFileInfo(dir)
        self.lineEditProjectsRootDir.setText(dir_info.absoluteFilePath())

            
    def accept(self):
        self.settings.setValue("options/general/projects_database", self.lineEditProjectsDatabase.text())
        self.projectsDatabaseHasChanged.emit()
     
        self.settings.setValue("options/general/projects_root_directory", self.lineEditProjectsRootDir.text())

        self.settings.setValue("options/import/jar", self.lineEditImportJar.text())
        self.settings.setValue("options/import/vm_arguments", self.plainTextEditImportVMArguments.toPlainText())

        self.settings.setValue("options/db/host", self.lineEditDbHost.text())
        self.settings.setValue("options/db/name", self.lineEditDbDatabase.text())
        self.settings.setValue("options/db/port", self.lineEditDbPort.text())
        self.settings.setValue("options/db/user", self.lineEditDbUser.text())
        self.settings.setValue("options/db/pwd", self.lineEditDbUserPwd.text())
        self.settings.setValue("options/db/admin", self.lineEditDbAdmin.text())
        self.settings.setValue("options/db/adminpwd", self.lineEditDbAdminPwd.text())

        self.close()

    def tr(self, message):
        return QCoreApplication.translate('VeriSO', message)
