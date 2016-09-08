# coding=utf-8
import os
import sys
import traceback
from builtins import str
from qgis.PyQt.QtCore import QDir, QObject, QSettings, Qt
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsProject
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
        self.project_dir = None
        self.project_id = None

    def run(self):
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        self.project_dir = self.settings.value("project/projectdir")
        self.project_id = self.settings.value("project/id")

        locale = QSettings().value('locale/userLocale')[
                 0:2]  # this is for multilingual legends

        if locale == "fr":
            pass
        elif locale == "it":
            pass
        else:
            locale = "de"

        if not project_id:
            self.message_bar.pushCritical("Error",
                                          _translate("VeriSO_V+D_BB",
                                                     "project_id not set",
                                                     None)
                                          )
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_V+D_BB", "Bodenbedeckung", None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_BB", "BB.BoFlaeche", None),
                "featuretype": "bodenbedeckung_boflaeche", "geom": "geometrie",
                "key": "ogc_fid", "sql": "", "readonly": True, "group": group,
                "style": "bodenbedeckung/boflaeche_color.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_BB", "BB.ProjBoFlaeche",
                                    None),
                "featuretype": "bodenbedeckung_projboflaeche",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "bodenbedeckung/projboflaeche_color.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_BB", "EO.Flaechenelemente",
                                    None),
                "featuretype": "v_einzelobjekte_flaechenelement",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "einzelobjekte/eo_flaeche_color.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_BB", "EO.Linienelemente",
                                    None),
                "featuretype": "v_einzelobjekte_linienelement",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "einzelobjekte/eo_linie_color.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_BB", "EO.Punktelemente",
                                    None),
                "featuretype": "v_einzelobjekte_punktelement",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "einzelobjekte/eo_punkte_color.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_BB", "BB.Symbole", None),
                "featuretype": "v_bodenbedeckung_boflaechesymbol",
                "geom": "pos", "key": "ogc_fid", "sql": "", "readonly": True,
                "group": group, "style": "bodenbedeckung/bb_symbole.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True)

            # export some statistics here.

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_BB", "Gemeindegrenze",
                                    None),
                "featuretype": "gemeindegrenzen_gemeindegrenze",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "global_qml/gemeindegrenze/gemgre_strichliert.qml"
            }

            gemgrelayer = self.layer_loader.load(layer)
            if gemgrelayer:
                rect = gemgrelayer.extent()
                self.iface.mapCanvas().setExtent(rect)
                self.iface.mapCanvas().refresh()

                #            self.export_lfp3_pro_ts(vlayer_lfp3_pro_ts)

        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()

    def export_lfp3_pro_ts(self, vlayer):
        try:
            import xlsxwriter
        except Exception as e:
            self.message_bar.pushMessage("Error", str(e),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
            return

            # Create excel file.
        filename = QDir.convertSeparators(
                QDir.cleanPath(
                        os.path.join(self.project_dir, "lfp3_pro_ts.xlsx")))
        workbook = xlsxwriter.Workbook(filename)
        fmt_bold = workbook.add_format({'bold': True, 'font_name': 'Cadastra'})
        fmt_bold_border = workbook.add_format(
                {'bold': True, 'border': 1, 'font_name': 'Cadastra'})
        fmt_border = workbook.add_format({'border': 1, 'font_name': 'Cadastra'})
        fmt_border_decimal = workbook.add_format(
                {'border': 1, 'font_name': 'Cadastra', 'num_format': '0.00'})
        fmt_header = workbook.add_format(
                {'bg_color': '#CACACA', 'border': 1, 'font_name': 'Cadastra'})
        fmt_italic = workbook.add_format(
                {'italic': True, 'border': 1, 'font_name': 'Cadastra'})
        fmt_sum = workbook.add_format({
            'bold': True, 'font_color': 'blue',
            'border': 1, 'font_name': 'Cadastra'
        })
        fmt_sum_decimal = workbook.add_format({
            'bold': True,
            'font_color': 'blue',
            'border': 1,
            'font_name': 'Cadastra',
            'num_format': '0.00'
        })

        # Create the worksheet for the points defects.
        worksheet = workbook.add_worksheet(
                _translate("VeriSO_V+D_BB", u'LFP3 pro TS', None))
        worksheet.set_paper(9)
        worksheet.set_portrait()

        # Write project name into worksheet.
        worksheet.write(0, 0, _translate("VeriSO_V+D_BB", "Operat: ", None),
                        fmt_bold)
        worksheet.write(0, 1, self.project_id, fmt_bold)

        # Write headers.
        worksheet.write(4, 0,
                        _translate("VeriSO_V+D_BB", "Toleranzstufe", None),
                        fmt_header)
        worksheet.write(4, 1,
                        _translate("VeriSO_V+D_BB", "Fläche TS [ha]", None),
                        fmt_header)
        worksheet.write(4, 2,
                        _translate("VeriSO_V+D_BB", "Ist-Anzahl LFP3", None),
                        fmt_header)
        worksheet.write(4, 3,
                        _translate("VeriSO_V+D_BB", "Soll-Anzahl LFP3", None),
                        fmt_header)
        worksheet.write(4, 4,
                        _translate("VeriSO_V+D_BB", "Ist-Soll LFP3", None),
                        fmt_header)

        # Loop through features and add them to worksheet.
        iterator = vlayer.getFeatures()
        j = 0

        ts_idx = vlayer.fieldNameIndex("toleranzstufe")
        area_idx = vlayer.fieldNameIndex("flaeche")
        current_idx = vlayer.fieldNameIndex("ist_anzahl")
        target_idx = vlayer.fieldNameIndex("soll_anzahl")

        start_row = 5
        sum_area = 0
        sum_current = 0
        sum_target = 0
        sum_diff = 0
        for feature in iterator:
            ts = feature.attributes()[ts_idx]
            area = feature.attributes()[area_idx]
            current = feature.attributes()[current_idx]
            target = feature.attributes()[target_idx]

            worksheet.write(start_row + j, 0, ts, fmt_bold_border)
            worksheet.write(start_row + j, 1, area, fmt_border_decimal)
            worksheet.write(start_row + j, 2, current, fmt_border)
            worksheet.write(start_row + j, 3, target, fmt_border)
            worksheet.write(start_row + j, 4, (current - target), fmt_border)

            sum_area += area
            sum_current += current
            sum_target += target
            sum_diff += (current - target)

            j += 1

            # do not forget sum/total
        worksheet.write(start_row + j, 0,
                        _translate("VeriSO_V+D_BB", "Total", None),
                        fmt_bold_border)
        worksheet.write(start_row + j, 1, sum_area, fmt_sum_decimal)
        worksheet.write(start_row + j, 2, sum_current, fmt_sum)
        worksheet.write(start_row + j, 3, sum_target, fmt_sum)
        worksheet.write(start_row + j, 4, sum_diff, fmt_sum)

        # Close excel file.
        workbook.close()
