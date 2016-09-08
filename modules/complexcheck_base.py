# coding=utf-8

from qgis.PyQt.QtCore import QObject, QSettings
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsProject

from veriso.base.utils.loadlayer import LoadLayer
from veriso.base.utils.utils import tr


class ComplexCheckBase(QObject):
    """Base class for checks

    it has to be subclassed like this:

    from collections import OrderedDict
    from veriso.modules.complexcheck_base import ComplexCheckBase

    class ComplexCheck(ComplexCheckBase):
        shortcut = 'F12'

        name = 'this name will be neglected'
        # or
        names = OrderedDict()
        names['de'] = u'Übersicht'  # use u'' for unicode strings
        names['fr'] = 'Vue d'ensemble'

        def __init__(self, iface):
            super(ComplexCheck, self).__init__(iface)
    """

    @classmethod
    def get_name(cls):
        """Returns names or name that HAS to be defined in the subclasses

        names has priority over name

        it has to be defined as a class attribute like this:
        class ComplexCheck(ComplexCheckBase):
            name = 'this name will be neglected'
            # or
            names = OrderedDict()
            names['de'] = u'Übersicht'  # use u'' for unicode strings
            names['fr'] = 'Vue d'ensemble'
        """
        try:
            return cls.names
        except AttributeError:
            pass
        try:
            return cls.name
        except:
            path = cls.__module__ + "." + cls.__name__
            message = "%s does not define whether names nor name" % path
            raise Exception(message)

    @classmethod
    def get_shortcut(cls):
        """Returns the shortcut that can to be defined in the subclasses
        if not defined no shortcut will be set.

        it can to be defined as a class attribute like this:
        class ComplexCheck(ComplexCheckBase):
            shortcut = 'F12'
        """
        try:
            return cls.shortcut
        except:
            return ''

    def __init__(self, iface):
        super(ComplexCheckBase, self).__init__()
        self.iface = iface
        self.message_bar = self.iface.messageBar()

        self.root = QgsProject.instance().layerTreeRoot()
        self.layer_loader = LoadLayer(self.iface)
        self.settings = QSettings("CatAIS", "VeriSO")

    def run(self):
        raise NotImplementedError()

    def tr(self, context, text, disambig):
        try:
            _encoding = QApplication.UnicodeUTF8
            return tr(context, text, disambig, _encoding)
        except AttributeError:
            return tr(context, text, disambig)
