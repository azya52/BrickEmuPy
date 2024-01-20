from PyQt6 import QtCore
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import time

from mcu import MCU
from disassembler import Disassembler
from sound import Sound

FPS = 60
EXAMINE_RATE = 30

DISPLAY_UPDTE_NS = 1000000000 / FPS
EXAMINE_UPDTE_NS = 1000000000 / EXAMINE_RATE

class Brick(QObject):
    btnPressSignal = pyqtSignal(str, int)
    btnReleaseSignal = pyqtSignal(str, int)
    stepSignal = pyqtSignal()
    pauseSignal = pyqtSignal()
    runSignal = pyqtSignal()
    stopSignal = pyqtSignal()
    setSpeedSignal = pyqtSignal(float)
    setBreakpointSignal = pyqtSignal(int, bool)
    examineSignal = pyqtSignal(dict)
    uiDisplayUpdateSignal = pyqtSignal(tuple)
    setConfigSignal = pyqtSignal(dict)

    def __init__(self, config, ui):
        super().__init__()
        self._config = config
        self._ui = ui

        self.btnPressSignal.connect(self._btnPressed)
        self.btnReleaseSignal.connect(self._btnReleased)
        self.setBreakpointSignal.connect(self._setBreakpoint)
        self.runSignal.connect(self._run)
        self.pauseSignal.connect(self._pause)
        self.stepSignal.connect(self._step)
        self.stopSignal.connect(self._stop)
        self.setConfigSignal.connect(self._setConfig)
        self.stopSignal.connect(self._stop)
        self.setSpeedSignal.connect(self._setSpeed)

    @pyqtSlot()
    def run(self):
        self._sound = Sound(self._config['mask_options'], self._config['clock'])
        self._CPU = MCU(self._config['mask_options'], self._sound)

        self._breakpoints = {}
        self._debug = False
        self._mcycleTimeNs = self._getMCicleTimeNs()
        self._mcyclesOnStop = 0

        self.uiDisplayUpdateSignal.connect(self._ui.render)
        self.examineSignal.connect(self._ui.examineSlot)

        self._uiDisplayUpdate()
        self._uiExamineUpdate()

        self.examineSignal.emit(Disassembler().disassemble(self._CPU.get_ROM()))

        self._clock()

    @pyqtSlot()
    def finish(self):
        self.examineSignal.disconnect()
        self.uiDisplayUpdateSignal.disconnect()
        self.btnPressSignal.disconnect()
        self.btnReleaseSignal.disconnect()
        self.setBreakpointSignal.disconnect()
        self.runSignal.disconnect()
        self.pauseSignal.disconnect()
        self.stepSignal.disconnect()
        self.stopSignal.disconnect()
        self.setConfigSignal.disconnect()
        self.setSpeedSignal.disconnect()
        self._sound.stop()

    @pyqtSlot(dict)
    def editState(self, state):
        if ("PC" in state):
            self._CPU.setPC(state["PC"])
        if ("ST" in state):
            self._CPU.setSTACK(state["ST"])
        if ("CF" in state):
            self._CPU.setCF(state["CF"])
        if ("EF" in state):
            self._CPU.setEF(state["EF"])
        if ("TF" in state):
            self._CPU.setTF(state["TF"])
        if ("EI" in state):
            self._CPU.setEI(state["EI"])
        if ("HALT" in state):
            self._CPU.setHALT(state["HALT"])
        if ("WR" in state):
            for i, value in state["WR"].items():
                self._CPU.setWR(i, value)
        if ("TC" in state):
            self._CPU.setTC(state["TC"])
        if ("PA" in state):
            self._CPU.setPA(state["PA"])
        if ("PP" in state):
            self._CPU.setPP(state["PP"])
        if ("PM" in state):
            self._CPU.setPM(state["PM"])
        if ("PS" in state):
            self._CPU.setPS(state["PS"])
        if ("RAM" in state):
            for i, value in state["RAM"].items():
                self._CPU.setRAM(i, value)
        if ("MEMORY" in state):
            self._ROM.writeWord(state["MEMORY"][0], state["MEMORY"][1])
        
        self._uiDisplayUpdate()
        self._uiExamineUpdate()

    def _clock(self):
        thread = self.thread().currentThread()
        lastTick = time.perf_counter_ns()
        lastExamine = lastTick
        lastDisplayUpdate = lastTick
        while not(thread.isInterruptionRequested() or self._debug):
            ns = time.perf_counter_ns()
            while (ns > lastTick and ns < lastDisplayUpdate and ns < lastExamine and not self._debug):                
                lastTick += self._mcycleTimeNs
                if (self._CPU.mclock() == 0):
                    if (self._CPU.PC() in self._breakpoints):
                        self.examineSignal.emit({"DEBUG": True})
                        self._pause()

                ns = time.perf_counter_ns()
            
            if (ns > lastDisplayUpdate):
                lastDisplayUpdate += DISPLAY_UPDTE_NS
                self._uiDisplayUpdate()
            elif (ns > lastExamine):
                lastExamine += EXAMINE_UPDTE_NS
                self._uiExamineUpdate()

            QtCore.QCoreApplication.processEvents()
            
            
    @pyqtSlot()
    def _run(self):
        self._debug = False
        self._clock()

    @pyqtSlot()
    def _pause(self):
        self._debug = True
        self._uiDisplayUpdate()
        self._uiExamineUpdate()
        self._mcyclesOnStop = self._CPU.mcycles()

    @pyqtSlot()
    def _step(self):
        while (self._CPU.mclock()):
            pass
        self._uiDisplayUpdate()
        self._uiExamineUpdate()

    @pyqtSlot()
    def _stop(self):
        self._debug = True
        self._sound = Sound(self._config['mask_options'], self._config['clock'])
        self._CPU = MCU(self._config['mask_options'], self._sound)
        self._uiDisplayUpdate()
        self._uiExamineUpdate()
            
    @pyqtSlot(int, bool)
    def _setBreakpoint(self, pc, add):
        if (add):
            self._breakpoints[pc] = True
        else:
            if (pc in self._breakpoints):
                del self._breakpoints[pc]

    @pyqtSlot(dict)
    def _setConfig(self, config):
        self._sound = Sound(self._config['mask_options'], self._config['clock'])
        self._CPU = MCU(config['mask_options'], self._sound)
        self.examineSignal.emit(Disassembler().disassemble(self._CPU.get_ROM()))

    def _uiDisplayUpdate(self):
        self.uiDisplayUpdateSignal.emit(self._CPU.get_VRAM()) 

    def _uiExamineUpdate(self):
        self.examineSignal.emit({
            **self._CPU.examine(),
            **{"MC": self._CPU.mcycles() - self._mcyclesOnStop}
        })

    @pyqtSlot(str, int)
    def _btnPressed(self, port, pinMask):
        self._CPU.pin_ground(port, pinMask)

    @pyqtSlot(str, int)
    def _btnReleased(self, port, pinMask):
        self._CPU.pin_release(port, pinMask)

    @pyqtSlot(float)
    def _setSpeed(self, speed):
        self._mcycleTimeNs = int(self._getMCicleTimeNs() * speed)

    def _getMCicleTimeNs(self):
        return 1000000000 / self._config["clock"] * 4

    def debugRun(self):
        self.runSignal.emit()

    def debugStep(self):
        self.stepSignal.emit()

    def debugPause(self):
        self.pauseSignal.emit()

    def debugStop(self):
        self.stopSignal.emit()

    def debugSetBreakpoint(self, pc, checked):
        self.setBreakpointSignal.emit(pc, checked)

    def btnPressed(self, port, pinMask):
        self.btnPressSignal.emit(port, pinMask)

    def btnReleased(self, port, pinMask):
        self.btnReleaseSignal.emit(port, pinMask)

    def setConfig(self, config):
        self.setConfigSignal.emit(config)

    def setSpeed(self, speed):
        self.setSpeedSignal.emit(speed)
