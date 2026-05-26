from PyQt6 import QtCore, QtGui, QtWidgets, QtSvgWidgets, QtSvg
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import QGraphicsScene, QMessageBox
from functools import partial

from brick import Brick

DEFAULT_MOTION_BLUR = 0.6
DEFAULT_GHOST_SEGMENTS = 0
DEFAULT_SHADOW = 5

class BrickWidget(QtWidgets.QGraphicsView):
    def __init__(self, examine, config, settings):
        super().__init__()

        self._config = config
        self._settings = settings

        self._displaySettings = {}
        
        self._motionBlur = DEFAULT_MOTION_BLUR
        self._ghostSegments = DEFAULT_GHOST_SEGMENTS
        self._shadow = DEFAULT_SHADOW

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
        self._brick.start()

    def __del__(self):
        self._brick.close()
        self._saveSettings()
        super().close()

    def showEvent(self, event):
        self._fitBrickInView()
        return super().showEvent(event)
        
    def _loadSettings(self):
        self._scene_rect = self._settings.value("brick/" + self._config["id"] + "/scene_rect")
        self._displaySettings = self._settings.value("display", None)

    def _saveSettings(self):
        self._settings.setValue("brick/" + self._config["id"] + "/scene_rect", self.mapToScene(self.viewport().rect()).boundingRect())

    @pyqtSlot(dict)
    def editState(self, state):
        self._brick.editState(state)

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
            for name, value in self._config["buttons"].items():
                if (event.key() in value["hot_keys"]):
                    self._brick.btnPressed(name)

    def keyReleaseEvent(self, event):            
        if not event.isAutoRepeat():
            for name, value in self._config["buttons"].items():
                if (event.key() in value["hot_keys"]):
                    self._brick.btnReleased(name)

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
            for ramByte in range(256):
                nextId = str(ramByte) + "_" + str(ramBit)
                if (faceRenderer.elementExists(nextId)):
                    group = QtWidgets.QGraphicsItemGroup()
                    segment = QtSvgWidgets.QGraphicsSvgItem()
                    segment.setSharedRenderer(faceRenderer)
                    segment.setElementId(nextId)
                    segment.setPos(faceRenderer.boundsOnElement(nextId).topLeft())
                    group.addToGroup(segment)
                    
                    segment_shadow = QtSvgWidgets.QGraphicsSvgItem()
                    segment_shadow.setSharedRenderer(faceRenderer)
                    segment_shadow.setElementId(nextId)
                    segment_shadow.setVisible(False)
                    segment_shadow.setOpacity(0.1)
                    group.addToGroup(segment_shadow)

                    self.scene().addItem(group)
                    self._segments.append([ramByte, ramBit, group, -1])
        
        self._updateDisplaySettings()

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
                btn.pressed.connect(partial(self._brick.btnPressed, name))
                btn.released.connect(partial(self._brick.btnReleased, name))
                self.scene().addWidget(btn)

    @pyqtSlot(tuple)
    def render(self, RAM):
        k = 1 - self._motionBlur
        ghostSegments = self._ghostSegments
        ramSize = len(RAM)
        for seg in self._segments:
            nibble, bit, segment, opacity = seg
            if nibble < ramSize:
                target = ((RAM[nibble] >> bit) & 0x1) + ghostSegments
                if (opacity != target):
                    opacity += k * (target - opacity)
                    if abs(opacity - target) < 1e-3:
                        opacity = target
                    segment.setOpacity(opacity)
                    seg[-1] = opacity
            else:
                seg[-1] = 0
                segment.setOpacity(ghostSegments)

    @pyqtSlot(str)
    def error(self, error):
        QMessageBox(parent=self, text=error).exec()
        self.close()
    
    def setDisplaySetting(self, key, value):
        self._displaySettings[key] = value
        self._updateDisplaySettings()
    
    def _updateDisplaySettings(self):
        if (self._displaySettings):
            if (self._displaySettings.get("motion_blur", False)):
                self._motionBlur = self._config.get("display", {}).get("motion_blur", DEFAULT_MOTION_BLUR)
            else:
                self._motionBlur = 0
            if (self._displaySettings.get("ghost_segments", False)):
                self._ghostSegments = self._config.get("display", {}).get("ghost_segments", DEFAULT_GHOST_SEGMENTS)
            else:
                self._ghostSegments = 0
            if (self._displaySettings.get("shadow", False)):
                self._shadow = self._config.get("display", {}).get("shadow", DEFAULT_SHADOW)
            else:
                self._shadow = 0

        for seg in self._segments:
            segmentItem = seg[2].childItems()[0]
            shadowItem = seg[2].childItems()[1]
            if (self._shadow):
                shadowItem.setPos(segmentItem.sceneBoundingRect().topLeft() + QtCore.QPointF(self._shadow, self._shadow))
                shadowItem.setVisible(True)
            else:
                shadowItem.setVisible(False)