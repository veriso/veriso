# -*- coding: utf-8 -*-

import os

from qgis.PyQt.QtCore import (
    QFileInfo, QRegExp, QSettings, pyqtSignal)
from qgis.PyQt.QtGui import QRegExpValidator
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QWidget, QInputDialog, QLineEdit

from veriso.base.utils.utils import open_psql_db, get_projects_db, tr, \
    get_ui_class
from veriso.base.utils.exceptions import VerisoError

FORM_CLASS = get_ui_class('options.ui')


# noinspection PyPep8Naming
class OptionsDialog(QDialog, FORM_CLASS):
    projectsDatabaseHasChanged = pyqtSignal()

    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)

        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.setupUi(self)

        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)

        self.settings = QSettings("CatAIS", "VeriSO")
        self.projects_database = self.settings.value(
            "options/general/projects_database")
        if self.projects_database is not None:
            self.projects_database_path = QFileInfo(
                self.projects_database).absolutePath()
        self.projects_root_directory = self.settings.value(
            "options/general/projects_root_directory")
        self.import_jar = self.settings.value("options/import/jar")
        self.import_jar_path = QFileInfo(self.import_jar).absolutePath()

        self.btnBrowseImportJar.clicked.connect(self.btnBrowseImportJar_clicked)
        self.btnBrowseProjectsDatabase.clicked.connect(
            self.btnBrowseProjectsDatabase_clicked)
        self.btnBrowseProjectsRootDir.clicked.connect(
            self.btnBrowseProjectsRootDir_clicked)
        self.btnTestProjectDB.clicked.connect(self.btnTestProjectDB_clicked)
        self.btnTestConnection.clicked.connect(self.btnTestConnection_clicked)
        self.listWidgetModelRepos.itemSelectionChanged.connect(
            self.listWidgetModelRepos_itemSelectionChanged)
        self.btnDeleteModelRepo.clicked.connect(
            self.btnDeleteModelRepo_clicked)
        self.btnAddModelRepo.clicked.connect(self.btnAddModelRepo_clicked)
        self.btnAddLocalModelRepo.clicked.connect(
            self.btnAddLocalModelRepo_clicked)
        self.btnEditModelRepo.clicked.connect(self.btnEditModelRepo_clicked)

    # noinspection PyPep8Naming
    def init_gui(self):
        self.lineEditDbPort.setValidator(
            QRegExpValidator(QRegExp("[0-9]+"), self.lineEditDbPort))

        if self.projects_database is not None:
            self.lineEditProjectsDatabase.setText(
                self.settings.value("options/general/projects_database"))
        self.lineEditProjectsRootDir.setText(
            self.settings.value("options/general/projects_root_directory"))

        self.lineEditImportJar.setText(
            self.settings.value("options/import/jar"))

        self.chkPgProjectsDb.setChecked(self.settings.value(
            "options/general/use_pg_projects_database", False, type=bool))

        self.chkTopicsTablesMenu.setChecked(self.settings.value(
            "options/general/topics_tables_menu", False, type=bool))

        self.chkIgnoreIli2pgErrors.setChecked(self.settings.value(
            "options/import/ignore_ili2pg_errors", False, type=bool))

        self.chkIgnorePostprocessingErrors.setChecked(self.settings.value(
            "options/import/ignore_postprocessing_errors", False, type=bool))

        vm_arguments = self.settings.value("options/import/vm_arguments")
        if vm_arguments == "" or not vm_arguments or vm_arguments is None:
            self.plainTextEditImportVMArguments.insertPlainText(
                "-Xms128m -Xmx1024m")
        else:
            self.plainTextEditImportVMArguments.insertPlainText(vm_arguments)

        self.lineEditDbHost.setText("")
        self.lineEditDbDatabase.setText("")
        self.lineEditDbPort.setText("")
        self.lineEditDbUser.setText("")
        self.lineEditDbUserPwd.setText("")
        self.lineEditDbAdmin.setText("")
        self.lineEditDbAdminPwd.setText("")

        if self.settings.value("options/db/host") is not None:
            self.lineEditDbHost.setText(self.settings.value("options/db/host"))
        if self.settings.value("options/db/name") is not None:
            self.lineEditDbDatabase.setText(
                self.settings.value("options/db/name"))
        if self.settings.value("options/db/port") is not None:
            self.lineEditDbPort.setText(self.settings.value("options/db/port"))
        if self.settings.value("options/db/user") is not None:
            self.lineEditDbUser.setText(self.settings.value("options/db/user"))
        if self.settings.value("options/db/pwd") is not None:
            self.lineEditDbUserPwd.setText(
                self.settings.value("options/db/pwd"))
        if self.settings.value("options/db/admin") is not None:
            self.lineEditDbAdmin.setText(
                self.settings.value("options/db/admin"))
        if self.settings.value("options/db/adminpwd") is not None:
            self.lineEditDbAdminPwd.setText(
                self.settings.value("options/db/adminpwd"))

        default_repo = ['http://models.geo.admin.ch/',
                        'http://models.geo.be.ch/',
                        'http://models.geo.ti.ch/']

        self.listWidgetModelRepos.insertItems(0, self.settings.value(
            "options/model_repositories/repositories", default_repo))

        QWidget.setTabOrder(self.lineEditDbHost, self.lineEditDbDatabase)
        QWidget.setTabOrder(self.lineEditDbDatabase, self.lineEditDbPort)
        QWidget.setTabOrder(self.lineEditDbPort, self.lineEditDbUser)
        QWidget.setTabOrder(self.lineEditDbUser, self.lineEditDbUserPwd)
        QWidget.setTabOrder(self.lineEditDbUserPwd, self.lineEditDbAdmin)
        QWidget.setTabOrder(self.lineEditDbAdmin, self.lineEditDbAdminPwd)

    def btnBrowseImportJar_clicked(self):
        file_path = QFileDialog.getOpenFileName(
            self, tr("Open import jar file"), self.import_jar_path,
            "jar (*.jar *.JAR)")[0]
        file_info = QFileInfo(file_path)

        self.lineEditImportJar.setText(file_info.absoluteFilePath())

    def btnBrowseProjectsDatabase_clicked(self):
        file_path = QFileDialog.getOpenFileName(self, tr(
            "Choose projects definitions database"),
            self.projects_database_path,
            "SQLite (*.sqlite *.db *.DB)")[0]
        file_info = QFileInfo(file_path)
        self.lineEditProjectsDatabase.setText(file_info.absoluteFilePath())

    def btnBrowseProjectsRootDir_clicked(self):
        dir_path = QFileDialog.getExistingDirectory(self, tr(
            "Choose projects root directory"), self.projects_root_directory)
        dir_info = QFileInfo(dir_path)
        self.lineEditProjectsRootDir.setText(dir_info.absoluteFilePath())

    def test_connection_succes(self):
        self.message_bar.pushSuccess(
            "Success", "Test connection successful")

    def test_connection_failed(self, e):
        self.message_bar.pushCritical(
            "Error", "Test connection failed: " + str(e))

    def btnTestProjectDB_clicked(self):
        try:
            current_path = self.lineEditProjectsDatabase.text()
            db = get_projects_db(current_path)
            db.close()
            self.test_connection_succes()
        except Exception as e:
            self.test_connection_failed(e)

    def btnTestConnection_clicked(self):
        try:
            db = open_psql_db(self.lineEditDbHost.text(),
                              self.lineEditDbDatabase.text(),
                              self.lineEditDbPort.text(),
                              self.lineEditDbAdmin.text(),
                              self.lineEditDbAdminPwd.text())
            sql = "select postgis_full_version();"
            query = db.exec_(sql)
            count = query.size()
            db.close()
            if count < 1:
                raise VerisoError(
                    "No PostGIS found on the DB %s" % db.connectionName())
        except Exception as e:
            self.test_connection_failed(e)
        else:
            self.test_connection_succes()

    def listWidgetModelRepos_itemSelectionChanged(self):
        has_selected = bool(self.listWidgetModelRepos.selectedItems())
        self.btnDeleteModelRepo.setEnabled(has_selected)
        self.btnEditModelRepo.setEnabled(has_selected)

    def btnDeleteModelRepo_clicked(self):
        for item in self.listWidgetModelRepos.selectedItems():
            self.listWidgetModelRepos.takeItem(
                self.listWidgetModelRepos.row(item))

    def ask_url(self, default_text=None):
        text, ok = QInputDialog.getText(
            self,
            tr("Add new model repository"),
            tr("Repository URL:"),
            QLineEdit.Normal,
            default_text)
        return text, ok

    def btnAddModelRepo_clicked(self):
        text, ok = self.ask_url()
        if ok and text:
            self.listWidgetModelRepos.addItem(text)

    def btnAddLocalModelRepo_clicked(self):
        path = QFileDialog.getExistingDirectory(
            self, tr("Open Directory"),
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        if path:
            self.listWidgetModelRepos.addItem(path)

    def btnEditModelRepo_clicked(self):
        item = self.listWidgetModelRepos.currentItem()
        text, ok = self.ask_url(item.text())
        if ok and text:
            item.setText(text)

    def accept(self):
        if self.projects_database is not None:
            self.settings.setValue(
                "options/general/projects_database",
                self.lineEditProjectsDatabase.text().strip())
        else:
            self.settings.setValue("options/general/projects_database", "")

        self.settings.setValue("options/general/projects_root_directory",
                               self.lineEditProjectsRootDir.text().strip())

        self.settings.setValue("options/general/use_pg_projects_database",
                               self.chkPgProjectsDb.isChecked())

        self.projectsDatabaseHasChanged.emit()

        self.settings.setValue("options/general/topics_tables_menu",
                               self.chkTopicsTablesMenu.isChecked())

        self.settings.setValue("options/import/ignore_ili2pg_errors",
                               self.chkIgnoreIli2pgErrors.isChecked())

        self.settings.setValue("options/import/ignore_postprocessing_errors",
                               self.chkIgnorePostprocessingErrors.isChecked())

        self.settings.setValue(
            "options/import/jar", self.lineEditImportJar.text().strip())

        self.settings.setValue(
            "options/import/vm_arguments",
            self.plainTextEditImportVMArguments.toPlainText().strip())

        self.settings.setValue("options/db/host", self.lineEditDbHost.text())
        self.settings.setValue("options/db/name",
                               self.lineEditDbDatabase.text())
        self.settings.setValue("options/db/port", self.lineEditDbPort.text())
        self.settings.setValue("options/db/user", self.lineEditDbUser.text())
        self.settings.setValue("options/db/pwd", self.lineEditDbUserPwd.text())
        self.settings.setValue("options/db/admin", self.lineEditDbAdmin.text())
        self.settings.setValue("options/db/adminpwd",
                               self.lineEditDbAdminPwd.text())

        repos = []
        for index in range(self.listWidgetModelRepos.count()):
            repos.append(self.listWidgetModelRepos.item(index).text())
        self.settings.setValue("options/model_repositories/repositories",
                               repos)
        self.close()
