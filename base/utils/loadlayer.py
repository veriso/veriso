# coding=utf-8
from builtins import str
from qgis.PyQt.QtCore import QObject, QSettings, Qt
from qgis.core import QgsDataSourceURI, QgsMapLayerRegistry, \
    QgsMessageLog, QgsProject, QgsRasterLayer, QgsVectorLayer

from qgis.gui import QgsMessageBar

from veriso.base.utils.utils import tr, get_absolute_path

from veriso.base.utils.exceptions import VerisoErrorWithBar


class LoadLayer(QObject):
    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.canvas = self.iface.mapCanvas()
        self.root = QgsProject.instance().layerTreeRoot()

    def load(self, layer_definition, visible=True, collapsed_legend=False,
             collapsed_group=False):

        settings = QSettings("CatAIS", "VeriSO")

        module_name = settings.value("project/appmodule")
        self.check_parameter('module name', module_name)

        epsg = settings.value("project/epsg")
        self.check_parameter('epsg', epsg)

        try:
            loaded_layer = self._load(epsg, layer_definition)

            self.set_style(module_name, loaded_layer, layer_definition)
            self.set_transparency(loaded_layer, layer_definition)

            if not loaded_layer.isValid():
                # str(layer['title']) throws some ascii out of range error...
                error = layer_definition['title'] + tr(" is not valid layer.")
                raise VerisoErrorWithBar(self.message_bar, error)
            else:
                try:
                    group = str(layer_definition["group"])
                except KeyError:
                    group = None
                # QgsMapLayerRegistry.instance().addMapLayer(loaded_layer)
                if group:  # Layer soll in eine bestimmte Gruppe hinzugefügt
                    # werden.
                    QgsMapLayerRegistry.instance().addMapLayer(loaded_layer,
                                                               False)
                    my_group_node = self.root.findGroup(group)
                    if not my_group_node:  # Gruppe noch nicht vorhanden.
                        my_group_node = self.root.addGroup(group)
                        """
                        Achtung: Das ist eher ein Workaround. Meines
                        # Erachtens hats noch einen Bug.
                        # Mit QgsMapLayerRegistry.instance().addMapLayer(
                        # loaded_layer, False)  wird
                        # ein Layer noch nicht in die Legende gehängt.
                        # Anschliessend kann man ihn
                        # mit my_layer_node = self.root.addLayer(loaded_layer)
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
                    #                    print loaded_layer.id()
                    #                    my_layer_node = self.root.findLayer(
                    # loaded_layer.id())
                    #                    print my_layer_node
                    #                    cloned_layer = my_layer_node.clone()
                    #                    print cloned_layer
                    #                    my_group_node.insertChildNode(0,
                    # cloned_layer)
                    #                    self.root.removeChildNode(
                    # my_layer_node)
                    #                    my_layer_node = self.root.findLayer(
                    # loaded_layer.id()) # Layer bekommt neuen layer_node.

                    # "Direkt(er)"
                    """
                    my_layer_node = my_group_node.insertLayer(0, loaded_layer)

                else:
                    QgsMapLayerRegistry.instance().addMapLayer(loaded_layer,
                                                               False)
                    my_layer_node = self.root.addLayer(loaded_layer)

                my_layer_node.setVisible(Qt.Unchecked)

                if visible:
                    my_layer_node.setVisible(Qt.Checked)

                if collapsed_legend:
                    my_layer_node.setExpanded(False)
                else:
                    my_layer_node.setExpanded(True)

            return loaded_layer
        except VerisoErrorWithBar:
            return
        except Exception as e:
            raise VerisoErrorWithBar(self.message_bar, str(e), e)

    @staticmethod
    def set_style(module_name, loaded_layer, layer_definition):
        try:
            style = str(layer_definition["style"])
            if style.startswith('global_qml'):
                qml_path = style
            else:
                qml_path = "modules/%s/qml/%s" % (module_name, style)

            loaded_layer.loadNamedStyle(get_absolute_path(qml_path))
        except KeyError:
            # layer["style"] doesn't exist
            pass

    def set_transparency(self, loaded_layer, layer_definition):
        try:
            transparency = layer_definition["transparency"]
            if 0 <= transparency <= 100:
                opacity = (100 - transparency) / 100.0
            else:
                message = tr('Ignoring invalid transparency value. 0 is full '
                             'opaque, 100 is full transparent. Found %s for '
                             'layer %s') % (transparency,
                                          layer_definition['title'])
                self.message_bar.pushMessage("Invalid transparency", message,
                                             QgsMessageBar.WARNING, duration=5)
                opacity = 1
            loaded_layer.renderer().setOpacity(opacity)
        except KeyError:
            # layer["transparency"] doesn't exist
            pass

    def _load(self, epsg, layer_definition):
        if layer_definition["type"] == "postgres":
            loaded_layer = self._load_pg_layer(layer_definition)

        elif layer_definition["type"] in ["wms", "wmts"]:
            loaded_layer = self._load_wms_layer(layer_definition, epsg)

        elif layer_definition["type"] in ["gdal", "ogr"]:
            loaded_layer = self._load_gdal_ogr_layer(layer_definition)

        else:
            error = tr("Data provider not yet supported: ") + str(
                    layer_definition["type"])
            raise VerisoErrorWithBar(self.message_bar, error)

        return loaded_layer

    def check_parameters(self, parameters_dict):
        for name in parameters_dict:
            self.check_parameter(name, parameters_dict[name])
            QgsMessageLog.logMessage(
                    'All parameters checks passed',
                    "VeriSO",
                    QgsMessageLog.INFO)

    def check_parameter(self, parameter_name, parameter):

        error_message = tr("Missing %s parameter. Cannot load "
                           "layer.") % parameter_name
        if not parameter:
            raise VerisoErrorWithBar(self.message_bar, error_message)

    @staticmethod
    def _load_gdal_ogr_layer(layer_definition):
        """
        Load local ogr and gdal formats

        :param layer_definition:
        :return:
        """
        title = layer_definition["title"]
        url = layer_definition["url"]
        if layer_definition["type"] == 'ogr':
            loaded_layer = QgsVectorLayer(url, title, layer_definition["type"])
        else:
            loaded_layer = QgsRasterLayer(url, title)
        return loaded_layer

    @staticmethod
    def _load_wms_layer(layer_definition, epsg):
        """
        Load a WMS / WMTS layer

        WMTS is a bit ugly since we need to know the tileMatrixSet:
        Load layer manually in QGIS once an look for the tileMatrixSet
        in the layer properties.

        :param layer_definition:
        :param epsg:
        :return:
        """

        url = layer_definition["url"]
        title = layer_definition["title"]
        layers = layer_definition["layers"]
        format = layer_definition["format"]
        try:
            tilematrixset = layer_definition["tilematrixset"]
        except KeyError:
            tilematrixset = None
        try:
            crs = layer_definition["crs"]
        except KeyError:
            crs = "EPSG:" + str(epsg)
        try:
            styles = layer_definition["styles"]
        except KeyError:
            styles = ""
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
        if layer_definition["type"] == "wms":
            uri = "IgnoreGetMapUrl=1&crs=" + crs + layer_string + \
                  style_string + "&format=" + format + "&url=" + url
        else:
            uri = "crs=" + crs + layer_string + style_string + \
                  "&format=" + format + "&tileMatrixSet=" + \
                  tilematrixset + "&url=" + url
        loaded_layer = QgsRasterLayer(uri, title, "wms", False)
        return loaded_layer

    def _load_pg_layer(self, layer_definition):
        """
        load a Postgres layer
        :param layer_definition:
        :param settings:
        :return:
        """

        settings = QSettings("CatAIS", "VeriSO")
        provider = settings.value("project/provider")
        db_host = settings.value("project/dbhost")
        db_port = settings.value("project/dbport")
        db_name = settings.value("project/dbname")
        db_schema = settings.value("project/dbschema")
        db_user = settings.value("project/dbuser")
        db_pwd = settings.value("project/dbpwd")
        db_admin = settings.value("project/dbadmin")
        db_admin_pwd = settings.value("project/dbadminpwd")

        self.check_parameters({
            'database schema': db_schema,
            'database host': db_host,
            'database name': db_name,
            'database port': db_port,
            'database user': db_user,
            'database password': db_pwd,
            'database admin': db_admin,
            'database admin password': db_admin_pwd,
            'provider': provider
        })

        featuretype = str(layer_definition["featuretype"])
        title = layer_definition["title"]
        key = str(layer_definition["key"])
        try:
            readonly = (layer_definition["readonly"])
        except KeyError:
            readonly = True
        try:
            geom = str(layer_definition["geom"])
            if geom == "":
                geom = None
        except KeyError:
            geom = None
        try:
            sql = str(layer_definition["sql"])
        except KeyError:
            sql = ""

        # Overwrite the active project settings/parameters to add
        # *any* postgres layers.
        try:
            params = layer_definition["params"]
            provider = layer_definition["type"]
            db_host = params["dbhost"]
            db_port = str(params["dbport"])
            db_name = params["dbname"]
            db_schema = params["dbschema"]
            db_user = params["dbuser"]
            db_pwd = params["dbpwd"]
            db_admin = params["dbadmin"]
            db_admin_pwd = params["dbadminpwd"]
        except:
            pass
        uri = QgsDataSourceURI()
        if readonly:
            uri.setConnection(db_host, db_port, db_name, db_user,
                              db_pwd)
        else:
            uri.setConnection(db_host, db_port, db_name, db_admin,
                              db_admin_pwd)
        uri.setDataSource(db_schema, featuretype, geom, sql, key)
        loaded_layer = QgsVectorLayer(uri.uri(), title, provider)
        return loaded_layer
