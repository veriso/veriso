# -*- coding: utf-8 -*-

# Import the PyQt and the QGIS libraries
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
import shutil
import codecs
import traceback

from Ui_importproject import Ui_ImportProject

class ImportProjectDialog(QDialog, Ui_ImportProject):
  
    projectsDatabaseHasChanged = pyqtSignal()

    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.okButton.setText("Import")
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)
        
        self.settings = QSettings("CatAIS","VeriSO")
        self.input_itf_path = QFileInfo(self.settings.value("file/import/inputitfpath")).absolutePath()

        today = QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(today)
        self.dateTimeEdit.setCalendarPopup(True)


    def initGui(self):       
        self.lineEditDbSchema.setValidator(QRegExpValidator(QRegExp("^[a-z][a-z0-9_]+"), self.lineEditDbSchema))

        try:
            filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/modules.json"))
            self.modules = json.load(open(filename)) 
#            print self.modules
            if self.modules:
                sortedModulesList = sorted(self.modules["modules"], key=lambda k: k['displayname']) 
                self.cmbBoxAppModule.clear()
                for module in sortedModulesList:
                    self.cmbBoxAppModule.insertItem(self.cmbBoxAppModule.count(), unicode(module["displayname"]), module)
                self.cmbBoxAppModule.insertItem(0, "", None)
                self.cmbBoxAppModule.setCurrentIndex(0)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", self.tr("Error while reading modules.json."))
            return
            
        self.cmbBoxIliModelName.insertItem(0, "", None)
        
        return True

    @pyqtSignature("on_btnProjectName_clicked()")    
    def on_btnProjectName_clicked(self):
        if self.lineEditDbSchema.text().strip() <> "":
            try:            
                dbhost = self.settings.value("options/db/host")
                dbname = self.settings.value("options/db/name")
                dbport = self.settings.value("options/db/port")
                dbadmin = self.settings.value("options/db/admin")
                dbadminpwd = self.settings.value("options/db/adminpwd")

                db = QSqlDatabase.addDatabase("QPSQL")
                db.setHostName(dbhost)
                db.setPort(int(dbport))
                db.setDatabaseName(dbname)
                db.setUserName(dbadmin)
                db.setPassword(dbadminpwd)

                if not db.open():
                    QMessageBox.critical(None, "VeriSO", self.tr("Could not open database: ") + db.lastError().driverText())
                    return  
                    
                sql = "SELECT schema_name FROM information_schema.schemata WHERE schema_name = '" + self.lineEditDbSchema.text() + "';"
                
                query = db.exec_(sql)
                if query.isActive():
                    count = query.size()
                    if count > 0:
                        QMessageBox.warning(None, "VeriSO", self.tr("Project name already in use."))
                    else:
                        QMessageBox.information(None, "VeriSO", self.tr("Project name is valid."))

                db.close()
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                if dbport == "":
                    QMessageBox.information(None, "VeriSO", self.tr("Could not check. Database port is not set."))
                else:
                    QMessageBox.critical(None, "VeriSO", str(traceback.format_exc(exc_traceback)))

    @pyqtSignature("on_cmbBoxAppModule_currentIndexChanged(int)")      
    def on_cmbBoxAppModule_currentIndexChanged(self, idx):
        self.cmbBoxIliModelName.clear()        
        moduleData = self.cmbBoxAppModule.itemData(idx)
        
        if moduleData:
            ilimodels = moduleData["ilimodels"]
            
            self.appmodule = moduleData["dirname"]
            self.appmodule_name = self.cmbBoxAppModule.currentText()

            for i in range(len(ilimodels)):
                model_name = ilimodels[i]["ilimodel"]
                reference_frame = ilimodels[i]["referenceframe"]
                self.cmbBoxIliModelName.insertItem(self.cmbBoxIliModelName.count(), str(model_name), ilimodels[i])
            self.cmbBoxIliModelName.insertItem(0, "", None)
            
            if len(ilimodels) == 1:
                self.cmbBoxIliModelName.setCurrentIndex(1)
                self.cmbBoxIliModelName.setEnabled(False)
            else:
                self.cmbBoxIliModelName.setCurrentIndex(0)
                self.cmbBoxIliModelName.setEnabled(True)
            
        else:
            self.appmodule = ""
            self.appmodule_name = ""
            
    @pyqtSignature("on_cmbBoxIliModelName_currentIndexChanged(int)")      
    def on_cmbBoxIliModelName_currentIndexChanged(self, idx):
        module_data = self.cmbBoxIliModelName.itemData(idx)

        if module_data:
            self.ili = module_data["ilimodel"]
            self.epsg = module_data["epsg"]
            reference_frame = module_data["referenceframe"]
            self.lineEditRefFrame.setText(str(reference_frame) + " (EPSG:" + str(self.epsg) + ")")
        else:
            self.ili = ""
            self.epsg =""
            self.lineEditRefFrame.clear()

    @pyqtSignature("on_btnBrowsInputFile_clicked()")    
    def on_btnBrowsInputFile_clicked(self):
        file = QFileDialog.getOpenFileName(self, self.tr("Choose interlis transfer file"), self.input_itf_path,  "ITF (*.itf *.ITF)")
        fileInfo = QFileInfo(file)
        self.lineEditInputFile.setText(fileInfo.absoluteFilePath())

    def accept(self):
        # save the settings
        self.settings.setValue("file/import/inputitfpath", self.lineEditInputFile.text())
        self.settings.setValue("file/import/ili", self.ili)

        # gather all data/information for properties file (needed by java import program)
        self.itf = self.lineEditInputFile.text()
        self.dbschema = self.lineEditDbSchema.text()    
    
        self.datadate = self.dateTimeEdit.date().toString("yyyy-MM-dd")
        
        self.notes = self.textEditNotes.toPlainText()
        if len(self.notes) > 10000:
            QMessageBox.critical(None, "VeriSO", self.tr("Notes are too big (more than 10000 characters)."))            
            return

        self.dbhost = self.settings.value("options/db/host")
        self.dbname = self.settings.value("options/db/name")
        self.dbport = self.settings.value("options/db/port")
        self.dbuser = self.settings.value("options/db/user")
        self.dbpwd = self.settings.value("options/db/pwd")
        self.dbadmin = self.settings.value("options/db/admin")
        self.dbadminpwd = self.settings.value("options/db/adminpwd")

        self.projects_database = self.settings.value("options/general/projectsdatabase") 
        self.projects_rootdir = self.settings.value("options/general/projectsrootdir") 
        
        import_jar = self.settings.value("options/import/jar") 
        import_vm_args = self.settings.value("options/import/vmarguments") 
        
        # check if we have everything
        if not os.path.isfile(self.projects_database) and self.projects_database <> "":
            QMessageBox.warning(None, "VeriSO", self.tr("Projects database not found: ") + str(self.projects_database))                        
            return
        
        if self.itf == "":
            QMessageBox.warning(None, "VeriSO", self.tr("No Interlis transfer file set."))                                    
            return
        
        if self.ili == "":
            QMessageBox.warning(None, "VeriSO", self.tr("No Interlis model name set."))                                    
            return
            
        if self.dbschema == "":
            QMessageBox.warning(None, "VeriSO", self.tr("No database schema set."))                                    
            return
            
        if self.cmbBoxAppModule.currentIndex() == 0:
            QMessageBox.warning(None, "VeriSO", self.tr("No application module chosen."))                                    
            return
            
        if self.dbhost == None or self.dbname == None or self.dbport == None or self.dbuser == None or self.dbpwd == None or self.dbadmin == None or self.dbadminpwd == None:
            QMessageBox.warning(None, "VeriSO", self.tr("Missing database parameters.") + str(self.projects_database))                                    
            return
        
        if self.projects_rootdir == "":
            QMessageBox.warning(None, "VeriSO", self.tr("No root directory for projects set."))                                                
            self.bar.pushMessage("Warning",  QCoreApplication.translate("Qcadastre", "No root directory for projects set."), level=QgsMessageBar.WARNING)                                    
            return
            
        if self.projects_database.strip() == "":
            QMessageBox.warning(None, "VeriSO", self.tr("No projects database found. Will create one in the project root directory."))
            
        if import_jar == "":
            QMessageBox.warning(None, "VeriSO", self.tr("No jar file set for import."))            
            return
            
        # create java properties file
        tmpPropertiesFile = self.writePropertiesFile()
        if tmpPropertiesFile is None:
            return
        
        # clear output textedit
        self.textEditImportOutput.clear()
         
        # import data
        arguments = []
        
        vm_args = import_vm_args.split(" ")
        for i in range(len(vm_args)):
            arguments.append(vm_args[i])
            
        arguments.append("-jar")
        arguments.append(import_jar)
        arguments.append(tmpPropertiesFile)
        
        self.process = QProcess()
        self.connect(self.process, SIGNAL("readyReadStandardOutput()"), self.readOutput)
        self.connect(self.process, SIGNAL("readyReadStandardError()"), self.readError)
        self.connect(self.process, SIGNAL("finished(int)"), self.finishImport)     
     
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.buttonBox.setEnabled(False)
        try:
            self.process.start("java", arguments)
        except:
            QApplication.restoreOverrideCursor()
            self.buttonBox.setEnabled(True)            

    def readOutput(self):
        self.textEditImportOutput.insertPlainText(str(self.process.readAllStandardOutput()))
        self.textEditImportOutput.ensureCursorVisible()        

    def readError(self):
        self.textEditImportOutput.insertPlainText(str(self.process.readAllStandardError()))        

    def finishImport(self,  i):
        QApplication.restoreOverrideCursor()        
        self.buttonBox.setEnabled(True)

        updated = self.updateProjectsDatabase()
        if not updated:
            QMessageBox.critical(None, "VeriSO", self.tr("Import process not sucessfully finished. Could not update projects database."))                        
            return

        # Check if there are some errors/fatals in the output.
        # Prüfung erst hier, da es einfacher ist den misslungenen Import zu löschen, wenn
        # in der Projektedatenbank bereits ein Eintrag ist.
        output = unicode(self.textEditImportOutput.toPlainText())
        if output.find("FATAL") > 0 or output.find("ERROR") > 0 or output.strip() == "":
            QMessageBox.critical(None, "VeriSO", self.tr("Import process not sucessfully finished."))                                    
            return            
            
        # Create project directory in projects root directory.
        proj_dir = self.createProjectDir()
        if proj_dir:
            QMessageBox.information(None, "VeriSO", self.tr("Import process finished."))                                                
        else:
            QMessageBox.critical(None, "VeriSO", self.tr("Import process not sucessfully finished. Could not create project directory."))                                    
            
    def createProjectDir(self):
        try:
            os.makedirs(os.path.join(str(self.projects_rootdir), str(self.dbschema)))
            return True
        except:
            return False

    def writePropertiesFile(self):
        tmpDir = tempfile.gettempdir()
        tmpPropertiesFile = os.path.join(tmpDir, str(time.time()) + ".properties")
    
        try:
            # "utf-8" macht momentan beim Java-Import Probleme! (Scheint aber mal funktioniert zu haben).
            # Mit "iso-8859-1" funktionierts. Im Output-Fenster erscheint aber immer noch Kauderwelsch.
            # Das Java-Properties-File muss angeblich immer iso-8859-1 sein....
            f = codecs.open(tmpPropertiesFile, "w", "iso-8859-1")
        
            try:
                f.write("dbhost = " + self.dbhost + "\n")
                f.write("dbname = " + self.dbname + "\n")
                f.write("dbschema = " + self.dbschema + "\n")
                f.write("dbport = " + self.dbport + "\n")
                f.write("dbuser = " + self.dbuser + "\n")
                f.write("dbpwd = " + self.dbpwd + "\n")
                f.write("dbadmin = " + self.dbadmin + "\n")
                f.write("dbadminpwd = " + self.dbadminpwd + "\n")
                f.write("\n")
                f.write("epsg = " + self.epsg + "\n")
                f.write("\n")
                f.write("vacuum = true\n")
                f.write("reindex = true\n")
                f.write("\n")
                f.write("importModelName = " + str(self.ili) + "\n")
                f.write("importItfFile = " + unicode(self.itf) + "\n")
                f.write("\n")
                f.write("enumerationText = true\n")
                f.write("renumberTid = true\n")
                f.write("\n");
                f.write("schemaOnly = false\n")
                f.write("\n");
                f.write("qgisFiles = false\n")
                f.write("\n");
                
                filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/"+self.appmodule+"/postprocessing/postprocessing.db"))                    
                f.write("postprocessingDatabase = " + str(filename))
                
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                QMessageBox.critical(None, "VeriSO", self.tr("Error while creating properties file.") + str(traceback.format_exc(exc_traceback)))                                    
                return

            finally:
                f.close()
                return tmpPropertiesFile
        
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", self.tr("Error while creating properties file.") + str(traceback.format_exc(exc_traceback)))                                    
            return
        
        return

    def updateProjectsDatabase(self):
        db = QSqlDatabase.addDatabase("QSQLITE", "Projectdatabase")

        try:
            # Create a new projects database if there is none (copy one from the templates).
            if self.projects_database.strip() == "":
                srcdatabase = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/templates/template_projects.db"))
                self.projects_database = QDir.convertSeparators(QDir.cleanPath(self.projects_rootdir + "/projects.db"))
                shutil.copyfile(srcdatabase, self.projects_database)
                self.settings.setValue("options/general/projectsdatabase", self.projects_database)

            db.setDatabaseName(self.projects_database) 

            if not db.open():
                QMessageBox.critical(None, "VeriSO", self.tr("Could not open projects database."))                                                    
                return  
             
            projectrootdir = QDir.convertSeparators(QDir.cleanPath(self.projects_rootdir + "/" + str(self.dbschema)))
        
            sql = "INSERT INTO projects (id, displayname, dbhost, dbname, dbport, dbschema, dbuser, dbpwd, dbadmin, dbadminpwd, provider, epsg, ilimodelname, appmodule, appmodulename, projectrootdir, projectdir, datadate, notes, itf) \
VALUES ('"+str(self.dbschema)+"', '"+str(self.dbschema)+"', '"+str(self.dbhost)+"', '"+str(self.dbname)+"', "+str(self.dbport)+", '"+str(self.dbschema)+"', '"+str(self.dbuser)+"', '"+str(self.dbpwd)+"', \
'"+str(self.dbadmin)+"', '"+str(self.dbadminpwd)+"', 'postgres'," + str(self.epsg) + " , '"+str(self.ili)+"', '"+str(self.appmodule)+"','"+unicode(self.appmodule_name)+"', '"+str(self.projects_rootdir)+"', '"+projectrootdir+"', '"+self.datadate+"', '"+self.notes+"', '"+self.itf+"');"

            query = db.exec_(sql)
            
            if query.isActive() == False:
                QMessageBox.critical(None, "VeriSO", self.tr("Error while updating projects database."))                                    
                return 
            
            db.close()
            self.projectsDatabaseHasChanged.emit()
            return True
        
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", self.tr("Error while updating projects database.") + str(traceback.format_exc(exc_traceback)))                                    

    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('VeriSO', message)
