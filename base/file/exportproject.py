# coding=utf-8
from __future__ import absolute_import

import os, sys
import shutil
from builtins import str
from qgis.PyQt.QtCore import Qt, pyqtSignal, QSettings, pyqtSignature, QFileInfo, \
    QProcess
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import QApplication, QDialog, QDialogButtonBox, \
    QFileDialog
from qgis.gui import QgsMessageBar
from qgis.core import QgsApplication, QgsMessageLog

from veriso.base.utils.utils import open_psql_db, get_projects_db, \
    get_projects, tr, get_ui_class, jre_version, win_which
from veriso.base.utils.exceptions import VerisoError

FORM_CLASS = get_ui_class('exportproject.ui')


class ExportProjectDialog(QDialog, FORM_CLASS):
    projectsDatabaseHasChanged = pyqtSignal()

    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.okButton.setText("Export")
        self.settings = QSettings("CatAIS", "VeriSO")

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
        self.db_port = None
        self.db_schema = None
        self.db_admin = None
        self.db_admin_pwd = None
        self.project_index = None
        self.projects = None
        self.db_user = None
        self.db_pwd = None

    def init_gui(self):
        projects = get_projects()

        self.cBoxProject.clear()

        if not projects:
            return

        self.projects = projects
        sorted_projects = sorted(self.projects, key=lambda k: k['displayname'])

        for project in sorted_projects:
            self.cBoxProject.addItem(str(project["displayname"]),
                                     project["dbschema"])

        self.cBoxProject.insertItem(0, "", None)
        self.cBoxProject.setCurrentIndex(0)

        return True

    # noinspection PyPep8Naming,PyPep8Naming
    @pyqtSignature("on_btnBrowseOutputFile_clicked()")
    def on_btnBrowseInputFile_clicked(self):
        file_path = QFileDialog.getSaveFileName(
            self,
            tr("Choose interlis transfer file"),
            "",
            #self.input_itf_path,
            "ITF (*.itf *.ITF)")
        file_info = QFileInfo(file_path)
        self.lineEditOutputFile.setText(file_info.absoluteFilePath())

    def accept(self):

        """Collecting all the stuff we need to know to start the import process.
        """
        # Save the settings.
        self.settings.value("file/export/output_itf_path",
                               self.lineEditOutputFile.text())

        # Gather all data/information for ili2pg arguments.
        self.itf = self.lineEditOutputFile.text().strip()

        current_index = self.cBoxProject.currentIndex()
        if current_index == 0:
            return

        db_schema = str(self.cBoxProject.itemData(current_index))

        # Get the connections parameters from the projects list we created in
        #  the init_gui method.
        i = 0
        for project in self.projects:
            if db_schema == str(project["dbschema"]):
                self.db_host = str(project["dbhost"])
                self.db_name = str(project["dbname"])
                self.db_port = str(project["dbport"])
                self.db_schema = db_schema
                self.db_admin = str(project["dbadmin"])
                self.db_admin_pwd = str(project["dbadminpwd"])
                self.app_module = str(project["appmodule"])
                self.app_module_name = str(project["appmodulename"])
                self.db_user = str(project["dbuser"])
                self.db_pwd = str(project["dbpwd"])
                self.ili = str(project["ilimodelname"])
                self.project_index = i
                break
            i += 1

        import_vm_arguments = self.settings.value("options/import/vm_arguments", "")

        # Check if we have everything we need.
        if self.itf == "":
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


        if self.app_module == "":
            self.message_bar.pushWarning("VeriSO",
                                         tr(
                                                 "No application module "
                                                 "set."))
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

        if jre_version() is None:
            self.message_bar.pushWarning("VeriSO",
                                         tr("No java runtime detected."))
            return

        self.textEditExportOutput.clear()

        # Set all the arguments for ili2pg.
        arguments = []

        vm_arguments_list = import_vm_arguments.split(" ")
        for arg in vm_arguments_list:
            arguments.append(arg)

        import_jar = os.path.dirname(__file__) + '/../../lib/ili2pg-3.6.1/ili2pg.jar'

        arguments.append("-jar")
        arguments.append(import_jar)
        arguments.append("--export")
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
            message = "Could not start export process."
            self.message_bar.pushMessage("VeriSO", tr(message),
                                         QgsMessageBar.CRITICAL, duration=0)
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)

    def read_output(self):
        output = self.process.readAllStandardOutput()
        self.show_output(output)

    def read_error(self):
        error = self.process.readAllStandardError()
        self.show_output(error)

    def show_output(self, byte_array):
        if(sys.platform == 'win32'):
            unicode_text = byte_array.data().decode('ISO-8859-1')
        else:
            unicode_text = byte_array.data().decode('utf-8')
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

        except VerisoError as e:
            self.message_bar.pushMessage("VeriSO", tr(str(e)),
                                         QgsMessageBar.CRITICAL, duration=0)
            return
        finally:
            self.restore_cursor()

        # When we reach here we can claim a successful import.
        message = "Export process finished."
        self.report_progress(message, 'green')
        self.message_bar.pushInfo("VeriSO", tr(message))

    def read_import_output(self):
        """
        Reads the output of the ili2pg conversion
        :return:
        """
        output = self.textEditExportOutput.toPlainText()
        if output.find("Info: ...export done") < 0 or output.find(
                "compiler failed") >= 0:
            message = "Export process not successfully finished."
            raise VerisoError(message)

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
            self.textEditExportOutput.appendHtml(
                    "<span style='color:%s'>%s</span>" % (color, text))
        else:
            self.textEditExportOutput.appendPlainText(
                    "%s\n" % text.rstrip("\n "))
        self.textEditExportOutput.ensureCursorVisible()

    def restore_cursor(self):
        QApplication.restoreOverrideCursor()
        self.buttonBox.setEnabled(True)
