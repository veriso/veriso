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
from collections import OrderedDict

from veriso.base.utils.loadlayer import LoadLayer

# Translation was a pain in the a...
# Umlaute from files etc.
# This seems to work.
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
        self.module_name = self.settings.value("project/appmodule")        
        
    def initGui(self):
        """Initialize all the additional menus.
        """
        self.clean_gui()
        self.do_init_checks_menu()        
        self.do_init_defects_menu()        
        self.do_init_topics_tables_menu()
        self.do_init_baselayer_menu()
        
    def do_init_checks_menu(self):
        """Initialize checks menu.
        """        
        menubar = QMenuBar(self.toolbar)
        menubar.setObjectName("VeriSOModule.LoadChecksMenuBar")        
        menubar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        menu = QMenu(menubar)
        menu.setTitle(_translate("VeriSO_EE", "Checks",  None))
        
        locale = QSettings().value('locale/userLocale')[0:2]

        check_topics = self.get_check_topics()
        if not check_topics:
            message = "Something went wrong reading check topics from json file."
            self.iface.messageBar().pushMessage("Error",   _translate("VeriSO_EE", message, None), level=QgsMessageBar.CRITICAL, duration=10)   
            return

        for check_topic in check_topics:
            checkfile = check_topics[check_topic]['file']
            single_check_menu = menu.addMenu(unicode(check_topic))         
            
            checks = self.get_checks_from_check_topic(checkfile)
            if not checks:
                message = "Something went wrong reading check topics from json file."
                self.iface.messageBar().pushMessage("Error",   _translate("VeriSO_EE", message, None), level=QgsMessageBar.CRITICAL, duration=10)   
                return

            for check in checks:
                check_name = check["name"]
                
              # Same multilingual strategy as in get_check_topics().  
                try: 
                    keys = check_name.keys()
                    try:
                        check_name = unicode(check_name[locale])
                        # language found
                    except:
                        # language *not* found
                        check_name = unicode(check_name.values()[0])
                except:
                    check_name = unicode(check_name)

                if check_name == "separator":
                    single_check_menu.addSeparator()
                else:
                    action = QAction(check_name, self.iface.mainWindow())
                    
                    try:
                        shortcut = check["shortcut"]
                        action.setShortcut(shortcut)
                    except:
                        pass

                    single_check_menu.addAction(action)                                         
                    QObject.connect(action, SIGNAL( "triggered()"), lambda complex_check=check: self.do_show_complex_check(complex_check))

        menubar.addMenu(menu)
        self.toolbar.insertWidget(self.beforeAction, menubar)

    def get_checks_from_check_topic(self, checkfile):
        """Reads all checks from a from a checkfile 
        (= all checks for a specific topic)
        
        Returns:
          A list with all checks. False if an error occured.
        """
        filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/"+self.module_name+"/checks/"+checkfile+".json"))
   
        try:
            checks = json.load(open(filename), object_pairs_hook=collections.OrderedDict) 
        except Exception, e:
            QgsMessageLog.logMessage(str(e), "VeriSO_EE", QgsMessageLog.CRITICAL)
            return
    
        try:
            topic_checks = []
            for check in checks["checks"]:
                topic_checks.append(check)
            return topic_checks
        except Exception, e:
            QgsMessageLog.logMessage(str(e), "VeriSO_EE", QgsMessageLog.CRITICAL)
            return

    def get_check_topics(self):
        """Get all check topics (aka groups).
        
        Different languages are support. See the json file how to deal with it.
        
        Returns:
          A ordererd dictionary with the topic name and corresponding check files (python). False if something went wrong.
        """
        filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/"+self.module_name+"/checks/checks.json"))

        try:
            checks = json.load(open(filename), object_pairs_hook=collections.OrderedDict) 
        except Exception, e:
            QgsMessageLog.logMessage(str(e), "VeriSO_EE", QgsMessageLog.CRITICAL)
            return
            
        locale = QSettings().value('locale/userLocale')[0:2]

        try:
            topics = OrderedDict()
            for check in checks["checks"]:
                topic = check["topic"]
                
                # Check, if json file is multilingual.
                try:
                    if topics.has_key(topic):
                        continue
                    topics[topic] = check
                    # Json is *not* multilingual.
                except:
                    # Json is multilingual.
                    
                    # If the language set in QGIS is not available in the
                    # jsons file, one (1) language will be chosen (in this
                    # case the first one).
                    try:
                        my_topic = topic[locale]
                        my_check = OrderedDict()
                        my_check["topic"] = my_topic
                        my_check["file"] = check["file"]
                        topics[my_topic] = my_check
                        # language found
                    except:
                        # language *not* found
                        my_check = OrderedDict()
                        my_check["topic"] = topic.values()[0]
                        my_check["file"] = check["file"]
                        topics[my_check["topic"]] = my_check
            return topics
        except Exception, e:
            QgsMessageLog.logMessage(str(e), "VeriSO_EE", QgsMessageLog.CRITICAL)
            return

    def do_show_complex_check(self, check):
        try:
            module = str(check["file"])
            _temp = __import__(module, globals(), locals(), ['ComplexCheck'])
            c = _temp.ComplexCheck(self.iface)
            c.run()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            QMessageBox.critical(None, "VeriSO_EE", str(traceback.format_exc(exc_traceback)))               
            return

    def do_init_baselayer_menu(self):
        """Initialize baselayer menu:
        
        Adds the menu and reads all baselayers from the json file
        and adds them into the menu.
        
        Language support is working!
        """
        menubar = QMenuBar(self.toolbar)
        menubar.setObjectName("VeriSOModule.LoadBaselayerMenuBar")        
        menubar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        menu = QMenu(menubar)
        menu.setTitle(_translate("VeriSO_EE", "Baselayer",  None))  
        
        locale = QSettings().value('locale/userLocale')[0:2]        
        
        baselayers = self.get_baselayers()
        if not baselayers:
            message = "Could not load baselayer definitions file."
            self.iface.messageBar().pushMessage("Error",   _translate("VeriSO_EE", message, None), level=QgsMessageBar.CRITICAL, duration=10)   
            return

        for baselayer in baselayers["baselayer"]:
            baselayer_title = baselayer["title"]
            try: 
                keys = baselayer_title.keys()
                try:
                    baselayer_title = unicode(baselayer_title[locale])
                    # language found
                except:
                    # language *not* found
                    baselayer_title = unicode(baselayer_title.values()[0])
            except:
                baselayer_title = unicode(baselayer_title)
                
            baselayer["title"] = baselayer_title
            
            action = QAction(baselayer_title, self.iface.mainWindow())
            menu.addAction(action)     
            QObject.connect(action, SIGNAL("triggered()" ), lambda layer=baselayer: self.do_show_baselayer(layer))    

        menubar.addMenu(menu)
        self.toolbar.insertWidget(self.beforeAction, menubar)        
        
    def do_show_baselayer(self, layer):
        """Load a baselayer into map canvas.
        
        Uses an universal 'load layer' method.
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            layer_loader = LoadLayer(self.iface) 
            layer_loader.load(layer, True, True) # Do not show legend for baselayers -> collapse legend.
        except Exception, e:
            QApplication.restoreOverrideCursor()
            QgsMessageLog.logMessage(str(e), "VeriSO_EE", QgsMessageLog.CRITICAL)
            return
            
        QApplication.restoreOverrideCursor()

    def get_baselayers(self):
        """Reads all baselayer definitions from a json file.
        
        Returns
          A list of dictionaries with all baselayer definitions. Otherwise False.
        """
        filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/veriso/modules/" + self.module_name + "/baselayer/baselayer.json"))
    
        try:
            baselayers = json.load(open(filename), object_pairs_hook=collections.OrderedDict) 
            return baselayers
        except Exception, e:
            QgsMessageLog.logMessage(str(e), "VeriSO_EE", QgsMessageLog.CRITICAL)
            return

    def do_init_topics_tables_menu(self):
        """Creates the topics and tables loader menu.
        Topics and tables are sorted alphanumerically. I'm not sure if ili2pg saves enough 
        information in the database to find out the interlis model order.
        
        At the moment there is no locale support here.
        Seems to be not very handy without mapping tables anyway...
        """
        menubar = QMenuBar(self.toolbar)
        menubar.setObjectName("VeriSOModule.LoadTopicsTablesMenuBar")        
        menubar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        menu = QMenu(menubar)
        menu.setTitle(_translate("VeriSO_EE", "Tables", None))  
        
        locale = QSettings().value('locale/userLocale')[0:2]        
        
        topics = self.get_topics_tables()
        if not topics:
            message = "Something went wrong catching the topics/tables list from the database."
            QMessageBox.critical(None, "VeriSO_EE", self.tr(message))
            return

        for topic in topics:
            topic_menu = menu.addMenu(unicode(topic["topic"]))      
            
            action = QAction(_translate("VeriSO_EE", "Load Topic",  None), self.iface.mainWindow())
            topic_menu.addAction(action)    
            topic_menu.addSeparator()      
            QObject.connect(action, SIGNAL( "triggered()" ), lambda topic=topic: self.do_show_topic(topic))                   
        
            layers = self.get_layers_from_topic(topic)        
            for my_layer in layers:
                action = QAction(my_layer["title"], self.iface.mainWindow())
                topic_menu.addAction(action)     
                QObject.connect(action, SIGNAL("triggered()" ), lambda layer=my_layer: self.do_show_single_topic_layer(layer))    
 
        menubar.addMenu(menu)
        self.toolbar.insertWidget(self.beforeAction, menubar)
        
    def get_layers_from_topic(self, topic):
        """Converts the layer information into a dictionary from
        a topic list.
        
        Adds the geometry column name if there are more than
        one geometry column in a layer.
        
        Returns: Dictionary with all the necessary data.
        """
        dd = {}
        for table in topic["tables"]:
            dd[table] = dd.get(table, 0) + 1

        i = 0
        layers = []
        for table in topic["tables"]:
            my_layer = {}
            my_layer["type"] = "postgres"
            my_layer["featuretype"] = table
            my_layer["key"] = topic["primary_keys"][i]
            my_layer["geom"] = topic["geometry_columns"][i]
            my_layer["group"] = topic["topic"]
            my_layer["title"] = topic["class_names"][i]
            i += 1
            # If there is more than one geometry column in the table
            # the name of the geometry columns is written in brackets
            # following the name of the table.
            if dd[table] > 1:
                my_layer["title"] =   my_layer["title"] + " (" + my_layer["geom"] + ")"

            layers.append(my_layer)
            
        return layers
        
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
                QgsMessageLog.logMessage(self.tr(message) + db.lastError().driverText(), "VeriSO_EE", QgsMessageLog.CRITICAL)                                
                return
                
            # I think libpg cannot deal with arrays from postgresql. So we return a comma sperated string.
            # Everything is ordered alphanumerical. Not sure if we would know enough to sort by interlis model ordering?!
            sql = "SELECT topic, array_to_string(array_agg(sql_name ORDER BY sql_name),',') as tables, "
            sql += "array_to_string(array_agg(coalesce(f_geometry_column,'') ORDER BY sql_name),',') as geometry_columns, "
            sql += "array_to_string(array_agg(class_name ORDER BY sql_name),',') as class_names, "
            sql += "array_to_string(array_agg(primary_key ORDER BY sql_name),',') as primary_keys "
            sql += "FROM " + db_schema + ".t_topics_tables GROUP BY topic ORDER BY topic;"

            query = db.exec_(sql)
            
            if not query.isActive():
                message = "Error while reading from database."
                QgsMessageLog.logMessage(self.tr(message), "VeriSO_EE", QgsMessageLog.CRITICAL)            
                QgsMessageLog.logMessage(str(QSqlQuery.lastError(query).text()), "VeriSO_EE", QgsMessageLog.CRITICAL)      
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
                
                primary_keys = []
                for primary_key in str(query.value(record.indexOf("primary_keys"))).split(","):
                    primary_keys.append(primary_key)
                topic["primary_keys"] = primary_keys

                topics.append(topic)
                
            db.close()
            del db
            
            return topics
            
        except Exception, e:
            message = "Something went wrong catching the topics tables list from the database."
            QgsMessageLog.logMessage(self.tr(message), "VeriSO_EE", QgsMessageLog.CRITICAL)                        
            QgsMessageLog.logMessage(str(e), "VeriSO_EE", QgsMessageLog.CRITICAL)     
            return 

    def do_show_single_topic_layer(self, layer):
        """Loads an interlis table from the database
        into the map canvas.
        
        Uses an universal 'load layer' method.
        """
        layer["type"] = str(self.provider)
        layer_loader = LoadLayer(self.iface)
        layer_loader.load(layer)

    def do_show_topic(self, topic):
        """Loads all interlis tables of a topic (from
        the database) into the map canvas.
        
        Uses an universal 'load layer' method.        
        """
        layers = self.get_layers_from_topic(topic)
        for layer in layers:
            self.do_show_single_topic_layer(layer)
        
    def do_init_defects_menu(self):
        """Inititializes the defects menu:
        - load defects
        - export defects
        
        Export defects usese some external python excel library.
        """
        menubar = QMenuBar(self.toolbar)
        menubar.setObjectName("VeriSOModule.LoadDefectsMenuBar")        
        menubar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        menu = QMenu(menubar)
        menu.setTitle(_translate("VeriSO_EE", "Defects",  None))  

        action = QAction(_translate("VeriSO_EE", "Load defects layer",  None), self.iface.mainWindow())
        QObject.connect(action, SIGNAL( "triggered()"), lambda foo="bar": self.do_load_defects(foo))
        menu.addAction(action)     
        
        action = QAction(QCoreApplication.translate("VeriSO_EE", "Export defects layer"), self.iface.mainWindow())
        QObject.connect(action, SIGNAL( "triggered()"), lambda foo="bar": self.do_export_defects(foo))
        menu.addAction(action)     

        menubar.addMenu(menu)
        self.toolbar.insertWidget(self.beforeAction, menubar)

    def do_load_defects(self, bar):
        from tools.loaddefects import LoadDefects
        d = LoadDefects(self.iface)
        d.run()

    def do_export_defects(self, bar):
        from tools.exportdefects import ExportDefects        
        d = ExportDefects(self.iface)
        d.run()

    def clean_gui(self):
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
#        menubar = QMenuBar(self.toolBar)
#        menubar.setObjectName("QGeoAppModule.QVeriso.LoadDefectsMenuBar")        
#        menubar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
#        menu = QMenu(menubar)
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
#        menubar.addMenu(menu)
#        self.toolBar.insertWidget(self.beforeAction, menubar)
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
#        menubar = QMenuBar(self.toolBar)
#        menubar.setObjectName("QGeoAppModule.QVeriso.LoadChecksMenuBar")        
#        menubar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
#        menu = QMenu(menubar)
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
#        menubar.addMenu(menu)
#        self.toolBar.insertWidget(self.beforeAction, menubar)
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
#        menubar = QMenuBar(self.toolBar)
#        menubar.setObjectName("QGeoAppModule.QVeriso.LoadBaseLayersMenuBar")        
#        menubar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
#        menu = QMenu(menubar)
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
#        menubar.addMenu(menu)
#        self.toolBar.insertWidget(self.beforeAction, menubar)
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
#        menubar = QMenuBar(self.toolBar)
#        menubar.setObjectName("QGeoAppModule.QVeriso.LoadTopicsTablesMenuBar")        
#        menubar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
#        menu = QMenu(menubar)
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
#        menubar.addMenu(menu)
#        self.toolBar.insertWidget(self.beforeAction, menubar)
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

        
        


