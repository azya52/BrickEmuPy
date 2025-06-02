from PyQt6 import QtCore, QtGui, QtWidgets, QtSvgWidgets, QtSvg
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import QGraphicsScene, QMessageBox
from functools import partial

from brick import Brick

class BrickWidget(QtWidgets.QGraphicsView):
    def __init__(self, examine, config, settings):
        super().__init__()

        self._config = config
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

        self._brick = Brick(config)
        self._brick.uiDisplayUpdateSignal.connect(self.render)
        self._brick.examineSignal.connect(examine)
        self._brick.errorSignal.connect(self.error)
        
        self._draw(config["face_path"])

        self._brickThread = QtCore.QThread()
        self._brick.moveToThread(self._brickThread)
        self._brickThread.started.connect(self._brick.run)
        self._brickThread.finished.connect(self._brick.deleteLater)
        self._brickThread.finished.connect(self._brickThread.deleteLater)
        self._brickThread.start(QtCore.QThread.Priority.LowestPriority)

    def __del__(self):
        self._brick.uiDisplayUpdateSignal.disconnect()
        self._brick.examineSignal.disconnect()
        self._brick.errorSignal.disconnect()
        try:
            self._brickThread.requestInterruption()
            self._brickThread.quit()
            self._brickThread.wait(1000)
            self._brickThread.terminate()
            self._brickThread.wait()
            del self._brick
        except:
            pass

        self._saveSettings()

    @pyqtSlot(dict)
    def editState(self, state):
        self._brick.editState(state)

    def showEvent(self, event):
        self._fitBrickInView()
        return super().showEvent(event)
        
    def _loadSettings(self):
        self._scene_rect = self._settings.value("brick/" + self._config["id"] + "/scene_rect")

    def _saveSettings(self):
        self._settings.setValue("brick/" + self._config["id"] + "/scene_rect", self.mapToScene(self.viewport().rect()).boundingRect())

    def setConfig(self, config):
        self._config = config
        self._brick.setConfig(self._config)
        self._draw(self._config["face_path"])
        self._scene_rect = None
        self._fitBrickInView()

    @pyqtSlot()
    def step(self):
        self._brick.debugStep()

    @pyqtSlot()
    def pause(self):
        self._brick.debugPause()
    
    @pyqtSlot()
    def stop(self):
        self._brick.debugStop()
    
    @pyqtSlot()
    def run(self):
        self._brick.debugRun()

    def setBreakpoint(self, pc, checked):
        self._brick.setBreakpoint(pc, checked)

    @pyqtSlot()
    def setSpeed(self):
        self._brick.setSpeed(self.sender().checkedAction().property("factor"))
    
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
                    self._brick.btnPressed(button["port"], button["pin"], button["level"])

    def keyReleaseEvent(self, event):            
        if not event.isAutoRepeat():
            for button in self._config["buttons"].values():
                if (event.key() in button["hot_keys"]):
                    self._brick.btnReleased(button["port"], button["pin"])

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
        if (not faceRenderer.isValid()):
            QMessageBox(parent=self, text="Error loading SVG file").exec()
        
        body = QtSvgWidgets.QGraphicsSvgItem()
        body.setSharedRenderer(faceRenderer)
        body.setElementId("body")
        self.scene().addItem(body)

        overlay = QtSvgWidgets.QGraphicsSvgItem()
        overlay.setSharedRenderer(faceRenderer)
        overlay.setElementId("overlay")

        self._segments = []
        for ramBit in range(8):
            for ramNibble in range(256):
                nextId = str(ramNibble) + "_" + str(ramBit)
                if (faceRenderer.elementExists(nextId)):
                    segment = QtSvgWidgets.QGraphicsSvgItem()
                    segment.setSharedRenderer(faceRenderer)
                    segment.setElementId(nextId)
                    segment.setPos(faceRenderer.boundsOnElement(nextId).topLeft())
                    self.scene().addItem(segment)
                    self._segments.append((ramNibble, ramBit, segment))
        
        overlay.setPos(faceRenderer.boundsOnElement("overlay").topLeft())
        self.scene().addItem(overlay)

        for name, value in self._config["buttons"].items():
            if (faceRenderer.elementExists(name)):
                btn = QtWidgets.QPushButton(objectName = "brickButton")
                btn.setGeometry(faceRenderer.boundsOnElement(name).toRect())
                shortcuts = "Shortcuts: "
                for shortcut in value["hot_keys"]:
                    shortcuts += Qt.Key(shortcut).name + ", "
                btn.setToolTip(shortcuts[:-2])
                btn.pressed.connect(partial(self._brick.btnPressed, value["port"], value["pin"], value["level"]))
                btn.released.connect(partial(self._brick.btnReleased, value["port"], value["pin"]))
                self.scene().addWidget(btn)

    @pyqtSlot(tuple)
    def render(self, RAM):
        for nibble, bit, segment in self._segments:
            if (len(RAM) > nibble):
                segment.setOpacity(0.40 * ((RAM[nibble] >> bit) & 0x1) + 0.60 * segment.opacity())
            else:
                segment.setOpacity(0 + 0.60 * segment.opacity())

    @pyqtSlot(str)
    def error(self, error):
        QMessageBox(parent=self, text=error).exec()
        self.close()