# coding=utf-8
import sys
import traceback
from builtins import range, str
from qgis.PyQt.QtCore import QObject, QSettings, QSizeF, Qt
from qgis.PyQt.QtGui import QColor, QTextDocument
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsFeature, QgsMapLayer, QgsMapLayerRegistry, QgsPoint, \
    QgsProject, QgsRectangle
from qgis.gui import QgsMessageBar, QgsTextAnnotationItem

from veriso.base.utils.loadlayer import LoadLayer

try:
    _encoding = QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

from collections import OrderedDict
from veriso.modules.complexcheck_base import ComplexCheckBase


class ComplexCheck(ComplexCheckBase):
    shortcut = 'F12'
    names = OrderedDict()
    names['de'] = 'Lokalisation'
    names['fr'] = 'Localisation'

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)
        self.canvas = self.iface.mapCanvas()

    # noinspection PyUnboundLocalVariable,PyUnboundLocalVariable,
    # PyUnboundLocalVariable
    # noinspection PyUnboundLocalVariable,PyUnboundLocalVariable,
    # PyUnboundLocalVariable
    # noinspection PyUnboundLocalVariable,PyUnboundLocalVariable,
    # PyUnboundLocalVariable
    # noinspection PyUnboundLocalVariable
    def run(self):
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")

        locale = QSettings().value('locale/userLocale')[0:2]

        if not project_id:
            self.message_bar.pushCritical("Error", _translate(
                    "VeriSO_EE_Geb_LokTest", "project_id not set", None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_Geb_LokTest",
                               "Gebaeudeadressen - Lokalisationstest", None)
            group += " (" + str(project_id) + ")"

            # TODO: Check "tid" vs. t_ili_tid... in queries. Do not import
            # i_ili_tid?

            # define layer names here
            lokalisation = _translate("VeriSO_EE_Geb_LokTest",
                                      "Lokalisation Lokalisationstest", None)
            strassenstueck_geometrie = _translate("VeriSO_EE_Geb_LokTest",
                                                  "Strassenstueck (geometrie) "
                                                  "Lokalisationstest",
                                                  None)
            strassenstueck_anfangspunkt = _translate("VeriSO_EE_Geb_LokTest",
                                                     "Strassenstueck ("
                                                     "anfangspunkt) "
                                                     "Lokalisationstest",
                                                     None)
            benanntesgebiet = _translate("VeriSO_EE_Geb_LokTest",
                                         "Benanntes Gebiet Lokalisationstest",
                                         None)
            gebaeudeeingang = _translate("VeriSO_EE_Geb_LokTest",
                                         "Gebaeudeeingang Lokalisationstest",
                                         None)
            shortestline = _translate("VeriSO_EE_Geb_LokTest",
                                      "Kuerzeste Linie Lokalisationstest", None)
            hausnummerpos = _translate("VeriSO_EE_Geb_LokTest",
                                       "HausnummerPos Lokalisationstest", None)
            lokalisationsname = _translate("VeriSO_EE_Geb_LokTest",
                                           "LokalisationsName", None)

            vlayer_lokalisation = self.get_vector_layer_by_name(lokalisation)
            if not vlayer_lokalisation:
                layer = {
                    "type": "postgres", "title": lokalisation,
                    "featuretype": "gebaeudeadressen_lokalisation",
                    "key": "ogc_fid", "sql": "ogc_fid = -1", "readonly": True,
                    "group": group
                }
                vlayer_lokalisation = self.layer_loader.load(layer)

            vlayer_strassenstueck_geometrie = self.get_vector_layer_by_name(
                    strassenstueck_geometrie)
            if not vlayer_strassenstueck_geometrie:
                layer = {
                    "type": "postgres",
                    "title": "Strassenstueck (geometrie) Lokalisationstest",
                    "featuretype": "gebaeudeadressen_strassenstueck",
                    "geom": "geometrie", "key": "ogc_fid",
                    "sql": "strassenstueck_von = -1", "readonly": True,
                    "group": group,
                    "style": "global_qml/gebaeudeadressen/strassenachsen_rot"
                             ".qml"
                }
                vlayer_strassenstueck_geometrie = self.layer_loader.load(layer)

            vlayer_strassenstueck_anfangspunkt = self.get_vector_layer_by_name(
                    strassenstueck_anfangspunkt)
            if not vlayer_strassenstueck_anfangspunkt:
                layer = {
                    "type": "postgres",
                    "title": "Strassenstueck (anfangspunkt) Lokalisationstest",
                    "featuretype": "gebaeudeadressen_strassenstueck",
                    "geom": "anfangspunkt", "key": "ogc_fid",
                    "sql": "strassenstueck_von = -1", "readonly": True,
                    "group": group,
                    "style": "global_qml/gebaeudeadressen/anfangspunkt_rot.qml"
                }
                vlayer_strassenstueck_anfangspunkt = self.layer_loader.load(
                        layer)

            vlayer_benanntesgebiet = self.get_vector_layer_by_name(
                    benanntesgebiet)
            if not vlayer_benanntesgebiet:
                layer = {
                    "type": "postgres",
                    "title": "Benanntes Gebiet Lokalisationstest",
                    "featuretype": "gebaeudeadressen_benanntesgebiet",
                    "geom": "flaeche", "key": "ogc_fid",
                    "sql": "benanntesgebiet_von = -1", "readonly": True,
                    "group": group,
                    "style": "global_qml/gebaeudeadressen/benanntesgebiet_rot"
                             ".qml"
                }
                vlayer_benanntesgebiet = self.layer_loader.load(layer)

            vlayer_gebaeudeeingang = self.get_vector_layer_by_name(
                    gebaeudeeingang)
            if not vlayer_gebaeudeeingang:
                layer = {
                    "type": "postgres",
                    "title": "Gebaeudeeingang Lokalisationstest",
                    "featuretype": "gebaeudeadressen_gebaeudeeingang",
                    "geom": "lage", "key": "ogc_fid",
                    "sql": "gebaeudeeingang_von = -1", "readonly": True,
                    "group": group,
                    "style": "global_qml/gebaeudeadressen/gebaeudeeingang_rot"
                             ".qml"
                }
                vlayer_gebaeudeeingang = self.layer_loader.load(layer)

            vlayer_shortestline = self.get_vector_layer_by_name(shortestline)
            if not vlayer_shortestline:
                layer = {
                    "type": "postgres",
                    "title": "Kuerzeste Linie Lokalisationstest",
                    "featuretype": "t_shortestline_hausnummerpos",
                    "geom": "the_geom", "key": "ogc_fid", "sql": "lok_tid = -1",
                    "readonly": True, "group": group,
                    "style":
                        "global_qml/gebaeudeadressen/shortestline_linie_rot.qml"
                }
                vlayer_shortestline = self.layer_loader.load(layer)

            vlayer_hausnummerpos = self.get_vector_layer_by_name(hausnummerpos)
            if not vlayer_hausnummerpos:
                layer = {
                    "type": "postgres",
                    "title": "HausnummerPos Lokalisationstest",
                    "featuretype": "v_gebaeudeadressen_hausnummerpos",
                    "geom": "pos", "key": "ogc_fid", "sql": "lok_tid = -1",
                    "readonly": True, "group": group,
                    "style": "global_qml/gebaeudeadressen/hausnummerpos_rot.qml"
                }
                vlayer_hausnummerpos = self.layer_loader.load(layer)

            vlayer_lokalisationsname = self.get_vector_layer_by_name(
                    lokalisationsname)
            if not vlayer_lokalisationsname:
                self.message_bar.pushMessage(
                        "Error",
                        _translate(
                                "VeriSO_EE_Geb_LokTest",
                                "Layer _LokalisationsName_ not found.",
                                None),
                        level=QgsMessageBar.CRITICAL,
                        duration=0)
                QApplication.restoreOverrideCursor()
                return

            iterator = vlayer_lokalisationsname.getFeatures()
            ids = []

            for feature in iterator:
                ids.append(feature.id())

            if vlayer_lokalisationsname.selectedFeatureCount() < 1:
                self.message_bar.pushCritical("Error", _translate(
                        "VeriSO_EE_Geb_LokTest",
                        "No _LokalisationsName_ selected.",
                        None))
                QApplication.restoreOverrideCursor()
                return

            if vlayer_lokalisationsname.selectedFeatureCount() > 1:
                self.message_bar.pushCritical("Error", _translate(
                        "VeriSO_EE_Geb_LokTest",
                        "Please select only one (1) _LokalisationsName_.",
                        None))
                QApplication.restoreOverrideCursor()
                return

            feat = QgsFeature()
            id = vlayer_lokalisationsname.selectedFeaturesIds()[0]
            feat = vlayer_lokalisationsname.selectedFeatures()[0]
            idx = ids.index(id)

            benannte_idx = vlayer_lokalisationsname.fieldNameIndex("benannte")
            text_idx = vlayer_lokalisationsname.fieldNameIndex("atext")

            if benannte_idx == -1 or text_idx == -1:
                self.message_bar.pushCritical(
                        "Error",
                        _translate(
                                "VeriSO_EE_Geb_LokTest",
                                "Field _benannte_ or _text_ not found.",
                                None))
                QApplication.restoreOverrideCursor()
                return

            benannte = feat.attributes()[benannte_idx]
            lokalisationsname = feat.attributes()[text_idx]

            vlayer_strassenstueck_geometrie.setSubsetString(
                    "(strassenstueck_von = " + str(benannte) + ")")
            vlayer_strassenstueck_anfangspunkt.setSubsetString(
                    "(strassenstueck_von = " + str(benannte) + ")")
            vlayer_benanntesgebiet.setSubsetString(
                    "(benanntesgebiet_von = " + str(benannte) + ")")
            vlayer_gebaeudeeingang.setSubsetString(
                    "(gebaeudeeingang_von = " + str(benannte) + ")")
            vlayer_lokalisation.setSubsetString(
                    "(ogc_fid = " + str(benannte) + ")")
            vlayer_shortestline.setSubsetString(
                    "(lok_tid = " + str(benannte) + ")")
            vlayer_hausnummerpos.setSubsetString(
                    "(lok_tid = " + str(benannte) + ")")

            if vlayer_strassenstueck_geometrie.featureCount() > 0:
                x_min = vlayer_strassenstueck_geometrie.extent().xMinimum()
                y_min = vlayer_strassenstueck_geometrie.extent().yMinimum()
                x_max = vlayer_strassenstueck_geometrie.extent().xMaximum()
                y_max = vlayer_strassenstueck_geometrie.extent().yMaximum()

            if vlayer_benanntesgebiet.featureCount() > 0:
                x_min = vlayer_benanntesgebiet.extent().xMinimum()
                y_min = vlayer_benanntesgebiet.extent().yMinimum()
                x_max = vlayer_benanntesgebiet.extent().xMaximum()
                y_max = vlayer_benanntesgebiet.extent().yMaximum()

            try:
                if vlayer_gebaeudeeingang.featureCount() > 0:
                    if vlayer_gebaeudeeingang.extent().xMinimum() < x_min:
                        x_min = vlayer_gebaeudeeingang.extent().xMinimum()
                    if vlayer_gebaeudeeingang.extent().yMinimum() < y_min:
                        y_min = vlayer_gebaeudeeingang.extent().yMinimum()
                    if vlayer_gebaeudeeingang.extent().xMaximum() > x_max:
                        x_max = vlayer_gebaeudeeingang.extent().xMaximum()
                    if vlayer_gebaeudeeingang.extent().yMaximum() > y_max:
                        y_max = vlayer_gebaeudeeingang.extent().yMaximum()

                rect = QgsRectangle(x_min, y_min, x_max, y_max)
                rect.scale(1.3)

            except UnboundLocalError:
                vlayer_gemeindegrenze = self.getVectorLayerByName(
                        "Gemeindegrenze")
                if vlayer_gemeindegrenze is None:
                    rect = self.canvas.fullExtent()
                else:
                    rect = vlayer_gemeindegrenze.extent()

            self.iface.mapCanvas().setExtent(rect)
            self.iface.mapCanvas().refresh()

            iterator = vlayer_lokalisation.getFeatures()

            # only one feature is selected
            for feature in iterator:
                prinzip_idx = vlayer_lokalisation.fieldNameIndex(
                        "nummerierungsprinzip_txt")
                attributeprovisorisch_idx = vlayer_lokalisation.fieldNameIndex(
                        "attributeprovisorisch_txt")
                offiziell_idx = vlayer_lokalisation.fieldNameIndex(
                        "istoffiziellebezeichnung_txt")
                status_idx = vlayer_lokalisation.fieldNameIndex("status_txt")
                inaenderung_idx = vlayer_lokalisation.fieldNameIndex(
                        "inaenderung_txt")
                art_idx = vlayer_lokalisation.fieldNameIndex("art_txt")

                something_missing = (
                    prinzip_idx == -1
                    or attributeprovisorisch_idx == -1
                    or offiziell_idx == -1
                    or status_idx == -1
                    or inaenderung_idx == -1
                    or art_idx == -1)
                if something_missing:
                    self.message_bar.pushMessage(
                            "Error",
                            _translate("VeriSO_EE_Geb_LokTest",
                                       "Field not found.",
                                       None),
                            level=QgsMessageBar.CRITICAL,
                            duration=0)
                    QApplication.restoreOverrideCursor()
                    return

                prinzip = feature.attributes()[prinzip_idx]
                attributeprovisorisch = feature.attributes()[
                    attributeprovisorisch_idx]
                offiziell = feature.attributes()[offiziell_idx]
                status = feature.attributes()[status_idx]
                inaenderung = feature.attributes()[inaenderung_idx]
                art = feature.attributes()[art_idx]

                map_extent = self.canvas.extent()
                x = map_extent.xMinimum()
                y = map_extent.yMaximum()

            text_item_found = False
            items = list(self.iface.mapCanvas().scene().items())
            for i in range(len(items)):
                try:
                    name = items[i].data(0)
                    if str(name) == "LokalisationsInfo":
                        text_item = items[i]
                        text_item_found = True
                except Exception:
                    pass

            if not text_item_found:
                text_item = QgsTextAnnotationItem(self.canvas)
                text_item.setData(0, "LokalisationsInfo")

            # noinspection PyUnboundLocalVariable
            text_item.setMapPosition(
                    QgsPoint(x + 10 * self.canvas.mapUnitsPerPixel(),
                             y - 10 * self.canvas.mapUnitsPerPixel()))
            text_item.setMapPositionFixed(False)
            text_item.setFrameBorderWidth(0.0)
            text_item.setFrameColor(QColor(250, 250, 250, 255))
            text_item.setFrameBackgroundColor(QColor(250, 250, 250, 123))
            text_item.setFrameSize(QSizeF(250, 150))
            text_document = QTextDocument()
            text_document.setHtml(
                    "<table style='font-size:12px;'><tr><td>Lok.Name: </td><td>"
                    + lokalisationsname + "</td></tr><tr><td>TID: </td><td>"
                    + str(
                            benannte) + "</td></tr> <tr><td>Num.prinzip: "
                                        "</td><td>" +
                    str(prinzip) + "</td></tr> <tr><td>Attr. prov.: </td><td>" +
                    str(attributeprovisorisch) + "</td></tr> <tr><td>ist "
                                                 "offiziell: </td><td>" + str(
                            offiziell) + "</td></tr> <tr><td>Status: "
                                         "</td><td>" + str(
                            status) + "</td></tr> <tr><td>in Aenderung: "
                                      "</td><td>" + str(
                            inaenderung) + "</td></tr> <tr><td>Art: "
                                           "</td><td>" + str(
                            art) + "</td></tr>  </table>")
            text_item.setDocument(text_document)

            # This is a workaround: first ever position is not correct.
            text_item.setMapPosition(
                    QgsPoint(x + 10 * self.canvas.mapUnitsPerPixel(),
                             y - 10 * self.canvas.mapUnitsPerPixel()))
            text_item.update()

            self.iface.mapCanvas().refresh()

            try:
                vlayer_lokalisationsname.setSelectedFeatures([ids[idx + 1]])
            except IndexError:
                self.message_bar.pushInfo("Information", _translate(
                        "VeriSO_EE_Geb_LokTest", "End of table.", None))

        except Exception as e:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()
        QApplication.restoreOverrideCursor()

        # Return QgsVectorLayer from a layer name ( as string )

    # (c) Carson Farmer / fTools
    @staticmethod
    def get_vector_layer_by_name(my_name):
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in list(layermap.items()):
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == \
                    my_name:
                if layer.isValid():
                    return layer
                else:
                    return None
