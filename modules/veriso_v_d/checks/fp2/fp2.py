# coding=utf-8
import sys
import traceback
from builtins import str
from qgis.PyQt.QtCore import QObject, QSettings, Qt
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsProject, QgsVectorJoinInfo
from qgis.gui import QgsMessageBar

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
    names = OrderedDict()
    names['de'] = u'Übersicht'
    names['fr'] = "Vue d'ensemble"

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)

    def run(self):
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")

        locale = QSettings().value('locale/userLocale')[
                 0:2]  # this is for multilingual legends

        # If locale is different to frence or italian, german will be used.
        # Otherwise we get into troubles with the legends, e.g. locale = "en"
        # but
        # there is no english legend (qml file).
        if locale == "fr":
            pass
        elif locale == "it":
            pass
        else:
            locale = "de"

        if not project_id:
            self.message_bar.pushCritical("Error",
                                          _translate("VeriSO_V+D_FP2",
                                                     "project_id not set",
                                                     None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_V+D_FP2", "FixpunkteKategorie2", None)
            group += " (" + str(project_id) + ")"

            # Lagefixpunkte 2

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP2", "LFP2 Nachführung",
                                    None),
                "featuretype": "fixpunktekategorie2_lfp2nachfuehrung",
                "geom": "perimeter", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group
            }

            # Visibility and if legend and/or groupd should be collapsed can
            # be set with parameters in the self.layer_loader.load()
            # method:
            # load(layer, visibility=True, collapsed_legend=False,
            # collapsed_group=False)
            vlayer_lfp2_nf = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP2", "LFP2", None),
                "featuretype": "fixpunktekategorie2_lfp2", "geom": "geometrie",
                "key": "ogc_fid", "sql": "", "readonly": True, "group": group,
                "style": "fixpunkte/lfp2.qml"
            }

            vlayer_lfp2 = self.layer_loader.load(layer)

            # Join two layers (lfp2 and lfp2nachfuehrung)
            lfp2_field = "entstehung"
            lfp2_nf_field = "ogc_fid"
            join_obj = QgsVectorJoinInfo()
            join_obj.joinLayerId = vlayer_lfp2_nf.id()
            join_obj.joinFieldName = lfp2_nf_field
            join_obj.targetFieldName = lfp2_field
            join_obj.memoryCache = True
            join_obj.prefix = "lfp2_nf_"
            vlayer_lfp2.addJoin(join_obj)

            # This is how WMS layer work.
            layer = {
                "type": "wms",
                "title": _translate("VeriSO_V+D_FP2", "LFP2 Schweiz (WMS)",
                                    None),
                "url": "http://wms.geo.admin.ch/",
                "layers": "ch.swisstopo.fixpunkte-lfp2",
                "format": "image/png", "crs": "EPSG:" + str(epsg),
                "group": group
            }

            vlayer = self.layer_loader.load(layer, False, True)

            # Höhenfixpunkte 2
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP2", "HFP2 Nachführung",
                                    None),
                "featuretype": "fixpunktekategorie2_hfp2nachfuehrung",
                "geom": "perimeter", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group
            }

            vlayer_hfp2_nf = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP2", "HFP2", None),
                "featuretype": "fixpunktekategorie2_hfp2", "geom": "geometrie",
                "key": "ogc_fid", "sql": "", "readonly": True, "group": group,
                "style": "fixpunkte/hfp2.qml"
            }

            vlayer_hfp2 = self.layer_loader.load(layer)

            # Join two layers (hfp2 and hfp2nachfuehrung)
            hfp2_field = "entstehung"
            hfp2_nf_field = "ogc_fid"
            join_obj = QgsVectorJoinInfo()
            join_obj.joinLayerId = vlayer_hfp2_nf.id()
            join_obj.joinFieldName = hfp2_nf_field
            join_obj.targetFieldName = hfp2_field
            join_obj.memoryCache = True
            join_obj.prefix = "hfp2_nf_"
            vlayer_hfp2.addJoin(join_obj)

            layer = {
                "type": "wms",
                "title": _translate("VeriSO_V+D_FP2", "HFP2 Schweiz (WMS)",
                                    None),
                "url": "http://wms.geo.admin.ch/",
                "layers": "ch.swisstopo.fixpunkte-hfp2",
                "format": "image/png", "crs": "EPSG:" + str(epsg),
                "group": group
            }

            vlayer = self.layer_loader.load(layer, False, True)

            # Business as usual: Gemeindegrenzen
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP2", "Gemeindegrenze",
                                    None),
                "featuretype": "gemeindegrenzen_gemeindegrenze",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "global_qml/gemeindegrenze/gemgre_strichliert.qml"
            }

            gemgrelayer = self.layer_loader.load(layer)

            # Change map extent.
            # Bug (?) in QGIS: http://hub.qgis.org/issues/10980
            # Closed for the lack of feedback. Upsi...
            # Still a problem? (sz / 2015-04-12)
            if gemgrelayer:
                rect = gemgrelayer.extent()
                rect.scale(5)
                self.iface.mapCanvas().setExtent(rect)
                self.iface.mapCanvas().refresh()
                # Sometimes it does make much more sense
                # to zoom to maximal extent:
                # self.iface.mapCanvas().zoomToFullExtent()

        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()
