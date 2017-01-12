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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_arealstatistik", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_arealstatistik", "Arealstatistik", None)
            group += " (" + str(project_id) + ")"

            settings = QSettings("CatAIS","VeriSO")
            module_name = settings.value("project/appmodule")
            provider = settings.value("project/provider")
            db_host = settings.value("project/dbhost")
            db_port = settings.value("project/dbport")
            db_name = settings.value("project/dbname")
            db_schema = settings.value("project/dbschema")
            db_user = settings.value("project/dbuser")
            db_pwd = settings.value("project/dbpwd")


            db = QSqlDatabase.addDatabase("QPSQL", "db")
            db.setHostName(db_host)
            db.setPort(int(db_port))
            db.setDatabaseName(db_name)
            db.setUserName(db_user)
            db.setPassword(db_pwd)
            
            self.dbobj = DbObj("default", "postgres",  db_host, db_port, db, db_user, db_pwd)
            connected = self.dbobj.connect()
            
            if connected == True:
                try:            
                 
                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=0),0) as Flaeche")    
                    areaGeb = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=0),0) as Flaeche")    
                    areaGebZ = result['FLAECHE'][0]
               
                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=1),0) as Flaeche")                   
                    areaStr = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=2),0) as Flaeche")                    
                    areaTro = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=3),0) as Flaeche")                   
                    areaVer = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=4),0) as Flaeche")                   
                    areaBah = result['FLAECHE'][0]


                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=5),0) as Flaeche")                
                    areaFlu = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=6),0) as Flaeche")                
                    areaWas = result['FLAECHE'][0]
                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=7),0) as Flaeche")                
                    areaUeb = result['FLAECHE'][0]
                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=8),0) as Flaeche")                
                    areaAck = result['FLAECHE'][0]
                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=9),0) as Flaeche")                
                    areaReb = result['FLAECHE'][0]
                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=10),0) as Flaeche")                
                    areaInt = result['FLAECHE'][0]
                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=11),0) as Flaeche")                
                    areaGar = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=12),0) as Flaeche")                
                    areaHoc = result['FLAECHE'][0]
                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=13),0) as Flaeche")                
                    areaHum = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=14),0) as Flaeche")                
                    areaSte = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=15),0) as Flaeche")                
                    areaFli = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=16),0) as Flaeche")                
                    areaSch = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=17),0) as Flaeche")                
                    areaWal = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=18),0) as Flaeche")                
                    areaWyd = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=19),0) as Flaeche")                
                    areaWyo = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=20),0) as Flaeche")                
                    areaBes = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=21),0) as Flaeche")                
                    areaFel = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=22),0) as Flaeche")                
                    areaFir = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=23),0) as Flaeche")                
                    areaSan = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=24),0) as Flaeche")                
                    areaAbb = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select round(sum(st_area(geometrie))) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=25),0) as Flaeche")                
                    areaVeg = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=1),0) as Flaeche")                   
                    areaStrZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=2),0) as Flaeche")                    
                    areaTroZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=3),0) as Flaeche")                   
                    areaVerZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=4),0) as Flaeche")                   
                    areaBahZ = result['FLAECHE'][0]


                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=5),0) as Flaeche")                
                    areaFluZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=6),0) as Flaeche")                
                    areaWasZ = result['FLAECHE'][0]
                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=7),0) as Flaeche")                
                    areaUebZ = result['FLAECHE'][0]
                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=8),0) as Flaeche")                
                    areaAckZ = result['FLAECHE'][0]
                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=9),0) as Flaeche")                
                    areaRebZ = result['FLAECHE'][0]
                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=10),0) as Flaeche")                
                    areaIntZ = result['FLAECHE'][0]
                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=11),0) as Flaeche")                
                    areaGarZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=12),0) as Flaeche")                
                    areaHocZ = result['FLAECHE'][0]
                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=13),0) as Flaeche")                
                    areaHumZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=14),0) as Flaeche")                
                    areaSteZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=15),0) as Flaeche")                
                    areaFliZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=16),0) as Flaeche")                
                    areaSchZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=17),0) as Flaeche")                
                    areaWalZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=18),0) as Flaeche")                
                    areaWydZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=19),0) as Flaeche")                
                    areaWyoZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=20),0) as Flaeche")                
                    areaBesZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=21),0) as Flaeche")                
                    areaFelZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=22),0) as Flaeche")                
                    areaFirZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=23),0) as Flaeche")                
                    areaSanZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=24),0) as Flaeche")                
                    areaAbbZ = result['FLAECHE'][0]

                    result = self.dbobj.read( "select coalesce((select count(art) FROM "+db_schema+".bodenbedeckung_boflaeche group by art having  art=25),0) as Flaeche")                
                    areaVegZ = result['FLAECHE'][0]





                    # Die Excel-Datei anlegen und die Statistik hineinschreiben.
                    wb = pycel.Workbook(encoding='utf-8')
                    wb.country_code = 41

                    style1 = pycel.easyxf('font: bold on;');
                    style2 = pycel.easyxf('font: italic on;');
                    
                    ws = wb.add_sheet(u'Arealstatistik')
                    
                    # Operatsinfo in die Datei schreiben.
                    self.writeXLSTitle(ws,  fosnr,  lotnr,  date)
                                
                    # Die Statistik hineinschreiben.
                    ws.write(4, 0, "BB Art", style2)
                    ws.write(4, 1, u'Fläche [m2]', style2)
                    ws.write(4, 2, 'Anzahl', style2)

                    ws.write(5, 0, "Gebäude")
                    ws.write(5, 1, float(areaGeb))       
                    ws.write(5, 2, float(areaGebZ))       
   
                    ws.write(6, 0, "Strasse / Weg")
                    ws.write(6, 1, float(areaStr))    
                    ws.write(6, 2, float(areaStrZ)) 
   
                    ws.write(7, 0, "Trottoir")
                    ws.write(7, 1, float(areaTro))       
                    ws.write(7, 2, float(areaTroZ))   
   
                    ws.write(8, 0, "Verkehrsinsel")
                    ws.write(8, 1, float(areaVer))       
                    ws.write(8, 2, float(areaVerZ))
   
                    ws.write(9, 0, "Bahn")
                    ws.write(9, 1, float(areaBah))
                    ws.write(9, 2, float(areaBahZ))    
   
                    ws.write(10, 0, "Flugplatz") 
                    ws.write(10, 1, float(areaFlu)) 
                    ws.write(10, 2, float(areaFluZ)) 
   
                    ws.write(11, 0, "Wasserbecken") 
                    ws.write(11, 1, float(areaWas))
                    ws.write(11, 2, float(areaWasZ))

                    ws.write(12, 0, "uebrige befestigte") 
                    ws.write(12, 1, float(areaUeb))
                    ws.write(12, 2, float(areaUebZ))
                                    
                    ws.write(13, 0, "Acker Wiese Weide") 
                    ws.write(13, 1, float(areaAck))
                    ws.write(13, 2, float(areaAckZ))
                                   
                    ws.write(14, 0, "Reben") 
                    ws.write(14, 1, float(areaReb))
                    ws.write(14, 2, float(areaRebZ))

                    ws.write(15, 0, "ueb Intensivkultur") 
                    ws.write(15, 1, float(areaInt))
                    ws.write(15, 2, float(areaIntZ))
                                    
                    ws.write(16, 0, "Gartenanlage") 
                    ws.write(16, 1, float(areaGar))
                    ws.write(16, 2, float(areaGarZ))
                                    
                    ws.write(17, 0, "Hoch- Flachmoor") 
                    ws.write(17, 1, float(areaHoc))
                    ws.write(17, 2, float(areaHocZ))
                                    
                    ws.write(18, 0, "ueb humisierte") 
                    ws.write(18, 1, float(areaHum))        
                    ws.write(18, 2, float(areaHumZ))                            
                                    
                    ws.write(19, 0, "stehendes Gewaesser") 
                    ws.write(19, 1, float(areaSte))   
                    ws.write(19, 2, float(areaSteZ))                                 
                                    
                    ws.write(20, 0, "fliessendes Gewaesser") 
                    ws.write(20, 1, float(areaFli))    
                    ws.write(20, 2, float(areaFliZ))                                     
                                    
                    ws.write(21, 0, "Schilfguertel") 
                    ws.write(21, 1, float(areaSch))  
                    ws.write(21, 2, float(areaSchZ))                                 
                                    
                    ws.write(22, 0, "geschlossener Wald") 
                    ws.write(22, 1, float(areaWal))  
                    ws.write(22, 2, float(areaWalZ))                                   
                                    
                    ws.write(23, 0, "Wytweide dicht") 
                    ws.write(23, 1, float(areaWyd)) 
                    ws.write(23, 2, float(areaWydZ))                                  
                                    
                    ws.write(24, 0, "Wytweide offen") 
                    ws.write(24, 1, float(areaWyo))  
                    ws.write(24, 2, float(areaWyoZ))                                  
                                    
                    ws.write(25, 0, "ueb bestockte") 
                    ws.write(25, 1, float(areaBes)) 
                    ws.write(25, 2, float(areaBesZ))
                                    
                    ws.write(26, 0, "Fels") 
                    ws.write(26, 1, float(areaFel))   
                    ws.write(26, 2, float(areaFelZ))
                                  
                    ws.write(27, 0, "Gletscher Firn") 
                    ws.write(27, 1, float(areaFir)) 
                    ws.write(27, 2, float(areaFirZ))
                                    
                    ws.write(28, 0, "Geroell Sand") 
                    ws.write(28, 1, float(areaSan)) 
                    ws.write(28, 2, float(areaSanZ)) 
                                    
                    ws.write(29, 0, "Abbau Deponie") 
                    ws.write(29, 1, float(areaAbb))  
                    ws.write(29, 2, float(areaAbbZ))
                                   
                    ws.write(30, 0, "ueb vegetationslos") 
                    ws.write(30, 1, float(areaVeg))
                    ws.write(30, 2, float(areaVegZ))        

                    ws.write(32,  0,  "Total")
                    ws.write(32,  1,  pycel.Formula("SUM(B5:B30)"))                          
                                    
                    # Excel-Datei speichern.
                    file = tempdir+os.sep+"Arealstatistik_"+fosnr+"_"+lotnr+"_"+date+".xls"
                    try:
                        wb.save(file)
                        QApplication.restoreOverrideCursor()
                        QMessageBox.information( None, "Export Arealstatistik", "Datei gespeichert:\n"+ file)
                    except IOError:
                        QApplication.restoreOverrideCursor()
                        QMessageBox.warning( None, "Export Arealstatistik", "Datei <b>nicht</b> gespeichert!<br>"+ file)                    
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
