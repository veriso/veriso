 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from qgis.gui import *
import os
import json
import time
import sys
import traceback
import collections

from veriso.modules.veriso_ee.tools.utils import Utils
from veriso.base.utils.doLoadLayer import LoadLayer

# Die Übersetzung hat grosse Probleme gemacht. So 
# funktionierts. Die einfache "self.tr(...)"-Geschichte
# wollte wirklich nicht funktionieren...
try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class ApplicationModule(QObject):
    def __init__(self, iface, toolbar, locale_path):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.toolbar = toolbar
        
        self.settings = QSettings("CatAIS","VeriSO")
        self.epsg = self.settings.value("project/epsg")
        self.provider = self.settings.value("project/provider")
        
    def initGui(self):
        self.cleanGui()
        self.doInitChecksMenu()        
        self.doInitDefectsMenu()        
        self.do_init_topics_tables_menu()
        self.doInitBaselayerMenu()
        
    def doInitChecksMenu(self):
        menuBar = QMenuBar(self.toolbar)
        menuBar.setObjectName("VeriSOModule.LoadChecksMenuBar")        
        menuBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        menu = QMenu(menuBar)
        menu.setTitle(_translate("VeriSO_EE", "Checks",  None))
        
        locale = QSettings().value('locale/userLocale')[0:2]
        
        topics = Utils().getCheckTopics()
        if topics:
            for topic in topics:
                checkfile = topics[topic]['file']
                singleCheckMenu = menu.addMenu(unicode(topic))                        
                checks = Utils().getChecks(checkfile)
                
                for check in checks:
                    checkName = check["name"]
                    
                    # Prüfen ob multilingual.
                    # Logik ähnlich wie in Utils().getCheckTopics() Methode.
                    try: 
                        keys = checkName.keys()
                        try:
                            checkName = unicode(checkName[locale])
                            # Sprache gefunden.
                        except:
                            # Sprache nicht gefunden.
                            checkName = unicode(checkName.values()[0])
                    except:
                        checkName = unicode(checkName)
                    
                    if checkName == "separator":
                        singleCheckMenu.addSeparator()
                    else:
                        action = QAction(checkName, self.iface.mainWindow())
                        
                        try:
                            shortcut = check["shortcut"]
                            action.setShortcut(shortcut)
                        except:
                            pass
                         
                        singleCheckMenu.addAction(action)                                         
                        QObject.connect(action, SIGNAL( "triggered()"), lambda complexCheck=check: self.doShowComplexCheck(complexCheck))

        menuBar.addMenu(menu)
        self.toolbar.insertWidget(self.beforeAction, menuBar)

    def doShowComplexCheck(self, check):
        try:
            module = str(check["file"])
            _temp = __import__(module, globals(), locals(), ['ComplexCheck'])
            c = _temp.ComplexCheck(self.iface)
            c.run()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO", str(traceback.format_exc(exc_traceback)))               
            return

    def doInitBaselayerMenu(self):
        menuBar = QMenuBar(self.toolbar)
        menuBar.setObjectName("VeriSOModule.LoadBaselayerMenuBar")        
        menuBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        menu = QMenu(menuBar)
        menu.setTitle(_translate("VeriSO_EE", "Baselayer",  None))  
        
        locale = QSettings().value('locale/userLocale')[0:2]        
        
        baselayers = Utils().getBaselayers()
        
        for baselayer in baselayers["baselayer"]:
            baselayerTitle = baselayer["title"]
            try: 
                keys = baselayerTitle.keys()
                try:
                    baselayerTitle = unicode(baselayerTitle[locale])
                    # Sprache gefunden.
                except:
                    # Sprache nicht gefunden.
                    baselayerTitle = unicode(baselayerTitle.values()[0])
            except:
                baselayerTitle = unicode(baselayerTitle)
                
            baselayer["title"] = baselayerTitle
            
            action = QAction(baselayerTitle, self.iface.mainWindow())
            menu.addAction(action)     
            QObject.connect(action, SIGNAL("triggered()" ), lambda layer=baselayer: self.doShowBaselayer(layer))    

        menuBar.addMenu(menu)
        self.toolbar.insertWidget(self.beforeAction, menuBar)        
        
    def doShowBaselayer(self, layer):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            layerLoader = LoadLayer(self.iface)
            layerLoader.load(layer)
        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error",  str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=10)                                
            return
        QApplication.restoreOverrideCursor()        

    def do_init_topics_tables_menu(self):
        menubar = QMenuBar(self.toolbar)
        menubar.setObjectName("VeriSOModule.LoadTopicsTablesMenuBar")        
        menubar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        menu = QMenu(menubar)
        menu.setTitle(_translate("VeriSO_EE", "Tables", None))  
        
        locale = QSettings().value('locale/userLocale')[0:2]        
        
        topics = self.get_topics_tables()
        print topics
        if not topics:
            message = "Something went wrong catching the topics tables list from the database."
            QMessageBox.critical(None, "VeriSO", self.tr(message))
            return

        for topic in topics:
            print "********"
            print topic
            topic_menu = menu.addMenu(unicode(topic["topic"]))      
            
            i = 0
            for table in topic["tables"]:
                
                print table
                print topic["geometry_columns"][i]
                print topic["class_names"][i]
                i += 1
                
                # At the moment there is no locale support here.
                # Seems to be not very handy without mapping tables anyway...
                
                title = topic["class_names"][i]
                
        
