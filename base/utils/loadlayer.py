# coding=utf-8
from builtins import str
from qgis.PyQt.QtCore import QDir, QObject, QSettings, Qt
from qgis.core import QgsApplication, QgsDataSourceURI, QgsMapLayerRegistry, \
    QgsMessageLog, QgsProject, QgsRasterLayer, QgsVectorLayer

from qgis.gui import QgsMessageBar

from veriso.base.utils.exceptions import VerisoError
from veriso.base.utils.utils import tr


class LoadLayer(QObject):
    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.canvas = self.iface.mapCanvas()
        self.root = QgsProject.instance().layerTreeRoot()

    def load(self, layer, visible=True, collapsed_legend=False,
             collapsed_group=False):

        settings = QSettings("CatAIS", "VeriSO")
        module_name = settings.value("project/appmodule")
        provider = settings.value("project/provider")
        db_host = settings.value("project/dbhost")
        db_port = settings.value("project/dbport")
        db_name = settings.value("project/dbname")
        db_schema = settings.value("project/dbschema")
        db_user = settings.value("project/dbuser")
        db_pwd = settings.value("project/dbpwd")
        db_admin = settings.value("project/dbadmin")
        db_admin_pwd = settings.value("project/dbadminpwd")
        epsg = settings.value("project/epsg")

        if not db_schema:
            self.message_bar.pushMessage("Error", tr(
                    "Missing database schema parameter."),
                                         QgsMessageBar.CRITICAL, duration=0)
            return

        if not db_host:
            self.message_bar.pushMessage("Error", tr(
                    "Missing database host parameter."), QgsMessageBar.CRITICAL,
                                         duration=0)
            return

        if not db_name:
            self.message_bar.pushMessage("Error", tr(
                    "Missing database name parameter."), QgsMessageBar.CRITICAL,
                                         duration=0)
            return

        if not db_port:
            self.message_bar.pushMessage("Error", tr(
                    "Missing database port parameter."), QgsMessageBar.CRITICAL,
                                         duration=0)
            return

        if not db_user:
            self.message_bar.pushMessage("Error", tr(
                    "Missing database user parameter."), QgsMessageBar.CRITICAL,
                                         duration=0)
            return

        if not db_pwd:
            self.message_bar.pushMessage("Error", tr(
                    "Missing database user password parameter."),
                                         QgsMessageBar.CRITICAL, duration=0)
            return

        if not db_admin:
            self.message_bar.pushMessage("Error", tr(
                    "Missing database administrator parameter."),
                                         QgsMessageBar.CRITICAL, duration=0)
            return

        if not db_admin_pwd:
            self.message_bar.pushMessage("Error", tr(
                    "Missing database administrator password parameter."),
                                         QgsMessageBar.CRITICAL, duration=0)
            return

        if not provider:
            self.message_bar.pushMessage("Error", tr(
                    "Missing provider parameter. Cannot load layer."),
                                         QgsMessageBar.CRITICAL, duration=0)
            return

        if not module_name:
            self.message_bar.pushMessage("Error", tr(
                    "Missing module name parameter. Cannot load layer."),
                                         QgsMessageBar.CRITICAL, duration=0)
            return

        try:
            # Postgres
            if layer["type"] == "postgres":
                featuretype = str(layer["featuretype"])
                title = layer["title"]
                key = str(layer["key"])

                try:
                    readonly = (layer["readonly"])
                except:
                    readonly = True

                try:
                    geom = str(layer["geom"])
                    if geom == "":
                        geom = None
                except:
                    geom = None

                try:
                    style = str(layer["style"])
                except:
                    style = ""

                try:
                    group = str(layer["group"])
                except:
                    group = None

                try:
                    sql = str(layer["sql"])
                except:
                    sql = ""

                # Overwrite the active project settings/parameters to add
                # *any* postgres layers.
                try:
                    params = layer["params"]
                    provider = "postgres"
                    db_host = params["dbhost"]
                    db_port = str(params["dbport"])
                    db_name = params["dbname"]
                    db_schema = params["dbschema"]
                    db_user = params["dbuser"]
                    db_pwd = params["dbpwd"]
                    db_admin = params["dbadmin"]
                    db_admin_pwd = params["dbadminpwd"]
                except Exception as e:
                    raise VerisoError(e, params)

                uri = QgsDataSourceURI()

                if readonly:
                    uri.setConnection(db_host, db_port, db_name, db_user,
                                      db_pwd)
                else:
                    uri.setConnection(db_host, db_port, db_name, db_admin,
                                      db_admin_pwd)

                uri.setDataSource(db_schema, featuretype, geom, sql, key)

                my_layer = QgsVectorLayer(uri.uri(), title, provider)

            # WMS / WMTS:
            # WMTS is a bit ugly since we need to know the tileMatrixSet:
            # Load layer manually in QGIS once an look for the tileMatrixSet
            # in the layer properties.
            elif layer["type"] == "wms" or layer["type"] == "wmts":
                url = layer["url"]
                title = layer["title"]
                layers = layer["layers"]
                format = layer["format"]

                try:
                    tilematrixset = layer["tilematrixset"]
                except:
                    tilematrixset = None

                try:
                    crs = layer["crs"]
                except:
                    crs = "EPSG:" + str(epsg)

                try:
                    styles = layer["styles"]
                except:
                    styles = ""

                try:
                    group = layer["group"]
                except:
                    group = None

                try:
                    style = layer["style"]
                except:
                    style = ""

                my_layers = layers.split(",")
                my_styles = styles.split(",")
                layer_string = ""
                style_string = ""
                for my_layer in my_layers:
                    layer_string += "&layers=" + my_layer
                    # So werden einfach leere Styles requested.
                    # Korrekterweise wäre style=qml und wmsstyle = Style der
                    # vom WMS requested wird.
                    style_string += "&styles="

                if layer["type"] == "wms":
                    uri = "IgnoreGetMapUrl=1&crs=" + crs + layer_string + \
                          style_string + "&format=" + format + "&url=" + url
                else:
                    uri = "crs=" + crs + layer_string + style_string + \
                          "&format=" + format + "&tileMatrixSet=" + \
                          tilematrixset + "&url=" + url

                my_layer = QgsRasterLayer(uri, title, "wms", False)

            else:
                self.message_bar.pushMessage(
                        "Error",
                        tr(
                                "Data provider not yet supported: ") + str(
                                layer["type"]), QgsMessageBar.CRITICAL,
                        duration=0)
                return

            if style != "":
                if style.startswith('global_qml'):
                    qml_dir = "/python/plugins/veriso/"
                else:
                    qml_dir = "/python/plugins/veriso/modules/%s/qml/" % \
                              module_name
                qml_path = QDir.convertSeparators(QDir.cleanPath(
                        QgsApplication.qgisSettingsDirPath() +
                        qml_dir + style))

                qml = QDir.convertSeparators(QDir.cleanPath(qml_path))
                my_layer.loadNamedStyle(qml)

            if not my_layer.isValid():
                # str(title) throws some ascii out of range error...
                self.message_bar.pushMessage("Error", title + tr(
                        " is not valid layer."), QgsMessageBar.CRITICAL,
                                             duration=0)
                return
            else:
                # QgsMapLayerRegistry.instance().addMapLayer(my_layer)    
                if group:  # Layer soll in eine bestimmte Gruppe hinzugefügt
                    # werden.
                    QgsMapLayerRegistry.instance().addMapLayer(my_layer, False)
                    my_group_node = self.root.findGroup(group)
                    if not my_group_node:  # Gruppe noch nicht vorhanden.
                        my_group_node = self.root.addGroup(group)
                        # Achtung: Das ist eher ein Workaround. Meines
                        # Erachtens hats noch einen Bug.
                        # Mit QgsMapLayerRegistry.instance().addMapLayer(
                        # my_layer, False)  wird
                        # ein Layer noch nicht in die Legende gehängt.
                        # Anschliessend kann man ihn
                        # mit my_layer_node = self.root.addLayer(my_layer)
                        # der Legende hinzufügen.
                        # Das führt aber dazu, dass was mit dem MapCanvas
                        # nicht mehr stimmt, dh.
                        # .setExtent() funktioniert nicht mehr richtig. Wird
                        # der Layer jedoch direkt
                        # in die Legende gehängt, funktioniert .setExtent()
                        # tadellos. Jetzt wird halt
                        # momentan der Layer direkt eingehängt und
                        # anschliessend in die gewünschte
                        # Gruppe verschoben.
                        # Kleiner (positiver) Nebeneffekt: Der Layer ist
                        # defaultmässig ausgeschaltet.
                        #
                        # NEIN: Anscheinend ist es ein Problem wenn man dann
                        # layer_node.setVisible(Qt.Checked)
                        # macht. Dann funktionierts nicht mehr. -> Wieder
                        # zurückändern auf einfachere Methode.

                        # "Umweg": Hat Probleme gemacht, falls ein Gruppe
                        # "active" war. Dann wurden der neue
                        # Layer ebenfalls (zusätzlich) ihr hinzugefügt.
                    #                    print my_layer.id()
                    #                    my_layer_node = self.root.findLayer(
                    # my_layer.id())
                    #                    print my_layer_node
                    #                    cloned_layer = my_layer_node.clone()
                    #                    print cloned_layer
                    #                    my_group_node.insertChildNode(0,
                    # cloned_layer)
                    #                    self.root.removeChildNode(
                    # my_layer_node)
                    #                    my_layer_node = self.root.findLayer(
                    # my_layer.id()) # Layer bekommt neuen layer_node.

                    # "Direkt(er)"
                    my_layer_node = my_group_node.insertLayer(0, my_layer)

                else:
                    QgsMapLayerRegistry.instance().addMapLayer(my_layer, False)
                    my_layer_node = self.root.addLayer(my_layer)

                my_layer_node.setVisible(Qt.Unchecked)

                if visible:
                    my_layer_node.setVisible(Qt.Checked)

                if collapsed_legend:
                    my_layer_node.setExpanded(False)
                else:
                    my_layer_node.setExpanded(True)

            return my_layer

        except Exception as e:
            self.message_bar.pushMessage("Error", str(e),
                                         QgsMessageBar.CRITICAL, duration=0)
            QgsMessageLog.logMessage(str(e), "VeriSO", QgsMessageLog.CRITICAL)
            return
