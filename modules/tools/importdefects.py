# coding=utf-8
import os
import sys
import traceback

from builtins import range, str

from openpyxl import load_workbook

from qgis.PyQt.QtCore import QDateTime, QDir, QFileInfo, \
    QProcess, QRegExp, QSettings, Qt, pyqtSignal, pyqtSignature, pyqtSlot

from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

from qgis.core import QgsApplication, QgsDataSourceURI, QgsMessageLog, QgsVectorLayer
from qgis.gui import QgsMessageBar

from qgis.PyQt.QtCore import QDateTime

from qgis.PyQt.QtWidgets import QApplication, QDialog, QDialogButtonBox, \
    QFileDialog

from veriso.base.utils.utils import (open_psql_db, open_sqlite_db,
                                     get_projects_db, get_modules_dir,
                                     yaml_load_file, tr,
                                     get_subdirs, get_ui_class,
                                     db_user_has_role, get_absolute_path)

from veriso.base.utils.utils import dynamic_import

FORM_CLASS = get_ui_class('importdefects.ui')

class ImportDefectsDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, defects_list_dock):
        QDialog.__init__(self, None)
        self.setupUi(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.defects_list_dock = defects_list_dock

        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.okButton.setText('Import')

        settings = QSettings("CatAIS", "VeriSO")
        self.input_xlsx_path = settings.value("project/projectdir")

        self.module_name = settings.value("project/appmodule")
        self.provider = settings.value("project/provider")
        self.db_host = settings.value("project/dbhost")
        self.db_port = settings.value("project/dbport")
        self.db_name = settings.value("project/dbname")
        self.db_schema = settings.value("project/dbschema")
        self.db_user = settings.value("project/dbuser")
        self.db_pwd = settings.value("project/dbpwd")

        self.db = None

    def init_gui(self):
        return True

    def accept(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)

        xlsx = self.lineEditDefectsFile.text().strip()
        load_checked = self.load_defects_check.isChecked()

        header_list_punkte, rows_list_punkte = '', ''
        header_list_linien, rows_list_linien = '', ''
        header_list_polygone, rows_list_polygone = '', ''


        if xlsx == '':
            self.message_bar.pushWarning("VeriSO",
                                         tr("No Defects file set."))
            return

        self.wb = load_workbook(filename = xlsx, read_only = True)

        try:
            header_list_punkte, rows_list_punkte = self.read_sheet(u'Mängelliste (Punkte)')
            header_list_linien, rows_list_linien = self.read_sheet(u'Mängelliste (Linien)')
            header_list_polygone, rows_list_polygone = self.read_sheet(u'Mängelliste (Polygone)')
        except WrongExcelError as e:
            self.iface.messageBar().pushMessage('Wrong Excel file', e.value,
                                                level=QgsMessageBar.CRITICAL, duration=5)
            QApplication.restoreOverrideCursor()
            return

        punkte_query = self.create_query('t_maengel_punkt', header_list_punkte, rows_list_punkte)
        linien_query = self.create_query('t_maengel_linie', header_list_linien, rows_list_linien)
        polygone_query = self.create_query('t_maengel_polygon', header_list_polygone, rows_list_polygone)

        try:
            self.open_db()

            self.execute_query(punkte_query)
            self.execute_query(linien_query)
            self.execute_query(polygone_query)

            self.db.close()
            self.iface.messageBar().pushInfo("VeriSo", "Defects imported")

            if load_checked:
                defects_module = 'veriso.modules.loaddefects_base'
                defects_module = dynamic_import(defects_module)
                d = defects_module.LoadDefectsBase(self.iface, self.module_name)
                defects_layers = d.run()
                self.defects_list_dock.load_layers(defects_layers)

            QApplication.restoreOverrideCursor()

        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error",
                str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)
            return

        QApplication.restoreOverrideCursor()

        self.close()

    def read_sheet(self, sheet_name):
        sheet = self.wb[sheet_name]

        # list of dictionaries. A dictionary per row with key = column header
        rows_list = []
        header_list = []

        # check if the cells are in the original positions
        if(sheet['A5'].value != 'ogc_fid'):
             raise WrongExcelError('Wrong Excel file, cell A5 is not equal to \'ogc_fid\'')
        else:
            # get the column names (row 5)
            for cell in sheet[5]:
                header_list.append(sheet.cell(column = cell.column, row = 5).value)

            # get the rows from the row 6 (column header is row 5)
            for i in range(6, sheet.max_row + 1):
                values_list = []
                row = sheet[i]
                for cell in row:
                    values_list.append(cell.value)
                rows_list.append(values_list)

        return header_list, rows_list

    def create_query(self, table_name, header_list, rows_list):
        query = 'INSERT INTO '+self.db_schema+'.'+table_name+'('
        # don't write ogc_fid and coordinates
        query += ', '.join(header_list[1:11])
        query += ', ' + 'the_geom)'
        query += ' VALUES '
        query += '(\''
        query += '), (\''.join(['\', \''.join([str(value) for value in row[1:11]])
                                + '\', ST_GeomFromText(\''+row[-1]+'\', 2056)' for row in rows_list])
        query += ')'

        return query

    def open_db(self):

        try:
            self.db = QSqlDatabase.addDatabase("QPSQL")
            self.db.setHostName(self.db_host)
            self.db.setPort(int(self.db_port))
            self.db.setDatabaseName(self.db_name)
            self.db.setUserName(self.db_user)
            self.db.setPassword(self.db_pwd)
            self.db.open()

        except Exception as e:
            raise e

    def execute_query(self, sql):
        query = QSqlQuery(self.db)

        res = query.exec_(sql)

        if(res == False):
            raise QueryExecutionError(query.lastError().text())

    # noinspection PyPep8Naming,PyPep8Naming
    @pyqtSignature("on_btnBrowseDefectsFile_clicked()")
    def on_btnBrowseDefectsFile_clicked(self):
        file_path = QFileDialog.getOpenFileName(
                self,
                tr("Choose defects file"),
                self.input_xlsx_path,
                "XLSX (*.xlsx)")
        file_info = QFileInfo(file_path)
        self.lineEditDefectsFile.setText(file_info.absoluteFilePath())

class QueryExecutionError(Exception):
    def __init__(self, value):
        self.value = value
        def __str__(self):
            return repr(self.value)

class WrongExcelError(Exception):
    def __init__(self, value):
        self.value = value
        def __str__(self):
            return repr(self.value)

