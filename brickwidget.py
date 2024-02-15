from PyQt6 import QtCore, QtGui, QtWidgets, QtSvgWidgets, QtSvg
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import QGraphicsScene

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

        self._examine = examine

        self._draw(self._config["face_path"])        

        self._brick = Brick(self._config, self)
        
        self._brickThread = QtCore.QThread()
        self._brick.moveToThread(self._brickThread)
        self._brickThread.started.connect(self._brick.run)
        self._brickThread.finished.connect(self._brick.finish)
        self._brickThread.finished.connect(self._brick.deleteLater)
        self._brickThread.finished.connect(self._brickThread.deleteLater)
        self._brickThread.start(QtCore.QThread.Priority.LowestPriority)

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

    def step(self):
        self._brick.debugStep()

    def pause(self):
        self._brick.debugPause()
    
    def stop(self):
        self._brick.debugStop()
    
    def run(self):
        self._brick.debugRun()

    def setBreakpoint(self, pc, checked):
        self._brick.setBreakpoint(pc, checked)

    def setSpeed(self, speed):
        self._brick.setSpeed(speed)

    def closeEvent(self, event):
        self._brickThread.requestInterruption()
        self._brickThread.quit()
        self._brickThread.wait(1000)
        self._brickThread.terminate()
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
                btn.pressed.connect(lambda port = value["port"], pin = value["pin"], level = value["level"]: 
                                    self._brick.btnPressed(port, pin, level))
                btn.released.connect(lambda port = value["port"], pin = value["pin"], level = value["level"]: 
                                    self._brick.btnReleased(port, pin))
                self.scene().addWidget(btn)

    @pyqtSlot(tuple)
    def render(self, RAM):
        for nibble, bit, segment in self._segments:
            if (len(RAM) > nibble):
                segment.setOpacity(0.40 * ((RAM[nibble] >> bit) & 0x1) + 0.60 * segment.opacity())

    @pyqtSlot(dict)
    def examineSlot(self, info):
        if (self._examine != None):
            self._examine(info)