import sys
import multiprocessing

from PyQt6 import QtCore
from PyQt6.QtCore import QObject, pyqtSignal

import audio_engine
from emulator_process import *

def emulatorProcess(config, cmd_queue, data_queue):
    timerPeriodSet = False
    if sys.platform == "win32": 
        import ctypes
        try:
            ctypes.windll.winmm.timeBeginPeriod(1)
            timerPeriodSet = True
        except Exception as e:
            pass

    try:
        EmulatorProcess(config, cmd_queue, data_queue).run()
    finally:
        try:
            if sys.platform == "win32" and timerPeriodSet:
                ctypes.windll.winmm.timeEndPeriod(1)
        except Exception as e:
            pass


class Brick(QObject):
    examineSignal = pyqtSignal(dict)
    uiDisplayUpdateSignal = pyqtSignal(tuple)
    errorSignal = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self._config = config
        self._proc = None
        self._audioEngine = audio_engine.getAudioEngine()

    def start(self):
        self._cmdQueue = multiprocessing.Queue()
        self._dataQueue = multiprocessing.Queue()

        self._proc = multiprocessing.Process(
            target=emulatorProcess,
            args=(self._config, self._cmdQueue, self._dataQueue),
            daemon=False,
        )
        self._proc.start()

        self._pollTimer = QtCore.QTimer(self)
        self._pollTimer.setInterval(int(1000 / max(FPS, EXAMINE_RATE) / 2))
        self._pollTimer.timeout.connect(self._poll)
        self._pollTimer.start()

    def _poll(self):
        while not self._dataQueue.empty():
            try:
                msg = self._dataQueue.get_nowait()
            except Exception:
                break
            op = msg[0]
            if op == MSG_VRAM: 
                self.uiDisplayUpdateSignal.emit(msg[1])
            elif op == MSG_EXAMINE:
                self.examineSignal.emit(msg[1])
            elif op == MSG_ERROR:
                self.errorSignal.emit(msg[1])
            elif op == MSG_SOUND_DATA:
                self._soundProcess(msg[1], msg[2], msg[3])
            elif op == MSG_SOUND_RESET:
                self._soundReset()
                
    def close(self):
        self._pollTimer.stop()
        if self._proc and self._proc.is_alive():
            self._cmdQueue.put((CMD_QUIT,))
            self._proc.join(timeout=1.0)
            if self._proc.is_alive():
                self._proc.terminate()
                self._proc.join()
        self._cmdQueue = None
        self._dataQueue = None

    def _soundReset(self):
        self._audioEngine.reset()

    def _soundProcess(self, channel, data, tick):
        if (data):
            self._audioEngine.play(channel, data[0], data[1], data[2], tick / 1e9, data[3])
        else:
            self._audioEngine.stop(channel, tick / 1e9)

    def debugRun(self):
        self._cmdQueue.put((CMD_DEBUG, CMD_DEBUG_RUN))

    def debugPause(self):
        self._cmdQueue.put((CMD_DEBUG, CMD_DEBUG_PAUSE))

    def debugStep(self):
        self._cmdQueue.put((CMD_DEBUG, CMD_DEBUG_STEP))

    def debugStop(self):
        self._cmdQueue.put((CMD_DEBUG, CMD_DEBUG_STOP))

    def setSpeed(self, speed):
        self._cmdQueue.put((CMD_SPEED, speed))

    def setBreakpoint(self, pc, add):
        self._cmdQueue.put((CMD_BREAKPOINT, pc, add))

    def editState(self, state):
        self._cmdQueue.put((CMD_EDIT_STATE, state))

    def btnPressed(self, key):
        self._cmdQueue.put((CMD_BTN_PRESS, key))

    def btnReleased(self, key):
        self._cmdQueue.put((CMD_BTN_RELEASE, key))