import argparse
import json

from PyQt6 import uic, QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot, QByteArray
from PyQt6.QtWidgets import QFileDialog

from debugwidget import DebugWidget
from brickwidget import BrickWidget

class Window(QtWidgets.QMainWindow):    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        uic.loadUi('ui/main_window.ui', self)
        self._setupUI()
        
        self._breakpoints = []
        self._settings = QtCore.QSettings('azya', 'BrickEmuPy')
        self._loadSettings()
        self._parseArgs()

        self._brickWidget = self._debugWidget = None
        self._setDeviceUI()

    def _setupUI(self):       
        groupTool = QtGui.QActionGroup(self)
        groupTool.addAction(self.actionSpeedx01)
        groupTool.addAction(self.actionSpeedx02)
        groupTool.addAction(self.actionSpeedx05)
        groupTool.addAction(self.actionSpeedx1)
        groupTool.addAction(self.actionSpeedx2)
        groupTool.addAction(self.actionSpeedx5)
        groupTool.addAction(self.actionSpeedx10)
        groupTool.addAction(self.actionSpeedMax)
        groupTool.setExclusive(True)

        self.iCounterLabel = QtWidgets.QLabel("0")
        self.iCounterLabel.setToolTip("Instructions from previous pause")
        self.statusBar().addPermanentWidget(self.iCounterLabel)

    def _setDeviceUI(self):
        if (self._brickWidget):
            #self._brickWidget.deleteLater()
            self._brickWidget.close()
            self._brickWidget.deleteLater()
        if (self._debugWidget != None):
            #self._debugWidget.deleteLater()
            self._debugWidget.close()
            self._debugWidget.deleteLater()

        self._debugWidget = DebugWidget(self._brick_config["core"], self._breakpoints)
        self.sideWidget.layout().addWidget(self._debugWidget)

        self._brickWidget = BrickWidget(self._examine, self._brick_config, self._settings)

        for addr in self._breakpoints:
            self._brickWidget.setBreakpoint(addr, True)

        self._debugWidget.editStateSignal.connect(self._brickWidget.editState)
        self._debugWidget.debugRunSignal.connect(self.actionRun.trigger)
        self._debugWidget.debugStopSignal.connect(self.actionStop.trigger)
        self._debugWidget.debugPauseSignal.connect(self.actionPause.trigger)
        self._debugWidget.debugStepSignal.connect(self.actionStep.trigger)
        self.actionDebug.setChecked(False)
        self.actionDebug.toggled['bool'].connect(self._debugWidget.actionDebug.toggle)

        self.deviceWidget.layout().addWidget(self._brickWidget)
        self._brickWidget.setFocus()
        self._loadSettingsUI()
        
    def _parseArgs(self):
        parser = argparse.ArgumentParser(
            description='BrickEmuPy, Brick Game family emulator.'
        )
        parser.add_argument('-brick', nargs='?', help='Brick Game Config file (*.brick)')
        parser.add_argument('-bp', nargs='+', help='Breakpoints list')
        args = parser.parse_args()
        if args.brick:
            with open(args.brick) as f:
                self._brick_config = json.loads(f.read())
        if args.bp:
            for pc in args.bp:
                try:
                    self._breakpoints.append(int(pc, 0))
                except ValueError:
                    pass

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

    def _loadSettings(self):
        brick_config_path = self._settings.value("brick/config", "./assets/E23PlusMarkII96in1.brick")
        with open(brick_config_path) as f:
            self._brick_config = json.loads(f.read())

    def _saveSettings(self):
        self._settings.setValue('window/window_geometry', self.saveGeometry())
        self._settings.setValue('window/mainsplitter_state', self.mainSplitter.saveState())

    def closeEvent(self, event):
        self._saveSettings()
        self._debugWidget.close()
        self._brickWidget.close()
        
        super().closeEvent(event)

    @pyqtSlot()
    def on_actionRun_triggered(self):
        self._brickWidget.run()

    @pyqtSlot()
    def on_actionPause_triggered(self):
        self._brickWidget.pause()

    @pyqtSlot()
    def on_actionStep_triggered(self):
        self._brickWidget.step()
    
    @pyqtSlot()
    def on_actionStop_triggered(self):
        self._brickWidget.stop()

    @pyqtSlot()
    def on_actionSpeedx01_triggered(self):
        self._brickWidget.setSpeed(10)
    
    @pyqtSlot()
    def on_actionSpeedx02_triggered(self):
        self._brickWidget.setSpeed(5)
    
    @pyqtSlot()
    def on_actionSpeedx05_triggered(self):
        self._brickWidget.setSpeed(2)

    @pyqtSlot()
    def on_actionSpeedx1_triggered(self):
        self._brickWidget.setSpeed(1)

    @pyqtSlot()
    def on_actionSpeedx2_triggered(self):
        self._brickWidget.setSpeed(0.5)

    @pyqtSlot()
    def on_actionSpeedx5_triggered(self):
        self._brickWidget.setSpeed(0.2)

    @pyqtSlot()
    def on_actionSpeedx10_triggered(self):
        self._brickWidget.setSpeed(0.1)

    @pyqtSlot()
    def on_actionSpeedMax_triggered(self):
        self._brickWidget.setSpeed(0)

    @pyqtSlot()
    def on_actionOpenBrick_triggered(self):
        path, _ = QFileDialog.getOpenFileName(self,
            caption = "Select Brick Game Config File",
            filter = "Brick Files (*.brick)")
        if path:
            with open(path) as f:
                self._settings.setValue("brick/config", path)
                self._brick_config = json.loads(f.read())
                self._setDeviceUI()

    def _examine(self, info):
        self._debugWidget.examine(info)
        
        if ("DEBUG" in info):
            self.actionDebug.setChecked(info["DEBUG"])

        if ("ICTR" in info):
            self.iCounterLabel.setText("%d" % info["ICTR"])