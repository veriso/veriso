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
            import xlsxwriter
        except Exception, e:
            self.iface.messageBar().pushMessage("Error", str(e), level=QgsMessageBar.CRITICAL, duration=10)                    
            return        
        
        try:        
            settings = QSettings("CatAIS","VeriSO")
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
                self.iface.messageBar().pushMessage("Error",  self.tr("Missing database schema parameter."), level=QgsMessageBar.CRITICAL, duration=5)                                
                return
                
            if not db_host:
                self.iface.messageBar().pushMessage("Error",  self.tr("Missing database host parameter."), level=QgsMessageBar.CRITICAL, duration=5)                                
                return
            
            if not db_name:
                self.iface.messageBar().pushMessage("Error",  self.tr("Missing database name parameter."), level=QgsMessageBar.CRITICAL, duration=5)                                
                return

            if not db_port:
                self.iface.messageBar().pushMessage("Error",  self.tr("Missing database port parameter."), level=QgsMessageBar.CRITICAL, duration=5)                                
                return
                
            if not db_user:
                self.iface.messageBar().pushMessage("Error",  self.tr("Missing database user parameter."), level=QgsMessageBar.CRITICAL, duration=5)                                
                return

            if not db_pwd:
                self.iface.messageBar().pushMessage("Error",  self.tr("Missing database user password parameter."), level=QgsMessageBar.CRITICAL, duration=5)                                
                return

#            if not db_admin:
#                self.iface.messageBar().pushMessage("Error",  self.tr("Missing database administrator parameter."), level=QgsMessageBar.CRITICAL, duration=5)                                
#                return
#                
#            if not db_admin_pwd:
#                self.iface.messageBar().pushMessage("Error",  self.tr("Missing database administrator password parameter."), level=QgsMessageBar.CRITICAL, duration=5)                                
#                return
                
            if not provider:
                self.iface.messageBar().pushMessage("Error",  self.tr("Missing provider parameter. Cannot load layer."), level=QgsMessageBar.CRITICAL, duration=5)                    
                return        
            
            if not module_name:
                self.iface.messageBar().pushMessage("Error",  self.tr("Missing module name parameter. Cannot load layer."), level=QgsMessageBar.CRITICAL, duration=5)                    
                return        
            
            uri = QgsDataSourceURI()        
            uri.setConnection(db_host, db_port, db_name, db_user, db_pwd)
            uri.setDataSource(db_schema, "t_maengel_punkt", "the_geom", "", "ogc_fid")        
            vlayer_points = QgsVectorLayer(uri.uri(), "Maengel (Punkte)", "postgres")
            
            uri = QgsDataSourceURI()        
            uri.setConnection(db_host, db_port, db_name, db_user, db_pwd)
            uri.setDataSource(db_schema, "t_maengel_linie", "the_geom", "", "ogc_fid")        
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

            # Create excel file.
            filename = QDir.convertSeparators(QDir.cleanPath(os.path.join(project_dir, "maengel.xlsx")))     
            workbook = xlsxwriter.Workbook(filename)
            fmt_bold = workbook.add_format({'bold': True})
            fmt_italic = workbook.add_format({'italic': True})
            
            # Create the worksheet for the points defects.
            worksheet_points = workbook.add_worksheet( _translate("VeriSO_EE_Defects", u'Mängelliste (Punkte)', None))
            worksheet_points.set_paper(9)
            worksheet_points.set_portrait()
            
            # Write project name into worksheet.
            worksheet_points.write(0, 0,  _translate("VeriSO_EE_Defects", "Operat: ", None), fmt_bold)
            worksheet_points.write(0, 1,  project_id, fmt_bold)
            
            # Write defects. Loop through field to write header.
            # Then loop through features.
            provider = vlayer_points.dataProvider()
            attrs = provider.fields()

#            types = []            
            for i in range(len(attrs)):
                worksheet_points.write(4, i, str(attrs.at(i).name()), fmt_italic)
#                types.append(attrs.at(i).type())

            worksheet_points.write(4, i+1, _translate("VeriSO_EE_Defects", "Y-Koordinate", None), fmt_italic)
            worksheet_points.write(4, i+2, _translate("VeriSO_EE_Defects", "X-Koordinate", None), fmt_italic)            

            iter = vlayer_points.getFeatures()
            j = 0

            for feat in iter:
                geom = feat.geometry()
                point = geom.asPoint()            
                attrs = feat.attributes()
                k = 0
                
                # Types are not needed anymore?
                # "write" uses appropriate method (write_datetime etc) for
                # specific python type.
                # But, possible bug in QGIS: "datum" is mapped to QString.
                # It is a timestamp in the database.
                for attr in attrs:
                    if attr: # Unsupported type <class 'PyQt4.QtCore.QPyNullVariant'> in write()                    
                        worksheet_points.write(5+j, k, attr)
                    k += 1
                    
                # TODO: better use formats instead of rounding.                    
                worksheet_points.write(5+j, k, round(point.x(), 3))
                worksheet_points.write(5+j, k+1, round(point.y(), 3))
                j += 1 

            # Create the worksheet for the line defects.
            worksheet_lines = workbook.add_worksheet( _translate("VeriSO_EE_Defects", u'Mängelliste (Linien)', None))
            worksheet_lines.set_paper(9)
            worksheet_lines.set_portrait()
            
            # Write project name into worksheet.
            worksheet_lines.write(0, 0,  _translate("VeriSO_EE_Defects", "Operat: ", None), fmt_bold)
            worksheet_lines.write(0, 1,  project_id, fmt_bold)
            
            # Write defects. Loop through field to write header.
            # Then loop through features.
            provider = vlayer_lines.dataProvider()
            attrs = provider.fields()

#            types = []
            for i in range(len(attrs)):
                worksheet_lines.write(4, i, str(attrs.at(i).name()), fmt_italic)
#                types.append(attrs.at(i).type())

            worksheet_lines.write(4, i+1, _translate("VeriSO_EE_Defects", "Y-Koordinate", None), fmt_italic)
            worksheet_lines.write(4, i+2, _translate("VeriSO_EE_Defects", "X-Koordinate", None), fmt_italic)            
            worksheet_lines.write(4, i+3, _translate("VeriSO_EE_Defects", u"Länge [hm]", None), fmt_italic)            

            iter = vlayer_lines.getFeatures()
            j = 0

            for feat in iter:
                geom = feat.geometry()
                point = geom.vertexAt(0)
                attrs = feat.attributes()
                k = 0
                
                for attr in attrs:
                    if attr: # Unsupported type <class 'PyQt4.QtCore.QPyNullVariant'> in write()
                        worksheet_lines.write(5+j, k, attr)
                    k += 1
              
                worksheet_lines.write(5+j, k, round(point.x(), 3))
                worksheet_lines.write(5+j, k+1, round(point.y(), 3))
                worksheet_lines.write(5+j, k+2, round(geom.length(), 2))
                j += 1      
            
            # Close excel file.
            workbook.close()
            
            self.iface.messageBar().pushMessage("Information",  _translate("VeriSO_EE_Defects", "Defect(s) written: ", None) + str(filename), level=QgsMessageBar.INFO, duration=10)                                                    
        except Exception, e:
            message = "Error while writing defects file."
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_Defects", message, None), level=QgsMessageBar.CRITICAL, duration=10)       
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)                  
            return
