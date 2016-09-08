# coding=utf-8
from qgis.core import QgsMessageLog


class VerisoError(Exception):
    def __init__(
            self, message, exception=None, long_message=None, tag="VeriSO"):
        """
        an Exception that automatically logs the error to the QgsMessageLog
        :param exception:
        :param message: a short message to be logged and used by str()
        :param long_message: a longer message only shown in the log
        """

        # Call the base class constructor with the parameters it needs
        super(VerisoError, self).__init__(message)

        self.message = message
        self.exception = exception
        self.long_message = long_message

        log_message = self.message

        if self.long_message is not None:
            log_message = "\nDetails:\n %s" % self.long_message

        if self.exception is not None:
            log_message = "\nException:\n %s" % self.long_message

        QgsMessageLog.logMessage(log_message, tag, QgsMessageLog.CRITICAL)
