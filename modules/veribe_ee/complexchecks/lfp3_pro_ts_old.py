 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import sys
import traceback

from veriso.base.utils.doLoadLayer import LoadLayer

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class ComplexCheck(QObject):

    def __init__(self, iface):
        self.iface = iface
        
        self.root = QgsProject.instance().layerTreeRoot()        
        self.layerLoader = LoadLayer(self.iface)

    def run(self):        
        self.settings = QSettings("CatAIS","VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        
        locale = QSettings().value('locale/userLocale')[0:2] # Für Multilingual-Legenden.

        if not project_id:
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_FP3_pro_TS", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_FP3", "FixpunkteKategorie3_pro_TS", None)
            group += " (" + str(project_id) + ")"


            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "VeriSO_EE_FP3", "LFP3", None
            layer["featuretype"] = "fixpunktekategorie3_lfp3"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True            
            layer["group"] = group
            layer["style"] = "fixpunkte/lfp3.qml"

            vlayer = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Toleranzstufen"
            layer["featuretype"] = "tseinteilung_toleranzstufe"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group    
            layer["style"] = "tseinteilung/toleranzstufe.qml"
            vlayer = self.layerLoader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "LFP3 ausserhalb Perimeter"
            layer["featuretype"] = "fixpunktekategorie3_lfp3_ausserhalb_perimeter_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group    
            layer["style"] = "fixpunkte/lfp3_aussen.qml"
            vlayer = self.layerLoader.load(layer, True, True)
      
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "LFP3 pro Toleranzstufe"
            layer["featuretype"] = "fixpunktekategorie3_lfp3_pro_toleranzstufe_v"
            layer["geom"] = ""
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group    
            vlayer = self.layerLoader.load(layer, True, True)
      

           # Bitmap erzeugen.
            img = QImage(QSize(800,600), QImage.Format_ARGB32_Premultiplied)
            color = QColor(255,255,255)
            img.fill(color.rgb())
            p = QPainter()
            p.begin(img)
            p.setRenderHint(QPainter.Antialiasing)
            render = QgsMapRenderer()
            lst = [vlayerOutsidePerimeter.getLayerID(), vlayerLFP3.getLayerID(), vlayerTS.getLayerID() ]  
            render.setLayerSet(lst)
            rect = QgsRectangle(render.fullExtent())
            rect.scale(1.1)
            render.setExtent(rect)
            render.setOutputSize(img.size(), img.logicalDpiX())
            render.render(p)
            p.end()
            img.save("/home/stefan/Downloads/render.png","png")        


        # Statistik aus Datenbank lesen.
            self.dbobj = DbObj("default", "pg",  host,  port,  database,  username,  password)
            self.connected = self.dbobj.connect()
        
            abfrage = """SELECT a.art+1 as toleranzstufe, count(b.tid) as ist, 
CASE 
 WHEN a.art=0 THEN (round(150*c.ts_flaeche/1000000)) 
 WHEN a.art=1 THEN (round(70*c.ts_flaeche/1000000)) 
 WHEN a.art=2 THEN (round(20*c.ts_flaeche/1000000)) 
 WHEN a.art=3 THEN (round(10*c.ts_flaeche/1000000)) 
 WHEN a.art=4 THEN (round(2*c.ts_flaeche/1000000)) 
END as soll, 
CASE 
 WHEN a.art=0 THEN (count(b.tid)-round(150*c.ts_flaeche/1000000)) 
 WHEN a.art=1 THEN (count(b.tid)-round(70*c.ts_flaeche/1000000)) 
 WHEN a.art=2 THEN (count(b.tid)-round(20*c.ts_flaeche/1000000)) 
 WHEN a.art=3 THEN (count(b.tid)-round(10*c.ts_flaeche/1000000)) 
 WHEN a.art=4 THEN (count(b.tid)-round(2*c.ts_flaeche/1000000)) 
END as diff, 
c.ts_flaeche, round((c.ts_flaeche/10000)::numeric, 2) as ts_hektare, c.ts_flaeche/1000000 as ts_km2
FROM """+schema+""".tseinteilung_toleranzstufe as a, """+schema+""".fixpunktekategorie3_lfp3 as b, 
 (SELECT art, sum(ST_Area(a.geometrie)) as ts_flaeche
 FROM """+schema+""".tseinteilung_toleranzstufe a
 WHERE a.gem_bfs = """ + fosnr + """
 AND a.los = """ + lotnr + """
 AND a.lieferdatum = '""" + date + """'
 GROUP BY art
 ORDER BY art) as c
WHERE a.gem_bfs = """ + fosnr + """
AND a.los = """ + lotnr + """
AND a.lieferdatum = '""" + date + """'
AND b.gem_bfs = """ + fosnr + """
AND b.los = """ + lotnr + """
AND b.lieferdatum = '""" + date + """'
AND a.gem_bfs = b.gem_bfs
AND a.los = b.los
AND a.lieferdatum = b.lieferdatum
AND a.art = c.art
AND ST_Distance(a.geometrie, b.geometrie) = 0
GROUP BY a.art, c.ts_flaeche
ORDER BY a.art"""

        if self.connected == True:
            statistik = self.dbobj.read( abfrage )        
            print statistik
            
            if len(statistik['TOLERANZSTUFE']) <> 0:
                try:
                    # Die Excel-Datei anlegen und die Statistik hineinschreiben.
                    wb = pycel.Workbook(encoding='utf-8')
                    wb.country_code = 41

                    style1 = pycel.easyxf('font: bold on;');
                    style2 = pycel.easyxf('font: italic on;');
                    
                    ws = wb.add_sheet(u'LFP3-Statistik')
                    
                    # Operatsinfo in die Datei schreiben.
                    self.writeXLSTitle(ws,  fosnr,  lotnr,  date)
                                
                    # Die Statistik hineinschreiben.
                    ws.write(4, 0, "Toleranzstufe", style2)
                    ws.write(4, 1, u'Fläche [ha]', style2)
                    ws.write(4, 2, "Ist-Anzahl (LFP3)", style2)
                    ws.write(4, 3, "Soll-Anzahl (LFP3)", style2)
                    ws.write(4, 4, "Ist-Soll (LFP3)", style2)    
                    
                    for i in range(len(statistik['TOLERANZSTUFE'])):
                        ws.write(5+i,  0,  str( statistik['TOLERANZSTUFE'][i] ) )
                        ws.write(5+i,  1,  float( statistik['TS_HEKTARE'][i] ) )
                        ws.write(5+i,  2,  int( statistik['IST'][i] ) )
                        ws.write(5+i,  3,  int( statistik['SOLL'][i] ) )
                        ws.write(5+i,  4,  int( statistik['DIFF'][i] ) )

                    ws.write(5+i+2,  0,  "Total")
                    ws.write(5+i+2,  1,  pycel.Formula("SUM(B6:B"+(str(5+1+i))+")"))
                    ws.write(5+i+2,  2,  pycel.Formula("SUM(C6:C"+(str(5+1+i))+")"))                
                    ws.write(5+i+2,  3,  pycel.Formula("SUM(D6:D"+(str(5+1+i))+")"))                     
                    ws.write(5+i+2,  4,  pycel.Formula("SUM(E6:E"+(str(5+1+i))+")"))     
                    
                    # Punkte ausserhalb Gemeindegrenze.
                    ws.write(5+i+4,  0,  "Punkte ausserhalb Perimetergrenze")
                    ws.write(5+i+4,  1,  int(vlayerOutsidePerimeter.featureCount()))
                    
                    # Das Bild in die Datei einfügen.
    #                ws.insert_bitmap(tempdir+os.sep+"render.bmp", 5+i+6,  0)
                    
                    # Excel-Datei speichern.
                    file = tempdir+os.sep+"lfp3-statistik_"+fosnr+"_"+lotnr+"_"+date+".xls"
                    try:
                        wb.save(file)
                        QApplication.restoreOverrideCursor()
                        QMessageBox.information( None, "Export LFP3 statistics", "File written:\n"+ file)
                    except IOError:
                        QApplication.restoreOverrideCursor()
                        QMessageBox.warning( None, "Export LFP3 statistics", "File <b>not</b> written!<br>"+ file)                    
                        return
               
                except KeyError:
                    QMessageBox.warning( None, "", "Database query error.")                
        else:
            QMessageBox.warning( None, "", "Could not connect to database.")
        
        QApplication.restoreOverrideCursor()
            

            
    def writeXLSTitle(self,  ws,  fosnr,  lotnr,  date):
        
            style1 = pycel.easyxf('font: bold on;');
            
            try:
                gemname = self.dbobj.read("SELECT gemname FROM public.gg25 WHERE objectval = "+fosnr)

                ws.write(0, 0,  str("Gemeinde: "), style1 )
                ws.write(0, 1,  unicode( gemname['GEMNAME'][0] ) + str(" (")+str(fosnr)+str(")"))
                    
                ws.write(1, 0,  str("Los: "), style1 )
                ws.write(1, 1, str(lotnr) )
                
                ws.write(2, 0,  str("Lieferdatum"), style1 )
                ws.write(2, 1,  str(date))

            except KeyError:
                QMessageBox.warning( None, "", "Database query error.")
                QApplication.restoreOverrideCursor()
                