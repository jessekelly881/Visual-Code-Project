from IPython.external.qt import QtCore, QtGui
from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
from IPython.qt.inprocess import QtInProcessKernelManager
import sys, os

class IPythonWidget(RichIPythonWidget):

    def __init__(self, parent=None, config=None):
        super(IPythonWidget, self).__init__(config=config, parent=parent)

        self.kernel_manager = QtInProcessKernelManager(config=config)
        self.kernel_manager.start_kernel()
        self.kernel_manager.kernel.gui = 'qt4'
        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()
        self.shell = self.kernel_manager.kernel.shell
        self.user_ns = self.kernel_manager.kernel.shell.user_ns


    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F2: print "f2"


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    shell = IPythonWidget()
    shell.setWindowFlags(shell.windowFlags() | QtCore.Qt.FramelessWindowHint)

    shell.show()
    app.exec_()

