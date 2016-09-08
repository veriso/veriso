# coding=utf-8
import os
from builtins import next
from collections import OrderedDict
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtSql import QSqlQuery
from qgis.core import QgsMessageLog

from veriso.base.utils.utils import tr, dynamic_import
from veriso.base.utils.exceptions import VerisoError
from veriso.base.utils.utils import (get_modules_dir, yaml_load_file,
                                     get_subdirs, get_default_db)


def get_layers_from_topic(topic):
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
        my_layer = {
            "type": "postgres", "featuretype": table,
            "key": topic["primary_keys"][i],
            "geom": topic["geometry_columns"][i], "group": topic["topic"],
            "title": topic["class_names"][i]
        }
        i += 1
        # If there is more than one geometry column in the table
        # the name of the geometry columns is written in brackets
        # following the name of the table.
        if dd[table] > 1:
            my_layer["title"] = my_layer["title"] + " (" + my_layer[
                "geom"] + ")"

        layers.append(my_layer)

    return layers


def get_topics_tables(module_name):
    """Requests the topics and tables from the topic_tables database table.
    This table was created in the postprocessing step.

    Returns:
      False: If something went wrong when trying to get the list from the
      database. Otherwise a python dictionary.
    """
    try:
        db = get_default_db()

        # I think libpg cannot deal with arrays from postgresql. So we
        # return a comma sperated string.
        # Everything is ordered alphanumerical. Not sure if we would know
        #  enough to sort by interlis model ordering?!
        db_schema = QSettings("CatAIS", "VeriSO").value("project/dbschema")

        sql = ("SELECT topic,"
               "array_to_string(array_agg(sql_name ORDER BY sql_name),',') "
               "as tables, "
               "array_to_string(array_agg(coalesce(f_geometry_column,'') "
               "ORDER BY sql_name),',') as geometry_columns, "
               "array_to_string(array_agg(class_name ORDER BY sql_name), "
               "',') as class_names, "
               "array_to_string(array_agg(primary_key ORDER BY sql_name),"
               "',') as primary_keys "
               "FROM " + db_schema + ".t_topics_tables GROUP BY topic "
                                     "ORDER BY topic;")

        query = db.exec_(sql)

        if not query.isActive():
            message = "Error while reading from database."
            QgsMessageLog.logMessage(tr(message), module_name,
                                     QgsMessageLog.CRITICAL)
            QgsMessageLog.logMessage(
                    str(QSqlQuery.lastError(query).text()),
                    module_name,
                    QgsMessageLog.CRITICAL)
            return

        topics = []
        record = query.record()
        while next(query):
            topic = {"topic": str(query.value(record.indexOf("topic")))}

            tables = []
            for table in str(query.value(record.indexOf("tables"))).split(
                    ","):
                tables.append(table)
            topic["tables"] = tables

            geometry_columns = []
            for geometry_column in str(
                    query.value(record.indexOf("geometry_columns"))).split(
                    ","):
                geometry_columns.append(geometry_column)
            topic["geometry_columns"] = geometry_columns

            class_names = []
            for class_name in str(
                    query.value(record.indexOf("class_names"))).split(","):
                class_names.append(class_name)
            topic["class_names"] = class_names

            primary_keys = []
            for primary_key in str(
                    query.value(record.indexOf("primary_keys"))).split(","):
                primary_keys.append(primary_key)
            topic["primary_keys"] = primary_keys

            topics.append(topic)

        db.close()
        del db

        return topics

    except Exception as e:
        message = "Something went wrong catching the topics tables list " \
                  "from the database."
        QgsMessageLog.logMessage(tr(message), module_name,
                                 QgsMessageLog.CRITICAL)
        QgsMessageLog.logMessage(str(e), module_name,
                                 QgsMessageLog.CRITICAL)
        return


def get_baselayers(module_name):
    """Reads all baselayer definitions from a yaml file.

    Returns
      A list of dictionaries with all baselayer definitions. Otherwise
      False.
    """
    filename = os.path.join(
            get_modules_dir(),
            module_name,
            "baselayer",
            "baselayer.yml")
    try:
        baselayers = yaml_load_file(filename)
        return baselayers
    except Exception as e:
        QgsMessageLog.logMessage(str(e), module_name,
                                 QgsMessageLog.CRITICAL)
        return


def get_check_topics(module_name):
    """Get all check topics (aka groups).

    Different languages are support. See the yaml file how to deal with it.

    Returns:
      A ordered dictionary with the topic name and corresponding check
      files (python). False if something went wrong.
    """

    topics_dir = os.path.join(
            get_modules_dir(), module_name, 'checks')

    checks = []
    for topic_dir in get_subdirs(topics_dir):
        topic_file = os.path.join(topics_dir, topic_dir, 'topic.yml')
        if os.path.isfile(topic_file):
            try:
                topic = yaml_load_file(topic_file)
                topic['topic_dir'] = topic_dir
                checks.append(topic)
            except VerisoError:
                raise
    try:
        locale = QSettings().value('locale/userLocale')[0:2]
    except TypeError:
        locale = 'en'
    try:
        topics = OrderedDict()
        for check in checks:
            topic = check["topic"]
            topic_dir = check["topic_dir"]

            # Check, if yaml file is multilingual.
            try:
                if topic in topics:
                    continue
                topics[topic] = check
                # TODO control this whe using checks_from_files
                # yaml is *not* multilingual.
            except:
                # yaml is multilingual.
                # If the language set in QGIS is not available in the
                # yaml file, the first language will be chosen

                # dinamically get the checks based on the available files
                checks_from_files = get_checks_from_files(
                        module_name, topic_dir)
                try:
                    my_topic = topic[locale]
                    my_check = OrderedDict()
                    my_check["topic"] = my_topic
                    # my_check["checks"] = check["checks"]
                    my_check["checks"] = checks_from_files
                    my_check["topic_dir"] = topic_dir
                    topics[my_topic] = my_check
                    # language found

                except:
                    # language *not* found
                    my_check = OrderedDict()
                    my_check["topic"] = list(topic.values())[0]
                    # my_check["checks"] = check["checks"]
                    my_check["checks"] = checks_from_files
                    my_check["topic_dir"] = topic_dir
                    topics[my_check["topic"]] = my_check
        return topics
    except Exception as e:
        raise VerisoError(str(e), e, tag=module_name)


def get_checks_from_files(module_name, topic_dir, modules_dir=None):
    """

    :param module_name:
    :param topic_dir:
    :param modules_dir:
    :return:
    """

    if modules_dir is None:
        modules_dir = get_modules_dir()
    path = os.path.join(modules_dir, module_name, 'checks', topic_dir)
    package = 'veriso.modules.%s.checks.%s' % (module_name, topic_dir)
    checks = []

    files = os.listdir(path)
    # alpha-numeric sorting to assure the same order in the menus
    # see http://stackoverflow.com/a/2669523/1193450
    files = sorted(files, key=lambda item: (
        int(item.partition(' ')[0]) if item[0].isdigit() else float('inf'),
        item))
    for f in files:
        check = {}
        if f.endswith(".py") and f != '__init__.py':
            filename = f[:-3]
            module = '%s.%s' % (package, filename)
            try:
                module = dynamic_import(module)
                check['id'] = filename
                check['file'] = filename
                check['shortcut'] = module.ComplexCheck.get_shortcut()
                check['name'] = module.ComplexCheck.get_name()
                checks.append(check)
            except:
                continue
    return checks