#        topics = Utils().getTopicsTables()
#                
#        if topics:
#            for topic in topics:
#                topicMenu = menu.addMenu(unicode(topic))        
#                
#                # Wenn wir das hier machen, müssen wir es
#                # nur einmal machen.
#                for table in topics[topic]["tables"]:
#                    tableTitle = table["title"]
#                    try:
#                        keys = tableTitle.keys()
#                        try:
#                            tableTitle = unicode(tableTitle[locale])
#                        except:
#                            # Sprache nicht gefunden.
#                            tableTitle = unicode(tableTitle.values()[0])
#                    except:
#                        tableTitle = unicode(tableTitle)
#                        
#                    table["title"] = tableTitle
#
#                action = QAction(_translate("VeriSO_EE", "Load Topic",  None), self.iface.mainWindow())
#                topicMenu.addAction(action)    
#                topicMenu.addSeparator()      
#                QObject.connect(action, SIGNAL( "triggered()" ), lambda topic=topic: self.doShowTopic(topics[topic]))                   
#
#                for table in topics[topic]["tables"]:
#                    action = QAction(table["title"], self.iface.mainWindow())
#                    topicMenu.addAction(action)     
#                    QObject.connect(action, SIGNAL("triggered()" ), lambda layer=table: self.doShowSingleTopicLayer(layer))    

        menubar.addMenu(menu)
        self.toolbar.insertWidget(self.beforeAction, menubar)
        
    def get_topics_tables(self):
        """Requests the topics and tables from the topic_tables database table.
        This table was created in the postprocessing step.
        
        Returns:
          False: If something went wrong when trying to get the list from the database. Otherwise a python dictionary.
        """
        try:            
            db_host = self.settings.value("project/dbhost")
            db_name = self.settings.value("project/dbname")
            db_port = self.settings.value("project/dbport")
            db_schema = self.settings.value("project/dbschema")
            db_admin = self.settings.value("project/dbadmin")
            db_admin_pwd = self.settings.value("project/dbadminpwd")

            db = QSqlDatabase.addDatabase("QPSQL")
            db.setHostName(db_host)
            db.setPort(int(db_port))
            db.setDatabaseName(db_name)
            db.setUserName(db_admin)
            db.setPassword(db_admin_pwd)
    
            if not db.open():
                message = "Could not open database: "
                QgsMessageLog.logMessage(self.tr(message) + db.lastError().driverText(), "VeriSO", QgsMessageLog.CRITICAL)                                
                return
                
            # I think libpg cannot deal with arrays from postgresql. So we return a comma sperated string.
            # Everything is ordered alphanumerical. Not sure if we would know enough to sort by interlis model ordering?!
            sql = "SELECT topic, array_to_string(array_agg(sql_name ORDER BY sql_name),',') as tables, "
            sql += "array_to_string(array_agg(coalesce(f_geometry_column,'') ORDER BY sql_name),',') as geometry_columns ,"
            sql += "array_to_string(array_agg(class_name ORDER BY sql_name),',') as class_names "
            sql += "FROM " + db_schema + ".t_topic_tables GROUP BY topic ORDER BY topic;"

            query = db.exec_(sql)
            
            if not query.isActive():
                message = "Error while reading from database."
                QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)            
                QgsMessageLog.logMessage(str(QSqlQuery.lastError(query).text()), "VeriSO", QgsMessageLog.CRITICAL)      
                return 
            
            topics = []  
            record = query.record()
            while query.next():
                topic = {}
                topic["topic"] = str(query.value(record.indexOf("topic")))
                
                tables = []
                for table in str(query.value(record.indexOf("tables"))).split(","):
                    tables.append(table)
                topic["tables"] = tables
                
                geometry_columns = []
                for geometry_column in str(query.value(record.indexOf("geometry_columns"))).split(","):
                    geometry_columns.append(geometry_column)
                topic["geometry_columns"] = geometry_columns
                    
                class_names = []
                for class_name in str(query.value(record.indexOf("class_names"))).split(","):
                    class_names.append(class_name)
                topic["class_names"] = class_names
                
                topics.append(topic)
                
            db.close()
            del db
            
            return topics
            
        except Exception, e:
            message = "Something went wrong catching the topics tables list from the database."
            QgsMessageLog.logMessage(self.tr(message), "VeriSO", QgsMessageLog.CRITICAL)                        
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)     
            return 

        
        
        
    def doShowSingleTopicLayer(self, layer):
        layer["type"] = str(self.provider)
        layerLoader = LoadLayer(self.iface)
        layerLoader.load(layer)

    def doShowTopic(self, topic):
        tables = topic["tables"]
        for table in tables[::-1]:
            self.doShowSingleTopicLayer(table)
        
    def doInitDefectsMenu(self):
        menuBar = QMenuBar(self.toolbar)
        menuBar.setObjectName("VeriSOModule.LoadDefectsMenuBar")        
        menuBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        menu = QMenu(menuBar)
        menu.setTitle(_translate("VeriSO_EE", "Defects",  None))  

        action = QAction(_translate("VeriSO_EE", "Load defects layer",  None), self.iface.mainWindow())
        QObject.connect(action, SIGNAL( "triggered()"), lambda foo="bar": self.doLoadDefects(foo))
        menu.addAction(action)     
        
        action = QAction(QCoreApplication.translate("VeriSO_EE", "Export defects layer"), self.iface.mainWindow())
        QObject.connect(action, SIGNAL( "triggered()"), lambda foo="bar": self.doExportDefects(foo))
        menu.addAction(action)     

        menuBar.addMenu(menu)
        self.toolbar.insertWidget(self.beforeAction, menuBar)

    def doLoadDefects(self, bar):
        from tools.doLoadDefects import LoadDefects
        d = LoadDefects(self.iface)
        d.run()

    def doExportDefects(self, foo):
        from tools.doExportDefects import ExportDefects        
        d = ExportDefects(self.iface)
        d.run()


    def cleanGui(self):
        # Remove all the applications module specific menus.
        actions = self.toolbar.actions()
        for action in actions:
            try:
                objectName = action.defaultWidget().objectName()
                # Delete existing module menus.
                if objectName[0:12] == "VeriSOModule":
                    self.toolbar.removeAction(action)
                # Remember the action where we want to insert our new menu 
                # (e.g. settings menu bar).
                if objectName == "VeriSO.Main.SettingsMenuBar":
                    self.beforeAction = action
                # Get settings menu bar for module specific settings.
                if objectName == "VeriSO.Main.SettingsMenuBar":
                    self.settingsAction = action
            except AttributeError:
                pass
                
        # Remove all the application module specific options/settings in the settings menu.
        settingsMenuBar = self.settingsAction.defaultWidget()
        settingsMenu = self.settingsAction.defaultWidget().actions()[0].parentWidget()
        
        actions = settingsMenu.actions()
        for action in actions:
            objectName = action.objectName()
            if objectName[0:12] == "VeriSOModule":
               settingsMenu.removeAction(action) 
            
            if action.isSeparator():
                settingsMenu.removeAction(action)

