 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import os
import json
import time
import sys

from veriso.modules.veriso_ee.tools.utils import Utils

class ApplicationModule(QObject):
    def __init__(self, iface, toolBar):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.toolBar = toolBar
        
        self.settings = QSettings("CatAIS","VeriSO")
        self.epsg = self.settings.value("project/epsg")

    def initGui(self):
        self.cleanGui()
        self.doInitChecksMenu()        
#        self.doInitDefectsMenu()        
#        self.doInitTopicsTablesMenu()
#        self.doInitBaselayerMenu()
        
    def doInitChecksMenu(self):
        menuBar = QMenuBar(self.toolBar)
        menuBar.setObjectName("VeriSOModule.LoadChecksMenuBar")        
        menuBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        menu = QMenu(menuBar)
        menu.setTitle(self.tr("Checks"))  
        
        topics = Utils().getCheckTopics()
        print topics
        
#        topics = utils.getCheckTopics(self.iface)
#        if topics:
#            for topic in topics:
#                checkfile = topics[topic]['file']
#                singleCheckMenu = menu.addMenu(unicode(topic))                        
#                checks = utils.getChecks(self.iface, checkfile)
#                
#                for check in checks:
#                    checkName = unicode(check["name"])
#                    if checkName == "separator":
#                        singleCheckMenu.addSeparator()
#                    else:
#                        action = QAction(checkName, self.iface.mainWindow())
#                        
#                        try:
#                            shortcut = check["shortcut"]
#                            action.setShortcut(shortcut)
#                        except:
#                            pass
#                            
#                        singleCheckMenu.addAction(action)                                         
#                        QObject.connect(action, SIGNAL( "triggered()"), lambda complexCheck=check: self.doShowComplexCheck(complexCheck))
#
        menuBar.addMenu(menu)
        self.toolBar.insertWidget(self.beforeAction, menuBar)

