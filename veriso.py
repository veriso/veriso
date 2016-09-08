# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VeriSO
                                 A QGIS plugin
 Verification application module for Interlis data.
                              -------------------
        begin                : 2014-07-28
        git sha              : $Format:%H$
        copyright            : (C) 2016 OPENGIS.ch
                             :     2014 by Stefan Ziegler
        email                : info@opengis.ch
                             : edi.gonzales@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from __future__ import absolute_import

import os.path
from builtins import object, str
from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator, qVersion
from qgis.PyQt.QtGui import QPalette
from qgis.PyQt.QtWidgets import QAction, QMenu, QMenuBar, QSizePolicy

from qgis.gui import QgsMessageBar

from veriso.base.utils.utils import tr, get_projects, dynamic_import


class VeriSO(object):
    def __init__(self, iface):
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.plugin_dir = os.path.dirname(__file__)

        self.settings = QSettings("CatAIS", "VeriSO")

        locale = QSettings().value('locale/userLocale')[0:2]
        self.locale_path = os.path.join(
                self.plugin_dir,
                'i18n',
                'veriso_{}.qm'.format(locale))

        if os.path.exists(self.locale_path):
            self.translator = QTranslator()
            self.translator.load(self.locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # members
        self.toolbar = None
        self.menubar_projects = None
        self.menubar_file = None
        self.menu_file = None
        self.import_project = None
        self.delete_project = None
        self.menubar_settings = None
        self.menu_projects = None
        self.menu_settings = None
        self.options = None
        self.import_dlg = None
        self.delete_dlg = None
        self.options_dlg = None

    # noinspection PyPep8Naming
    def initGui(self):
        icon_path = ':/plugins/veriso/icon.png'

        # Qt offers some themes which you also can change in QGIS settings.
        # Since the background color of the menu toolbar can be different than
        # the background color of the button toolbars, the veriso toolbar 
        # doesn't suit well. So we change it manually by finding out the 
        # background color of one (e.g. file) toolbar and applying it 
        # to the veriso toolbar.
        # This approach works (well?) for xfce 4.12 and standard (gtk+) theme.
        # We need to do this also in other methods when we add new menus :-(

        # 20150406: Only change QToolBar background color. 
        # Otherweise the later added menus will have white hover color and
        # other quirks.
        # Strange: QToolBar stylesheet seems to need an border.
        background_color = self.iface.mainWindow().menuBar().palette().color(
                QPalette.Window).name()

        # main toolbar
        self.toolbar = self.iface.addToolBar("VeriSO")
        self.toolbar.setStyleSheet(
                "QToolBar {background-color: " + background_color +
                "; border: 0px solid " + background_color + ";}")

        self.toolbar.setObjectName("VeriSO.Main.ToolBar")
        self.toolbar.setSizePolicy(
                QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        # projects
        self.menubar_projects = QMenuBar()
        self.menubar_projects.setObjectName("VeriSO.Main.ProjectsMenuBar")
        self.menubar_projects.setSizePolicy(
                QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred))
        self.menu_projects = QMenu()
        self.menu_projects.setTitle(tr("Projects"))
        self.menubar_projects.addMenu(self.menu_projects)

        # files
        self.menubar_file = QMenuBar()
        self.menubar_file.setObjectName("VeriSO.Main.FileMenuBar")
        self.menubar_file.setSizePolicy(
                QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.menu_file = QMenu()
        self.menu_file.setTitle(tr("File"))
        self.import_project = QAction(tr("Import project"),
                                      self.iface.mainWindow())
        self.import_project.triggered.connect(self.do_import_project)
        self.delete_project = QAction(tr("Delete project"),
                                      self.iface.mainWindow())
        self.delete_project.triggered.connect(self.do_delete_project)
        self.menu_file.addActions([self.import_project, self.delete_project])
        self.menubar_file.addMenu(self.menu_file)

        # settings
        self.menubar_settings = QMenuBar()
        self.menubar_settings.setObjectName("VeriSO.Main.SettingsMenuBar")
        self.menubar_settings.setSizePolicy(
                QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.menu_settings = QMenu()
        self.menu_settings.setTitle(tr("Settings"))

        self.options = QAction(tr("Options"), self.iface.mainWindow())
        self.options.triggered.connect(self.do_options)
        self.menu_settings.addActions([self.options])
        self.menubar_settings.addMenu(self.menu_settings)

        # Add menus to toolbar.
        self.toolbar.addWidget(self.menubar_projects)
        self.toolbar.addWidget(self.menubar_file)
        self.toolbar.addWidget(self.menubar_settings)

        # Initial load of project menu entries.
        self.do_load_projects_database()

    def do_import_project(self):
        from .base.file.importproject import ImportProjectDialog
        self.import_dlg = ImportProjectDialog(self.iface)
        if self.import_dlg.init_gui():
            self.import_dlg.show()
            self.import_dlg.projectsDatabaseHasChanged.connect(
                    self.do_load_projects_database)

    def do_delete_project(self):
        from .base.file.deleteproject import DeleteProjectDialog
        self.delete_dlg = DeleteProjectDialog(self.iface)
        if self.delete_dlg.init_gui():
            self.delete_dlg.show()
            self.delete_dlg.projectsDatabaseHasChanged.connect(
                    self.do_load_projects_database)

    def do_options(self):
        from .base.settings.options import OptionsDialog
        self.options_dlg = OptionsDialog(self.iface)
        self.options_dlg.init_gui()
        self.options_dlg.show()
        self.options_dlg.projectsDatabaseHasChanged.connect(
                self.do_load_projects_database)

    def do_load_projects_database(self):
        projects = get_projects()

        if projects is not None:
            grouped_projects = {}
            for project in projects:
                module_name = project["appmodulename"]
                try:
                    module_list = grouped_projects[module_name]
                except KeyError:
                    module_list = []

                module_list.append(project)
                grouped_projects[module_name] = module_list

            self.menu_projects.clear()
            for key in sorted(grouped_projects):
                modules = grouped_projects[key]
                group_menu = self.menu_projects.addMenu(str(key))
                sorted_projects_list = sorted(modules,
                                              key=lambda k: k['displayname'])
                for project in sorted_projects_list:
                    action = QAction(str(project["displayname"]),
                                     self.iface.mainWindow())
                    group_menu.addAction(action)
                    action.triggered.connect(
                            lambda checked, active_project=project:
                            self.do_load_project(active_project))

    def do_load_project(self, project):
        self.settings.setValue("project/id", str(project["id"]))
        self.settings.setValue("project/displayname",
                               str(project["displayname"]))
        self.settings.setValue("project/appmodule", str(project["appmodule"]))
        self.settings.setValue("project/appmodulename",
                               str(project["appmodulename"]))
        self.settings.setValue("project/ilimodelname",
                               str(project["ilimodelname"]))
        self.settings.setValue("project/epsg", str(project["epsg"]))
        self.settings.setValue("project/provider", str(project["provider"]))
        self.settings.setValue("project/dbhost", str(project["dbhost"]))
        self.settings.setValue("project/dbport", str(project["dbport"]))
        self.settings.setValue("project/dbname", str(project["dbname"]))
        self.settings.setValue("project/dbschema", str(project["dbschema"]))
        self.settings.setValue("project/dbuser", str(project["dbuser"]))
        self.settings.setValue("project/dbpwd", str(project["dbpwd"]))
        self.settings.setValue("project/dbadmin", str(project["dbadmin"]))
        self.settings.setValue("project/dbadminpwd", str(project["dbadminpwd"]))
        self.settings.setValue("project/projectdir", str(project["projectdir"]))

        module_name = str(project["appmodule"]).lower()
        try:
            module_name = "veriso.modules." + module_name + ".applicationmodule"
            module = dynamic_import(module_name)
            application_module = module.ApplicationModule(
                    self.iface, self.toolbar, self.locale_path)
            application_module.init_gui()

        except Exception as e:
            self.message_bar.pushMessage("VeriSO", str(e),
                                         QgsMessageBar.CRITICAL, duration=0)

    def unload(self):
        self.iface.mainWindow().removeToolBar(self.toolbar)
