# coding=utf-8
import sys
import traceback
from builtins import str
from collections import OrderedDict
from qgis.PyQt.QtCore import QSettings, Qt
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsProject
from qgis.gui import QgsMessageBar

from veriso.modules.complexcheck_base import ComplexCheckBase
from veriso.base.utils.loadlayer import LoadLayer

try:
    _encoding = QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class ComplexCheck(ComplexCheckBase):
    names = OrderedDict()
    names['de'] = u'Übersicht'
    names['fr'] = "Vue d'ensemble"

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)
        self.iface = iface
        self.message_bar = self.iface.messageBar()

        self.root = QgsProject.instance().layerTreeRoot()
        self.layer_loader = LoadLayer(self.iface)
        self.settings = QSettings("CatAIS", "VeriSO")

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
                                          _translate("VeriSO_EE_FP3",
                                                     "project_id not set",
                                                     None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_FP3", "FixpunkteKategorie3", None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_FP3", "Toleranzstufen",
                                    None),
                "featuretype": "tseinteilung_toleranzstufe",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "tseinteilung/toleranzstufe_" + locale + ".qml"
            }

            # Visibility and if legend and/or groupd should be collapsed can
            # be set with parameters in the self.layer_loader.load()
            # method:
            # load(layer, visibility=True, collapsed_legend=False,
            # collapsed_group=False)
            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_FP3", "LFP3 Nachführung",
                                    None),
                "featuretype": "fixpunktekategorie3_lfp3nachfuehrung",
                "geom": "perimeter", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group
            }

            vlayer = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_FP3", "LFP3", None),
                "featuretype": "fixpunktekategorie3_lfp3", "geom": "geometrie",
                "key": "ogc_fid", "sql": "", "readonly": True, "group": group,
                "style": "fixpunkte/lfp3_" + locale + ".qml"
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres", "title": _translate("VeriSO_EE_FP3",
                                                        "LFP3 ausserhalb "
                                                        "Gemeinde",
                                                        None),
                "featuretype": "t_lfp3_ausserhalb_gemeinde",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "fixpunkte/lfp3ausserhalb.qml"
            }

            vlayer = self.layer_loader.load(layer)

            # This is how WMS layer work.
            layer = {
                "type": "wms",
                "title": _translate("VeriSO_EE_FP3", "LFP1 + LFP2 Schweiz",
                                    None),
                "url": "http://wms.geo.admin.ch/",
                "layers": "ch.swisstopo.fixpunkte-lfp1,"
                          "ch.swisstopo.fixpunkte-lfp2",
                "format": "image/png", "crs": "EPSG:" + str(epsg),
                "group": group
            }

            vlayer = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_FP3", "Gemeindegrenze",
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
