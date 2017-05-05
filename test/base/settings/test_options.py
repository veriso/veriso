from __future__ import absolute_import
from unittest import TestCase
try:
    from mock import patch, Mock
except ImportError:
    from unittest.mock import patch, Mock
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtCore import Qt
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

    @patch('qgis.PyQt.QtWidgets.QFileDialog.getOpenFileName')
    def test_on_btnBrowseProjectsDatabase_clicked(self, mock_getOpenFileName):
        '''test Button Browse Project Database'''
        mock_getOpenFileName.return_value = "/foo/bar.db"
        button = self.dialog.btnBrowseProjectsDatabase
        button.click()
        self.assertEquals(self.dialog.lineEditProjectsDatabase.text(), "/foo/bar.db")

    @patch('qgis.PyQt.QtWidgets.QFileDialog.getExistingDirectory')
    def test_on_btnBrowseProjectsRootDir_clicked(self, mock_getExistingDirectory):
        '''test Button Project Root Dir'''
        mock_getExistingDirectory.return_value = "/foo/bar/"
        button = self.dialog.btnBrowseProjectsRootDir
        button.click()
        self.assertEquals(self.dialog.lineEditProjectsRootDir.text(), "/foo/bar/")

    @patch('veriso.base.settings.options.OptionsDialog.test_connection_succes')
    @patch('veriso.base.settings.options.OptionsDialog.test_connection_failed')
    def xtest_on_btnTestProjectDB_clicked(self, mock_test_connection_failed, mock_test_connection_succes):
         '''test Button Test Project DB with default options'''
         self.dialog.lineEditProjectsDatabase.setText('')
         button = self.dialog.btnTestProjectDB
         button.click()
         assert mock_test_connection_succes.called

    @patch('veriso.base.settings.options.OptionsDialog.test_connection_succes')
    @patch('veriso.base.settings.options.OptionsDialog.test_connection_failed')
    def test_on_btnTestConnection_clicked(self, mock_test_connection_failed, mock_test_connection_succes):
        '''test Button Test Connection with current settings'''
        button = self.dialog.btnTestConnection
        button.click()
        assert mock_test_connection_succes.called

    def test_on_listWidgetModelRepos_itemSelectionChanged(self):
        '''test Item selection on List Model Repos Widget'''
        self.dialog.listWidgetModelRepos.clearSelection()
        self.assertFalse(self.dialog.btnDeleteModelRepo.isEnabled())
        self.assertFalse(self.dialog.btnEditModelRepo.isEnabled())
        self.dialog.listWidgetModelRepos.setItemSelected(self.dialog.listWidgetModelRepos.item(0), True)
        self.assertTrue(self.dialog.btnDeleteModelRepo.isEnabled())
        self.assertTrue(self.dialog.btnEditModelRepo.isEnabled())

    def test_on_btnDeleteModelRepo_clicked(self):
        '''test Button Delete Model Repo'''
        count = self.dialog.listWidgetModelRepos.count()
        self.dialog.listWidgetModelRepos.clearSelection()
        self.dialog.listWidgetModelRepos.insertItem(0,"http://foo.bar")
        self.dialog.listWidgetModelRepos.setItemSelected(self.dialog.listWidgetModelRepos.item(0),True)
        button = self.dialog.btnDeleteModelRepo
        button.click()
        self.assertEqual(count, self.dialog.listWidgetModelRepos.count())

    @patch('veriso.base.settings.options.OptionsDialog.ask_url')
    def test_on_btnAddModelRepo_clicked(self, mock_ask_url):
        '''test Button Add Model Repo'''
        mock_ask_url.return_value=['http://foo.bar', True]
        count = self.dialog.listWidgetModelRepos.count()
        button = self.dialog.btnAddModelRepo
        button.click()
        self.assertEqual(count +1, self.dialog.listWidgetModelRepos.count())

    @patch('qgis.PyQt.QtWidgets.QFileDialog.getExistingDirectory')
    def test_on_btnAddLocalModelRepo_clicked(self, mock_getExistingDirectory):
        '''test Button Add Local Model Repo'''
        mock_getExistingDirectory.return_value = "/foo/bar/"
        count = self.dialog.listWidgetModelRepos.count()
        button = self.dialog.btnAddLocalModelRepo
        button.click()
        self.assertEqual(count + 1, self.dialog.listWidgetModelRepos.count())

    @patch('veriso.base.settings.options.OptionsDialog.ask_url')
    def test_on_btnEditModelRepo_clicked(self, mock_ask_url):
        '''test Button Edit Model Repo'''
        mock_ask_url.return_value=['http://foo.bar', True]
        self.dialog.listWidgetModelRepos.insertItem(0, 'http://bar.foo')
        self.dialog.listWidgetModelRepos.setCurrentItem(self.dialog.listWidgetModelRepos.item(0))
        button = self.dialog.btnEditModelRepo
        button.click()
        self.assertEqual(self.dialog.listWidgetModelRepos.item(0).text(), 'http://foo.bar')

