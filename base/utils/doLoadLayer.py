 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import sys
import traceback

class LoadLayer(QObject):
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.root = QgsProject.instance().layerTreeRoot()

    def load(self, layer, visible= True, collapsed_legend = False, collapsed_group = False):
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
        epsg = settings.value("project/epsg")
        
        if not dbhost or not dbport or not dbname or not dbschema or not dbuser or not dbpwd or not dbadmin or not dbadminpwd:
            self.iface.messageBar().pushMessage("Error",  self.tr("Missing database parameter. Cannot load layer."), level=QgsMessageBar.CRITICAL, duration=5)                    
            return
            
        if not module_name or not provider:
            self.iface.messageBar().pushMessage("Error",  self.tr("Missing parameter. Cannot load layer."), level=QgsMessageBar.CRITICAL, duration=5)                    
            return        
        
        try:
            # Postgres
            if layer["type"] == "postgres":
                feature_type = str(layer["featuretype"])
                title = layer["title"]
                key = str(layer["key"])            
            
                try:
                    readonly = (layer["readonly"])
                except:
                    readonly = True
                    
                try:
                    geom = str(layer["geom"])
                except:
                    geom = None
                    
                try:
                    style = str(layer["style"])
                except:
                    style = ""
                    
                try:
                    group = unicode(layer["group"])
                except:
                    group = None
                    
                try:
                    sql = str(layer["sql"])
                except:
                    sql = ""
                    
                # Overwrite the active project settings/parameters to add *any* postgres layers.
                try:
                    params = layer["params"]
                    module_name = params["appmodule"]
                    provider = params["provider"]
                    dbhost = params["dbhost"]
                    dbport = params["dbport"]
                    dbname = params["dbname"]
                    dbschema = params["dbschema"]
                    dbuser = params["dbuser"]
                    dbpwd = params["dbpwd"]
                    dbadmin = params["dbadmin"]
                    dbadminpwd = params["dbadminpwd"]
                except:
                    pass                    

                uri = QgsDataSourceURI()
                if readonly:
                    uri.setConnection(dbhost, dbport, dbname, dbuser, dbpwd)
                else:
                    uri.setConnection(dbhost, dbport, dbname, dbadmin, dbadminpwd)
                uri.setDataSource(dbschema, feature_type, geom, sql, key)

                my_layer = QgsVectorLayer(uri.uri(), title, provider)

            #WMS
            elif layer["type"] == "wms":
                url = layer["url"]
                title = layer["title"]
                layers = layer["layers"]
                format = layer["format"]
                
                try:
                    crs = layer["crs"]
                except:
                    crs = "EPSG:" + str(epsg)
                
                try:
                    styles = layer["styles"]
                except:
                    styles = ""

                try:
                    group = layer["group"]
                except:
                    group = None
                    
                try:
                    style = layer["style"]
                except:
                    style = ""
            
                uri = "IgnoreGetMapUrl=1&crs="+crs+"&layers="+layers+"&styles="+styles+"&format="+format+"&url="+url
                my_layer = QgsRasterLayer (uri, title, "wms", False)      

            else:
                self.iface.messageBar().pushMessage("Error",  self.tr("Data provider not yet supported: ") + str(layer["type"]), level=QgsMessageBar.CRITICAL, duration=5)                                                            
                return

            if style <> "":
                qml_path = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/"+module_name+"/qml/"+style))
                qml = QDir.convertSeparators(QDir.cleanPath(qml_path))
                my_layer.loadNamedStyle(qml)
                
            if not my_layer.isValid():                
                self.iface.messageBar().pushMessage("Error",  self.tr("Layer is not valid"), level=QgsMessageBar.CRITICAL, duration=5)                                                            
                return       
            else:
                QgsMapLayerRegistry.instance().addMapLayer(my_layer)                
                if group: # Layer soll in eine bestimmte Gruppe hinzugefügt werden.
                    my_group_node = self.root.findGroup(group)
                    if not my_group_node: # Gruppe noch nicht vorhanden.
                        my_group_node = self.root.addGroup(group)
                    # Achtung: Das ist eher ein Workaround. Meines Erachtens hats noch einen Bug. 
                    # Mit QgsMapLayerRegistry.instance().addMapLayer(my_layer, False)  wird
                    # ein Layer nocht nicht in die Legende gehängt. Anschliessend kann man ihn
                    # mit my_layer_node = self.root.addLayer(my_layer) der Legende hinzufügen.
                    # Das führt aber dazu, dass was mit dem MapCanvas nicht mehr stimmt, dh.
                    # .setExtent() funktioniert nicht mehr richtig. Wir der Layer jedoch direkt
                    # in die Legende gehängt, funktioniert .setExtent() tadellos. Jetzt wird halt
                    # momentan der Layer direkt eingehängt und anschliessen die die gewünschte
                    # Gruppe verschoben. 
                    # Kleiner (positiver) Nebeneffekt: Der Layer ist defaultmässig ausgeschaltet.
                    #
                    # NEIN: Anscheinend ist es ein Problem wenn man dann layer_node.setVisible(Qt.Checked)
                    # macht. Dann funktionierts nicht mehr. -> Wieder zurückändern auf einfachere Methode.
                    my_layer_node = self.root.findLayer(my_layer.id())
                    cloned_layer = my_layer_node.clone()
                    my_group_node.insertChildNode(0, cloned_layer)
                    self.root.removeChildNode(my_layer_node)
                    my_layer_node = self.root.findLayer(my_layer.id()) # Layer bekommt neuen layer_node.
                    
                else:  # layer_node suchen für nicht verschobenen Layer.
                    my_layer_node = self.root.findLayer(my_layer.id())
                    
                if visible:
                    my_layer_node.setVisible(Qt.Checked)
                    
                if collapsed_legend:
                    my_layer_node.setExpanded(False)       
                   
            return my_layer

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error",  str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                                
            return


        
    def tr(self, message):
        return QCoreApplication.translate('VeriSO', message)
        
