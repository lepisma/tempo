# Main script

from PyQt4 import QtGui, QtCore, QtWebKit

class RightClickMenu(QtGui.QMenu):
    """
    The right click menu for tray icon
    """

    def __init__(self, parent):
        QtGui.QMenu.__init__(self, "tempo")
        
        # Show dash
        dash_action = QtGui.QAction("Dashboard", self)
        dash_action.triggered.connect(parent.show_dash)
        self.addAction(dash_action)

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

        self.activated.connect(self.click_trap)

    def message(self):
        self.showMessage("tempo", "tempo is still running")

    def click_trap(self, value):
        # Trigger for single click on tray icon
        if value == self.Trigger:
            self.show_dash()

    def show_dash(self):
        if self.parent().isMinimized():
            self.parent().setWindowState(QtCore.Qt.WindowActive)
        self.parent().show()

class MainWindow(QtGui.QWidget):
    """
    Main window
    """

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.tray_icon = SystemTrayIcon(self)
        self.tray_icon.show()

        self.init_ui()

    def init_ui(self):
        self.resize(200, 400)
        self.setWindowTitle("tempo")
        self.setWindowIcon(QtGui.QIcon("./icons/1.png"))
        self.layout = QtGui.QGridLayout(self)
        self.layout.setMargin(0)
        self.layout.setSpacing(0)

        self.view = QtWebKit.QWebView(self)
        view_url = "./view/dash.html"
        self.view.setUrl(QtCore.QUrl(view_url))

        self.layout.addWidget(self.view, 0, 0, 1, 1)
        self.show()

    def closeEvent(self, event):
        self.hide()
        QtCore.QTimer.singleShot(100, self.tray_icon.message)
        event.ignore()

def main():
    # Initialize Qt Application
    app = QtGui.QApplication([])

    parent_widget = MainWindow()
    app.exec_()

if __name__ == "__main__":
    main()
