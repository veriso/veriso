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
import shutil
import codecs
import traceback

from veriso.base.settings.settings import Settings
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
        self.input_itf_path = QFileInfo(self.settings.value("file/import/input_itf_path")).absolutePath()

    def initGui(self):
        """Initialize the dialog:
        Set the current date.
        Accept only lower characters as project name (= database schema).
        Fill modules combobox.
        """
        today = QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(today)
        self.dateTimeEdit.setCalendarPopup(True)

        # You are only allowed to use lower case characters as project name (= database schema).
        self.lineEditDbSchema.setValidator(QRegExpValidator(QRegExp("^[a-z][a-z0-9_]+"), self.lineEditDbSchema))
                
        # Fill out the modules combobox.
        try:
            filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/modules.json"))
            self.modules = json.load(open(filename)) 
            if self.modules:
                sortedModulesList = sorted(self.modules["modules"], key=lambda k: k['displayname']) 
                self.cmbBoxAppModule.clear()
                for module in sortedModulesList:
                    self.cmbBoxAppModule.insertItem(self.cmbBoxAppModule.count(), unicode(module["displayname"]), module)
                self.cmbBoxAppModule.insertItem(0, "", None)
                self.cmbBoxAppModule.setCurrentIndex(0)
        except Exception, e:
            message = "Error while reading modules.json."
            QMessageBox.critical(None, "VeriSO", self.tr(message))
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)            
            return
            
        self.cmbBoxIliModelName.insertItem(0, "", None)
        
        return True

    @pyqtSignature("on_btnProjectName_clicked()")    
    def on_btnProjectName_clicked(self):
        """Check wether the project (=database schema) already exists.
        """
        project_name =  self.lineEditDbSchema.text().strip()
        if len(project_name) > 0:
            
            project_found = self.check_project_name(project_name)
            
            if project_found == -1:
                message = "An error occured while connecting the database."
                QMessageBox.critical(None, "VeriSO", self.tr(message))
                return
            
            elif project_found == 1:
                message = "Project name already exists."
                QMessageBox.warning(None, "VeriSO", self.tr(message))
                QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.WARNING)             
                return
                
            elif project_found == 0:
                message = "Project name is valid."
                QMessageBox.information(None, "VeriSO", self.tr(message))
                return True

    def check_project_name(self, project_name):
        """Makes a database request and checks if the given schema already exists.
        
        Returns:
            -1 if an error occured. 0 if schema was not found. 1 if schema already exists.
        """
        # 'public' will not be found with the query.
        if project_name == "public":
            return 1
        
        try:            
            db_host = self.settings.value("options/db/host")
            db_name = self.settings.value("options/db/name")
            db_port = self.settings.value("options/db/port")
            db_admin = self.settings.value("options/db/admin")
            db_admin_pwd = self.settings.value("options/db/adminpwd")
        
            db = QSqlDatabase.addDatabase("QPSQL", "db")
            db.setHostName(db_host)
            db.setPort(int(db_port))
            db.setDatabaseName(db_name)
            db.setUserName(db_admin)
            db.setPassword(db_admin_pwd)
    
            if not db.open():
                message = "Could not open database: "
                QgsMessageLog.logMessage(self.tr(message) + db.lastError().driverText(), "VeriSO", QgsMessageLog.CRITICAL)                                
                return -1
                
            sql = "SELECT schema_name FROM information_schema.schemata WHERE schema_name = '" + self.lineEditDbSchema.text().strip() + "';"
            query = db.exec_(sql)
            
            if query.isActive():
                count = query.size()
                
                # I can't get rid of the 'duplicate connections' warning... Seems possible though. There is even 
                # an PyQt example.
                db.close
                del db

                if  count > 0:
                    return 1
                else:
                    return 0
            
        except Exception, e:
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)     
            return -1

    @pyqtSignature("on_cmbBoxAppModule_currentIndexChanged(int)")      
    def on_cmbBoxAppModule_currentIndexChanged(self, idx):
        """Fill out the model name combobox with all interlis models you can use with a specific module.
        """
        self.cmbBoxIliModelName.clear()        
        module_data = self.cmbBoxAppModule.itemData(idx)
        
        if module_data:
            ilimodels = module_data["ilimodels"]
            
            self.app_module = module_data["dirname"]
            self.app_module_name = self.cmbBoxAppModule.currentText()

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
            self.app_module = ""
            self.app_module_name = ""
            
    @pyqtSignature("on_cmbBoxIliModelName_currentIndexChanged(int)")      
    def on_cmbBoxIliModelName_currentIndexChanged(self, idx):
        """Fill out the reference frame lineedit (read only). 
        """
        module_data = self.cmbBoxIliModelName.itemData(idx)

        if module_data:
            self.ili = module_data["ilimodel"]
            self.epsg = module_data["epsg"]
            reference_frame = module_data["referenceframe"]
            self.lineEditRefFrame.setText(str(reference_frame) + " (EPSG:" + str(self.epsg) + ")")
        else:
            self.ili = ""
            self.epsg = ""
            self.lineEditRefFrame.clear()

    @pyqtSignature("on_btnBrowseInputFile_clicked()")    
    def on_btnBrowseInputFile_clicked(self):
        file = QFileDialog.getOpenFileName(self, self.tr("Choose interlis transfer file"), self.input_itf_path,  "ITF (*.itf *.ITF)")
        fileInfo = QFileInfo(file)
        self.lineEditInputFile.setText(fileInfo.absoluteFilePath())

    def accept(self):
        """Collecting all the stuff we need to know to start the import process.
        """
        # Save the settings.
        self.settings.setValue("file/import/input_itf_path", self.lineEditInputFile.text())
        self.settings.setValue("file/import/ili", self.ili)

        # Check if project name (db schema) already exists.
        project_name =  self.lineEditDbSchema.text().strip()
        if len(project_name) > 0:
            project_found = self.check_project_name(project_name)
            
            if project_found == -1:
                message = "An error occured while connecting the database."
                QMessageBox.critical(None, "VeriSO", self.tr(message))
                return
            
            elif project_found == 1:
                message = "Project name already exists."
                QMessageBox.warning(None, "VeriSO", self.tr(message))
                QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.WARNING)             
                return
        
        # Gather all data/information for ili2pg arguments.
        self.itf = self.lineEditInputFile.text().strip()
        self.db_schema = self.lineEditDbSchema.text().strip()
    
        self.data_date = self.dateTimeEdit.date().toString("yyyy-MM-dd")
        
        self.notes = self.textEditNotes.toPlainText().strip()
        if len(self.notes) > 10000:
            message = "Notes are to big (allowed 10000 characters): "
            QMessageBox.critical(None, "VeriSO", self.tr(message) + str(len(self.notes)))
            QgsMessageLog.logMessage(str(message) + str(len(self.notes)), "VeriSO", QgsMessageLog.WARNING)                 
            return
        
        self.db_host = self.settings.value("options/db/host")
        self.db_name = self.settings.value("options/db/name")
        self.db_port = self.settings.value("options/db/port")
        self.db_user = self.settings.value("options/db/user")
        self.db_pwd = self.settings.value("options/db/pwd")
        self.db_admin = self.settings.value("options/db/admin")
        self.db_admin_pwd = self.settings.value("options/db/adminpwd")

        self.projects_database = self.settings.value("options/general/projects_database", "") 
        self.projects_root_directory = self.settings.value("options/general/projects_root_directory", "") 
        
        import_jar = self.settings.value("options/import/jar", "") 
        import_vm_arguments = self.settings.value("options/import/vm_arguments", "") 
        
        # Check if we have everything we need.
        if not os.path.isfile(self.projects_database) and self.projects_database <> "":
            QMessageBox.warning(None, "VeriSO", self.tr("Projects database not found: ") + str(self.projects_database))                        
            return
        
        if self.itf == "":
            QMessageBox.warning(None, "VeriSO", self.tr("No Interlis transfer file set."))                                    
            return
        
        if self.ili == "":
            QMessageBox.warning(None, "VeriSO", self.tr("No Interlis model name set."))                                    
            return
            
        if self.db_schema == "":
            QMessageBox.warning(None, "VeriSO", self.tr("No project name set."))                                    
            return
            
        if self.cmbBoxAppModule.currentIndex() == 0:
            QMessageBox.warning(None, "VeriSO", self.tr("No application module chosen."))                                    
            return
            
        if not self.db_host:
            QMessageBox.warning(None, "VeriSO", self.tr("Missing database host parameter."))
            return
        
        if not self.db_name:
            QMessageBox.warning(None, "VeriSO", self.tr("Missing database name parameter."))
            return

        if not self.db_port:
            QMessageBox.warning(None, "VeriSO", self.tr("Missing database port parameter."))
            return
            
        if not self.db_user:
            QMessageBox.warning(None, "VeriSO", self.tr("Missing database user parameter."))
            return

        if not self.db_pwd:
            QMessageBox.warning(None, "VeriSO", self.tr("Missing database password parameter."))
            return

        if not self.db_admin:
            QMessageBox.warning(None, "VeriSO", self.tr("Missing database administrator parameter."))
            return
            
        if not self.db_admin_pwd:
            QMessageBox.warning(None, "VeriSO", self.tr("Missing database administrator password parameter."))
            return
            
        if self.projects_root_directory == "":
            QMessageBox.warning(None, "VeriSO", self.tr("No root directory for projects set."))                                                
            return
            
        if self.projects_database == "":
            QMessageBox.information(None, "VeriSO", self.tr("No projects database found. Will create one in the project root directory."))
            
        if import_jar == "":
            QMessageBox.warning(None, "VeriSO", self.tr("No jar file set for import."))            
            return
        
        self.textEditImportOutput.clear()
         
        # Set all the arguments for ili2pg.
        arguments = []
        
        vm_arguments_list = import_vm_arguments.split(" ")
        for i in range(len(vm_arguments_list)):
            arguments.append(vm_arguments_list[i])
            
        arguments.append("-jar")
        arguments.append(import_jar)
        arguments.append("--import")
        arguments.append("--dbhost")
        arguments.append(self.db_host)
        arguments.append("--dbport")
        arguments.append(self.db_port)
        arguments.append("--dbdatabase")
        arguments.append(self.db_name)
        arguments.append("--dbschema")
        arguments.append(self.db_schema)
        arguments.append("--dbusr")
        arguments.append(self.db_admin)
        arguments.append("--dbpwd")
        arguments.append(self.db_admin_pwd)
        arguments.append("--modeldir")
        arguments.append("http://www.catais.org/models/;http://models.geo.admin.ch/")
        arguments.append("--models")
        arguments.append(self.ili)
        arguments.append("--defaultSrsAuth")
        arguments.append("EPSG")
        arguments.append("--defaultSrsCode")
        arguments.append(self.epsg)
        # TODO: ili2pg has a lot of  options. At least some of them should be exposed to the user.
        arguments.append("--t_id_Name")
        arguments.append("ogc_fid")
        arguments.append("--importTid")
        arguments.append("--createGeomIdx")
        arguments.append("--createEnumTabs")
        #arguments.append("--createEnumTxtCol")
        arguments.append("--nameByTopic")
        arguments.append("--strokeArcs")
        arguments.append(self.itf)
        
        self.process = QProcess()
        self.connect(self.process, SIGNAL("readyReadStandardOutput()"), self.read_output)
        self.connect(self.process, SIGNAL("readyReadStandardError()"), self.read_error)
        self.connect(self.process, SIGNAL("finished(int)"), self.finish_import)     
     
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.buttonBox.setEnabled(False)
        try:
            self.process.start("java", arguments)
        except Exception, e:
            self.restore_cursor()
            message = "Could not start import process."
            QMessageBox.critical(None, "VeriSO", self.tr(message))                        
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)                 

    def restore_cursor(self):
        QApplication.restoreOverrideCursor()        
        self.buttonBox.setEnabled(True)

    def read_output(self):
        self.textEditImportOutput.insertPlainText(str(self.process.readAllStandardOutput()))
        self.textEditImportOutput.ensureCursorVisible()        

    def read_error(self):
        self.textEditImportOutput.insertPlainText(str(self.process.readAllStandardError()))        

    def finish_import(self, i):
        # Check if import was successful.
        # This is the simplest method to find out if the import of the data
        # was successfull. 
        # Is there any better idea?
        # Works for:
        # - wrong interlis model
        # - 
        # If schema exists it throws an compiler error?
        output = unicode(self.textEditImportOutput.toPlainText())
        if output.find("Info: ...import done") < 0 or output.find("compiler failed") >= 0:
            self.restore_cursor()                     
            message = "Import process not successfully finished."
            QMessageBox.critical(None, "VeriSO", self.tr(message))
            return
        
        # Get the postprocessing queries that are stored in a sqlite database.
        # Placeholder (e.g. $$DBSCHEMA, $$EPSG etc ) will be replaced.
        sql_queries = self.get_postprocessing_queries()
        if not sql_queries:
            self.restore_cursor()                     
            message = "Something went wrong while catching postprocessing queries from sqlite database. You need to delete the database schema manually."
            QMessageBox.critical(None, "VeriSO", self.tr(message))
            return
            
        # Do the postprocessing in the postgresql database.
        postprocessing_errors = self.postprocess_data(sql_queries)
        if postprocessing_errors <> 0:
            self.restore_cursor()         
            message = "Something went wrong while postprocessing data. You need to delete the database schema manually."
            QMessageBox.critical(None, "VeriSO", self.tr(message))
            return
            
        # Update the projects database    
        updated = self.update_projects_database()
        if not updated:
            self.restore_cursor()         
            message = "Something went wrong while updating projects database. You need to delete the database schema manually."
            QMessageBox.critical(None, "VeriSO", self.tr(message))
            return

        # Create the project directory in the root directory.
        directory = self.create_project_directory()
        if not directory:
            self.restore_cursor()         
            message = "Something went wrong while creating project directory."
            QMessageBox.critical(None, "VeriSO", self.tr(message))
            return

        # When we reach here we can claim a successful import.
        self.restore_cursor()        
        message = "Import process finished."
        QMessageBox.information(None, "VeriSO", self.tr(message))
    
    def create_project_directory(self):
        """Creates a directory with the same name as the project (db schema) 
        in the project root directory. This will be for exports, maps etc.
        It emits a projects database changed signal.
        
        Returns:
          False: If the directory could not be created. Otherwise True.
        """
        try:
            os.makedirs(os.path.join(str(self.projects_root_directory), str(self.db_schema)))
            return True
        except Exception, e:
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)  
            return
            
    def update_projects_database(self):
        """Updates the sqlite projects database.
        
        Returns:
          False: When there an error occured. Otherswise True.
        """
        try:
            # Create a new projects database if there is none (copy one from the templates).
            if self.projects_database == "":
                template = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/templates/template_projects.db"))
                self.projects_database = QDir.convertSeparators(QDir.cleanPath(self.projects_root_directory + "/projects.db"))
                shutil.copyfile(template, self.projects_database)
                self.settings.setValue("options/general/projects_database", self.projects_database)

            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(self.projects_database) 

            if not db.open():
                message = "Could not open projects database."
                QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)            
                QgsMessageLog.logMessage(str(db.lastError().text()), "VeriSO", QgsMessageLog.CRITICAL)            
                return  
             
            project_root_directory = QDir.convertSeparators(QDir.cleanPath(self.projects_root_directory + "/" + str(self.db_schema)))
        
            sql = "INSERT INTO projects (id, displayname, dbhost, dbname, dbport, dbschema, dbuser, dbpwd, dbadmin, dbadminpwd, provider, epsg, ilimodelname, appmodule, appmodulename, projectrootdir, projectdir, datadate, notes, itf) \
VALUES ('"+str(self.db_schema)+"', '"+str(self.db_schema)+"', '"+str(self.db_host)+"', '"+str(self.db_name)+"', "+str(self.db_port)+", '"+str(self.db_schema)+"', '"+str(self.db_user)+"', '"+str(self.db_pwd)+"', \
'"+str(self.db_admin)+"', '"+str(self.db_admin_pwd)+"', 'postgres'," + str(self.epsg) + " , '"+str(self.ili)+"', '"+str(self.app_module)+"','"+unicode(self.app_module_name)+"', '"+str(self.projects_root_directory)+"', '"+project_root_directory+"', '"+self.data_date+"', '"+self.notes+"', '"+self.itf+"');"

            query = db.exec_(sql)
            
            if not query.isActive():
                message = "Error while updating projects database."
                QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)            
                QgsMessageLog.logMessage(str(QSqlQuery.lastError(query).text()), "VeriSO", QgsMessageLog.CRITICAL)      
                return 
            
            db.close()
    
            self.projectsDatabaseHasChanged.emit()
    
            return True
        
        except Exception, e:
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)  
            return

    def postprocess_data(self, queries):
        """Does the postprocessing in the postgresql/postgis database.
        
        Returns:
          -1: If the process fails (e.g. no db connection etc.). Otherwise number of errors occured while postprocessing.
        """
        try:            
            db_host = self.settings.value("options/db/host")
            db_name = self.settings.value("options/db/name")
            db_port = self.settings.value("options/db/port")
            db_admin = self.settings.value("options/db/admin")
            db_admin_pwd = self.settings.value("options/db/adminpwd")
        
            db = QSqlDatabase.addDatabase("QPSQL", "db")
            db.setHostName(db_host)
            db.setPort(int(db_port))
            db.setDatabaseName(db_name)
            db.setUserName(db_admin)
            db.setPassword(db_admin_pwd)
    
            if not db.open():
                message = "Could not open database."
                QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)            
                QgsMessageLog.logMessage(str(db.lastError().driverText()), "VeriSO", QgsMessageLog.CRITICAL)      
                return
                
            errors = 0
            self.textEditImportOutput.insertPlainText(str("\n \n"))            
            for sql in queries:
                self.textEditImportOutput.insertPlainText(str(sql) + str("\n \n"))
                self.textEditImportOutput.ensureCursorVisible()                
                
                query = db.exec_(str(sql))
                
                if not query.isActive():
                    errors += 1
                    message = "Error while postprocessing data:"
                    QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)            
                    QgsMessageLog.logMessage(str(QSqlQuery.lastError(query).text()), "VeriSO", QgsMessageLog.CRITICAL)      
                
            self.textEditImportOutput.insertPlainText("Info: ...postprocessing done")
            self.textEditImportOutput.ensureCursorVisible()                

            db.close
            del db
            
            return errors
            
        except Exception, e:
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)     
            return -1

    def get_postprocessing_queries(self):
        """Gets the SQL queries that are stored in the sqlite database for the postprocessing process which is done in postgis.
        
        Language support: Everything that is not french or italian will be german.
        
        Returns:
          False: If the queries could not be fetched from the sqlite database. Otherwise a list with the SQL queries.
        """
        filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/"+self.app_module+"/postprocessing/postprocessing.db"))
        try:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(filename) 

            if not db.open():
                message = "Could not open database."
                QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)            
                QgsMessageLog.logMessage(str(db.lastError().driverText()), "VeriSO", QgsMessageLog.CRITICAL)                      
                return
                
            
            locale = QSettings().value('locale/userLocale')[0:2]
            if locale == "fr":
                lang = locale
            elif locale == "it":
                lang = locale
            else:
                lang = "de"

            sql = "SELECT * FROM postprocessing WHERE (lang = '" + lang + "' OR lang IS NULL) AND apply = 1 ORDER BY 'order', ogc_fid;"
            print sql
            query = db.exec_(sql)
            
            if not query.isActive():
                message = "Database query not active."
                QgsMessageLog.logMessage(str(message), "VeriSO", QgsMessageLog.CRITICAL)        
                QgsMessageLog.logMessage(str(QSqlQuery.lastError(query).text()), "VeriSO", QgsMessageLog.CRITICAL)                      
                return
                
            queries = []
            record = query.record()
            while query.next():
                sql_query = str(query.value(record.indexOf("sql_query")))
                
                sql_query = sql_query.replace("$$DBSCHEMA", self.db_schema)
                sql_query = sql_query.replace("$$USER", self.db_user)
                sql_query = sql_query.replace("$$EPSG", self.epsg)
                
                queries.append(sql_query)
                
            db.close()
            del db
            
            return queries
            
        except Exception, e:
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)     
            return

    def tr(self, message):
        return QCoreApplication.translate('VeriSO', message)
