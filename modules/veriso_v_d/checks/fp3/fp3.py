# coding=utf-8
import os
import sys
import traceback
from builtins import str
from qgis.PyQt.QtCore import QDir, QObject, QSettings, Qt
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
        self.project_dir = None
        self.project_id = None

    def run(self):
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        self.project_dir = self.settings.value("project/projectdir")
        self.project_id = self.settings.value("project/id")

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
                                          _translate("VeriSO_V+D_FP3",
                                                     "project_id not set",
                                                     None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_V+D_FP3", "FixpunkteKategorie3", None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP3", "Toleranzstufen",
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
                "title": _translate("VeriSO_V+D_FP3", "LFP3 Nachführung",
                                    None),
                "featuretype": "fixpunktekategorie3_lfp3nachfuehrung",
                "geom": "perimeter", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group
            }

            vlayer_lfp3_nf = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP3", "LFP3", None),
                "featuretype": "fixpunktekategorie3_lfp3", "geom": "geometrie",
                "key": "ogc_fid", "sql": "", "readonly": True, "group": group,
                "style": "fixpunkte/lfp3_" + locale + ".qml"
            }

            vlayer_lfp3 = self.layer_loader.load(layer)

            # Join two layers (lfp3 and lfp3nachfuehrung)
            lfp3_field = "entstehung"
            lfp3_nf_field = "ogc_fid"
            join_obj = QgsVectorJoinInfo()
            join_obj.joinLayerId = vlayer_lfp3_nf.id()
            join_obj.joinFieldName = lfp3_nf_field
            join_obj.targetFieldName = lfp3_field
            join_obj.memoryCache = True
            join_obj.prefix = "lfp3_nf_"
            vlayer_lfp3.addJoin(join_obj)

            layer = {
                "type": "postgres", "title": _translate("VeriSO_V+D_FP3",
                                                        "LFP3 ausserhalb "
                                                        "Gemeinde",
                                                        None),
                "featuretype": "t_lfp3_ausserhalb_gemeinde",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "fixpunkte/lfp3ausserhalb.qml"
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP3", "LFP3 pro TS", None),
                "featuretype": "t_lfp3_pro_ts", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group
            }

            vlayer_lfp3_pro_ts = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_V+D_FP3", "Gemeindegrenze",
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
            # sz / 2015-04-20: 
            # Aaaah: still a problem. Some really strange combination of
            # checked/unchecked-order-of-layers-thing?
            # If wms is addes after gemgre then is scales (rect.scale(5))?!
            # So it seems that the last added layer HAS TO BE unchecked?
            # No not exactly. Only if a wms is added before?
            # rect.scale(5) has no effect?

            # I reopened the ticket / 2015-04-20 / sz

            if gemgrelayer:
                rect = gemgrelayer.extent()
                rect.scale(5)
                self.iface.mapCanvas().setExtent(rect)
                self.iface.mapCanvas().refresh()
                # Sometimes it does make much more sense
            # to zoom to maximal extent:
            # self.iface.mapCanvas().zoomToFullExtent()

            self.export_to_excel(vlayer_lfp3_pro_ts)

        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()

    def export_to_excel(self, vlayer):
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
                _translate("VeriSO_V+D_FP3", u'LFP3 pro TS', None))
        worksheet.set_paper(9)
        worksheet.set_portrait()

        # Write project name into worksheet.
        worksheet.write(0, 0, _translate("VeriSO_V+D_FP3", "Operat: ", None),
                        fmt_bold)
        worksheet.write(0, 1, self.project_id, fmt_bold)

        # Write headers.
        worksheet.write(4, 0,
                        _translate("VeriSO_V+D_FP3", "Toleranzstufe", None),
                        fmt_header)
        worksheet.write(4, 1,
                        _translate("VeriSO_V+D_FP3", "Fläche TS [ha]", None),
                        fmt_header)
        worksheet.write(4, 2,
                        _translate("VeriSO_V+D_FP3", "Ist-Anzahl LFP3", None),
                        fmt_header)
        worksheet.write(4, 3,
                        _translate("VeriSO_V+D_FP3", "Soll-Anzahl LFP3", None),
                        fmt_header)
        worksheet.write(4, 4,
                        _translate("VeriSO_V+D_FP3", "Ist-Soll LFP3", None),
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
                        _translate("VeriSO_V+D_FP3", "Total", None),
                        fmt_bold_border)
        worksheet.write(start_row + j, 1, sum_area, fmt_sum_decimal)
        worksheet.write(start_row + j, 2, sum_current, fmt_sum)
        worksheet.write(start_row + j, 3, sum_target, fmt_sum)
        worksheet.write(start_row + j, 4, sum_diff, fmt_sum)

        # Close excel file.
        workbook.close()
