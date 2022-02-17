# coding=utf-8
import os

from qgis.PyQt.QtCore import QDir, QObject, QSettings, QVariant
from qgis.core import QgsDataSourceUri, QgsMessageLog, QgsVectorLayer
from qgis.core import Qgis

from qgis.PyQt.QtCore import QDateTime
from veriso.base.utils.utils import tr


class ExportDefects(QObject):
    def __init__(self, iface, module, tr_tag, defects_type, defects_table_names):
        QObject.__init__(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()

        self.tr_tag = tr_tag  # "VeriSO_V+D_Defects" or "VeriSO_EE_Defects"
        self.defects_type = defects_type
        self.defects_table_names = defects_table_names

    def run(self):
        try:
            import xlsxwriter
        except Exception as e:
            self.message_bar.pushMessage("Error", str(e),
                                         level=Qgis.Critical,
                                         duration=0)
            return

        try:
            settings = QSettings("CatAIS", "VeriSO")
            module_name = settings.value("project/appmodule")
            provider = settings.value("project/provider")
            db_host = settings.value("project/dbhost")
            db_port = settings.value("project/dbport")
            db_name = settings.value("project/dbname")
            db_schema = settings.value("project/dbschema")
            db_user = settings.value("project/dbuser")
            db_pwd = settings.value("project/dbpwd")
            #            db_admin = settings.value("project/dbadmin")
            #            db_admin_pwd = settings.value("project/dbadminpwd")
            project_id = settings.value("project/id")
            project_dir = settings.value("project/projectdir")

            if not db_schema:
                self.message_bar.pushCritical(
                    "Error",
                    self.tr("Missing database schema parameter."))
                return

            if not db_host:
                self.message_bar.pushCritical(
                    "Error",
                    self.tr("Missing database host parameter."))
                return

            if not db_name:
                self.message_bar.pushCritical(
                    "Error", self.tr("Missing database name parameter."))
                return

            if not db_port:
                self.message_bar.pushCritical(
                    "Error",
                    self.tr("Missing database port parameter."))
                return

            if not db_user:
                self.message_bar.pushCritical(
                    "Error",
                    self.tr("Missing database user parameter."))
                return

            if not db_pwd:
                self.message_bar.pushCritical(
                    "Error",
                    self.tr("Missing database user password parameter."))
                return

            if not provider:
                self.message_bar.pushCritical(
                    "Error",
                    self.tr(
                        "Missing provider parameter. Cannot load "
                        "layer."))
                return

            if not module_name:
                self.message_bar.pushCritical(
                    "Error",
                    self.tr("Missing module name parameter. Cannot load "
                            "layer."))
                return

            point_layer_name = self.defects_table_names.get(self.defects_type, {}).get("point", None)
            line_layer_name = self.defects_table_names.get(self.defects_type, {}).get("line", None)
            polygon_layer_name = self.defects_table_names.get(self.defects_type, {}).get("polygon", None)

            if point_layer_name is not None:
                uri = QgsDataSourceUri()
                uri.setConnection(db_host, db_port, db_name, db_user, db_pwd)
                uri.setDataSource(db_schema, point_layer_name, "the_geom", "",
                                "ogc_fid")
                vlayer_points = QgsVectorLayer(uri.uri(), "Maengel (Punkte)",
                                            "postgres")

            if line_layer_name is not None:
                uri = QgsDataSourceUri()
                uri.setConnection(db_host, db_port, db_name, db_user, db_pwd)
                uri.setDataSource(db_schema, line_layer_name, "the_geom", "",
                                "ogc_fid")
                vlayer_lines = QgsVectorLayer(uri.uri(), "Maengel (Linien)",
                                            "postgres")

            if polygon_layer_name is not None:
                uri = QgsDataSourceUri()
                uri.setConnection(db_host, db_port, db_name, db_user, db_pwd)
                uri.setDataSource(db_schema, polygon_layer_name, "the_geom", "",
                                "ogc_fid")
                vlayer_polygons = QgsVectorLayer(uri.uri(), "Maengel (Polygon)",
                                                "postgres")

            if point_layer_name is not None and not vlayer_points.isValid():
                self.message_bar.pushMessage("Error",
                                             tr("Could not load defects layer.",
                                                self.tr_tag,
                                                None),
                                             level=Qgis.Critical,
                                             duration=0)
                return

            if line_layer_name is not None and not vlayer_lines.isValid():
                self.message_bar.pushMessage("Error",
                                             tr("Could not load defects layer.",
                                                self.tr_tag,
                                                None),
                                             level=Qgis.Critical,
                                             duration=0)
                return

            if polygon_layer_name is not None and not vlayer_polygons.isValid():
                self.message_bar.pushMessage("Error",
                                             tr("Could not load defects layer.",
                                                self.tr_tag,
                                                None),
                                             level=Qgis.Critical,
                                             duration=0)
                return

            if (point_layer_name is not None and vlayer_points.featureCount() == 0 and
                    (line_layer_name is not None and vlayer_lines.featureCount() == 0) and
                    (polygon_layer_name is not None and vlayer_polygons.featureCount() == 0)):
                self.message_bar.pushInfo(
                    "Information",
                    tr("Defects layer are empty.", self.tr_tag,
                        None))
                return

            # Create excel file.
            filename = QDir.toNativeSeparators(
                QDir.cleanPath(os.path.join(project_dir,
                               tr('maengel', self.tr_tag) + '.xlsx')))
            workbook = xlsxwriter.Workbook(filename)
            fmt_bold = workbook.add_format({'bold': True})
            fmt_italic = workbook.add_format({'italic': True})
            fmt_2dec = workbook.add_format({'num_format': '0.00'})
            fmt_3dec = workbook.add_format({'num_format': '0.000'})
            # 28/02/13 12:00
            fmt_date = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})

            # Create the worksheet for the points defects.
            if point_layer_name is not None:
                worksheet_points = workbook.add_worksheet(
                    self.tr('Mängelliste (Punkte)'))
                worksheet_points.set_paper(9)
                worksheet_points.set_portrait()

                # Write project name into worksheet.
                worksheet_points.write(0, 0,
                                    tr("Operat: ", self.tr_tag,
                                        None), fmt_bold)
                worksheet_points.write(0, 1, project_id, fmt_bold)

                # Write defects. Loop through field to write header.
                # Then loop through features.
                provider = vlayer_points.dataProvider()
                attrs = provider.fields()

                labels = [tr(attrs.at(i).name(), self.tr_tag)
                        for i in range(len(attrs))]

                #            types = []
                i = 0
                for i in range(len(attrs)):
                    worksheet_points.write(4, i, labels[i], fmt_italic)
                # types.append(attrs.at(i).type())

                worksheet_points.write(4, i + 1,
                                    tr("Y-Koordinate", self.tr_tag, None),
                                    fmt_italic)
                worksheet_points.write(4, i + 2,
                                    tr("X-Koordinate", self.tr_tag, None),
                                    fmt_italic)
                worksheet_points.write(4, i + 3,
                                    tr("WKT", self.tr_tag, None),
                                    fmt_italic)

                iterator = vlayer_points.getFeatures()
                j = 0

                for feat in iterator:
                    geom = feat.geometry()
                    point = geom.asPoint()
                    attrs = feat.attributes()
                    k = 0

                    for attr in attrs:
                        fmt = None
                        if type(attr) == QDateTime:
                            # this is to avoid:
                            # Unsupported type
                            # <class 'PyQt4.QtCore.QDateTime'> in write()
                            fmt = fmt_date
                            attr = attr.toPyDateTime()
                        if type(attr) == QVariant and attr.isNull():
                            attr = None
                        worksheet_points.write(5 + j, k, attr, fmt)
                        k += 1

                    worksheet_points.write(5 + j, k, point.x(), fmt_3dec)
                    worksheet_points.write(5 + j, k + 1, point.y(), fmt_3dec)
                    worksheet_points.write(5 + j, k + 2, geom.asWkt())
                    j += 1

            # Create the worksheet for the line defects.
            if line_layer_name is not None:
                worksheet_lines = workbook.add_worksheet(
                    self.tr('Mängelliste (Linien)'))
                worksheet_lines.set_paper(9)
                worksheet_lines.set_portrait()

                # Write project name into worksheet.
                worksheet_lines.write(0, 0,
                                    tr("Operat: ", self.tr_tag,
                                        None), fmt_bold)
                worksheet_lines.write(0, 1, project_id, fmt_bold)

                # Write defects. Loop through field to write header.
                # Then loop through features.
                provider = vlayer_lines.dataProvider()
                attrs = provider.fields()

                #            types = []
                for i in range(len(attrs)):
                    worksheet_lines.write(4, i, labels[i], fmt_italic)
                # types.append(attrs.at(i).type())

                worksheet_lines.write(4, i + 1,
                                    tr("Y-Koordinate", self.tr_tag, None),
                                    fmt_italic)
                worksheet_lines.write(4, i + 2,
                                    tr("X-Koordinate", self.tr_tag, None),
                                    fmt_italic)
                worksheet_lines.write(4, i + 3,
                                    tr(u"Länge [hm]", self.tr_tag, None),
                                    fmt_italic)
                worksheet_lines.write(4, i + 4,
                                    tr('WKT', self.tr_tag, None),
                                    fmt_italic)

                iterator = vlayer_lines.getFeatures()
                j = 0

                for feat in iterator:
                    geom = feat.geometry()
                    point = geom.vertexAt(0)
                    attrs = feat.attributes()
                    k = 0

                    for attr in attrs:
                        fmt = None
                        if type(attr) == QDateTime:
                            # this is to avoid:
                            # Unsupported type
                            # <class 'PyQt4.QtCore.QDateTime'> in write()
                            fmt = fmt_date
                            attr = attr.toPyDateTime()
                        if type(attr) == QVariant and attr.isNull():
                            attr = None
                        worksheet_lines.write(5 + j, k, attr, fmt)
                        k += 1

                    worksheet_lines.write(5 + j, k, point.x(), fmt_3dec)
                    worksheet_lines.write(5 + j, k + 1, point.y(), fmt_3dec)
                    worksheet_lines.write(5 + j, k + 2, geom.length(), fmt_2dec)
                    worksheet_lines.write(5 + j, k + 3, geom.asWkt())
                    j += 1

            # Create the worksheet for the polygon defects.
            if polygon_layer_name is not None:
                worksheet_polygons = workbook.add_worksheet(
                    self.tr('Mängelliste (Polygone)'))
                worksheet_polygons.set_paper(9)
                worksheet_polygons.set_portrait()

                # Write project name into worksheet.
                worksheet_polygons.write(0, 0,
                                        tr("Operat: ", self.tr_tag,
                                            None), fmt_bold)
                worksheet_polygons.write(0, 1, project_id, fmt_bold)

                # Write defects. Loop through field to write header.
                # Then loop through features.
                provider = vlayer_polygons.dataProvider()
                attrs = provider.fields()

                #            types = []
                for i in range(len(attrs)):
                    worksheet_polygons.write(4, i, labels[i], fmt_italic)
                # types.append(attrs.at(i).type())

                worksheet_polygons.write(4, i + 1,
                                        tr("Y-Koordinate", self.tr_tag, None),
                                        fmt_italic)
                worksheet_polygons.write(4, i + 2,
                                        tr("X-Koordinate", self.tr_tag, None),
                                        fmt_italic)
                worksheet_polygons.write(4, i + 3,
                                        tr(u"Fläche [m2]", self.tr_tag, None),
                                        fmt_italic)
                worksheet_polygons.write(4, i + 4,
                                        tr(u"Umfang [hm]", self.tr_tag, None),
                                        fmt_italic)
                worksheet_polygons.write(4, i + 5,
                                        tr('WKT', self.tr_tag, None),
                                        fmt_italic)

                iterator = vlayer_polygons.getFeatures()
                j = 0

                for feat in iterator:
                    geom = feat.geometry()
                    point = geom.vertexAt(0)
                    attrs = feat.attributes()
                    k = 0

                    for attr in attrs:
                        fmt = None
                        if type(attr) == QDateTime:
                            # this is to avoid:
                            # Unsupported type
                            # <class 'PyQt4.QtCore.QDateTime'> in write()
                            fmt = fmt_date
                            attr = attr.toPyDateTime()
                        if type(attr) == QVariant and attr.isNull():
                            attr = None
                        worksheet_polygons.write(5 + j, k, attr, fmt)
                        k += 1

                    worksheet_polygons.write(5 + j, k, point.x(), fmt_3dec)
                    worksheet_polygons.write(5 + j, k + 1, point.y(), fmt_3dec)
                    worksheet_polygons.write(5 + j, k + 2, geom.area(),
                                            fmt_2dec)
                    worksheet_polygons.write(5 + j, k + 3, geom.length(),
                                            fmt_2dec)
                    worksheet_polygons.write(5 + j, k + 4, geom.asWkt())
                    j += 1

            # Close excel file.
            workbook.close()

            self.message_bar.pushInfo("Information",
                                      tr("Defect(s) written: ",
                                         self.tr_tag,
                                          None) + str(
                                          filename))
        except Exception as e:
            message = "Error while writing defects file."
            self.message_bar.pushMessage("Error",
                                         tr(self.tr_tag, message, None),
                                         level=Qgis.Critical,
                                         duration=0)
            QgsMessageLog.logMessage(str(e), "VeriSO", Qgis.Critical)
            return
