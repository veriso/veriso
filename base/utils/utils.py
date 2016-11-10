# coding=utf-8
import importlib
import os
import yaml
from builtins import next
from collections import OrderedDict
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QSettings, QCoreApplication
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

from qgis.core import QgsMessageLog
from veriso.base.utils.exceptions import VerisoError


def dynamic_import(module_name):
    """
    import a module from the given path in a safe manner
    :param module_name: string path to the module to load
    :return: the loaded module
    """
    try:
        module = importlib.import_module(module_name)
        QgsMessageLog.logMessage('Successfully loaded: %s ' % module_name,
                                 "VeriSO",
                                 QgsMessageLog.INFO)
        return module
    except Exception as e:
        message = tr("Error while loading application module: %s") % module_name
        raise VerisoError(message, e)


def get_modules_dir():
    """
    returns the directory where the modules are stored
    :return: str
    """
    path = os.path.join(get_root_dir(), 'modules')
    return path


def get_root_dir():
    """
    returns the directory where veriso.py is
    :return: str
    """
    path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            os.pardir,
            os.pardir)
    return path


def get_subdirs(path):
    """
    Returns the immediate subdirs of a given directory
    :param path: the path
    :return: list
    """
    return next(os.walk(path))[1]


def yaml_load_file(file_path):
    """
    High level method to parse YAML safely into an OrderedDict
    :param file_path: file path of the yml
    :return: dict
    """
    try:
        with open(file_path) as f:
            parsed_dict = yaml_ordered_load(f, Loader=yaml.SafeLoader)
        return parsed_dict
    except Exception as e:
        raise VerisoError("Something went wrong when parsing %s" % file_path, e)


def yaml_ordered_load(
        stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """
    Low level method to load YAML into an OrderedDict
    see: http://stackoverflow.com/a/21912744/1193450

    :param stream:  byte string, a Unicode string,
        an open binary file object, or an open text file object
    :param Loader: the loader to be used
    :param object_pairs_hook:
    :return: dict
    """

    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_mapping)
    return yaml.load(stream, OrderedLoader)


def get_projects():
    projects = []
    error_message = "Error while reading from projects database."

    try:
        db = get_projects_db()

        sql = "SELECT * FROM projects;"

        query = db.exec_(sql)

        if not query.isActive():
            QgsMessageLog.logMessage(tr(error_message), "VeriSO",
                                     QgsMessageLog.CRITICAL)
            QgsMessageLog.logMessage(str(QSqlQuery.lastError(query).text()),
                                     "VeriSO", QgsMessageLog.CRITICAL)
            return

        record = query.record()
        while next(query):
            project = {
                "id": str(query.value(record.indexOf("id"))),
                "displayname": str(
                        query.value(record.indexOf("displayname"))),
                "dbhost": str(query.value(record.indexOf("dbhost"))),
                "dbname": str(query.value(record.indexOf("dbname"))),
                "dbport": str(query.value(record.indexOf("dbport"))),
                "dbschema": str(
                        query.value(record.indexOf("dbschema"))),
                "dbuser": str(query.value(record.indexOf("dbuser"))),
                "dbpwd": str(query.value(record.indexOf("dbpwd"))),
                "dbadmin": str(
                        query.value(record.indexOf("dbadmin"))),
                "dbadminpwd": str(
                        query.value(record.indexOf("dbadminpwd"))),
                "provider": str(
                        query.value(record.indexOf("provider"))),
                "epsg": str(query.value(record.indexOf("epsg"))),
                "ilimodelname": str(
                        query.value(record.indexOf("ilimodelname"))),
                "appmodule": str(
                        query.value(record.indexOf("appmodule"))),
                "appmodulename": str(
                        query.value(record.indexOf("appmodulename"))),
                "projectrootdir": str(
                        query.value(record.indexOf("projectrootdir"))),
                "projectdir": str(
                        query.value(record.indexOf("projectdir"))),
                "datadate": str(
                        query.value(record.indexOf("datadate"))),
                "importdate": str(
                        query.value(record.indexOf("importdate")))
            }

            projects.append(project)

        db.close()
        del db

    except Exception as e:
        QgsMessageLog.logMessage(
                tr("Error while reading from projects database."),
                "VeriSO",
                QgsMessageLog.CRITICAL)
        QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)
        return

    return projects


def get_projects_db(force_filepath=None):
    """
    Opens a connection to the projects db
    :return: a db object
    :rtype: QSqlDatabase
    """

    if force_filepath is not None:
        filepath = force_filepath
    else:
        settings = QSettings("CatAIS", "VeriSO")
        filepath = settings.value("options/general/projects_database", "")
    return open_sqlite_db(filepath, 'projects_db')


def get_default_db():
    """
    Opens a connection to the postgis db that is currently set in the options
    :return: a db object
    :rtype: QSqlDatabase
    """
    settings = QSettings("CatAIS", "VeriSO")
    db_host = settings.value("project/dbhost")
    db_name = settings.value("project/dbname")
    db_port = settings.value("project/dbport")
    db_admin = settings.value("project/dbadmin")
    db_admin_pwd = settings.value("project/dbadminpwd")

    return open_psql_db(db_host, db_name, db_port, db_admin, db_admin_pwd)


def open_sqlite_db(file_path, connection_name):
    """
    Opens SQLite db connection taking care that the connection exists only once
    :param file_path: the oprional path of the SQLite file
    :return: a db object
    :rtype: QSqlDatabase
    """
    try:
        if connection_name in QSqlDatabase.connectionNames():
            db = QSqlDatabase.database(connection_name)
        else:
            db = QSqlDatabase.addDatabase("QSQLITE", connection_name)
            db.setDatabaseName(file_path)

        if not db.open():
            raise Exception()
    except Exception as e:
        message = "Could not open sqlite database: %s" % connection_name
        message = tr(message)
        raise VerisoError(message, e, db.lastError().text())
    return db


def open_psql_db(db_host, db_name, db_port, db_admin, db_admin_pwd):
    """
    Open PostGIS db connection taking care that the connection exists only once
    :param db_host: the db host
    :param db_name: the db name
    :param db_port: the db port
    :param db_admin: the db administrator username
    :param db_admin_pwd: the db administrator username password
    :return: a db object
    :rtype: QSqlDatabase
    """

    connection_name = "%s@%s:%s/%s" % (db_admin, db_host, db_port, db_name)
    try:
        if connection_name in QSqlDatabase.connectionNames():
            db = QSqlDatabase.database(connection_name)
        else:
            db = QSqlDatabase.addDatabase("QPSQL", connection_name)
            db.setHostName(db_host)
            db.setPort(int(db_port))
            db.setDatabaseName(db_name)
            db.setUserName(db_admin)
            db.setPassword(db_admin_pwd)

        if not db.open():
            raise Exception()
    except Exception as e:
        message = "Could not open psql database: %s" % connection_name
        message = tr(message)
        raise VerisoError(message, e, db.lastError().text())
    return db


def get_ui_class(ui_file):
    """Get UI Python class from .ui file.
       Can be filename.ui or subdirectory/filename.ui
    :param ui_file: The file of the ui in svir.ui
    :type ui_file: str
    """
    os.path.sep.join(ui_file.split('/'))
    ui_file_path = os.path.abspath(
            os.path.join(
                    os.path.dirname(__file__),
                    os.pardir,
                    'ui',
                    ui_file
            )
    )
    return uic.loadUiType(ui_file_path)[0]


def tr(message, context='VeriSO', disambig=None, encoding=None):
    if encoding is None:
        return QCoreApplication.translate(context, message, disambig)
    return QCoreApplication.translate(context, message, disambig, encoding)