#    def doSetDatabase(self, foo):
#        print "baaaar"
#        from settings.doSetDatabase import SetDatabaseDialog
#        d = SetDatabaseDialog(self.iface.mainWindow())        
#        d.initGui()
#        d.show()

            
        # and now add our module specific menus
#        self.doInitChecksLoader()
#        self.doInitDefectsLoader()
#        self.doInitTopicsTableLoader()
#        self.doInitBaseLayerLoader()


#    def doInitDefectsLoader(self):
#        menuBar = QMenuBar(self.toolBar)
#        menuBar.setObjectName("QGeoAppModule.QVeriso.LoadDefectsMenuBar")        
#        menuBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
#        menu = QMenu(menuBar)
#        menu.setTitle(QCoreApplication.translate( "QGeoAppModule.QVeriso","Defects"))  
#
#        action = QAction(QCoreApplication.translate("QGeoAppModule.QVeriso", "Load defects layer"), self.iface.mainWindow())
#        QObject.connect(action, SIGNAL( "triggered()"), lambda foo="bar": self.doLoadDefects(foo))
#        menu.addAction(action)     
#        
#        action = QAction(QCoreApplication.translate("QGeoAppModule.QVeriso", "Export defects layer"), self.iface.mainWindow())
#        QObject.connect(action, SIGNAL( "triggered()"), lambda foo="bar": self.doExportDefects(foo))
#        menu.addAction(action)     
#
#        menuBar.addMenu(menu)
#        self.toolBar.insertWidget(self.beforeAction, menuBar)
#
#
#    def doLoadDefects(self, foo):
#        d = LoadDefects(self.iface, self.projectId, self.subModuleName)
#        d.run()
#
#        
#    def doExportDefects(self, foo):
#        d = ExportDefects(self.iface)
#        d.run()
#
#
#    def doInitChecksLoader(self):
#        menuBar = QMenuBar(self.toolBar)
#        menuBar.setObjectName("QGeoAppModule.QVeriso.LoadChecksMenuBar")        
#        menuBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
#        menu = QMenu(menuBar)
#        menu.setTitle(QCoreApplication.translate( "QGeoAppModule.QVeriso","Checks"))  
#        
#        # load checklist
#        action = QAction(QCoreApplication.translate("QGeoAppModule.QVeriso", "Load checklist"), self.iface.mainWindow())
#        QObject.connect(action, SIGNAL( "triggered()"), lambda foo="bar": self.doLoadChecklist(foo))
#        menu.addAction(action)     
#
#        menu.addSeparator()
#        
#        # load checks
#        checkTopics = self.vutils.getCheckTopicsName(self.subModuleName)
#
#        try:
#            for checkTopic in checkTopics:
#                singleCheckMenu = menu.addMenu(unicode(checkTopic))   
#                checks = self.vutils.getChecks(self.subModuleName, checkTopic)
#                for check in checks:
#                    action = QAction(check["title"], self.iface.mainWindow())
#                    try:
#                        shortcut = check["shortcut"]
#                        action.setShortcut(shortcut)
#                    except:
#                        pass
#                    singleCheckMenu.addAction(action)                            
#                    if check["type"] == "simple":
#                        QObject.connect(action, SIGNAL( "triggered()"), lambda simpleCheck=check: self.doShowSimpleCheck(simpleCheck))
#                    elif check["type"] == "complex":
#                        QObject.connect(action, SIGNAL( "triggered()"), lambda complexCheck=check: self.doShowComplexCheck(complexCheck))
#        except:
#            print "No checks defined."
#            #messagebox
#            
#        menuBar.addMenu(menu)
#        self.toolBar.insertWidget(self.beforeAction, menuBar)
#        
#    
#    def doShowSimpleCheck(self, check):
#        print "simpleCheck"
#        
#        
#    def doShowComplexCheck(self, check):
#        try:
#            module = str(check["file"])
#            print module
#            _temp = __import__("submodules." + self.subModuleName+ "." + module, globals(), locals(), ['ComplexCheck'])
#            c = _temp.ComplexCheck(self.iface, self.projectId, self.subModuleName)
#            c.run()
#        except:
#            print "error loading complex check"
#           #messagebox
#                
#    
#    def doLoadChecklist(self, foo):
#        d = ShowChecklist(self.iface, self.projectId, self.projectsRootPath, self.subModuleName)
#        d.run()        
#
#
#    def doInitBaseLayerLoader(self):
#        menuBar = QMenuBar(self.toolBar)
#        menuBar.setObjectName("QGeoAppModule.QVeriso.LoadBaseLayersMenuBar")        
#        menuBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
#        menu = QMenu(menuBar)
#        menu.setTitle(QCoreApplication.translate( "QGeoAppModule.QVeriso","Baselayer"))        
#
#        #add the baselayers
#        baselayers = self.vutils.getBaselayers(self.subModuleName)
#        try:
#            for baselayer in baselayers:
#                action = QAction(unicode(baselayer["title"]), self.iface.mainWindow())
#                menu.addAction(action)
#                QObject.connect(action, SIGNAL( "triggered()" ), lambda layer=baselayer: self.doShowBaseLayer(layer))
#        except:
#            print "no baselayers found"
#            #messagebox
#
#        menuBar.addMenu(menu)
#        self.toolBar.insertWidget(self.beforeAction, menuBar)
#
#
#    def doShowBaseLayer(self, layer):
#        print "showbaselayer"
#        QApplication.setOverrideCursor(Qt.WaitCursor)
#        try:           
#            layer["group"] = "Baselayers"
#            self.qutils.loadLayer(self.iface, layer, None, "/python/plugins/qgeoapp/modules/qveriso/submodules/" + self.subModuleName + "/qml/")       
#        except:        
#            print "error adding baselayer"         
#            QApplication.restoreOverrideCursor()
#        QApplication.restoreOverrideCursor()
#
#
#    def doInitTopicsTableLoader(self):
#        menuBar = QMenuBar(self.toolBar)
#        menuBar.setObjectName("QGeoAppModule.QVeriso.LoadTopicsTablesMenuBar")        
#        menuBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
#        menu = QMenu(menuBar)
#        menu.setTitle(QCoreApplication.translate( "QGeoAppModule.QVeriso","Data"))        
#
#        # add the topic menus
#        topics = self.vutils.getTopics(self.subModuleName)
#        try:
#            for topic in topics:
#                singleTopicMenu = menu.addMenu(unicode(topic['title']))   
#                action = QAction( QCoreApplication.translate("QGeoAppModule.QVeriso", "Load topic"), self.iface.mainWindow() )
#                singleTopicMenu.addAction(action)    
#                singleTopicMenu.addSeparator()      
#                QObject.connect(action, SIGNAL("triggered()"), lambda topic=topic: self.doShowTopic(topic))                   
#                for table in topic["tables"]:
#                    action = QAction(unicode(table["title"]), self.iface.mainWindow())
#                    singleTopicMenu.addAction(action)     
#                    QObject.connect( action, SIGNAL( "triggered()" ), lambda layer=table: self.doShowSingleTopicLayer(layer) )    
#        except:
#            print "No topics found."
#            #messagebox
#
#        menuBar.addMenu(menu)
#        self.toolBar.insertWidget(self.beforeAction, menuBar)
#
#
#    def doShowTopic(self, topic):
#        tables = topic["tables"]
#        n = len(tables)
#        for i in reversed(xrange(0, n)):
#            QApplication.setOverrideCursor(Qt.WaitCursor)                    
#            try:
#                tables[i]["group"] =  tables[i]["group"] + " (" + str(self.dbschema) + ")"
#                self.qutils.loadLayer(self.iface, tables[i], None, "/python/plugins/qgeoapp/modules/qveriso/submodules/" + self.subModuleName + "/qml/")   
#            except:
#                QApplication.setOverrideCursor(Qt.WaitCursor)        
#            QApplication.restoreOverrideCursor()
#
#        
#    def doShowSingleTopicLayer(self, layer):
#        QApplication.setOverrideCursor(Qt.WaitCursor)          
#        try:
#            layer["group"] =  layer["group"] + " (" + str(self.dbschema) + ")"
#            self.qutils.loadLayer(self.iface, layer, None, "/python/plugins/qgeoapp/modules/qveriso/submodules/" + self.subModuleName + "/qml/")       
#        except:        
#            QApplication.restoreOverrideCursor()
#        QApplication.restoreOverrideCursor()


    def run(self):
        print "fubar"

        
        


