# -*- coding: utf-8 -*-

from __future__ import absolute_import

from qgis.PyQt.QtCore import (
    QFileInfo, QRegExp, QSettings, pyqtSignal, pyqtSignature)
from qgis.PyQt.QtGui import QRegExpValidator, QInputDialog, QLineEdit
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QWidget

from veriso.base.utils.utils import open_psql_db, get_projects_db, tr
from veriso.base.utils.exceptions import VerisoError

from .Ui_options import Ui_Options


# noinspection PyPep8Naming
class OptionsDialog(QDialog, Ui_Options):
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
        self.projects_database_path = QFileInfo(
                self.projects_database).absolutePath()
        self.projects_root_directory = self.settings.value(
                "options/general/projects_root_directory")
        self.import_jar = self.settings.value("options/import/jar")
        self.import_jar_path = QFileInfo(self.import_jar).absolutePath()

    # noinspection PyPep8Naming
    def init_gui(self):
        self.lineEditDbPort.setValidator(
                QRegExpValidator(QRegExp("[0-9]+"), self.lineEditDbPort))

        self.lineEditProjectsDatabase.setText(
                self.settings.value("options/general/projects_database"))
        self.lineEditProjectsRootDir.setText(
                self.settings.value("options/general/projects_root_directory"))

        self.lineEditImportJar.setText(
                self.settings.value("options/import/jar"))
        vm_arguments = self.settings.value("options/import/vm_arguments")
        if vm_arguments == "" or not vm_arguments or vm_arguments is None:
            self.plainTextEditImportVMArguments.insertPlainText(
                    "-Xms128m -Xmx1024m")
        else:
            self.plainTextEditImportVMArguments.insertPlainText(vm_arguments)

        self.lineEditDbHost.setText(self.settings.value("options/db/host"))
        self.lineEditDbDatabase.setText(self.settings.value("options/db/name"))
        self.lineEditDbPort.setText(self.settings.value("options/db/port"))
        self.lineEditDbUser.setText(self.settings.value("options/db/user"))
        self.lineEditDbUserPwd.setText(self.settings.value("options/db/pwd"))
        self.lineEditDbAdmin.setText(self.settings.value("options/db/admin"))
        self.lineEditDbAdminPwd.setText(
                self.settings.value("options/db/adminpwd"))

        default_repo = ['http://www.catais.org/models/',
                        'http://models.geo.admin.ch/']
        self.listWidgetModelRepos.insertItems(0, self.settings.value(
                "options/model_repositories/repositories", default_repo))

        QWidget.setTabOrder(self.lineEditDbHost, self.lineEditDbDatabase)
        QWidget.setTabOrder(self.lineEditDbDatabase, self.lineEditDbPort)
        QWidget.setTabOrder(self.lineEditDbPort, self.lineEditDbUser)
        QWidget.setTabOrder(self.lineEditDbUser, self.lineEditDbUserPwd)
        QWidget.setTabOrder(self.lineEditDbUserPwd, self.lineEditDbAdmin)
        QWidget.setTabOrder(self.lineEditDbAdmin, self.lineEditDbAdminPwd)

    @pyqtSignature("on_btnBrowseImportJar_clicked()")
    def on_btnBrowseImportJar_clicked(self):
        file_path = QFileDialog.getOpenFileName(self,
                                                tr("Open import jar file"),
                                                self.import_jar_path,
                                                "jar (*.jar *.JAR)")
        file_info = QFileInfo(file_path)
        self.lineEditImportJar.setText(file_info.absoluteFilePath())

    @pyqtSignature("on_btnBrowseProjectsDatabase_clicked()")
    def on_btnBrowseProjectsDatabase_clicked(self):
        file_path = QFileDialog.getOpenFileName(self, tr(
                "Choose projects definitions database"),
                                                self.projects_database_path,
                                                "SQLite (*.sqlite *.db *.DB)")
        file_info = QFileInfo(file_path)
        self.lineEditProjectsDatabase.setText(file_info.absoluteFilePath())

    @pyqtSignature("on_btnBrowseProjectsRootDir_clicked()")
    def on_btnBrowseProjectsRootDir_clicked(self):
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

    @pyqtSignature("on_btnTestProjectDB_clicked()")
    def on_btnTestProjectDB_clicked(self):
        try:
            current_path = self.lineEditProjectsDatabase.text()
            db = get_projects_db(current_path)
            db.close()
        except Exception as e:
            self.test_connection_failed(e)
        else:
            self.test_connection_succes()

    @pyqtSignature("on_btnTestConnection_clicked()")
    def on_btnTestConnection_clicked(self):
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

    @pyqtSignature("on_listWidgetModelRepos_itemSelectionChanged()")
    def on_listWidgetModelRepos_itemSelectionChanged(self):
        has_selected = bool(self.listWidgetModelRepos.selectedItems())
        self.btnDeleteModelRepo.setEnabled(has_selected)
        self.btnEditModelRepo.setEnabled(has_selected)

    @pyqtSignature("on_btnDeleteModelRepo_clicked()")
    def on_btnDeleteModelRepo_clicked(self):
        for item in self.listWidgetModelRepos.selectedItems():
            self.listWidgetModelRepos.takeItem(
                    self.listWidgetModelRepos.row(item))

    def ask_url(self, default_text=None):
        text, ok = QInputDialog.getText(
                self,
                tr("Add new model repository"),
                tr("Repository URL:"),
                QLineEdit.Normal,
                default_text
        )
        return text, ok

    @pyqtSignature("on_btnAddModelRepo_clicked()")
    def on_btnAddModelRepo_clicked(self):
        text, ok = self.ask_url()
        if ok and text:
            self.listWidgetModelRepos.addItem(text)

    @pyqtSignature("on_btnEditModelRepo_clicked()")
    def on_btnEditModelRepo_clicked(self):
        item = self.listWidgetModelRepos.currentItem()
        text, ok = self.ask_url(item.text())
        if ok and text:
            item.setText(text)

    def accept(self):
        self.settings.setValue("options/general/projects_database",
                               self.lineEditProjectsDatabase.text().strip())
        self.projectsDatabaseHasChanged.emit()

        self.settings.setValue("options/general/projects_root_directory",
                               self.lineEditProjectsRootDir.text().strip())

        self.settings.setValue("options/import/jar",
                               self.lineEditImportJar.text().strip())
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
        for index in xrange(self.listWidgetModelRepos.count()):
            repos.append(self.listWidgetModelRepos.item(index).text())
        self.settings.setValue("options/model_repositories/repositories", repos)

        self.close()
