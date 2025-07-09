from PyQt6 import QtCore
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import time

from cores import *

FPS = 60
EXAMINE_RATE = 30

DISPLAY_UPDTE_NS = 1000000000 / FPS
EXAMINE_UPDTE_NS = 1000000000 / EXAMINE_RATE

class Brick(QObject):
    btnPressSignal = pyqtSignal(str, int, int)
    btnMatrixPressSignal = pyqtSignal(str, int, dict)
    btnReleaseSignal = pyqtSignal(str, int)
    stepSignal = pyqtSignal()
    pauseSignal = pyqtSignal()
    runSignal = pyqtSignal()
    stopSignal = pyqtSignal()
    setSpeedSignal = pyqtSignal(float)
    setBreakpointSignal = pyqtSignal(int, bool)
    examineSignal = pyqtSignal(dict)
    editStateSignal = pyqtSignal(dict)
    uiDisplayUpdateSignal = pyqtSignal(tuple)
    setConfigSignal = pyqtSignal(dict)
    errorSignal = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self._config = config

        self.btnPressSignal.connect(self._btnPressed)
        self.btnMatrixPressSignal.connect(self._btnMatrixPressed)
        self.btnReleaseSignal.connect(self._btnReleased)
        self.setBreakpointSignal.connect(self._setBreakpoint)
        self.runSignal.connect(self._run)
        self.pauseSignal.connect(self._pause)
        self.stepSignal.connect(self._step)
        self.setConfigSignal.connect(self._setConfig)
        self.stopSignal.connect(self._stop)
        self.setSpeedSignal.connect(self._setSpeed)
        self.editStateSignal.connect(self._editState)

    @pyqtSlot()
    def run(self):
        self._breakpoints = {}
        self._debug = False
        self._cycleTimeNs = self._getCicleTimeNs()
        self._icounterOnStop = 0
        self._btn_matrix_out = {}
        self._btn_matrix_in = {}

        try:
            self._setConfig(self._config)
        except Exception as e:
            self.errorSignal.emit(str(e))
            return

        self._uiDisplayUpdate()
        self._uiExamineUpdate()
        
        self._clock()
    
    @pyqtSlot(dict)
    def _editState(self, state):
        if ("BRKPT" in state):
            self._setBreakpoint(state["BRKPT"][0], state["BRKPT"][1])
        self._CPU.edit_state(state)
        self._uiDisplayUpdate()
        self._uiExamineUpdate()

    def _clock(self):
        thread = self.thread().currentThread()
        lastTick = time.perf_counter_ns()
        lastExamine = lastTick
        lastDisplayUpdate = lastTick
        while not(thread.isInterruptionRequested() or self._debug):
            cycleTimeNs = self._cycleTimeNs
            ns = time.perf_counter_ns()
            while (ns > lastTick and ns < lastDisplayUpdate and ns < lastExamine and not self._debug):
                lastTick += self._CPU.clock() * cycleTimeNs
                if (self._breakpoints and self._CPU.pc() in self._breakpoints):
                    self.examineSignal.emit({"DEBUG": True})
                    self._pause()

                ns = time.perf_counter_ns()

            if (ns > lastDisplayUpdate):
                lastDisplayUpdate += DISPLAY_UPDTE_NS
                self._uiDisplayUpdate()
            elif (ns > lastExamine):
                lastExamine += EXAMINE_UPDTE_NS
                self._uiExamineUpdate()

            if (lastTick > ns):
                time.sleep((lastTick - ns) / 1000000000)
            else:
                lastTick = ns

            QtCore.QCoreApplication.processEvents()

    def _set_pin_state(self, port, pin, level):
        self._btn_matrix_out[(port, pin)] = level
        for port, pin in self._btn_matrix_in.get((port, pin), ()):
            self._CPU.pin_set(port, pin, level)

    @pyqtSlot()
    def _run(self):
        self._debug = False
        self._clock()

    @pyqtSlot()
    def _pause(self):
        self._debug = True
        self._uiDisplayUpdate()
        self._uiExamineUpdate()
        self._icounterOnStop = self._CPU.istr_counter()

    @pyqtSlot()
    def _step(self):
        self._CPU.clock()
        self._uiDisplayUpdate()
        self._uiExamineUpdate()

    @pyqtSlot()
    def _stop(self):
        self._debug = True
        self._CPU.reset()
        self._uiDisplayUpdate()
        self._uiExamineUpdate()
        self._icounterOnStop = self._CPU.istr_counter()
            
    @pyqtSlot(int, bool)
    def _setBreakpoint(self, pc, add):
        if (add):
            self._breakpoints[pc] = True
        else:
            if (pc in self._breakpoints):
                del self._breakpoints[pc]

    @pyqtSlot(dict)
    def _setConfig(self, config):
        self._config = config
        core = self._config["core"]
        if (core in cores_map):
            self._CPU = cores_map[core]["core"](config['mask_options'], config["clock"])
            self.examineSignal.emit(cores_map[core]["dasm"]().disassemble(self._CPU.get_ROM()))

            if (hasattr(self._CPU, "set_pin_state_callback")):
                self._CPU.set_pin_state_callback(self._set_pin_state)

    def _uiDisplayUpdate(self):
        self.uiDisplayUpdateSignal.emit(self._CPU.get_VRAM()) 

    def _uiExamineUpdate(self):
        self.examineSignal.emit({
            **self._CPU.examine(),
            "ICTR": self._CPU.istr_counter() - self._icounterOnStop
        })

    @pyqtSlot(str, int, int)
    def _btnPressed(self, port, pin, level):
        self._CPU.pin_set(port, pin, level)

    @pyqtSlot(str, int)
    def _btnReleased(self, port, pin):
        for _, item in self._btn_matrix_in.items():
            item.discard((port, pin))
        self._CPU.pin_release(port, pin)

    @pyqtSlot(str, int, dict)
    def _btnMatrixPressed(self, port, pin, level):
        key = (level["port"], level["pin"])
        self._btn_matrix_in.setdefault(key, set()).add((port, pin))
        if key in self._btn_matrix_out:
            self._CPU.pin_set(port, pin, self._btn_matrix_out[key])

    @pyqtSlot(float)
    def _setSpeed(self, speed):
        self._cycleTimeNs = int(self._getCicleTimeNs() * speed)

    def _getCicleTimeNs(self):
        return 1000000000 / self._config["clock"]

    def debugRun(self):
        self.runSignal.emit()

    def debugStep(self):
        self.stepSignal.emit()

    def debugPause(self):
        self.pauseSignal.emit()

    def debugStop(self):
        self.stopSignal.emit()

    def btnPressed(self, port, pin, level):
        if (type(level) is dict):
            self.btnMatrixPressSignal.emit(port, pin, level)
        else:
            self.btnPressSignal.emit(port, pin, level)

    def btnReleased(self, port, pinMask):
        self.btnReleaseSignal.emit(port, pinMask)

    def setConfig(self, config):
        self.setConfigSignal.emit(config)

    def setSpeed(self, speed):
        self.setSpeedSignal.emit(speed)

    def editState(self, state):
        self.editStateSignal.emit(state)

    def setBreakpoint(self, pc, add):
        self.setBreakpointSignal.emit(pc, add)

    def close(self):
        del self._CPU