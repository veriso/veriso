import os

from unittest import TestCase

try:
    import mock
except ImportError:
    from unittest import mock

from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtTest import QTest

from veriso.test.utilities import get_qgis_app
from veriso.base.settings.options import OptionsDialog


QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()

class TestUtils(TestCase):

    def setUp(self):
        self.dialog = OptionsDialog(IFACE)
        self.dialog.init_gui()
        self.settings = QSettings("CatAIS", "VeriSO")

    def test_dialog_lineEditDbPort_validator(self):
        '''test if validator in lineEditDbPort accepts wrong values'''
        before = self.dialog.lineEditDbPort.text()
        for i in range(ord('A'), ord('z')):
            self.dialog.lineEditDbPort.insert(chr(i))
        self.assertEquals(self.dialog.lineEditDbPort.text(), before)

    def test_dialog_settings(self):
        '''test if dialog reads the correct setting value'''
        self.assertEquals(self.dialog.lineEditProjectsDatabase.text(),
                          self.settings.value("options/general/projects_database"))
        self.assertEquals(self.dialog.lineEditProjectsRootDir.text(),
                          self.settings.value("options/general/projects_root_directory"))
        self.assertEquals(self.dialog.lineEditImportJar.text(),
                          self.settings.value("options/import/jar"))

        vm_arguments = self.settings.value("options/import/vm_arguments")
        if vm_arguments == "" or not vm_arguments or vm_arguments is None:
            self.assertEquals(self.dialog.plainTextEditImportVMArguments.toPlainText(), "-Xms128m -Xmx1024m")
        else:
            self.assertEquals(self.dialog.plainTextEditImportVMArguments.toPlainText(),
                              self.settings.value("options/import/vm_arguments"))
            self.assertEquals(self.dialog.lineEditDbHost.text(), self.settings.value("options/db/host"))
            self.assertEquals(self.dialog.lineEditDbDatabase.text(), self.settings.value("options/db/name"))
            self.assertEquals(self.dialog.lineEditDbPort.text(), self.settings.value("options/db/port"))
            self.assertEquals(self.dialog.lineEditDbUser.text(), self.settings.value("options/db/user"))
            self.assertEquals(self.dialog.lineEditDbUserPwd.text(), self.settings.value("options/db/pwd"))
            self.assertEquals(self.dialog.lineEditDbAdmin.text(), self.settings.value("options/db/admin"))
            self.assertEquals(self.dialog.lineEditDbAdminPwd.text(), self.settings.value("options/db/adminpwd"))

        lst_items = [i.text() for i in self.dialog.listWidgetModelRepos.findItems("", Qt.MatchContains)]
        self.assertEquals(lst_items[0], 'http://www.catais.org/models/')
        self.assertEquals(lst_items[1], 'http://models.geo.admin.ch/')

    def test_on_on_btnBrowseImportJar_clicked(self):
        '''test Button Browse Import Jar'''
        #button = self.dialog.btnBrowseImportJar
        #@mock.patch('test_options.QFileDialog')
        pass