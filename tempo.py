# Main script

from PyQt4 import QtGui

class RightClickMenu(QtGui.QMenu):
    """
    The right click menu for tray icon
    """

    def __init__(self, parent):
        QtGui.QMenu.__init__(self, "tempo")

        # Exit tempo
        exit_action = QtGui.QAction("Exit tempo", self)
        exit_action.triggered.connect(QtGui.qApp.quit)
        self.addAction(exit_action)

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    """
    System tray icon
    """

    def __init__(self, parent = None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QtGui.QIcon("./icons/1.png"))
        self.setContextMenu(RightClickMenu(self))

def main():
    # Initialize Qt Application
    app = QtGui.QApplication([])

    parent_widget = QtGui.QWidget()
    tray_icon = SystemTrayIcon(parent_widget)
    tray_icon.show()
    app.exec_()

if __name__ == "__main__":
    main()
