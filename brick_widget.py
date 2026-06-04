import queue
import multiprocessing

from PyQt6 import QtCore, QtGui, QtWidgets, QtSvgWidgets, QtSvg
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt6.QtWidgets import QGraphicsScene, QMessageBox
from functools import partial

import audio_engine
from emulator_process import *

DEFAULT_MOTION_BLUR = 0.6
DEFAULT_GHOST_SEGMENTS = 0
DEFAULT_SHADOW = 5

class QueueReaderThread(QThread):
    messageSignal = pyqtSignal(list)

    def __init__(self, data_queue):
        super().__init__()
        self._dataQueue = data_queue
        self._running = True

    def run(self):
        while self._running:
            try:
                self.messageSignal.emit(self._dataQueue.get(timeout=0.1))
            except queue.Empty:
                continue

    def stop(self):
        self._running = False
        self.wait()


class BrickWidget(QtWidgets.QGraphicsView):
    examineSignal = pyqtSignal(dict)

    def __init__(self, config, settings, serial=None):
        super().__init__()

        self.setViewportUpdateMode(QtWidgets.QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.NoRole)
        self.setFrameStyle(0)
        
        self._config = config
        self._settings = settings

        self._displaySettings = {}
        self._motionBlur = DEFAULT_MOTION_BLUR
        self._ghostSegments = DEFAULT_GHOST_SEGMENTS
        self._shadow = DEFAULT_SHADOW

        self._loadSettings()

        self._serial = serial
        if (self._serial is not None):
            self._serial.dataReceived.connect(self._serialRX)
            self._serial.error.connect(self._error)

        self._audioEngine = audio_engine.getAudioEngine()

        self._start_emulator()

        self._draw(config["face_path"])

    def _start_emulator(self):
        self._cmdQueue = multiprocessing.Queue()
        self._dataQueue = multiprocessing.Queue(maxsize=100)

        self._QueueReaderThread = QueueReaderThread(self._dataQueue)
        self._QueueReaderThread.messageSignal.connect(self._processMessage)
        self._QueueReaderThread.start()

        self._proc = multiprocessing.Process(
            target=EmulatorProcess.spawn,
            args=(self._config, self._cmdQueue, self._dataQueue),
            daemon=False,
        )
        self._proc.start()

    def _processMessage(self, msg):
        op = msg[0]
        if (op == MSG_VRAM):
            self._renderVRAM(msg[1])
        elif (op == MSG_EXAMINE):
            self.examineSignal.emit(msg[1])
        elif (op == MSG_ERROR):
            self._error(msg[1])
        elif (op == MSG_SOUND_DATA):
            self._soundProcess(msg[1], msg[2], msg[3])
        elif (op == MSG_SOUND_RESET):
            self._audioEngine.reset()
        elif (op == MSG_SERIAL_TX):
            self._serialTX(msg[1])

    def close(self):
        self._serial = None

        if (self._QueueReaderThread):
            self._QueueReaderThread.stop()
            self._QueueReaderThread = None

        if (self._proc and self._proc.is_alive()):
            self._cmdQueue.put((CMD_QUIT,))
            self._proc.join(timeout=1.0)
            if (self._proc.is_alive()):
                self._proc.terminate()
                self._proc.join()

        self._saveSettings()
        super().close()

    def showEvent(self, event):
        self._fitBrickInView()
        return super().showEvent(event)

    def _loadSettings(self):
        self._scene_rect = self._settings.value("brick/" + self._config["id"] + "/scene_rect")
        self._displaySettings = self._settings.value("display", {
            "motion_blur": True,
            "ghost_segments": True,
            "shadow": True,
        })

    def _saveSettings(self):
        self._settings.setValue("brick/" + self._config["id"] + "/scene_rect", self.mapToScene(self.viewport().rect()).boundingRect())

    def _soundProcess(self, channel, data, tick):
        if (data):
            self._audioEngine.play(channel, data[0], data[1], data[2], tick / 1e9, data[3])
        else:
            self._audioEngine.stop(channel, tick / 1e9)

    @pyqtSlot(dict)
    def editState(self, state):
        self._cmdQueue.put((CMD_EDIT_STATE, state))

    @pyqtSlot()
    def step(self):
        self._cmdQueue.put((CMD_DEBUG, CMD_DEBUG_STEP))

    @pyqtSlot()
    def pause(self):
        self._cmdQueue.put((CMD_DEBUG, CMD_DEBUG_PAUSE))

    @pyqtSlot()
    def stop(self):
        self._cmdQueue.put((CMD_DEBUG, CMD_DEBUG_STOP))

    @pyqtSlot()
    def run(self):
        self._cmdQueue.put((CMD_DEBUG, CMD_DEBUG_RUN))

    def setBreakpoint(self, pc, add):
        self._cmdQueue.put((CMD_BREAKPOINT, pc, add))

    @pyqtSlot()
    def setSpeed(self):
        self._cmdQueue.put((CMD_SPEED, self.sender().checkedAction().property("factor")))

    def _fitBrickInView(self):
        if (self._scene_rect is not None):
            self.fitInView(self._scene_rect, Qt.AspectRatioMode.KeepAspectRatio)
        else:
            self.fitInView(self.scene().sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        self._fitBrickInView()
        return super().resizeEvent(event)

    def keyPressEvent(self, event):
        if (not event.isAutoRepeat()):
            for name, value in self._config["buttons"].items():
                if (event.key() in value["hot_keys"]):
                    self._cmdQueue.put((CMD_BTN_PRESS, name))

    def keyReleaseEvent(self, event):
        if (not event.isAutoRepeat()):
            for name, value in self._config["buttons"].items():
                if (event.key() in value["hot_keys"]):
                    self._cmdQueue.put((CMD_BTN_RELEASE, name))

    def wheelEvent(self, event):
        zoomFactor = 1.1
        if (event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier):
            zoomFactor = 1.01
        if (event.angleDelta().y() < 0):
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
                btn = QtWidgets.QPushButton(objectName="brickButton")
                btn.setGeometry(faceRenderer.boundsOnElement(name).toRect())
                shortcuts = "Shortcuts: "
                for shortcut in value["hot_keys"]:
                    shortcuts += Qt.Key(shortcut).name + ", "
                btn.setToolTip(shortcuts[:-2])
                btn.pressed.connect(partial(self._cmdQueue.put, (CMD_BTN_PRESS, name)))
                btn.released.connect(partial(self._cmdQueue.put, (CMD_BTN_RELEASE, name)))
                self.scene().addWidget(btn)

    def _renderVRAM(self, RAM):
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

    def _error(self, error):
        QMessageBox(parent=self, text=error).exec()

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

    def _serialRX(self, data: bytes):
        self._cmdQueue.put((CMD_SERIAL_RX, data))

    def _serialTX(self, data):
        if self._serial:
            self._serial.send_data(data)