import argparse
import json

from PyQt6 import uic, QtCore, QtGui, QtWidgets, QtSvgWidgets, QtSvg
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QByteArray
from PyQt6.QtWidgets import QGraphicsScene, QFileDialog

from brick import Brick

class Window(QtWidgets.QMainWindow):    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        uic.loadUi('ui/main_window.ui', self)
        self._setupUI()
        
        self._breakpoints = []
        self._settings = QtCore.QSettings('azya', 'BrickEmuPy')
        self._loadSettings()
        self._parseArgs()
        
        self._brickUI = BrickUI(
            self._examine,
            self._brick_conf,
            self._settings
        )

        self.deviceWidget.layout().addWidget(self._brickUI)       

    def _parseArgs(self):
        parser = argparse.ArgumentParser(
            description='BrickEmuPy, Brick Game family emulator.'
        )
        parser.add_argument('-brick', nargs='?', help='Brick Game Config file (*.brick)')
        parser.add_argument('-bp', nargs='+', help='Breakpoints list')
        args = parser.parse_args()
        if args.brick:
            self._brick_conf = args.brick
        if args.bp:
            for pc in args.bp:
                try:
                    self._breakpoints.append(int(pc, 0))
                except ValueError:
                    pass

    def _loadSettings(self):
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
        state = self._settings.value("window/sidesplitter_state",  QByteArray())
        if (not state.isEmpty()):
            self.sideSplitter.restoreState(state.data())
        index = self._settings.value("window/debugtab_index",  int)
        if (isinstance(index, int)):
            self.debugTabWidget.setCurrentIndex(index)

        self._brick_conf = self._settings.value("brick/config", "./assets/E23PlusMarkII96in1.brick")

    def _saveSettings(self):
        self._settings.setValue('window/window_geometry', self.saveGeometry())
        self._settings.setValue('window/mainsplitter_state', self.mainSplitter.saveState())
        self._settings.setValue('window/sidesplitter_state', self.sideSplitter.saveState())
        self._settings.setValue('window/debugtab_index', self.debugTabWidget.currentIndex())

    def _setupUI(self):       
        self.ramDataTable.resizeRowsToContents()
        self.ramDataTable.resizeColumnsToContents()

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

        self.mcyclesLabel = QtWidgets.QLabel("0")
        self.mcyclesLabel.setToolTip("Machine cycles from previous pause")
        self.statusBar().addPermanentWidget(self.mcyclesLabel)

    def closeEvent(self, event):
        self._saveSettings()
        self._brickUI.close()

        super().closeEvent(event)

    @pyqtSlot(QtWidgets.QTableWidgetItem)
    def ramTblItemChanged(self, item):
        try:
            self._brickUI.editStateSignal.emit({"RAM": {item.row() * 16 + item.column(): int(item.text(), 0)}})
        except ValueError:
            pass

    @pyqtSlot(QtWidgets.QTableWidgetItem)
    def asmTblItemChanged(self, item):
        if (item.column() == 1):
            try:
                self._brickUI.editStateSignal.emit(
                    {"MEMORY": [item.row() * 2, int(item.text(), 0)]}
                )
            except ValueError:
                pass
        else:
            self._brickUI.setBreakpoint(item.row(), item.checkState() == Qt.CheckState.Checked)

    @pyqtSlot()
    def pcEditFinished(self):
        self.pcEdit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"PC": int(self.pcEdit.text(), 0)})
        except ValueError:
            pass

    @pyqtSlot()
    def aEditFinished(self):
        self.aEdit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"ACC": int(self.aEdit.text(), 0)})
        except ValueError:
            pass

    @pyqtSlot()
    def stEditFinished(self):
        self.stEdit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"ST": int(self.stEdit.text(), 0)})
        except ValueError:
            pass

    @pyqtSlot()
    def tcEditFinished(self):
        self.tcEdit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"TC": int(self.tcEdit.text(), 0)})
        except ValueError:
            pass

    @pyqtSlot()
    def r0EditFinished(self):
        self.r0Edit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"WR": {0: int(self.r0Edit.text(), 0)}})
        except ValueError:
            pass
        
    @pyqtSlot()
    def r1EditFinished(self):
        self.r1Edit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"WR": {1: int(self.r1Edit.text(), 0)}})
        except ValueError:
            pass
    
    @pyqtSlot()
    def r2EditFinished(self):
        self.r2Edit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"WR": {2: int(self.r2Edit.text(), 0)}})
        except ValueError:
            pass

    @pyqtSlot()
    def r3EditFinished(self):
        self.r3Edit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"WR": {3: int(self.r3Edit.text(), 0)}})
        except ValueError:
            pass

    @pyqtSlot()
    def r4EditFinished(self):
        self.r4Edit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"WR": {4: int(self.r4Edit.text(), 0)}})
        except ValueError:
            pass

    @pyqtSlot()
    def paEditFinished(self):
        self.paEdit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"PA": int(self.paEdit.text(), 0)})
        except ValueError:
            pass

    @pyqtSlot()
    def ppEditFinished(self):
        self.ppEdit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"PP": int(self.ppEdit.text(), 0)})
        except ValueError:
            pass
    
    @pyqtSlot()
    def pmEditFinished(self):
        self.pmEdit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"PM": int(self.pmEdit.text(), 0)})
        except ValueError:
            pass

    @pyqtSlot()
    def psEditFinished(self):
        self.psEdit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"PS": int(self.psEdit.text(), 0)})
        except ValueError:
            pass

    @pyqtSlot()
    def cbEditFinished(self):
        self.cbEdit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"CB": int(self.cbEdit.text(), 0)})
        except ValueError:
            pass

    @pyqtSlot()
    def abEditFinished(self):
        self.abEdit.clearFocus()
        try:
            self._brickUI.editStateSignal.emit({"CB": int(self.abEdit.text(), 0)})
        except ValueError:
            pass

    @pyqtSlot(int)
    def cfCheckBoxStateChanged(self, state):
        self._brickUI.editStateSignal.emit({"CF": int(state == Qt.CheckState.Checked.value)})

    @pyqtSlot(int)
    def efCheckBoxStateChanged(self, state):
        self._brickUI.editStateSignal.emit({"EF": int(state == Qt.CheckState.Checked.value)})

    @pyqtSlot(int)
    def tfCheckBoxStateChanged(self, state):
        self._brickUI.editStateSignal.emit({"TF": int(state == Qt.CheckState.Checked.value)})

    @pyqtSlot(int)
    def eiCheckBoxStateChanged(self, state):
        self._brickUI.editStateSignal.emit({"EI": int(state == Qt.CheckState.Checked.value)})

    @pyqtSlot(int)
    def diCheckBoxStateChanged(self, state):
        self._brickUI.editStateSignal.emit({"DI": int(state == Qt.CheckState.Checked.value)})

    @pyqtSlot(int)
    def haltCheckBoxStateChanged(self, state):
        self._brickUI.editStateSignal.emit({"HALT": int(state == Qt.CheckState.Checked.value)})

    @pyqtSlot()
    def on_actionRun_triggered(self):
        self._brickUI.run()

    @pyqtSlot()
    def on_actionPause_triggered(self):
        self._brickUI.pause()

    @pyqtSlot()
    def on_actionStep_triggered(self):
        self._brickUI.step()
    
    @pyqtSlot()
    def on_actionStop_triggered(self):
        self._brickUI.stop()

    @pyqtSlot()
    def on_actionSpeedx01_triggered(self):
        self._brickUI.setSpeed(10)
    
    @pyqtSlot()
    def on_actionSpeedx02_triggered(self):
        self._brickUI.setSpeed(5)
    
    @pyqtSlot()
    def on_actionSpeedx05_triggered(self):
        self._brickUI.setSpeed(2)

    @pyqtSlot()
    def on_actionSpeedx1_triggered(self):
        self._brickUI.setSpeed(1)

    @pyqtSlot()
    def on_actionSpeedx2_triggered(self):
        self._brickUI.setSpeed(0.5)

    @pyqtSlot()
    def on_actionSpeedx5_triggered(self):
        self._brickUI.setSpeed(0.2)

    @pyqtSlot()
    def on_actionSpeedx10_triggered(self):
        self._brickUI.setSpeed(0.1)

    @pyqtSlot()
    def on_actionSpeedMax_triggered(self):
        self._brickUI.setSpeed(0)

    @pyqtSlot()
    def on_actionOpenBrick_triggered(self):
        path, _ = QFileDialog.getOpenFileName(self,
            caption = "Select Brick Game Config File",
            filter = "Brick Files (*.brick)")
        if path:
            with open(path) as f: 
                self._brickUI.setConfig(path)
                self._settings.setValue('brick/config', path)

    def _examine(self, info):
        if ("DEBUG" in info):
            self.actionDebug.setChecked(info["DEBUG"])

        if ("MC" in info):
            self.mcyclesLabel.setText("%d" % info["MC"])
        
        if ("PC" in info):
            self.asmTable.selectRow(info["PC"])
            if (not self.pcEdit.hasFocus()):
                self.pcEdit.setText("0x%0.3X" % info["PC"])

        if ("ACC" in info and not self.aEdit.hasFocus()):
            self.aEdit.setText("0x%0.1X" % info["ACC"])

        if ("TC" in info and not self.tcEdit.hasFocus()):
            self.tcEdit.setText("0x%0.2X" % info["TC"])

        if ("ST" in info and not self.stEdit.hasFocus()):
            self.stEdit.setText("0x%0.4X" % info["ST"])

        if ("PA" in info and not self.paEdit.hasFocus()):
            self.paEdit.setText("0x%0.1X" % info["PA"])

        if ("PP" in info and not self.ppEdit.hasFocus()):
            self.ppEdit.setText("0x%0.1X" % info["PP"])

        if ("PM" in info and not self.pmEdit.hasFocus()):
            self.pmEdit.setText("0x%0.1X" % info["PM"])

        if ("PS" in info and not self.psEdit.hasFocus()):
            self.psEdit.setText("0x%0.1X" % info["PS"])

        if ("WR" in info):
            if (not self.r0Edit.hasFocus()):
                self.r0Edit.setText("0x%0.1X" % info["WR"][0])
            if (not self.r1Edit.hasFocus()):
                self.r1Edit.setText("0x%0.1X" % info["WR"][1])
            if (not self.r2Edit.hasFocus()):
                self.r2Edit.setText("0x%0.1X" % info["WR"][2])
            if (not self.r3Edit.hasFocus()):
                self.r3Edit.setText("0x%0.1X" % info["WR"][3])
            if (not self.r4Edit.hasFocus()):
                self.r4Edit.setText("0x%0.1X" % info["WR"][4])

        if ("CF" in info):
            self.cfCheckBox.blockSignals(True)
            self.cfCheckBox.setChecked(info["CF"])
            self.cfCheckBox.blockSignals(False)

        if ("EF" in info):
            self.efCheckBox.blockSignals(True)
            self.efCheckBox.setChecked(info["EF"])
            self.efCheckBox.blockSignals(False)

        if ("TF" in info):
            self.tfCheckBox.blockSignals(True)
            self.tfCheckBox.setChecked(info["TF"])
            self.tfCheckBox.blockSignals(False)

        if ("EI" in info):
            self.eiCheckBox.blockSignals(True)
            self.eiCheckBox.setChecked(info["EI"])
            self.eiCheckBox.blockSignals(False)

        if ("HALT" in info):
            self.haltCheckBox.blockSignals(True)
            self.haltCheckBox.setChecked(info["HALT"])
            self.haltCheckBox.blockSignals(False)

        if ("RAM" in info):
            if self.ramDataTable.state() != QtWidgets.QAbstractItemView.State.EditingState:
                self.ramDataTable.blockSignals(True)
                for i, value in enumerate(info["RAM"]):
                    self.ramDataTable.item(i // 16, i % 16).setText("0x%0.1X" % value)
                self.ramDataTable.blockSignals(False)

        if ("LISTING" in info):
            if self.asmTable.state() != QtWidgets.QAbstractItemView.State.EditingState:
                self.asmTable.blockSignals(True)
                self.asmTable.clear()
                self.asmTable.clearContents()
                self.asmTable.setRowCount(1)
                
                itemAdr = QtWidgets.QTableWidgetItem()
                itemAdr.setForeground(QtGui.QBrush(QtGui.QColor(128, 128, 128)))
                itemAdr.setFlags(itemAdr.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                itemAdr.setCheckState(Qt.CheckState.Unchecked)

                for i, instr in enumerate(info["LISTING"]):
                    item = itemAdr.clone()
                    if (i in self._breakpoints):
                        item.setCheckState(Qt.CheckState.Checked)
                        self._brickUI.setBreakpoint(i, True)
                    item.setText('0x%0.3X:' % i)
                    self.asmTable.setItem(i, 0, item)
                    itemOpcode = QtWidgets.QTableWidgetItem(' %0.2X ' % instr[1])
                    itemOpcode.setFlags(itemOpcode.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.asmTable.setItem(i, 1, itemOpcode)
                    itemAsm = QtWidgets.QTableWidgetItem(instr[2])
                    itemAsm.setFlags(itemAsm.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.asmTable.setItem(i, 2, itemAsm)
                    if (i == 0):
                        self.asmTable.resizeRowsToContents()
                        self.asmTable.resizeColumnsToContents()
                        self.asmTable.setRowCount(len(info["LISTING"]))
                self.asmTable.blockSignals(False)


class BrickUI(QtWidgets.QGraphicsView):    
    editStateSignal = pyqtSignal(dict)

    def __init__(self, examine, config_path, settings):
        super().__init__()

        self._settings = settings

        self._loadSettings()
        
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.NoRole)
        self.setFrameStyle(0)

        self._examine = examine

        self._config = self._loadConfig(config_path)
        self._draw(self._config["face_path"])        

        self._brick = Brick(self._config, self)
        
        self.editStateSignal.connect(self._brick.editState)
        
        self._brickThread = QtCore.QThread()
        self._brick.moveToThread(self._brickThread)
        self._brickThread.started.connect(self._brick.run)
        self._brickThread.finished.connect(self._brick.finish)
        self._brickThread.start(QtCore.QThread.Priority.LowestPriority)

    def showEvent(self, event):
        self._fitBrickInView()
        return super().showEvent(event)
        
    def _loadSettings(self):
        self._scene_rect = self._settings.value('brick/scene_rect')

    def _saveSettings(self):   
        self._settings.setValue('brick/scene_rect', self.mapToScene(self.viewport().rect()).boundingRect())

    def _loadConfig(self, path):
        with open(path) as f:
            return json.loads(f.read())

    def setConfig(self, path):
        self._config = self._loadConfig(path)
        self._brick.setConfig(self._config)
        self._draw(self._config["face_path"])
        self._scene_rect = None
        self._fitBrickInView()

    def step(self):
        self._brick.debugStep()

    def pause(self):
        self._brick.debugPause()
    
    def stop(self):
        self._brick.debugStop()
    
    def run(self):
        self._brick.debugRun()

    def setBreakpoint(self, pc, checked):
        self._brick.debugSetBreakpoint(pc, checked)

    def setSpeed(self, speed):
        self._brick.setSpeed(speed)

    def closeEvent(self, event):
        self._brickThread.requestInterruption()
        self._brickThread.quit()
        self._brickThread.wait()

        self._saveSettings()

        return super().closeEvent(event)
    
    def _fitBrickInView(self):
        if self._scene_rect is not None:
            self.fitInView(self._scene_rect, Qt.AspectRatioMode.KeepAspectRatio)
        else:
            self.fitInView(self.scene().sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        self._fitBrickInView()
        return super().resizeEvent(event)

    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            for button in self._config["buttons"].values():
                if (event.key() in button["hot_keys"]):
                    self._brick.btnPressed(button["port"], button["pin_mask"])

    def keyReleaseEvent(self, event):            
        if not event.isAutoRepeat():
            for button in self._config["buttons"].values():
                if (event.key() in button["hot_keys"]):
                    self._brick.btnReleased(button["port"], button["pin_mask"])

    def wheelEvent(self, event):
        zoomFactor = 1.1
        if (event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier):
            zoomFactor = 1.01
        if event.angleDelta().y() < 0:
            zoomFactor = 1 / zoomFactor
        self.scale(zoomFactor, zoomFactor)
        self.centerOn(self.scene().sceneRect().center().x(), self.mapToScene(self.viewport().rect().center()).y())
        self._scene_rect = self.mapToScene(self.viewport().rect()).boundingRect()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self._scene_rect = self.mapToScene(self.viewport().rect()).boundingRect()
        return super().mouseMoveEvent(event)

    def _draw(self, faceSVG):
        self.setScene(QGraphicsScene())
        self.scene().setItemIndexMethod(QGraphicsScene.ItemIndexMethod.NoIndex)
        faceRenderer = QtSvg.QSvgRenderer(faceSVG)
        
        body = QtSvgWidgets.QGraphicsSvgItem()
        body.setSharedRenderer(faceRenderer)
        body.setElementId("body")
        self.scene().addItem(body)  

        self._segments = []
        for ramBit in range(4):
            for ramNibble in range(256):
                nextId = str(ramNibble) + "_" + str(ramBit)
                if (faceRenderer.elementExists(nextId)):
                    segment = QtSvgWidgets.QGraphicsSvgItem()
                    segment.setSharedRenderer(faceRenderer)
                    segment.setElementId(nextId)
                    segment.setPos(faceRenderer.boundsOnElement(nextId).topLeft())
                    self.scene().addItem(segment)
                    self._segments.append((ramNibble, ramBit, segment))
     
        for name, value in self._config["buttons"].items():
            if (faceRenderer.elementExists(name)):
                btn = QtWidgets.QPushButton(objectName = "brickButton")
                btn.setGeometry(faceRenderer.boundsOnElement(name).toRect())
                shortcuts = "Shortcuts: "
                for shortcut in value["hot_keys"]:
                    shortcuts += Qt.Key(shortcut).name + ", "
                btn.setToolTip(shortcuts[:-2])
                btn.pressed.connect(lambda port = value["port"], pinMask = value["pin_mask"]: 
                                    self._brick.btnPressed(port, pinMask))
                btn.released.connect(lambda port = value["port"], pinMask = value["pin_mask"]: 
                                    self._brick.btnReleased(port, pinMask))
                self.scene().addWidget(btn)

    @pyqtSlot(tuple)
    def render(self, RAM):
        for nibble, bit, segment in self._segments:
            segment.setOpacity(0.40 * ((RAM[nibble] >> bit) & 0x1) + 0.60 * segment.opacity())

    @pyqtSlot(dict)
    def examineSlot(self, info):
        if (self._examine != None):
            self._examine(info)