# coding=utf-8
import json
import os
import random
import string
from unittest import TestCase

from qgis.PyQt.QtSql import QSqlDatabase
from veriso.base.utils.utils import (
    get_modules_dir,
    get_projects_db,
    get_default_db,
    open_sqlite_db,
    open_psql_db,
    yaml_load_file,
    get_projects,
    dynamic_import
)
from veriso.base.utils.exceptions import VerisoError


class TestUtils(TestCase):
    def test_get_modules_dir(self):
        self.assertIs(True, os.path.isdir(get_modules_dir()))

    def test_get_projects_db(self):
        db = get_projects_db()
        self.assertIs(QSqlDatabase, type(db))
        self.assertIs(True, os.path.exists(db.databaseName()))

    def test_get_default_db(self):
        self.assertIs(QSqlDatabase, type(get_default_db()))

    def test_open_sqlite_db(self):
        existing_db = get_projects_db()
        random_name = ''.join(random.choice(string.lowercase) for i in range(9))
        db = open_sqlite_db(existing_db.databaseName(), random_name)
        try:
            self.assertEqual(db.databaseName(), existing_db.databaseName())
        except:
            raise
        finally:
            db.close()
            QSqlDatabase.removeDatabase(random_name)

    def test_open_psql_db(self):
        with self.assertRaises(VerisoError):
            open_psql_db('rand', 'rand', 'rand', 'rand', 'rand')

    def test_yaml_load_file(self):
        file_path = os.path.join(get_modules_dir(), 'veriso_ee', 'module.yml')
        expected = {
            u'displayname': u'VeriSO (EE/EN)',
            u'ilimodels': [{
                u'epsg': u'21781',
                u'ilimodel': u'DM01AVCH24D',
                u'referenceframe': u'LV03'
            },
                {
                    u'epsg': u'2056',
                    u'ilimodel': u'DM01AVCH24LV95D',
                    u'referenceframe': u'LV95'
                },
                {
                    u'epsg': u'21781',
                    u'ilimodel': u'DM01AVBE11D',
                    u'referenceframe': u'LV03'
                },
                {
                    u'epsg': u'2056',
                    u'ilimodel': u'DM01AVBE11LV95D',
                    u'referenceframe': u'LV95'
                }]
        }
        loaded_dict = yaml_load_file(file_path)
        loaded_dict = json.loads(json.dumps(loaded_dict))
        self.assertDictEqual(loaded_dict, expected)

    def test_get_projects(self):
        projs = get_projects()[0]
        self.assertTrue('dbhost' in projs)
        self.assertTrue('ilimodelname' in projs)
        self.assertTrue('dbname' in projs)
        self.assertTrue('importdate' in projs)
        self.assertTrue('dbpwd' in projs)
        self.assertTrue('appmodule' in projs)
        self.assertTrue('dbadminpwd' in projs)
        self.assertTrue('provider' in projs)
        self.assertTrue('dbuser' in projs)
        self.assertTrue('dbadmin' in projs)
        self.assertTrue('datadate' in projs)
        self.assertTrue('id' in projs)
        self.assertTrue('dbschema' in projs)
        self.assertTrue('projectrootdir' in projs)
        self.assertTrue('dbport' in projs)
        self.assertTrue('displayname' in projs)
        self.assertTrue('projectdir' in projs)
        self.assertTrue('appmodulename' in projs)
        self.assertTrue('epsg' in projs)

    def test_dynamic_import(self):
        dynamic_import('veriso.base.utils.exceptions')
        with self.assertRaises(VerisoError):
            dynamic_import('veriso.base.utils.lalala')
