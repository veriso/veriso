# coding=utf-8
import os
import sys
import traceback
import shapefile


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
from veriso.base.utils.exceptions import VerisoErrorWithBar

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

        file_to_import = self.lineEditDefectsFile.text().strip()
        load_checked = self.load_defects_check.isChecked()

        if file_to_import == '':
            self.message_bar.pushWarning("VeriSO",
                                         tr("No Defects file set."))
            return

        #TODO testare il tipo di file importato se excel o shp o errore
        #self.import_xlsx()
        self.import_shp(file_to_import, load_checked)

        QApplication.restoreOverrideCursor()
        self.close()


    def import_shp(self, shp, load_checked):
        shp =  self.lineEditDefectsFile.text().strip()
        load_checked = self.load_defects_check.isChecked()

        sf = shapefile.Reader(shp)

        # TODO capire il tipo di geometria

        # Skip the first field (deletion flag)
        fields = sf.fields[1:]
        header_list = []
        rows_list = []

        for i in range(len(fields)):
            f = fields[i]
            f_name = f[0].lower()
            header_list.append(f_name)

        shape_records = (shp_rec for shp_rec in sf.iterShapeRecords())

        for sr in shape_records:
            row = []
            shape = sr.shape
            x, y = shape.points[0]
            for r in sr.record:
                print('type', type(str(r)))
                row.append(str(r))

            row.append('POINT({} {})'.format(x, y))
            rows_list.append(row)

        self.open_db()

        if len(rows_list) > 0:
            query_points = self.create_query('t_maengel_punkt', header_list, rows_list)
            print('query', query_points)
            self.execute_query(query_points)

        self.db.close()
        self.iface.messageBar().pushInfo("VeriSo", "Defects imported from Shapefile")


    def import_xlsx(self, xlsx, load_checked):

        self.wb = load_workbook(filename = xlsx, read_only = True)

        header_list_points, rows_list_points = self.read_sheet(u'Mängelliste (Punkte)')
        header_list_lines, rows_list_lines = self.read_sheet(u'Mängelliste (Linien)')
        header_list_polygons, rows_list_polygons = self.read_sheet(u'Mängelliste (Polygone)')

        self.open_db()

        if len(rows_list_points) > 0:
            query_points = self.create_query('t_maengel_punkt', header_list_points, rows_list_points)
            self.execute_query(query_points)
        if len(rows_list_lines) > 0:
            query_lines = self.create_query('t_maengel_linie', header_list_lines, rows_list_lines)
            self.execute_query(query_lines)
        if len(rows_list_polygons) > 0:
            query_polygons = self.create_query('t_maengel_polygon', header_list_polygons, rows_list_polygons)
            self.execute_query(query_polygons)

        self.db.close()
        self.iface.messageBar().pushInfo("VeriSo", "Defects imported from Excel file")

        if load_checked:
            defects_module = 'veriso.modules.loaddefects_base'
            defects_module = dynamic_import(defects_module)
            d = defects_module.LoadDefectsBase(self.iface, self.module_name)
            defects_layers = d.run()
            self.defects_list_dock.load_layers(defects_layers)


    def read_sheet(self, sheet_name):
        sheet = self.wb[sheet_name]

        # list of lists. A list per row
        rows_list = []
        header_list = []

        # check if the cells are in the original positions
        if sheet['A5'].value != 'ogc_fid':
            QApplication.restoreOverrideCursor()
            e = 'Wrong Excel file, cell A5 is not \'ogc_fid\''
            raise VerisoErrorWithBar(self.iface.messageBar(), e)
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
        query += ', '.join(header_list[1:12])
        query += ', ' + 'the_geom)'
        query += ' VALUES '
        query += '(\''
        query += '), (\''.join(['\', \''.join([str(value) for value in row[1:12]])
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
            raise VerisoErrorWithBar(self.iface.messageBar(), "Error " + e.message)

    def execute_query(self, sql):
        query = QSqlQuery(self.db)

        res = query.exec_(sql)

        if(res == False):
            QApplication.restoreOverrideCursor()
            raise VerisoErrorWithBar(self.iface.messageBar(), "Error " + (query.lastError().text()))

    # noinspection PyPep8Naming,PyPep8Naming
    @pyqtSignature("on_btnBrowseDefectsFile_clicked()")
    def on_btnBrowseDefectsFile_clicked(self):
        file_path = QFileDialog.getOpenFileName(
                self,
                tr("Choose defects file"),
                self.input_xlsx_path,
                "Defects layer (*.xlsx *.shp)")
        file_info = QFileInfo(file_path)
        self.lineEditDefectsFile.setText(file_info.absoluteFilePath())