#    def doShowComplexCheck(self, check):
#        try:
#            module = str(check["file"])
#            print module
#            _temp = __import__(module, globals(), locals(), ['ComplexCheck'])
#            c = _temp.ComplexCheck(self.iface)
#            c.run()
#        except Exception, e:
#            print "Couldn't do it: %s" % e
#            self.iface.messageBar().pushMessage("Error",  QCoreApplication.translate("QcadastreModule", str(e)), level=QgsMessageBar.CRITICAL)                                
#
#    def doInitBaselayerMenu(self):
#        menuBar = QMenuBar(self.toolBar)
#        menuBar.setObjectName("QcadastreModule.LoadBaselayerMenuBar")        
#        menuBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
#        menu = QMenu(menuBar)
#        menu.setTitle(QCoreApplication.translate( "QcadastreModule","Baselayer"))  
#        
#        baselayers = utils.getBaselayers(self.iface)
#        
#        for baselayer in baselayers["baselayer"]:
#            action = QAction(QCoreApplication.translate("QcadastreModule", baselayer["title"] ), self.iface.mainWindow())
#            menu.addAction(action)     
#            QObject.connect(action, SIGNAL("triggered()" ), lambda layer=baselayer: self.doShowBaselayer(layer))    
#
#        menuBar.addMenu(menu)
#        self.toolBar.insertWidget(self.beforeAction, menuBar)        
#        
#    def doShowBaselayer(self, layer):
#        QApplication.setOverrideCursor(Qt.WaitCursor)
#        try:
#            utils.loadLayer(self.iface, layer) 
#            self.updateCrsScale()        
#        except Exception, e:
#            QApplication.restoreOverrideCursor()            
#            print "Couldn't do it: %s" % e            
#            self.iface.messageBar().pushMessage("Error",  QCoreApplication.translate("QcadastreModule", str(e)), level=QgsMessageBar.CRITICAL, duration=5)                    
#        QApplication.restoreOverrideCursor()        
#
#    def doInitTopicsTablesMenu(self):
#        menuBar = QMenuBar(self.toolBar)
#        menuBar.setObjectName("QcadastreModule.LoadTopicsTablesMenuBar")        
#        menuBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
#        menu = QMenu(menuBar)
#        menu.setTitle(QCoreApplication.translate( "QcadastreModule","Tables"))  
#        
#        topics = utils.getTopicsTables(self.iface)
#                
#        if topics:
#            for topic in topics:
#                topicMenu = menu.addMenu(unicode(topic))        
#
#                action = QAction(QCoreApplication.translate("QcadastreModule", "Load topic" ), self.iface.mainWindow())
#                topicMenu.addAction(action)    
#                topicMenu.addSeparator()      
#                QObject.connect(action, SIGNAL( "triggered()" ), lambda topic=topic: self.doShowTopic(topics[topic]))                   
#
#                for table in topics[topic]["tables"]:
#                    action = QAction(QCoreApplication.translate("QcadastreModule", table["title"] ), self.iface.mainWindow())
#                    topicMenu.addAction(action)     
#                    QObject.connect(action, SIGNAL("triggered()" ), lambda layer=table: self.doShowSingleTopicLayer(layer))    
#
#        menuBar.addMenu(menu)
#        self.toolBar.insertWidget(self.beforeAction, menuBar)
#        
#    def doShowSingleTopicLayer(self, layer):
#        layer["type"] = str(self.provider)
#        utils.loadLayer(self.iface, layer) 
#        self.updateCrsScale()
#        
#    def doShowTopic(self, topic):
#        tables = topic["tables"]
#    
#        for table in tables[::-1]:
#            self.doShowSingleTopicLayer(table)
#        
#    def doInitDefectsMenu(self):
#        menuBar = QMenuBar(self.toolBar)
#        menuBar.setObjectName("QcadastreModule.LoadDefectsMenuBar")        
#        menuBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
#        menu = QMenu(menuBar)
#        menu.setTitle(QCoreApplication.translate( "QcadastreModule","Defects"))  
#
#        action = QAction(QCoreApplication.translate("QcadastreModule", "Load defects layer"), self.iface.mainWindow())
#        QObject.connect(action, SIGNAL( "triggered()"), lambda foo="bar": self.doLoadDefects(foo))
#        menu.addAction(action)     
#        
#        action = QAction(QCoreApplication.translate("QcadastreModule", "Export defects layer"), self.iface.mainWindow())
#        QObject.connect(action, SIGNAL( "triggered()"), lambda foo="bar": self.doExportDefects(foo))
#        menu.addAction(action)     
#
#        menuBar.addMenu(menu)
#        self.toolBar.insertWidget(self.beforeAction, menuBar)
#
#    def doLoadDefects(self, bar):
#        from tools.doLoadDefects import LoadDefects
#        d = LoadDefects(self.iface)
#        d.run()
#
#    def doExportDefects(self, foo):
#        from tools.doExportDefects import ExportDefects        
#        d = ExportDefects(self.iface)
#        d.run()
#
#    def updateCrsScale(self):
#        """
#            Update the scale map units and the crs manually since there is a bug with geometryless tables.
#        """
#        try:
#            self.canvas.setMapUnits(0)		
#            srs = QgsCoordinateReferenceSystem()
#            srs.createFromSrid(int(self.epsg))
#            renderer = self.canvas.mapRenderer()
#            renderer.setDestinationCrs(srs)
#        except Exception, e:
#            print "Couldn't do it: %s" % e            
#            self.iface.messageBar().pushMessage("Error",  QCoreApplication.translate("QcadastreModule", str(e)), level=QgsMessageBar.CRITICAL, duration=5)                    

    def cleanGui(self):
        # Remove all the applications module specific menus.
        actions = self.toolBar.actions()
        for action in actions:
            try:
                objectName = action.defaultWidget().objectName()
                # Eelete existing module menus.
                if objectName[0:12] == "VeriSOModule":
                    self.toolBar.removeAction(action)
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

    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('VeriSOModule', message)


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

        
        


