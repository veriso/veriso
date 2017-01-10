from __future__ import absolute_import, print_function

from builtins import next, range, str

from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QDialogButtonBox, QDockWidget

from veriso.base.utils.utils import (get_ui_class)
from veriso.base.utils.exceptions import VerisoError

FORM_CLASS = get_ui_class('./defect_list.ui')

class DefectsListDock(QDockWidget, FORM_CLASS):
    """

    """
    projectsDatabaseHasChanged = pyqtSignal()

    def __init__(self, iface, parent=None):
        QDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        #self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)

    def refresh(self, layers):
        print(layers)
