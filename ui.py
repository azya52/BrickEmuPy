import argparse
import json

from PyQt6 import uic, QtCore, QtWidgets, QtGui
from PyQt6.QtCore import pyqtSlot, QByteArray
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QShortcut

from debug_widget import DebugWidget
from brick_widget import BrickWidget
from serial_connection import SerialConnection

class Window(QtWidgets.QMainWindow):    
    
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi('ui/main_window.ui', self)
        self._setupUI()
        self._serialConnection = None
        self._brickWidget = self._debugWidget = None
        self._breakpoints = []
        self._settings = QtCore.QSettings('azya', 'BrickEmuPy')
        args = self._parseArgs()

        if (args.brick):
            self._openBrick(args.brick)
        else:
            brick_config_path = self._settings.value("brick/config", "./assets/E23PlusMarkII96in1.brick")
            self._openBrick(brick_config_path)
        
        self._loadSettingsUI()

    def _setupUI(self):
        self.iCredits = QtWidgets.QLabel()
        self.statusBar().addPermanentWidget(self.iCredits, 1)

        self.iCounterLabel = QtWidgets.QLabel()
        self.iCounterLabel.setToolTip("Instructions from previous pause")
        self.statusBar().addPermanentWidget(self.iCounterLabel)

        QShortcut(QtCore.Qt.Key.Key_F11, self).activated.connect(self._toggle_fullscreen)
        QShortcut("Ctrl+Meta+F", self).activated.connect(self._toggle_fullscreen)
        QShortcut(QtCore.Qt.Key.Key_Escape, self).activated.connect(self._exit_fullscreen)

        for act in self.menuBar().actions():
            self.addAction(act)
            if act.menu():
                for subact in act.menu().actions():
                    self.addAction(subact)

        self.serialPortGroup.triggered.connect(self._onSerialPortSelected)

    def _setDeviceUI(self, config):
        if (self._brickWidget):
            self.actionRun.triggered.disconnect(self._brickWidget.run)
            self.actionPause.triggered.disconnect(self._brickWidget.pause)
            self.actionStop.triggered.disconnect(self._brickWidget.stop)
            self.actionStep.triggered.disconnect(self._brickWidget.step)
            self.speedGroup.triggered.disconnect(self._brickWidget.setSpeed)
            self.actionMotionBlur.toggled.disconnect()
            self.actionGhostSegments.toggled.disconnect()
            self.actionShadow.toggled.disconnect()
            self._brickWidget.close()
            self._brickWidget.deleteLater()
            self._brickWidget = None
        if (self._debugWidget):
            self.actionDebug.toggled['bool'].disconnect(self._debugWidget.actionDebug.toggle)
            self._debugWidget.close()
            self._debugWidget.deleteLater()
            self._debugWidget = None

        self.actionDebug.setChecked(False)

        self._debugWidget = DebugWidget(config["core"], self._breakpoints)

        self.sideWidget.layout().addWidget(self._debugWidget)
        self._debugWidget.debugRunSignal.connect(self.actionRun.trigger)
        self._debugWidget.debugStopSignal.connect(self.actionStop.trigger)
        self._debugWidget.debugPauseSignal.connect(self.actionPause.trigger)
        self._debugWidget.debugStepSignal.connect(self.actionStep.trigger)
        self.actionDebug.toggled['bool'].connect(self._debugWidget.actionDebug.toggle)

        self._brickWidget = BrickWidget(config, self._settings)
        self._brickWidget.examineSignal.connect(self._examine)
        self._brickWidget.connectionSignal.connect(self._serialSendData)
        self._debugWidget.editStateSignal.connect(self._brickWidget.editState)
        self.actionRun.triggered.connect(self._brickWidget.run)
        self.actionPause.triggered.connect(self._brickWidget.pause)
        self.actionStop.triggered.connect(self._brickWidget.stop)
        self.actionStep.triggered.connect(self._brickWidget.step)
        self.speedGroup.triggered.connect(self._brickWidget.setSpeed)

        self.iCredits.setText(config.get("credits", ""))

        for addr in self._breakpoints:
            self._brickWidget.setBreakpoint(addr, True)

        self.deviceWidget.layout().addWidget(self._brickWidget)
        self._brickWidget.setFocus()
        
        self._refreshSerialPorts()
        
        self.actionMotionBlur.toggled.connect(lambda checked: self._brickWidget.setDisplaySetting("motion_blur", checked))
        self.actionGhostSegments.toggled.connect(lambda checked: self._brickWidget.setDisplaySetting("ghost_segments", checked))
        self.actionShadow.toggled.connect(lambda checked: self._brickWidget.setDisplaySetting("shadow", checked))
        
    def _refreshSerialPorts(self):       
        for action in list(self.serialPortGroup.actions()):
            self.serialPortGroup.removeAction(action)
        self.menuSerialPorts.clear()

        try:
            ports = SerialConnection.get_available_ports()
        except Exception:
            ports = []

        if ports:
            current = None
            if (self._serialConnection):
                current = self._serialConnection.get_port_name()
            for device, desc in ports:
                action = QtGui.QAction(self)
                action.setCheckable(True)
                action.setText(f"{device} ({desc})")
                action.setData(device)
                self.menuSerialPorts.addAction(action)
                self.serialPortGroup.addAction(action)
                if device == current:
                    action.setChecked(True)
        else:
            placeholder = QtGui.QAction("No ports", self)
            placeholder.setEnabled(False)
            self.menuSerialPorts.addAction(placeholder)
        
        self.actionDisconnect.setEnabled(self._serialConnection != None and self._serialConnection.is_connected())

    @pyqtSlot()
    def on_actionDisconnect_triggered(self):
        if self._serialConnection:
            self._serialConnection.close_port()
        
        self._refreshSerialPorts()

    @pyqtSlot(bytes)
    def _serialSendData(self, data):
        if (self._serialConnection):
            self._serialConnection.send_data(data)

    @pyqtSlot(bytes)
    def _serialReceiveData(self, data):
        if (self._brickWidget):
            self._brickWidget.receiveData(data)

    @pyqtSlot(QtGui.QAction)
    def _onSerialPortSelected(self, action):
        if action and action.data():
            new_port = action.data()
            if (not self._serialConnection):
                self._serialConnection = SerialConnection(self)
                self._serialConnection.dataReceived.connect(self._serialReceiveData)
                self._serialConnection.error.connect(self._error)
            
            prev_port = self._serialConnection.get_port_name()
            self._serialConnection.close_port()
            if (new_port != prev_port):
                self._serialConnection.open_port(new_port)
            self._refreshSerialPorts()

    def _parseArgs(self):
        parser = argparse.ArgumentParser(
            description='BrickEmuPy, Brick Game family emulator.'
        )
        parser.add_argument('-brick', nargs='?', help='Brick Game Config file (*.brick)')
        parser.add_argument('-bp', nargs='+', help='Breakpoints list')
        args = parser.parse_args()
        if args.bp:
            for pc in args.bp:
                try:
                    self._breakpoints.append(int(pc, 0))
                except ValueError:
                    pass
        return args

    def _loadSettingsUI(self):
        geometry = self._settings.value("window/window_geometry",  QByteArray())
        if (not geometry.isEmpty()):
            self.restoreGeometry(geometry.data())
        else:
            geometry = self.screen().availableGeometry()
            self.setGeometry(QtCore.QRect(geometry.bottomRight() / 5, 3 * geometry.size() / 5))
        
        state = self._settings.value("window/mainsplitter_state",  QByteArray())
        if (not state.isEmpty()):
            self.mainSplitter.restoreState(state.data())
        else:
            self.mainSplitter.setSizes(
                [int(self.geometry().width() * 0.6), int(self.geometry().width() * 0.4)]
            )

        state = self._settings.value("display", {})
        self.actionMotionBlur.setChecked(state.get("motion_blur", True))
        self.actionGhostSegments.setChecked(state.get("ghost_segments", True))
        self.actionShadow.setChecked(state.get("shadow", True))

    def _openBrick(self, path):
        try:
            with open(path) as f:
                brick_config = json.loads(f.read())
                self._setDeviceUI(brick_config)
                self._settings.setValue("brick/config", path)
        except Exception as e:
            QMessageBox(parent=self, text=str(e)).exec()

    @pyqtSlot()
    def on_actionOpenBrick_triggered(self):
        path, _ = QFileDialog.getOpenFileName(self,
            caption = "Select Brick Game Config File",
            filter = "Brick Files (*.brick)")
        if path:
            self._openBrick(path)

    def _saveSettings(self):
        self._settings.setValue('window/window_geometry', self.saveGeometry())
        self._settings.setValue('window/mainsplitter_state', self.mainSplitter.saveState())

        self._settings.setValue("display", {
            "motion_blur": self.actionMotionBlur.isChecked(),
            "ghost_segments": self.actionGhostSegments.isChecked(),
            "shadow": self.actionShadow.isChecked(),
        })

    def closeEvent(self, event):
        self._saveSettings()
        if self._serialConnection:
            self._serialConnection.close_port()
        if (self._brickWidget):
            self._brickWidget.close()
            self._brickWidget.deleteLater()
            self._brickWidget = None
        if (self._debugWidget):
            self._debugWidget.close()
            self._debugWidget.deleteLater()
            self._debugWidget = None
        super().closeEvent(event)

    @pyqtSlot(dict)
    def _examine(self, info):
        if (self._debugWidget):
            self._debugWidget.examine(info)
        if ("DEBUG" in info):
            self.actionDebug.setChecked(info["DEBUG"])
        if ("ICTR" in info):
            self.iCounterLabel.setText("%d" % info["ICTR"])

    def _toggle_fullscreen(self):  
        if self.isFullScreen():
            self._exit_fullscreen()
        else:
            self.showFullScreen()
            self.menuBar().hide()
            self.statusBar().hide()

    def _exit_fullscreen(self):
        self.showNormal()
        self.menuBar().show()
        self.statusBar().show()

    @pyqtSlot(str)
    def _error(self, error):
        QMessageBox(parent=self, text=error).exec()