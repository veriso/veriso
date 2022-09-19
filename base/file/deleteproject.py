# coding=utf-8

import os
import shutil
from qgis.PyQt.QtCore import Qt, pyqtSignal, QSettings
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import QApplication, QDialog, QDialogButtonBox
from qgis.core import Qgis

from veriso.base.utils.utils import open_psql_db, get_projects_db, \
    get_projects, tr, get_ui_class, get_default_db
from veriso.base.utils.exceptions import VerisoError

FORM_CLASS = get_ui_class('deleteproject.ui')


class DeleteProjectDialog(QDialog, FORM_CLASS):
    projectsDatabaseHasChanged = pyqtSignal()

    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.settings = QSettings("CatAIS", "VeriSO")
        self.setupUi(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.okButton.setText(tr("Delete", context="DeleteProject"))

        self.db_host = None
        self.db_name = None
        self.db_port = None
        self.db_schema = None
        self.db_admin = None
        self.db_admin_pwd = None
        self.project_index = None
        self.projects = None

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

    def accept(self):
        current_index = self.cBoxProject.currentIndex()
        if current_index == 0:
            return

        db_schema = str(self.cBoxProject.itemData(current_index))
        self.db_schema = db_schema

        # Get the connections parameters from the projects list we created in
        #  the init_gui method. Only when using sqlite projects.db
        if not self.settings.value("options/general/use_pg_projects_database",
                                   False, type=bool):
            i = 0
            for project in self.projects:
                if db_schema == str(project["dbschema"]):
                    self.db_host = str(project["dbhost"])
                    self.db_name = str(project["dbname"])
                    self.db_port = str(project["dbport"])
                    self.db_admin = str(project["dbadmin"])
                    self.db_admin_pwd = str(project["dbadminpwd"])
                    self.project_index = i
                    break
                i += 1

        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.buttonBox.setEnabled(False)

        try:
            self.delete_data_in_database()
            self.update_project_database()
            self.delete_project_directory()
        except VerisoError as e:
            self.restore_cursor()
            self.message_bar.pushMessage("VeriSO", tr(str(e)),
                                         Qgis.Critical, duration=0)
        else:
            self.projectsDatabaseHasChanged.emit()
            self.init_gui()

            message = "Project deleted succesfully"
            self.message_bar.pushSuccess("VeriSO", tr(message))

        self.restore_cursor()

    def update_project_database(self):

        if self.settings.value("options/general/use_pg_projects_database",
                               False, type=bool):
            return self.update_project_database_pg()
        return self.update_project_database_sqlite()

    def update_project_database_pg(self):
        """Deletes the deleted project from the postgres project table.

        Returns:
          False: If something went wrong. Otherwise True.
        """
        try:
            db = get_projects_db()

            sql = "DELETE FROM veriso_conf.project WHERE id = '%s';" % (
                self.db_schema)

            query = db.exec_(sql)

            if not query.isActive():
                message = "Error while reading from projects database."
                raise VerisoError(
                    message,
                    long_message=QSqlQuery.lastError(query).text())

            db.close()
            del db

            return True

        except Exception as e:
            message = "Something went wrong while updating projects database."
            raise VerisoError(message, e)

    def update_project_database_sqlite(self):
        """Deletes the deleted project from the sqlite project database.

        Returns:
          False: If something went wrong. Otherwise True.
        """
        try:
            db = get_projects_db()

            sql = "DELETE FROM projects WHERE dbschema = '%s';" % (
                self.db_schema)

            query = db.exec_(sql)

            if not query.isActive():
                message = "Error while reading from projects database."
                raise VerisoError(
                    message,
                    long_message=QSqlQuery.lastError(query).text())

            db.close()
            del db

            return True

        except Exception as e:
            message = "Something went wrong while updating projects database."
            raise VerisoError(message, e)

    def delete_data_in_database(self):
        """Deletes the project (= database schema) in the database.

        Returns:
          False: If something went wrong with deleting in the database.
          Otherwise True.
        """
        try:
            if self.settings.value("options/general/use_pg_projects_database",
                                   False, type=bool):
                db = get_default_db()
            else:
                db = open_psql_db(self.db_host, self.db_name, self.db_port,
                                  self.db_admin, self.db_admin_pwd)

            sql = "BEGIN;"
            sql += "DROP SCHEMA IF EXISTS %s CASCADE;" % self.db_schema
            sql += "COMMIT;"

            query = db.exec_(sql)

            if not query.isActive():
                message = "Error occured while deleting project in database."
                raise VerisoError(message, long_message=QSqlQuery.lastError(
                    query).text())

            db.close()
            del db

            return True

        except Exception as e:
            message = "Something went wrong while deleting the project."
            raise VerisoError(message, e)

    def delete_project_directory(self):
        """Deletes the directory with the same name as the project (db
        schema) in the project root directory.
        It emits a projects database changed signal.

        Returns:
          False: If the directory could not be deleted. Otherwise True.
        """
        try:
            projects_root_directory = QSettings("CatAIS", "VeriSO").value(
                "options/general/projects_root_directory")
            path = os.path.join(str(projects_root_directory),
                                str(self.db_schema))
            shutil.rmtree(path)
            return True
        except Exception as e:
            message = "Something went wrong while deleting the project folder."
            raise VerisoError(message, e)

    def restore_cursor(self):
        QApplication.restoreOverrideCursor()
        self.buttonBox.setEnabled(True)
