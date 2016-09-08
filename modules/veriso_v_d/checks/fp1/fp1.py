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
                                          _translate("VeriSO_V+D_FP1",
                                                     "project_id not set",
                                                     None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_V+D_FP1", "FixpunkteKategorie1", None)
            group += " (" + str(project_id) + ")"

            # Lagefixpunkte 1

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP1", "LFP1 Nachführung",
                                    None),
                "featuretype": "fixpunktekategorie1_lfp1nachfuehrung",
                "geom": "perimeter", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group
            }

            # Visibility and if legend and/or groupd should be collapsed can
            # be set with parameters in the self.layer_loader.load()
            # method:
            # load(layer, visibility=True, collapsed_legend=False,
            # collapsed_group=False)
            vlayer_lfp1_nf = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP1", "LFP1", None),
                "featuretype": "fixpunktekategorie1_lfp1", "geom": "geometrie",
                "key": "ogc_fid", "sql": "", "readonly": True, "group": group,
                "style": "fixpunkte/lfp2.qml"
            }

            vlayer_lfp1 = self.layer_loader.load(layer)

            # Join two layers (lfp1 and lfp1nachfuehrung)
            lfp1_field = "entstehung"
            lfp1_nf_field = "ogc_fid"
            join_obj = QgsVectorJoinInfo()
            join_obj.joinLayerId = vlayer_lfp1_nf.id()
            join_obj.joinFieldName = lfp1_nf_field
            join_obj.targetFieldName = lfp1_field
            join_obj.memoryCache = True
            join_obj.prefix = "lfp1_nf_"
            vlayer_lfp1.addJoin(join_obj)

            # This is how WMS layer work.
            layer = {
                "type": "wms",
                "title": _translate("VeriSO_V+D_FP1", "LFP1 Schweiz (WMS)",
                                    None),
                "url": "http://wms.geo.admin.ch/",
                "layers": "ch.swisstopo.fixpunkte-lfp1",
                "format": "image/png", "crs": "EPSG:" + str(epsg),
                "group": group
            }

            vlayer = self.layer_loader.load(layer, False, True)

            # Höhenfixpunkte 1
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP1", "HFP1 Nachführung",
                                    None),
                "featuretype": "fixpunktekategorie1_hfp1nachfuehrung",
                "geom": "perimeter", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group
            }

            vlayer_hfp1_nf = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP1", "HFP1", None),
                "featuretype": "fixpunktekategorie1_hfp1", "geom": "geometrie",
                "key": "ogc_fid", "sql": "", "readonly": True, "group": group,
                "style": "fixpunkte/hfp2.qml"
            }

            vlayer_hfp1 = self.layer_loader.load(layer)

            # Join two layers (hfp1 and hfp1nachfuehrung)
            hfp1_field = "entstehung"
            hfp1_nf_field = "ogc_fid"
            join_obj = QgsVectorJoinInfo()
            join_obj.joinLayerId = vlayer_hfp1_nf.id()
            join_obj.joinFieldName = hfp1_nf_field
            join_obj.targetFieldName = hfp1_field
            join_obj.memoryCache = True
            join_obj.prefix = "hfp1_nf_"
            vlayer_hfp1.addJoin(join_obj)

            layer = {
                "type": "wms",
                "title": _translate("VeriSO_V+D_FP1", "HFP1 Schweiz (WMS)",
                                    None),
                "url": "http://wms.geo.admin.ch/",
                "layers": "ch.swisstopo.fixpunkte-hfp1",
                "format": "image/png", "crs": "EPSG:" + str(epsg),
                "group": group
            }

            vlayer = self.layer_loader.load(layer, False, True)

            # Business as usual: Gemeindegrenzen
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP1", "Gemeindegrenze",
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
