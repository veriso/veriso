# coding=utf-8
from __future__ import absolute_import, print_function

import os, sys
import shutil
import tempfile
from builtins import next, range, str
from qgis.PyQt.QtCore import QDateTime, QDir, QFileInfo, \
    QProcess, QRegExp, QSettings, Qt, pyqtSignal, pyqtSignature, pyqtSlot, \
    QTextCodec, QPyNullVariant
from qgis.PyQt.QtGui import QRegExpValidator
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import QApplication, QDialog, QDialogButtonBox, \
    QFileDialog
from qgis.core import QgsApplication, QgsMessageLog

from qgis.gui import QgsMessageBar

from veriso.base.utils.utils import (open_psql_db, open_sqlite_db,
                                     get_projects_db, get_modules_dir,
                                     yaml_load_file, tr,
                                     get_subdirs, jre_version, get_ui_class,
                                     db_user_has_role, get_absolute_path,
                                     win_which, get_default_db)
from veriso.base.utils.exceptions import VerisoError


FORM_CLASS = get_ui_class('importproject.ui')


class ImportProjectDialog(QDialog, FORM_CLASS):
    projectsDatabaseHasChanged = pyqtSignal()

    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()

        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.okButton.setText("Import")

        self.settings = QSettings("CatAIS", "VeriSO")
        self.input_itf_path = QFileInfo(
                self.settings.value(
                        "file/import/input_itf_path")).absolutePath()

        # members
        self.modules = None
        self.app_module = None
        self.app_module_name = None
        self.ili = None
        self.epsg = None
        self.itf = None
        self.data_date = None
        self.notes = None
        self.db_host = None
        self.db_name = None
        self.db_schema = None
        self.db_port = None
        self.db_user = None
        self.db_pwd = None
        self.db_admin = None
        self.db_admin_pwd = None
        self.projects_database = None
        self.max_scale = None
        self.projects_root_directory = None
        self.process = None
        self.ignore_postprocessing_errors = False
        self.ignore_ili2pg_errors = False

    def init_gui(self):
        """Initialize the dialog:
        Set the current date.
        Accept only lower characters as project name (= database schema).
        Fill modules combobox.
        """
        today = QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(today)
        self.dateTimeEdit.setCalendarPopup(True)

        # You are only allowed to use lower case characters as project name (
        # = database schema).
        self.lineEditDbSchema.setValidator(
                QRegExpValidator(QRegExp("^[a-z][a-z0-9_]+"),
                                 self.lineEditDbSchema))

        # Fill out the modules combobox.
        try:
            modules_dir = os.path.join(get_modules_dir())
            modules = []

            for module_name in get_subdirs(modules_dir):
                module_file = os.path.join(
                        modules_dir, module_name, 'module.yml')
                if os.path.isfile(module_file):
                    module = yaml_load_file(module_file)
                    module['dirname'] = module_name
                    modules.append(module)

            if modules:
                sorted_modules_list = sorted(modules,
                                             key=lambda k: k['displayname'])
                self.cmbBoxAppModule.clear()
                for module in sorted_modules_list:
                    self.cmbBoxAppModule.addItem(
                            str(module["displayname"]), module)
                self.cmbBoxAppModule.insertItem(0, "", None)
                self.cmbBoxAppModule.setCurrentIndex(0)
        except Exception as e:
            message = "Error while parsing the available modules."
            self.message_bar.pushMessage("VeriSO", tr(message),
                                         QgsMessageBar.CRITICAL, duration=0)
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)
            return

        self.cmbBoxIliModelName.insertItem(0, "", None)

        return True

    # noinspection PyPep8Naming
    @pyqtSignature("on_btnProjectName_clicked()")
    def on_btnProjectName_clicked(self):
        """Check wether the project (=database schema) already exists.
        """
        project_name = self.lineEditDbSchema.text().strip()

        if len(project_name) <= 0:
            self.lineEditDbSchema.setPlaceholderText(
                    tr('Enter a valid name'))
        else:
            project_found = self.check_project_name(project_name)

            if project_found == -1:
                message = "An error occured while connecting the database."
                self.message_bar.pushMessage("VeriSO", tr(message),
                                             QgsMessageBar.CRITICAL, duration=0)
                return

            elif project_found == 1:
                message = "Project name already exists."
                self.message_bar.pushWarning("VeriSO", tr(message))
                return

            elif project_found == 0:
                message = "Project name is valid."
                self.message_bar.pushSuccess("VeriSO", tr(message))
                return True

    def check_project_name(self, project_name):
        """Makes a database request and checks if the given schema already
        exists.
        
        Returns:
            -1 if an error occured. 0 if schema was not found. 1 if schema
            already exists.
        """

        self.db_host = self.settings.value("options/db/host")
        self.db_name = self.settings.value("options/db/name")
        self.db_port = self.settings.value("options/db/port")
        self.db_user = self.settings.value("options/db/user")
        self.db_pwd = self.settings.value("options/db/pwd")
        self.db_admin = self.settings.value("options/db/admin")
        self.db_admin_pwd = self.settings.value("options/db/adminpwd")

        # 'public' will not be found with the query.
        if project_name == "public":
            return 1

        try:
            db = open_psql_db(self.db_host, self.db_name, self.db_port,
                              self.db_admin, self.db_admin_pwd)

            sql = "SELECT schema_name FROM information_schema.schemata WHERE " \
                  "schema_name = '%s';" % self.lineEditDbSchema.text().strip()
            query = db.exec_(sql)

            if query.isActive():
                count = query.size()
                db.close
                del db

                if count > 0:
                    return 1
                else:
                    return 0

        except Exception as e:
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)
            return -1

    # noinspection PyPep8Naming
    @pyqtSignature("on_cmbBoxAppModule_currentIndexChanged(int)")
    def on_cmbBoxAppModule_currentIndexChanged(self, idx):
        """Fill out the model name combobox with all interlis models you can
        use with a specific module.
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
                self.cmbBoxIliModelName.insertItem(
                        self.cmbBoxIliModelName.count(), str(model_name),
                        ilimodels[i])
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

        self.on_max_scale_check_toggled(self.max_scale_check.isChecked())

    # noinspection PyPep8Naming,PyPep8Naming
    @pyqtSignature("on_cmbBoxIliModelName_currentIndexChanged(int)")
    def on_cmbBoxIliModelName_currentIndexChanged(self, idx):
        """Fill out the reference frame lineedit (read only). 
        """
        module_data = self.cmbBoxIliModelName.itemData(idx)

        if module_data:
            self.ili = module_data["ilimodel"]
            self.epsg = module_data["epsg"]
            reference_frame = module_data["referenceframe"]
            self.lineEditRefFrame.setText(
                    str(reference_frame) + " (EPSG:" + str(self.epsg) + ")")
        else:
            self.ili = ""
            self.epsg = ""
            self.lineEditRefFrame.clear()

    # noinspection PyPep8Naming,PyPep8Naming
    @pyqtSignature("on_btnBrowseInputFile_clicked()")
    def on_btnBrowseInputFile_clicked(self):
        file_path = QFileDialog.getOpenFileName(
                self,
                tr("Choose interlis transfer file"),
                self.input_itf_path,
                "ITF (*.itf *.ITF)")
        file_info = QFileInfo(file_path)
        self.lineEditInputFile.setText(file_info.absoluteFilePath())

    # noinspection PyPep8Naming,PyPep8Naming
    @pyqtSlot(bool)
    def on_max_scale_check_toggled(self, enable):
        """Fill out the reference frame lineedit (read only).
        """
        db_user = self.settings.value("options/db/user")
        max_scale_role = self.get_module_allow_max_scale_role()
        if enable and (max_scale_role is None
                       or db_user_has_role(db_user, max_scale_role)):
            self.max_scale_value.setEnabled(True)
        else:
            self.max_scale_value.setEnabled(False)
            self.max_scale_value.setValue(1000)

    def get_module_allow_max_scale_role(self):
        """
        if a module.yml include a can_configure_max_scale_role list this
        method will behave as following:
        - no can_configure_max_scale_role list declared: all users can set
        the map scale in the importer.
        - can_configure_max_scale_role declared but empty: no user can set
        the map scale in the importer.
        - usernames in the list: these users can set the map scale in the
        importer.
        :return:
        """
        data = self.cmbBoxAppModule.itemData(
                self.cmbBoxAppModule.currentIndex())
        try:
            return data['can_configure_max_scale_role']
        except (KeyError, TypeError):
            return None

    def accept(self):
        """Collecting all the stuff we need to know to start the import process.
        """
        # Save the settings.
        self.settings.setValue("file/import/input_itf_path",
                               self.lineEditInputFile.text())
        self.settings.setValue("file/import/ili", self.ili)

        # Check if project name (db schema) already exists.
        project_name = self.lineEditDbSchema.text().strip()
        if len(project_name) > 0:
            project_found = self.check_project_name(project_name)

            if project_found == -1:
                message = "An error occured while connecting the database."
                self.message_bar.pushMessage("VeriSO", tr(message),
                                             QgsMessageBar.CRITICAL, duration=0)
                return

            elif project_found == 1:
                message = "Project name already exists."
                self.message_bar.pushWarning("VeriSO", tr(message))
                QgsMessageLog.logMessage(tr(message), "VeriSO",
                                         QgsMessageLog.WARNING)
                return

        # Gather all data/information for ili2pg arguments.
        self.itf = self.lineEditInputFile.text().strip()
        self.db_schema = self.lineEditDbSchema.text().strip()

        self.data_date = self.dateTimeEdit.date().toString("yyyy-MM-dd")

        self.notes = self.textEditNotes.toPlainText().strip()
        if len(self.notes) > 10000:
            message = "Notes are to big (allowed 10000 characters): "
            self.message_bar.pushMessage("VeriSO",
                                         tr(message) + str(
                                                 len(self.notes)),
                                         QgsMessageBar.CRITICAL, duration=0)
            QgsMessageLog.logMessage(str(message) + str(len(self.notes)),
                                     "VeriSO", QgsMessageLog.WARNING)
            return

        self.projects_database = self.settings.value(
                "options/general/projects_database", "")
        if type(self.projects_database) == QPyNullVariant:
            self.projects_database = ""
        self.projects_root_directory = self.settings.value(
                "options/general/projects_root_directory", "")

        self.use_pg_projects_database = self.settings.value(
            "options/general/use_pg_projects_database", False, type=bool)

        self.ignore_ili2pg_errors = self.settings.value(
            "options/import/ignore_ili2pg_errors", False, type=bool)

        self.ignore_postprocessing_errors = self.settings.value(
            "options/import/ignore_postprocessing_errors", False, type=bool)
        
        import_vm_arguments = self.settings.value("options/import/vm_arguments",
                                                  "")
        # Check if we have everything we need.
        if not os.path.isfile(
                self.projects_database) and self.projects_database != "":
            self.message_bar.pushWarning("VeriSO",
                                         tr(
                                                 "Projects database not "
                                                 "found: ")
                                         + str(
                                                 self.projects_database))
            return

        if self.itf == "":

            # in veriti, if no itf file is set, use a "empty" default itf file
            if self.app_module == 'veriti':
                self.itf = os.path.dirname(__file__)+"/../../modules/veriti/varia/default.itf"
                self.settings.setValue("file/import/input_itf_path","/")
            else:
                self.message_bar.pushWarning("VeriSO",
                                         tr(
                                                 "No Interlis transfer file "
                                                 "set."))
                return

        if self.ili == "":
            self.message_bar.pushWarning("VeriSO",
                                         tr("No Interlis model name set."))
            return

        if self.db_schema == "":
            self.message_bar.pushWarning("VeriSO",
                                         tr("No project name set."))
            return

        if self.cmbBoxAppModule.currentIndex() == 0:
            self.message_bar.pushWarning("VeriSO",
                                         tr(
                                                 "No application module "
                                                 "chosen."))
            return

        if not self.db_host:
            self.message_bar.pushWarning("VeriSO",
                                         tr(
                                                 "Missing database host "
                                                 "parameter."))
            return

        if not self.db_name:
            self.message_bar.pushWarning("VeriSO",
                                         tr(
                                                 "Missing database name "
                                                 "parameter."))
            return

        if not self.db_port:
            self.message_bar.pushWarning("VeriSO",
                                         tr(
                                                 "Missing database port "
                                                 "parameter."))
            return

        if not self.db_user:
            self.message_bar.pushWarning("VeriSO",
                                         tr(
                                                 "Missing database user "
                                                 "parameter."))
            return

        if not self.db_pwd:
            self.message_bar.pushWarning("VeriSO",
                                         tr(
                                                 "Missing database password "
                                                 "parameter."))
            return

        if not self.db_admin:
            self.message_bar.pushWarning("VeriSO", tr(
                    "Missing database administrator parameter."))
            return

        if not self.db_admin_pwd:
            self.message_bar.pushWarning("VeriSO", tr(
                    "Missing database administrator password parameter."))
            return

        if self.projects_root_directory == "":
            self.message_bar.pushWarning("VeriSO",
                                         tr(
                                                 "No root directory for "
                                                 "projects "
                                                 "set."))
            return

        if self.projects_database == "":
            self.message_bar.pushInfo("VeriSO", tr(
                    "No projects database found. Will create one in the "
                    "project root directory."))

        if jre_version() is None:
            self.message_bar.pushWarning("VeriSO",
                                         tr("No java runtime detected."))
            return

        max_scale_role = self.get_module_allow_max_scale_role()
        self.max_scale = 0
        if self.max_scale_check.isChecked():
            if db_user_has_role(self.db_user, max_scale_role):
                self.max_scale = self.max_scale_value.value()
            else:
                self.max_scale = 1000

        self.textEditImportOutput.clear()

        # Set all the arguments for ili2pg.
        arguments = []

        vm_arguments_list = import_vm_arguments.split(" ")
        for arg in vm_arguments_list:
            arguments.append(arg)

        import_jar = os.path.dirname(__file__)+'/../../lib/ili2pg-3.6.1/ili2pg.jar'              

        arguments.append("-Duser.country=CH")
        arguments.append("-Duser.language=de")

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
        model_dir = ';'.join(self.settings.value(
                "options/model_repositories/repositories"))
        arguments.append(model_dir)
        arguments.append("--models")
        arguments.append(self.ili)
        arguments.append("--defaultSrsAuth")
        arguments.append("EPSG")
        arguments.append("--defaultSrsCode")
        arguments.append(self.epsg)
        # TODO: ili2pg has a lot of  options. At least some of them should be
        #  exposed to the user.
        arguments.append("--t_id_Name")
        arguments.append("ogc_fid")
        arguments.append("--importTid")
        arguments.append("--createGeomIdx")
        if self.app_module == 'veriti':
            arguments.append("--createEnumTabs")
            arguments.append("--createFk")
        else:
            arguments.append("--createEnumColAsItfCode")
            arguments.append("--createEnumTxtCol")
        arguments.append("--nameByTopic")
        arguments.append("--strokeArcs")

        # Translate itf file for VeriVD
        if self.app_module == 'verivd':
            from veriso.opengisch_utils.interlis.itf_translator \
                .itf_translator_MD01MOVD import ITFTranslatorMD01MOVD

            translator = ITFTranslatorMD01MOVD(self.itf)
            tmp_translated_itf = tempfile.NamedTemporaryFile(
                prefix='verivd_', suffix='.itf', delete=False)
            tmp_translated_itf.close()
            print(tmp_translated_itf.name)

            translator.translate(
                tmp_translated_itf.name,
                translator.LANGUAGE_FR,
                translator.LANGUAGE_DE
            )
            arguments.append(tmp_translated_itf.name)
        else:
            arguments.append(self.itf)

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_error)
        self.process.finished.connect(self.finish_import)

        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.buttonBox.setEnabled(False)
        self.report_progress("Info: Starting ili2pg")
        self.report_progress("Info: java %s" % ' '.join(arguments))

        try:
            if(sys.platform =='win32'):
                j = win_which('java.exe')
                self.process.start(j, arguments)
            else:
                self.process.start("java", arguments)
        except Exception as e:
            self.restore_cursor()
            message = "Could not start import process."
            self.message_bar.pushMessage("VeriSO", tr(message),
                                         QgsMessageBar.CRITICAL, duration=0)
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)

    def restore_cursor(self):
        QApplication.restoreOverrideCursor()
        self.buttonBox.setEnabled(True)

    def read_output(self):
        output = self.process.readAllStandardOutput()
        self.show_output(output)

    def read_error(self):
        error = self.process.readAllStandardError()
        self.show_output(error)

    def show_output(self, byte_array):

        codec = QTextCodec.codecForLocale()
        unicode_text = codec.toUnicode(byte_array)

        self.report_progress(unicode_text)

    def finish_import(self, exit_code):
        """
        Check if import was successful.
        :param exitCode: the exit code of the process
        :return: None
        """
        try:
            # read the output of ili2pg
            self.read_import_output()

            # Get the postprocessing queries that are stored in a sqlite
            # database.
            # Placeholder (e.g. $$DBSCHEMA, $$EPSG etc ) will be replaced.
            sql_queries = self.get_postprocessing_queries()

            # Do the postprocessing in the postgresql database.
            self.postprocess_data(sql_queries)

            # Update the projects database
            self.update_projects_database()

            # Create the project directory in the root directory.
            directory = self.create_project_directory()

        except VerisoError as e:
            self.message_bar.pushMessage("VeriSO", tr(str(e)),
                                         QgsMessageBar.CRITICAL, duration=0)
            return
        finally:
            self.restore_cursor()

        # When we reach here we can claim a successful import.
        message = "Import process finished."
        self.report_progress(message, 'green')
        self.message_bar.pushInfo("VeriSO", tr(message))

    def read_import_output(self):
        """
        Reads the output of the ili2pg conversion
        :return:
        """
        output = self.textEditImportOutput.toPlainText()
        if (not self.ignore_ili2pg_errors) and (
                output.find("Info: ...import done") < 0 or output.find(
                "compiler failed") >= 0):
            message = "Import process not successfully finished."
            raise VerisoError(message)

    def create_project_directory(self):
        """Creates a directory with the same name as the project (db schema)
        in the project root directory. This will be for exports, maps etc.
        It emits a projects database changed signal.

        Returns:
          False: If the directory could not be created. Otherwise True.
        """
        try:
            os.makedirs(os.path.join(str(self.projects_root_directory),
                                     str(self.db_schema)))
            return True
        except Exception as e:
            message = "Something went wrong while creating project directory."
            raise VerisoError(message, e)

    def update_projects_database(self):
        if self.use_pg_projects_database:
            return self.update_projects_database_pg()
        return self.update_projects_database_sqlite()

    def update_projects_database_pg(self):
        """Updates the postgres projects database.

        Returns:
           False: When there an error occured. Otherswise True.
        """

        error_message = ("Something went wrong while updating projects "
                         "database. You need to delete the database schema "
                         "manually.")

        try:
            # Create a new projects database (schema and table on pg) if there is none

            table_exists = False
            schema_exists = False

            db = get_default_db()

            sql = "SELECT 1 FROM pg_namespace " \
                  "WHERE nspname = 'veriso_conf'"
            query = db.exec_(sql)

            if query.size() > 0:
                schema_exists = True

                sql = "SELECT 1 FROM   pg_tables " \
                      "WHERE  schemaname = 'veriso_conf' AND tablename = 'project'"
                query = db.exec_(sql)
                if query.size() > 0:
                    table_exists = True

            if not schema_exists:
                sql = "CREATE SCHEMA veriso_conf"
                query = db.exec_(sql)

            if not table_exists:
                sql = "CREATE TABLE veriso_conf.project (" \
                      "ogc_fid serial primary key, " \
                      "id character varying, " \
                      "displayname character varying," \
                      "provider character varying, " \
                      "epsg integer, " \
                      "ilimodelname character varying, " \
                      "appmodule character varying, " \
                      "appmodulename character varying, " \
                      "datadate timestamp, " \
                      "notes character varying, " \
                      "itf character varying, " \
                      "max_scale integer default 0 " \
                      ")"
                query = db.exec_(sql)

            values = (
                self.db_schema,
                self.db_schema,
                self.epsg,
                self.ili,
                self.app_module,
                self.app_module_name,
                self.data_date,
                self.notes,
                self.itf,
                self.max_scale
            )
            values = "VALUES ( "\
                     "'%s', '%s', 'postgres', '%s', '%s', '%s', '%s', '%s', " \
                     "'%s', '%s', '%s')" % values

            sql = "INSERT INTO veriso_conf.project (id, displayname, " \
                  "provider, epsg, ilimodelname, appmodule, appmodulename, " \
                  "datadate, notes, itf, " \
                  "max_scale)" + values

            query = db.exec_(sql)

            if not query.isActive():
                message = "Error while updating projects database."
                raise VerisoError(message, long_message=QSqlQuery.lastError(
                        query).text())

            db.close()

            self.projectsDatabaseHasChanged.emit()

            return True

        except Exception as e:
            raise VerisoError(error_message, e)

    def update_projects_database_sqlite(self):
        """Updates the sqlite projects database.
        
        Returns:
          False: When there an error occured. Otherswise True.
        """
        error_message = ("Something went wrong while updating projects "
                         "database. You need to delete the database schema "
                         "manually.")

        try:
            # Create a new projects database if there is none (copy one from
            # the templates).
            if self.projects_database == "":
                template = get_absolute_path(
                        "templates/template_projects.db")
                self.projects_database = QDir.convertSeparators(QDir.cleanPath(
                        self.projects_root_directory + "/projects.db"))
                shutil.copyfile(template, self.projects_database)
                self.settings.setValue("options/general/projects_database",
                                       self.projects_database)

            db = get_projects_db()

            project_root_directory = QDir.convertSeparators(QDir.cleanPath(
                    self.projects_root_directory + "/" + str(self.db_schema)))

            values = (
                self.db_schema,
                self.db_schema,
                self.db_host,
                self.db_name,
                self.db_port,
                self.db_schema,
                self.db_user,
                self.db_pwd,
                self.db_admin,
                self.db_admin_pwd,
                self.epsg,
                self.ili,
                self.app_module,
                self.app_module_name,
                self.projects_root_directory,
                project_root_directory,
                self.data_date,
                self.notes,
                self.itf,
                self.max_scale
            )
            values = "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                     "'%s', '%s', 'postgres', '%s', '%s', '%s', '%s', '%s', " \
                     "'%s', '%s', '%s', '%s', '%s')" % values

            sql = "INSERT INTO projects (id, displayname, dbhost, dbname, " \
                  "dbport, dbschema, dbuser, dbpwd, dbadmin, dbadminpwd, " \
                  "provider, epsg, ilimodelname, appmodule, appmodulename, " \
                  "projectrootdir, projectdir, datadate, notes, itf, " \
                  "max_scale)" + values

            query = db.exec_(sql)

            if not query.isActive():
                message = "Error while updating projects database."
                raise VerisoError(message, long_message=QSqlQuery.lastError(
                        query).text())

            db.close()

            self.projectsDatabaseHasChanged.emit()

            return True
        except Exception as e:
            raise VerisoError(error_message, e)

    def postprocess_data(self, queries):
        """Does the postprocessing in the postgresql/postgis database.

        Returns:
          -1: If the process fails (e.g. no db connection etc.). Otherwise
          number of errors occured while postprocessing.
        """
        try:
            db = open_psql_db(self.db_host, self.db_name, self.db_port,
                              self.db_admin, self.db_admin_pwd)
            errors = 0
            self.report_progress("\n\nInfo: Starting postprocessing...")
            for sql in queries:
                self.report_progress("\n\n%s" % sql)

                query = db.exec_(str(sql))

                if not query.isActive():
                    errors += 1
                    message = "Error while postprocessing data:"
                    QgsMessageLog.logMessage(tr(message), "VeriSO",
                                             QgsMessageLog.CRITICAL)
                    QgsMessageLog.logMessage(
                            str(QSqlQuery.lastError(query).text()) + str(sql), "VeriSO",
                            QgsMessageLog.CRITICAL)
                    self.report_progress("--> error, see log", 'orange')

            if errors > 0:
                self.report_progress(
                        "Error: ...postprocessing completed with errors",
                        "red"
                )
                if not self.ignore_postprocessing_errors:
                    raise Exception()
            self.report_progress("Info: ...postprocessing completed")

            db.close
            del db

        except Exception as e:
            message = "Something went wrong while postprocessing data. You " \
                      "need to delete the database schema manually."
            raise VerisoError(message, e)

    def get_postprocessing_queries(self):
        """Gets the SQL queries that are stored in the sqlite database for
        the postprocessing process which is done in postgis.
        
        Language support: Everything that is not french or italian will be
        german.
        
        Returns:
          False: If the queries could not be fetched from the sqlite
          database. Otherwise a list with the SQL queries.
        """
        path = "modules/%s/postprocessing/postprocessing.db" % self.app_module
        filename = get_absolute_path(path)

        self.report_progress("Info: getting postprocessing queries...")

        try:
            # This is NOT the project db
            connection_name = 'postprocessing_' + self.app_module
            db = open_sqlite_db(filename, connection_name)

            locale = QSettings().value('locale/userLocale')[0:2]
            if locale == "fr":
                lang = locale
            elif locale == "it":
                lang = locale
            else:
                lang = "de"

            sql = "SELECT * FROM postprocessing " \
                  "WHERE (lang = '%s' " \
                  "OR lang IS NULL) AND apply = 1 " \
                  "ORDER BY 'order', ogc_fid;" % lang

            query = db.exec_(sql)

            if not query.isActive():
                message = "Database query not active."
                raise VerisoError(message, long_message=QSqlQuery.lastError(
                        query).text())

            queries = []
            record = query.record()
            while next(query):
                sql_query = str(query.value(record.indexOf("sql_query")))

                sql_query = sql_query.replace("$$DBSCHEMA", self.db_schema)
                sql_query = sql_query.replace("$$USER", self.db_user)
                sql_query = sql_query.replace("$$EPSG", self.epsg)

                queries.append(sql_query)

            db.close()
            del db

            return queries

        except Exception as e:
            message = "Something went wrong while catching postprocessing " \
                      "queries from sqlite database. You need to delete the " \
                      "database schema manually."

            raise VerisoError(message, e)

    def report_progress(self, text, color=None):
        """
        Print the text in the output window
        :param text: str
        :return: None
        """

        if color is None:
            if text.lower().startswith('warning'):
                color = 'orange'
            elif text.lower().startswith('error'):
                color = 'red'
            elif text.lower().startswith('info'):
                color = 'blue'

        if color is not None:
            self.textEditImportOutput.appendHtml(
                    "<span style='color:%s'>%s</span>" % (color, text))
        else:
            self.textEditImportOutput.appendPlainText(
                    "%s\n" % text.rstrip("\n "))
        self.textEditImportOutput.ensureCursorVisible()
