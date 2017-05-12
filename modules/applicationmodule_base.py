# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import sys, os
import traceback
from collections import OrderedDict

from builtins import str
from qgis.PyQt.QtCore import QCoreApplication, QObject, QSettings, Qt
from qgis.PyQt.QtWidgets import QAction, QApplication, QMenu, QMenuBar, \
    QSizePolicy
from qgis.core import QgsMessageLog
from qgis.gui import QgsMessageBar

from veriso.base.utils.module import (get_topics_tables, get_baselayers,
                                      get_check_topics, get_layers_from_topic)
from veriso.base.utils.loadlayer import LoadLayer
from veriso.base.utils.utils import dynamic_import, get_modules_dir, get_subdirs, yaml_load_file

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


class ApplicationModuleBase(QObject):
    def __init__(self, veriso):
        QObject.__init__(self)
        self.iface = veriso.iface
        self.message_bar = self.iface.messageBar()
        self.canvas = self.iface.mapCanvas()
        self.toolbar = veriso.toolbar

        self.settings = QSettings("CatAIS", "VeriSO")
        self.epsg = self.settings.value("project/epsg")
        self.provider = self.settings.value("project/provider")
        self.module = self.settings.value("project/appmodule")
        self.module_name = self.settings.value("project/appmodulename")

        self.module_extended = self.get_extended_module_name()

        self.defects_layers = {}
        self.defects_list_dock = veriso.defects_list_dock

        self.beforeAction = None
        self.settingsAction = None

    # noinspection PyPep8Naming
    def init_gui(self):
        """Initialize all the additional menus.
        this method is the entry point when a new project is loaded
        """
 
        self.clean_gui()
        self.do_init_checks_menu()
        self.do_init_defects_menu()
        self.defects_list_dock.clear()
        show_topic_tables_menu = QSettings("CatAIS", "VeriSO").value(
                "options/general/topics_tables_menu", False, type=bool)
        if show_topic_tables_menu:
            self.do_init_topics_tables_menu()
        self.do_init_baselayer_menu()

        if(sys.platform == 'darwin'):
            self.iface.mainWindow().menuBar().setNativeMenuBar(False)
            self.iface.mainWindow().menuBar().setNativeMenuBar(True)

    def do_init_checks_menu(self):
        """Initialize checks menu.
        """
        try:
            check_topics = OrderedDict()

            # Load first the checks from the extended module
            if(self.module_extended):
                check_topics.update(get_check_topics(self.module_extended))

            check_topics.update(get_check_topics(self.module))
        except:
            message = "Something went wrong reading check topics from" \
                      "yaml file"
            self.message_bar.pushMessage("Error",
                                         _translate(self.module, message,
                                                    None),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
            return

        menubar = self.get_checks_menubar(check_topics)
        self.toolbar.insertWidget(self.beforeAction, menubar)
        if(sys.platform == 'darwin'):
            menubar.setNativeMenuBar(False)

    def get_checks_menubar(self, check_topics):
        menubar = QMenuBar(self.toolbar)
        menubar.setObjectName("VeriSOModule.LoadChecksMenuBar")
        menubar.setSizePolicy(
                QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        menu = QMenu(menubar)
        menu.setTitle(_translate(self.module, "Checks", None))

        locale = QSettings().value('locale/userLocale')[0:2]
        for check_topic in check_topics:
            checks = check_topics[check_topic]["checks"]
            if not checks:
                message = "The topic %s has no valid checks: skiping." % (
                    check_topic)
                self.message_bar.pushWarning(
                        "Warning",
                        _translate(self.module, message, None))

                # this topic has no valid checks
                continue

            single_check_menu = menu.addMenu(str(check_topic))

            for check in checks:
                check_name = check["name"]

                # Same multilingual strategy as in get_check_topics().
                try:
                    keys = list(check_name.keys())
                    try:
                        check_name = str(check_name[locale])
                        # language found
                    except:
                        # language *not* found
                        check_name = str(list(check_name.values())[0])
                except:
                    check_name = str(check_name)

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
                    topic_dir = check_topics[check_topic]['topic_dir']
                    action.triggered.connect(
                            lambda checked,
                            complex_check=check,
                            folder=topic_dir:
                            self.do_show_complex_check(folder, complex_check))

        menubar.addMenu(menu)
        return menubar

    def do_show_complex_check(self, folder, check):

        modules_dir = os.path.join(get_modules_dir())
        module_dir = os.path.join(
            modules_dir, self.module, 'checks', folder)

        # Search first in the module, if the check doesn't exist, try in the
        # extended module
        if (os.path.exists(module_dir)):
            module = "veriso.modules.%s.checks.%s.%s" % (
                self.module, folder, check["file"])
        else:
            module = "veriso.modules.%s.checks.%s.%s" % (
                self.module_extended, folder, check["file"])

        try:
            module = dynamic_import(module)
            c = module.ComplexCheck(self.iface)
            c.run()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage(self.module_name,
                                         str(traceback.format_exc(
                                                 exc_traceback)),
                                         QgsMessageBar.CRITICAL, duration=0)
            return

    def do_init_baselayer_menu(self):
        """Initialize baselayer menu:

        Adds the menu and reads all baselayers from the yaml file
        and adds them into the menu.

        Language support is working!
        """
        menubar = QMenuBar(self.toolbar)
        menubar.setObjectName("VeriSOModule.LoadBaselayerMenuBar")
        menubar.setSizePolicy(
                QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        menu = QMenu(menubar)
        menu.setTitle(_translate(self.module, "Baselayer", None))

        locale = QSettings().value('locale/userLocale')[0:2]

        baselayers = get_baselayers(self.module)
        if not baselayers:
            message = "Could not load baselayer definitions file."
            self.message_bar.pushMessage("Error",
                                         _translate(self.module, message,
                                                    None),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
            return

        for baselayer in baselayers["baselayer"]:
            baselayer_title = baselayer["title"]
            try:
                keys = list(baselayer_title.keys())
                try:
                    baselayer_title = str(baselayer_title[locale])
                    # language found
                except:
                    # language *not* found
                    baselayer_title = str(list(baselayer_title.values())[0])
            except:
                baselayer_title = str(baselayer_title)

            baselayer["title"] = baselayer_title

            action = QAction(baselayer_title, self.iface.mainWindow())
            menu.addAction(action)
            action.triggered.connect(
                    lambda checked, layer=baselayer: self.do_show_baselayer(
                            layer))

        menubar.addMenu(menu)
        self.toolbar.insertWidget(self.beforeAction, menubar)
        if(sys.platform == 'darwin'):
            menubar.setNativeMenuBar(False)

    def do_show_baselayer(self, layer):
        """Load a baselayer into map canvas.

        Uses an universal 'load layer' method.
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            layer_loader = LoadLayer(self.iface)
            layer_loader.load(layer, visible=True, collapsed_legend=True)
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QgsMessageLog.logMessage(str(e), self.module_name,
                                     QgsMessageLog.CRITICAL)
            return

        QApplication.restoreOverrideCursor()

    def do_init_topics_tables_menu(self):
        """Creates the topics and tables loader menu.
        Topics and tables are sorted alphanumerically. I'm not sure if ili2pg
        saves enough
        information in the database to find out the interlis model order.

        At the moment there is no locale support here.
        Seems to be not very handy without mapping tables anyway...
        """
        menubar = QMenuBar(self.toolbar)
        menubar.setObjectName("VeriSOModule.LoadTopicsTablesMenuBar")
        menubar.setSizePolicy(
                QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        menu = QMenu(menubar)
        menu.setTitle(_translate(self.module, "Tables", None))

        topics = get_topics_tables(self.module_name)
        if not topics:
            message = "Something went wrong catching the topics/tables list " \
                      "from the database."
            self.message_bar.pushMessage(self.module_name,
                                         _translate(self.module, message, None),
                                         QgsMessageBar.CRITICAL, duration=0)
            return

        for topic in topics:
            topic_menu = menu.addMenu(str(topic["topic"]))

            action = QAction(_translate(self.module, "Load Topic", None),
                             self.iface.mainWindow())
            topic_menu.addAction(action)
            topic_menu.addSeparator()
            action.triggered.connect(
                    lambda checked, topic=topic: self.do_show_topic(topic))

            layers = get_layers_from_topic(topic)
            for my_layer in layers:
                action = QAction(my_layer["title"], self.iface.mainWindow())
                topic_menu.addAction(action)
                action.triggered.connect(
                        lambda checked, layer=my_layer:
                        self.do_show_single_topic_layer(layer))

        menubar.addMenu(menu)
        self.toolbar.insertWidget(self.beforeAction, menubar)
        if(sys.platform == 'darwin'):
            menubar.setNativeMenuBar(False)

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
        layers = get_layers_from_topic(topic)
        for layer in layers:
            self.do_show_single_topic_layer(layer)

    def do_init_defects_menu(self):
        """Inititializes the defects menu:
        - load defects
        - import defects
        - export defects

        Import and Export defects use some external python excel library.
        xlsxwriter, openpyxl
        """
        menubar = self.toolbar.findChild(
                QMenuBar, 'VeriSO.Main.LoadDefectsMenuBar')

        menu = menubar.findChild(QMenu, 'VeriSO.Main.LoadDefectsMenu')
        menu.setTitle(_translate(self.module, "Defects", None))

        action = QAction(_translate(self.module, "Load defects layer", None),
                         self.iface.mainWindow())
        action.setObjectName("VeriSOModule.LoadDefectsAction")
        action.triggered.connect(self.do_load_defects_wrapper)
        menu.addAction(action)

        action = QAction(
                QCoreApplication.translate(
                        self.module, "Import defects layer"),
                self.iface.mainWindow())
        action.setObjectName("VeriSOModule.ImportDefectsAction")
        action.triggered.connect(self.do_import_defects)
        menu.addAction(action)

        action = QAction(
                QCoreApplication.translate(
                        self.module, "Export defects layer"),
                self.iface.mainWindow())
        action.setObjectName("VeriSOModule.ExportDefectsAction")
        action.triggered.connect(self.do_export_defects)
        menu.addAction(action)

        menubar.addMenu(menu)
        self.toolbar.insertWidget(self.beforeAction, menubar)

    def do_load_defects_wrapper(self):
        self.defects_layers = self.do_load_defects()
        self.defects_list_dock.load_layers(self.defects_layers)

    def do_load_defects(self):
        defects_module = 'veriso.modules.loaddefects_base'
        defects_module = dynamic_import(defects_module)
        d = defects_module.LoadDefectsBase(self.iface, self.module_name)
        return d.run()

    def do_import_defects(self):
        from veriso.modules.tools.importdefects import ImportDefectsDialog
        self.import_defects_dlg = ImportDefectsDialog(self.iface, self.defects_list_dock)
        if self.import_defects_dlg.init_gui():
            self.import_defects_dlg.show()

    def do_export_defects(self):
        defects_module = 'veriso.modules.tools.exportdefects'
        defects_module = dynamic_import(defects_module)
        d = defects_module.ExportDefects(self.iface, self.module,
                                         self.module_name)
        d.run()

    def clean_gui(self):
        # Remove all the applications module specific menus.
        actions = self.toolbar.actions()
        for action in actions:
            try:
                object_name = action.defaultWidget().objectName()
                # Delete existing module menus.
                if object_name[0:12] == "VeriSOModule":
                    self.toolbar.removeAction(action)
                # Remember the action where we want to insert our new menu 
                # (e.g. settings menu bar).
                if object_name == "VeriSO.Main.SettingsMenuBar":
                    self.beforeAction = action
                # Get settings menu bar for module specific settings.
                if object_name == "VeriSO.Main.SettingsMenuBar":
                    self.settingsAction = action
                if object_name == "VeriSO.Main.LoadDefectsMenuBar":
                    defects_action = action
            except AttributeError:
                pass

        settings_menu = self.settingsAction.defaultWidget().actions()[
            0].parentWidget()
        self.delete_actions_from_menu(settings_menu)

        defect_menu = defects_action.defaultWidget().actions()[
            0].parentWidget()

        self.delete_actions_from_menu(defect_menu)

    @staticmethod
    def delete_actions_from_menu(menu):
        """
        # Remove all the application module specific options/settings
        # in a menu.
        :param menu:
        :return:
        """
        actions = menu.actions()
        for action in actions:
            object_name = action.objectName()
            if object_name[0:12] == "VeriSOModule" or action.isSeparator():
                menu.removeAction(action)

    def get_extended_module_name(self):
        """
        # Read into module.yml to see if the module extends another module        
        :return: the name of the extended module 
        """
        modules_dir = os.path.join(get_modules_dir())
        module_file = os.path.join(
            modules_dir, self.module_name.lower(), 'module.yml')

        if os.path.isfile(module_file):
            module_yaml = yaml_load_file(module_file)

            if module_yaml.has_key('extends'):
                return module_yaml['extends']

        return None