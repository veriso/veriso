# coding=utf-8
from builtins import object
from qgis.PyQt import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    # noinspection PyPep8Naming
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,
# PyAttributeOutsideInit
# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,
# PyAttributeOutsideInit
# noinspection PyAttributeOutsideInit,PyPep8Naming
class Ui_DeleteProject(object):
    # noinspection PyPep8Naming,PyPep8Naming
    def setupUi(self, DeleteProject):
        DeleteProject.setObjectName(_fromUtf8("DeleteProject"))
        DeleteProject.resize(381, 124)
        self.gridLayout = QtGui.QGridLayout(DeleteProject)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(DeleteProject)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout2 = QtGui.QGridLayout()
        self.gridLayout2.setObjectName(_fromUtf8("gridLayout2"))
        self.cBoxProject = QtGui.QComboBox(self.groupBox)
        self.cBoxProject.setEnabled(True)
        self.cBoxProject.setMinimumSize(QtCore.QSize(0, 0))
        self.cBoxProject.setObjectName(_fromUtf8("cBoxProject"))
        self.gridLayout2.addWidget(self.cBoxProject, 0, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setEnabled(True)
        self.label_7.setMinimumSize(QtCore.QSize(0, 27))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout2.addWidget(self.label_7, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DeleteProject)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
                QtGui.QDialogButtonBox.Close | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(DeleteProject)
        QtCore.QObject.connect(self.buttonBox,
                               QtCore.SIGNAL(_fromUtf8("accepted()")),
                               DeleteProject.accept)
        QtCore.QObject.connect(self.buttonBox,
                               QtCore.SIGNAL(_fromUtf8("rejected()")),
                               DeleteProject.reject)
        QtCore.QMetaObject.connectSlotsByName(DeleteProject)

    # noinspection PyPep8Naming,PyPep8Naming
    def retranslateUi(self, DeleteProject):
        DeleteProject.setWindowTitle(
                _translate("DeleteProject", "Delete project", None))
        self.groupBox.setTitle(
                _translate("DeleteProject", "Delete project", None))
        self.label_7.setText(_translate("DeleteProject", "Project: ", None))
