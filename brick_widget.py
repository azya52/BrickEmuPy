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

        self._motionGhosting = 0.4
        self._ghostSegments = 0
        self._shadow = 0

        shadow_shift = self.scene().itemsBoundingRect().width() * self._shadow
        
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

                    if (shadow_shift):
                        segment_shadow = QtSvgWidgets.QGraphicsSvgItem()
                        segment_shadow.setSharedRenderer(faceRenderer)
                        segment_shadow.setElementId(nextId)
                        segment_shadow.setPos(faceRenderer.boundsOnElement(nextId).topLeft().x() + shadow_shift,
                                                faceRenderer.boundsOnElement(nextId).topLeft().y() + shadow_shift * 2)
                        segment_shadow.setOpacity(0.1)                   
                        group.addToGroup(segment_shadow)

                    self.scene().addItem(group)
                    self._segments.append([ramByte, ramBit, group, -1])
        
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
        motion_ghosting = self._motionGhosting
        ghost_segments = self._ghostSegments
        ramSize = len(RAM)
        for seg in self._segments:
            nibble, bit, segment, opacity = seg
            if nibble < ramSize:
                target = (RAM[nibble] >> bit) & 0x1
                if (opacity != target):
                    opacity += motion_ghosting * (target - opacity)
                    if abs(opacity - target) < 1e-3:
                        opacity = target
                    segment.setOpacity(opacity + ghost_segments)
                    seg[-1] = opacity
            else:
                seg[-1] = 0
                segment.setOpacity(ghost_segments)

    @pyqtSlot(str)
    def error(self, error):
        QMessageBox(parent=self, text=error).exec()
        self.close()