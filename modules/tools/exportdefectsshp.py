# coding=utf-8
import os
from builtins import range, str

from qgis.PyQt.QtCore import QDir, QObject, QSettings
from qgis.core import QgsDataSourceURI, QgsMessageLog, QgsVectorLayer, QgsVectorFileWriter
from qgis.gui import QgsMessageBar

from qgis.PyQt.QtCore import QDateTime, QPyNullVariant
from veriso.base.utils.utils import tr


class ExportDefectsShp(QObject):
    def __init__(self, iface, module, tr_tag):
        QObject.__init__(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()

        self.tr_tag = tr_tag  # "VeriSO_V+D_Defects" or "VeriSO_EE_Defects"

    def run(self):
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
                        self.tr(
                                "Missing module name parameter. Cannot load "
                                "layer."))
                return

            uri = QgsDataSourceURI()
            uri.setConnection(db_host, db_port, db_name, db_user, db_pwd)
            uri.setDataSource(db_schema, "t_maengel_punkt", "the_geom", "",
                              "ogc_fid")
            vlayer_points = QgsVectorLayer(uri.uri(), "Maengel (Punkte)",
                                           "postgres")

            uri = QgsDataSourceURI()
            uri.setConnection(db_host, db_port, db_name, db_user, db_pwd)
            uri.setDataSource(db_schema, "t_maengel_linie", "the_geom", "",
                              "ogc_fid")
            vlayer_lines = QgsVectorLayer(uri.uri(), "Maengel (Linien)",
                                          "postgres")

            uri = QgsDataSourceURI()
            uri.setConnection(db_host, db_port, db_name, db_user, db_pwd)
            uri.setDataSource(db_schema, "t_maengel_polygon", "the_geom", "",
                              "ogc_fid")
            vlayer_polygons = QgsVectorLayer(uri.uri(), "Maengel (Linien)",
                                             "postgres")

            if not vlayer_points.isValid():
                self.message_bar.pushMessage("Error",
                                             tr("Could not load defects layer.",
                                                self.tr_tag,
                                                None),
                                             level=QgsMessageBar.CRITICAL,
                                             duration=0)
                return

            if not vlayer_lines.isValid():
                self.message_bar.pushMessage("Error",
                                             tr("Could not load defects layer.",
                                                self.tr_tag,
                                                None),
                                             level=QgsMessageBar.CRITICAL,
                                             duration=0)
                return

            if not vlayer_polygons.isValid():
                self.message_bar.pushMessage("Error",
                                             tr("Could not load defects layer.",
                                                self.tr_tag,
                                                None),
                                             level=QgsMessageBar.CRITICAL,
                                             duration=0)
                return

            if (vlayer_points.featureCount() == 0 and
                    vlayer_lines.featureCount() == 0 and
                    vlayer_polygons.featureCount() == 0):
                self.message_bar.pushInfo(
                        "Information",
                        tr(
                                "Defects layer are empty.", self.tr_tag,
                                None))
                return

            filename = QDir.convertSeparators(
                QDir.cleanPath(os.path.join(project_dir, "maengel_punkt.shp")))

            error = QgsVectorFileWriter.writeAsVectorFormat(vlayer_points, filename, None, None,
                                                            "ESRI Shapefile")
            if error == QgsVectorFileWriter.NoError:
                self.message_bar.pushInfo("Information",
                                          tr(
                                              "Defect(s) written: ",
                                              self.tr_tag,
                                              None) + str(
                                              filename))

            filename = QDir.convertSeparators(
                QDir.cleanPath(os.path.join(project_dir, "maengel_linie.shp")))

            error = QgsVectorFileWriter.writeAsVectorFormat(vlayer_lines, filename, None, None,
                                                            "ESRI Shapefile")
            if error == QgsVectorFileWriter.NoError:
                self.message_bar.pushInfo("Information",
                                          tr(
                                              "Defect(s) written: ",
                                              self.tr_tag,
                                              None) + str(
                                              filename))

            filename = QDir.convertSeparators(
                QDir.cleanPath(os.path.join(project_dir, "maengel_polygon.shp")))

            error = QgsVectorFileWriter.writeAsVectorFormat(vlayer_polygons, filename, None, None,
                                                            "ESRI Shapefile")

            if error == QgsVectorFileWriter.NoError:
                self.message_bar.pushInfo("Information",
                                          tr(
                                              "Defect(s) written: ",
                                              self.tr_tag,
                                              None) + str(
                                              filename))


        except Exception as e:
            message = "Error while writing defects file."
            self.message_bar.pushMessage("Error",
                                         tr(
                                                 self.tr_tag, message, None),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)
            return
