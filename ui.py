import argparse
import json

from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtCore import pyqtSlot, QByteArray
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QShortcut

from debugwidget import DebugWidget
from brickwidget import BrickWidget

class Window(QtWidgets.QMainWindow):    
    
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi('ui/main_window.ui', self)
        self._setupUI()
        
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
        self.iCounterLabel = QtWidgets.QLabel("0")
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

    def _setDeviceUI(self, config):
        if (self._brickWidget):
            self._brickWidget.deleteLater()
            del self._brickWidget
        if (self._debugWidget):
            self._debugWidget.deleteLater()
            del self._debugWidget

        self.actionDebug.setChecked(False)

        self._debugWidget = DebugWidget(config["core"], self._breakpoints)

        self.sideWidget.layout().addWidget(self._debugWidget)
        self._debugWidget.debugRunSignal.connect(self.actionRun.trigger)
        self._debugWidget.debugStopSignal.connect(self.actionStop.trigger)
        self._debugWidget.debugPauseSignal.connect(self.actionPause.trigger)
        self._debugWidget.debugStepSignal.connect(self.actionStep.trigger)
        self.actionDebug.toggled['bool'].connect(self._debugWidget.actionDebug.toggle)

        self._brickWidget = BrickWidget(self._examine, config, self._settings)
        self._debugWidget.editStateSignal.connect(self._brickWidget.editState)
        self.actionRun.triggered.connect(self._brickWidget.run)
        self.actionPause.triggered.connect(self._brickWidget.pause)
        self.actionStop.triggered.connect(self._brickWidget.stop)
        self.actionStep.triggered.connect(self._brickWidget.step)
        self.speedGroup.triggered.connect(self._brickWidget.setSpeed)

        for addr in self._breakpoints:
            self._brickWidget.setBreakpoint(addr, True)

        self.deviceWidget.layout().addWidget(self._brickWidget)
        self._brickWidget.setFocus()
        
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

    def _openBrick(self, path):
        try:
            with open(path) as f:
                self._settings.setValue("brick/config", path)
                brick_config = json.loads(f.read())
                self._setDeviceUI(brick_config)
        except FileNotFoundError as e:
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

    def closeEvent(self, event):
        self._saveSettings()
        if (self._brickWidget):
            self._brickWidget.deleteLater()
            del self._brickWidget
        if (self._debugWidget):
            self._debugWidget.deleteLater()
            del self._debugWidget
        
        super().closeEvent(event)

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