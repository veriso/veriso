# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import time
import os
import sys
import traceback

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class ExportDefects(QObject):
    def __init__(self, iface):
        self.iface = iface
        
    def run(self):
        try:
            import xlwt as pycel
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=10)                    
            return        
        
        try:        
            settings = QSettings("CatAIS","VeriSO")
            module_name = settings.value("project/appmodule")
            provider = settings.value("project/provider")
            dbhost = settings.value("project/dbhost")
            dbport = settings.value("project/dbport")
            dbname = settings.value("project/dbname")
            dbschema = settings.value("project/dbschema")
            dbuser = settings.value("project/dbuser")
            dbpwd = settings.value("project/dbpwd")
            dbadmin = settings.value("project/dbadmin")
            dbadminpwd = settings.value("project/dbadminpwd")
            projectId = settings.value("project/id")
            projectdir = settings.value("project/projectdir")

            if not dbhost or not dbport or not dbname or not dbschema or not dbuser or not dbpwd or not dbadmin or not dbadminpwd:
                self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_Defects", "Missing database parameter. Cannot load layer.", None), level=QgsMessageBar.CRITICAL, duration=10)                    
                return
            
            uri = QgsDataSourceURI()        
            uri.setConnection(dbhost, dbport, dbname, dbuser, dbpwd)
            uri.setDataSource(dbschema, "t_maengel_punkt", "the_geom", "", "ogc_fid")        
            vlayer_points = QgsVectorLayer(uri.uri(), "Maengel (Punkte)", "postgres")
            
            uri = QgsDataSourceURI()        
            uri.setConnection(dbhost, dbport, dbname, dbuser, dbpwd)
            uri.setDataSource(dbschema, "t_maengel_linie", "the_geom", "", "ogc_fid")        
            vlayer_lines = QgsVectorLayer(uri.uri(), "Maengel (Linien)", "postgres")

            if not vlayer_points.isValid():
                self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_Defects", "Could not load defects layer.", None), level=QgsMessageBar.CRITICAL, duration=10)                    
                return
            
            if not vlayer_lines.isValid():
                self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_Defects", "Could not load defects layer.", None), level=QgsMessageBar.CRITICAL, duration=10)                                    
                return        
            
            if vlayer_points.featureCount() == 0 and vlayer_lines.featureCount() == 0:
                self.iface.messageBar().pushMessage("Information",  _translate("VeriSO_EE_Defects", "Defects layer are empty.", None), level=QgsMessageBar.INFO, duration=10)                                                    
                return

            # create excel file
            wb = pycel.Workbook(encoding='utf-8')
            wb.country_code = 41
            
            style1 = pycel.easyxf('font: bold on;');
            style2 = pycel.easyxf('font: italic on;');
            
            ws = wb.add_sheet(u'Mängelliste (Punkte)')
            ws.paper_size_code = 8
            ws.print_centered_vert = False
            ws.print_centered_horz = False
            ws.top_margin = 1.0
            ws.left_margin = 1.0 
            ws.bottom_margin = 1.0
            ws.portrait = True
            
            ws.write(0, 0,  str("Operat: "), style1 )
            ws.write(0, 1,  projectId)        


            provider = vlayer_points.dataProvider()
            attrs = provider.fields()
            types = []
            
            for i in range(len(attrs)):
                ws.write(4, i, str(attrs.at(i).name()), style2)
                types.append(attrs.at(i).type())

            ws.write(4, i+1, "Y-Koordinate", style2)
            ws.write(4, i+2, "X-Koordinate", style2)            

            iter = vlayer_points.getFeatures()
            j = 0

            for feat in iter:
                geom = feat.geometry()
                point = geom.asPoint()            
                attrs = feat.attributes()
                k = 0
                
                for attr in attrs:
                    type = types[k]
                    
                    if type == QVariant.Int or type == QVariant.LongLong:
                        value = int(attr)
                    elif type == QVariant.Double:
                        value = double(attr)
                    elif type == QVariant.String:
                        value = unicode(attr)
                    elif type == QVariant.Date or type == QVariant.DateTime:
                        value = attr.toString("dd.MM.yy")
                    else:
                        value = "unknown attribute type"
                        
                    ws.write(5+j, k, value)

                    k += 1
                    
                ws.write(5+j, k, round(point.x(), 3))
                ws.write(5+j, k+1, round(point.y(), 3))
                    
                j += 1                
                

            ws_line = wb.add_sheet(u'Mängelliste (Linien)')
            ws_line.paper_size_code = 8
            ws_line.print_centered_vert = False
            ws_line.print_centered_horz = False
            ws_line.top_margin = 1.0
            ws_line.left_margin = 1.0 
            ws_line.bottom_margin = 1.0
            ws_line.portrait = True
            
            ws_line.write(0, 0,  str("Operat: "), style1 )
            ws_line.write(0, 1,  projectId)        


            provider = vlayer_lines.dataProvider()
            attrs = provider.fields()
            types = []
            
            for i in range(len(attrs)):
                ws_line.write(4, i, str(attrs.at(i).name()), style2)
                types.append(attrs.at(i).type())

            ws_line.write(4, i+1, "Y-Koordinate", style2)
            ws_line.write(4, i+2, "X-Koordinate", style2)            
            ws_line.write(4, i+3, u"Länge [hm]", style2)  

            iter = vlayer_lines.getFeatures()
            j = 0

            for feat in iter:
                geom = feat.geometry()
                point = geom.vertexAt(0)
                attrs = feat.attributes()
                k = 0
                
                for attr in attrs:
                    type = types[k]
                    
                    if type == QVariant.Int or type == QVariant.LongLong:
                        value = int(attr)
                    elif type == QVariant.Double:
                        value = double(attr)
                    elif type == QVariant.String:
                        value = unicode(attr)
                    elif type == QVariant.Date or type == QVariant.DateTime:
                        value = attr.toString("dd.MM.yy")
                    else:
                        value = "unknown attribute type"
                        
                    ws_line.write(5+j, k, value)

                    k += 1
                    
                ws_line.write(5+j, k, round(point.x(), 3))
                ws_line.write(5+j, k+1, round(point.y(), 3))
                ws_line.write(5+j, k+2, round(geom.length(), 2))

                j += 1      

            file = QDir.convertSeparators(QDir.cleanPath(os.path.join(projectdir, "maengel.xls")))
            wb.save(file)
            
            self.iface.messageBar().pushMessage("Information",  _translate("VeriSO_EE_Defects", "Defect(s) written: ", None) + str(file), level=QgsMessageBar.INFO, duration=10)                                                    
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error",  _translate("QcadastreModule", "Defect(s) <b>not</b> written!<br>. ", None) + str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=10)                                
            return
