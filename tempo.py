# Main script

from PyQt4 import QtGui, QtCore

import time, sys
import json

from outweather import current_weather
from inweather import inside_temperature

try:
    config = json.load(open("config.json"))
except Exception:
    print("Error in reading config file.")
    sys.exit()

arduino_port = config["port"]

class RequestThread(QtCore.QThread):
    """
    Thread to interact with forecast.io and arduino and emit signal for updating the ui
    """

    def run(self):
        while True:
            # Requesting forecast
            weather = current_weather(config["API_KEY"], config["lat"], config["lng"])

            if weather == -1:
                # Error in requesting
                image_type = "na"
                temp_out = -1
            else:
                image_type = weather.icon
                temp_out = weather.temperature

            # Requesting arduino
            temp_in = inside_temperature(arduino_port)

            # Emit signal
            self.emit(QtCore.SIGNAL("update_gui(PyQt_PyObject, float, float)"), image_type, temp_out, temp_in)
            # Wait
            time.sleep(600)

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
        self.setIcon(QtGui.QIcon("./images/1.png"))
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

        # Tray icon setup
        self.tray_icon = SystemTrayIcon(self)
        self.tray_icon.show()

        # Ui initialization
        self.init_ui()

        # Thread for communicating with forecast and arduino
        self.requester = RequestThread()
        self.connect(self.requester, QtCore.SIGNAL("update_gui(PyQt_PyObject, float, float)"), self.update_gui)
        self.requester.start()

    def init_ui(self):
        # Main frame
        self.setFixedSize(400, 140)
        self.setWindowTitle("tempo")
        self.setWindowIcon(QtGui.QIcon("./images/1.png"))

        # Background
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("./images/back.png")))
        self.setPalette(palette)

        # Layout
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setMargin(20)
        self.layout.setSpacing(20)

        # Separator
        self.sep = QtGui.QFrame()
        self.sep.setFrameStyle(QtGui.QFrame.VLine)

        # Font
        font = QtGui.QFont("Segoe", 34, QtGui.QFont.Bold)
        color_ss = "QLabel {color : rgb(65, 65, 65)}"
        self.setStyleSheet(color_ss)

        # Weather icon
        self.weather_image = QtGui.QLabel(self)
        self.clear_image(self.weather_image)

        # Temperature out
        self.temp_out_image = QtGui.QLabel(self)
        self.temp_out_image.setFont(font)
        self.clear_image(self.temp_out_image)

        # Temperature in
        self.temp_in_image = QtGui.QLabel(self)
        self.temp_in_image.setFont(font)
        self.clear_image(self.temp_in_image)

        self.layout.addWidget(self.weather_image)
        self.layout.addWidget(self.temp_out_image)
        self.layout.addWidget(self.sep)
        self.layout.addWidget(self.temp_in_image)

        self.show()

    def clear_image(self, label):
        """
        Sets N/A image in label
        """

        pixmap = QtGui.QPixmap("./images/na.png")
        label.setPixmap(pixmap)

    def show_temp(self, label, value):
        """
        Shows the temperature in celsius in given label
        """
        deg = u'\N{DEGREE SIGN}'
        label.setText(str(int(value)) + deg)

    def update_gui(self, image_type, temp_out, temp_in):
        """
        Updates the weather image and the temperature
        """

        if temp_in == -1:
            # Temperature not found
            self.clear_image(self.temp_in_image)
        else:
            # Displaying
            self.show_temp(self.temp_in_image, temp_in)

        if temp_out == -1:
            # Temperature not found
            self.clear_image(self.temp_out_image)
        else:
            # Displaying
            self.show_temp(self.temp_out_image, temp_out)

        # Update weather image
        file_name = "./images/" + image_type + ".png"
        pixmap = QtGui.QPixmap(file_name)
        self.weather_image.setPixmap(pixmap)

    def closeEvent(self, event):
        """
        On close, hide and show 'still runnning' message
        """

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
