 # -*- coding: utf8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from soverify.tools.dbTools import DbObj
import soverify.tools.utils
import os, time
import xlwt as pycel

class ComplexCheck( QObject ):
    
    def __init__( self,  iface,  settings ):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        pass
        
    def run( self ):        
        settings = soverify.tools.utils.getSettings()

        if settings["fosnr"] == "" or settings["lotnr"] == "" or settings["date"] == "" or settings["tempdir"] == "":
            QMessageBox.warning( None, "", "No workspace parameters or temp directory set.")
            return

        if settings["host"] == "" or settings["database"] == "" or settings["port"] == "" or settings["schema"] == "" or settings["username"] == "" or settings["password"] == "":
            QMessageBox.warning( None, "", "No database parameters set.")
            return
            
        fosnr = settings["fosnr"]
        lotnr = settings["lotnr"]
        date = settings["date"]
        
        tempdir = settings["tempdir"]        
        
        host = settings["host"]
        database = settings["database"]
        schema = settings["schema"]
        port =  settings["port"]
        username = settings["username"]
        password = settings["password"]

        group = "Topologiefehler" + " (" + str(fosnr) + " / " + str(lotnr) + " / " + str(date) + ")"

        #Change the cursor.
        QApplication.setOverrideCursor(Qt.WaitCursor)

        try:


            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Gemeindegrenze (Referenzperimeter)"
            layer["readonly"] = True 
            layer["featuretype"] = "gemeindegrenzen_gemeindegrenze"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "gemeindegrenze/gemeindegrenze_"+_locale+".qml"           
            vlayerGemeinde = soverify.tools.utils.doShowSimpleLayer( self.iface,  table,  True,  settings,  True,  True)
                  
         
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Toleranzstufen "
            layer["readonly"] = True 
            layer["featuretype"] = "tseinteilung_toleranzstufe"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "tseinteilung/toleranzstufe_"+_locale+".qml"
            vlayerToleranzstufe = soverify.tools.utils.doShowSimpleLayer( self.iface,  table,  True,  settings, False,  False, False)            
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Toleranzstufen Topologiefehler"
            layer["readonly"] = True 
            layer["featuretype"] = "tseinteilung_toleranzstufe_topologiefehler"
            layer["geom"] = "the_geom"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "tseinteilung/topofehler_"+_locale+".qml"            
            vlayerToleranzstufeTopofehler = soverify.tools.utils.doShowSimpleLayer( self.iface,  table,  True,  settings, False,  False)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Plangeometrie"
            layer["readonly"] = True 
            layer["featuretype"] = "planeinteilungen_plan_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "planeinteilung/plangeometrie_"+_locale+".qml"
            vlayerPlangeometrie = soverify.tools.utils.doShowSimpleLayer( self.iface,  table,  True,  settings,  False,  True, False)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Plangeometrie Topologiefehler"
            layer["readonly"] = True 
            layer["featuretype"] = "planeinteilungen_plangeometrie_topologiefehler"
            layer["geom"] = "the_geom"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "planeinteilung/topofehler_"+_locale+".qml"
            vlayerPlangeometrieTopofehler = soverify.tools.utils.doShowSimpleLayer( self.iface,  table,  True,  settings,  False,  True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Liegenschaften"
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_liegenschaft"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group        
            layer["style"] = "liegenschaften/liegenschaft_"+_locale+".qml"
            vlayerLiegenschaften = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Liegenschaften Topologiefehler"
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_liegenschaft_topologiefehler"
            layer["geom"] = "the_geom"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group        
            layer["style"] = "tseinteilung/topofehler_"+_locale+".qml"
            vlayerLiegenschaftenTopofehler = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Flurnamen"
            layer["readonly"] = True 
            layer["featuretype"] = "nomenklatur_flurname"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group        
            layer["style"] = "nomenklatur/nomenklatur_"+_locale+".qml"
            vlayerFlurnamen = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Flurnamen Topologiefehler"
            layer["readonly"] = True 
            layer["featuretype"] = "nomenklatur_flurname_topologiefehler"
            layer["geom"] = "the_geom"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group        
            layer["style"] = "tseinteilung/topofehler_"+_locale+".qml"
            vlayerFlurnamenTopofehler = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Bodenbedeckung"
            layer["readonly"] = True 
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "bodenbedeckung/bb_kante_"+_locale+".qml"
            vlayerBodenbedeckung = soverify.tools.utils.doShowSimpleLayer( self.iface,  table,  True,  settings,  False,  False, False, False)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Bodenbedeckung Topologiefehler"
            layer["readonly"] = True 
            layer["featuretype"] = "bodenbedeckung_boflaeche_topologiefehler"
            layer["geom"] = "the_geom"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "tseinteilung/topofehler_"+_locale+".qml"
            vlayerBodenbedeckungTopofehler = self.layerLoader.load(layer)


         
            QApplication.restoreOverrideCursor()
            
            self.dbobj = DbObj("default", "pg",  host, port, database, username, password)
            connected = self.dbobj.connect()
            
            if connected == True:
                try:            
                    
                    result = self.dbobj.read( "SELECT ST_Area(geometrie) as flaeche FROM "+schema+".gemeindegrenzen_gemeindegrenze WHERE gem_bfs = " + fosnr + " AND los = " + lotnr + " AND lieferdatum = '" + date  + "'")
                    areaReference = result['FLAECHE'][0]
                
                    result = self.dbobj.read( "SELECT sum(ST_Area(geometrie)) as flaeche FROM "+schema+".bodenbedeckung_boflaeche WHERE gem_bfs = " + fosnr + " AND los = " + lotnr + " AND lieferdatum = '" + date + "'" )
                    areaBB = result['FLAECHE'][0]          
                  
                    result = self.dbobj.read( "SELECT sum(ST_Area(geometrie)) as flaeche FROM "+schema+".nomenklatur_flurname WHERE gem_bfs = " + fosnr + " AND los = " + lotnr + " AND lieferdatum = '" + date + "'" )
                    areaNO = result['FLAECHE'][0]   
                
                    result = self.dbobj.read( "SELECT sum(ST_Area(geometrie)) as flaeche FROM "+schema+".liegenschaften_liegenschaft WHERE gem_bfs = " + fosnr + " AND los = " + lotnr + " AND lieferdatum = '" + date + "'" )
                    areaLS = result['FLAECHE'][0]
                    
                    result = self.dbobj.read( "SELECT sum(ST_Area(geometrie)) as flaeche FROM "+schema+".planeinteilungen_plangeometrie WHERE gem_bfs = " + fosnr + " AND los = " + lotnr + " AND lieferdatum = '" + date + "'" )
                    areaPL = result['FLAECHE'][0]      
          
                    result = self.dbobj.read( "SELECT sum(ST_Area(geometrie)) as flaeche FROM "+schema+".tseinteilung_toleranzstufe WHERE gem_bfs = " + fosnr + " AND los = " + lotnr + " AND lieferdatum = '" + date + "'" )
                    areaTS = result['FLAECHE'][0]           

                    # Die Excel-Datei anlegen und die Statistik hineinschreiben.
                    wb = pycel.Workbook(encoding='utf-8')
                    wb.country_code = 41

                    style1 = pycel.easyxf('font: bold on;');
                    style2 = pycel.easyxf('font: italic on;');
                    
                    ws = wb.add_sheet(u'Topologiefehler')
                    
                    # Operatsinfo in die Datei schreiben.
                    self.writeXLSTitle(ws,  fosnr,  lotnr,  date)
                                
                    # Die Statistik hineinschreiben.
                    ws.write(4, 0, "Referenzperimeter", style2)
                    ws.write(4, 1, u'Fläche [m2]', style2)
                    ws.write(4, 2, "Testperimeter", style2)
                    ws.write(4, 3, u'Fläche [m2]', style2)
                    ws.write(4, 4, "Differenz [m2]", style2)    
                    
                    ws.write(5, 0, "Gemeindegrenze")
                    ws.write(5, 1, float(areaReference))   
       
                    ws.write(5, 2, "Bodenbedeckung")
                    ws.write(5, 3, float(areaBB))       
                    ws.write(5, 4, float(float(areaReference)  - float(areaBB)))      
                
                    ws.write(6, 2, "Flurnamen")
                    ws.write(6, 3, float(areaNO))       
                    ws.write(6, 4, float(float(areaReference)  - float(areaNO)))       
                    
                    ws.write(7, 2, "Liegenschaften")
                    ws.write(7, 3, float(areaLS))       
                    ws.write(7, 4, float(float(areaReference)  - float(areaLS)))      

                    ws.write(8, 2, "Plangeometrie")
                    ws.write(8, 3, float(areaPL))       
                    ws.write(8, 4, float(float(areaReference)  - float(areaPL)))    
                    
                    ws.write(9, 2, "Toleranzstufen")
                    ws.write(9, 3, float(areaTS))       
                    ws.write(9, 4, float(float(areaReference)  - float(areaTS)))                    
                                    
                    # Excel-Datei speichern.
                    file = tempdir+os.sep+"topologiefehler-statistik_"+fosnr+"_"+lotnr+"_"+date+".xls"
                    try:
                        wb.save(file)
                        QApplication.restoreOverrideCursor()
                        QMessageBox.information( None, "Export Topologiefehler Statistik", "Datei gespeichert:\n"+ file)
                    except IOError:
                        QApplication.restoreOverrideCursor()
                        QMessageBox.warning( None, "Export Topologiefehler Statistik", "Datei <b>nicht</b> gespeichert!<br>"+ file)                    
                        return                                    

                except KeyError:
                    QMessageBox.warning( None, "", "db query error")
                    print "db query error."                            

        except:        
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
