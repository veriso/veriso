# coding=utf-8
import importlib
import os, sys
import yaml
import subprocess
from builtins import next
from collections import OrderedDict
from qgis.PyQt.uic import loadUiType
from qgis.PyQt.QtCore import QSettings, QCoreApplication, QDir
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

from qgis.core import QgsMessageLog, QgsApplication
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
    settings = QSettings("CatAIS", "VeriSO")
    if settings.value("options/general/use_pg_projects_database", False, type=bool):
        QgsMessageLog.logMessage('Using Postgres projects database', 'VeriSO', QgsMessageLog.INFO)
        return get_projects_from_pg()
    QgsMessageLog.logMessage('Using Sqlite projects database', 'VeriSO', QgsMessageLog.INFO)
    return get_projects_from_sqlite()

def get_projects_from_pg():
    projects = []
    error_message = "Error while reading from projects database."
    settings = QSettings("CatAIS", "VeriSO")

    try:
        db = get_default_db()

        sql = "SELECT * FROM veriso_conf.project;"

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
                "dbschema": str(
                    query.value(record.indexOf("displayname"))),
                "provider": str(
                    query.value(record.indexOf("provider"))),
                "epsg": str(query.value(record.indexOf("epsg"))),
                "max_scale": int(query.value(record.indexOf("max_scale"))),
                "ilimodelname": str(
                    query.value(record.indexOf("ilimodelname"))),
                "appmodule": str(
                    query.value(record.indexOf("appmodule"))),
                "appmodulename": str(
                    query.value(record.indexOf("appmodulename"))),
                "datadate": str(
                    query.value(record.indexOf("datadate"))),
                "importdate": str(
                    query.value(record.indexOf("importdate"))),
                "dbhost": str(settings.value("options/db/host")),
                "dbname": str(settings.value("options/db/name")),
                "dbport": str(settings.value("options/db/port")),
                "dbuser": str(settings.value("options/db/user")),
                "dbpwd": str(settings.value("options/db/pwd")),
                "dbadmin": str(settings.value("options/db/admin")),
                "dbadminpwd": str(settings.value("options/db/adminpwd"))
                
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

def get_projects_from_sqlite():
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
                "max_scale": int(query.value(record.indexOf("max_scale"))),
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
    settings = QSettings("CatAIS", "VeriSO")

    if settings.value("options/general/use_pg_projects_database", False, type=bool):
        return get_default_db()

    if force_filepath is not None:
        filepath = force_filepath
    else:
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
            raise Exception("DB NOT OPEN")
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
            if not QSqlDatabase.isDriverAvailable("QPSQL"):
                raise VerisoError('Please install the PSQL Qt driver.\n')

            db = QSqlDatabase.addDatabase("QPSQL", connection_name)
            db.setHostName(db_host)
            db.setPort(int(db_port))
            db.setDatabaseName(db_name)
            db.setUserName(db_admin)
            db.setPassword(db_admin_pwd)

        if not db.open():
            raise Exception()
    except VerisoError:
        raise
    except Exception as e:
        message = "Could not open psql database: %s see log for more details"\
                  % connection_name
        message = tr(message)
        #
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
                    os.pardir,
                    'ui',
                    ui_file
            )
    )
    return loadUiType(ui_file_path)[0]


def tr(message, context='VeriSO', disambig=None, encoding=None):
    if encoding is None:
        return QCoreApplication.translate(context, message, disambig)
    return QCoreApplication.translate(context, message, disambig, encoding)


def jre_version():
    try:
        if(sys.platform == 'win32'):
            j = win_which('java.exe')
            version = subprocess.check_output(
                [j, '-version'], shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
             version = subprocess.check_output(
                 ['java', '-version'], stderr=subprocess.STDOUT)
        return version
    except:
        return None


def db_user_has_role(username, rolenames, require_all_roles=False):
    """
    This function returns true if the given username has at least one of the
    given rolenames
    :param username: the db username
    :param rolenames: a list of roles to test. passing an empty list will
    return False
    :return:
    """

    # for debugging use
    # select auth_members.roleid, auth_members.member, roles.rolname,
    # members.rolname

    operator = 'OR'
    if require_all_roles:
        operator = 'AND'

    role_sql = 'WHERE '
    for role in rolenames:
        role_sql += " roles.rolname = '%s' %s" % (role, operator)
    role_sql = role_sql[:-len(operator)]

    sql = "WITH RECURSIVE cte AS (" \
          "  SELECT oid FROM pg_roles " \
          "  WHERE rolname = '%s'" \
          "  UNION ALL" \
          "  SELECT m.roleid" \
          "  FROM   cte" \
          "  JOIN   pg_auth_members m " \
          "  ON m.member = cte.oid)" \
          "SELECT roles.rolname FROM cte c " \
          "join pg_roles roles " \
          "on c.oid = roles.oid " \
          "%s" % (username, role_sql)
    try:
        db = get_default_db()
        query = db.exec_(sql)

        return bool(query.size())
    except:
        return False


def get_absolute_path(path):
    path = "/python/plugins/veriso/%s" % path
    filename = QDir.convertSeparators(QDir.cleanPath(
            QgsApplication.qgisSettingsDirPath() + path))
    if not os.path.isfile(filename):
        filename = QDir.convertSeparators(QDir.cleanPath(
                QgsApplication.pkgDataPath() + path))

    # the plugin is not in the .qgis2 folder
    # lets try in the qgis installation folder (for central installation
    # on servers)
    if not os.path.isfile(filename):
        raise VerisoError('File not found at %s' % filename)
    return filename

# This function is like the linux which command for windows
# http://gis.stackexchange.com/questions/107204/system-variable-path-overwritten-in-qgis/156510#156510
def win_which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in win_getenv_system("PATH").split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

# This function gets a system variable
# it was necessary to use this instead of os.environ["PATH"] because QGIS overwrites the path variable
# the win32 libraries appear not to be part of the standard python install, but they are included in the 
# python version that comes with QGIS
def win_getenv_system(varname, default=''):
    import win32api
    import win32con
    v = default
    try:
        rkey = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment')
        try:
            v = str(win32api.RegQueryValueEx(rkey, varname)[0])
            v = win32api.ExpandEnvironmentStrings(v)
        except:
            pass
    finally:
        win32api.RegCloseKey(rkey)
    return v
