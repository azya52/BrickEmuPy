from time import perf_counter_ns, sleep

from cores import *
from peripherals import *
from interconnect import Interconnect

FPS = 60
EXAMINE_RATE = 30

DISPLAY_UPDTE_NS = 1e9 / FPS
EXAMINE_UPDTE_NS = 1e9 / EXAMINE_RATE

CMD_QUIT = 0
CMD_DEBUG = 10
CMD_DEBUG_RUN = 11
CMD_DEBUG_PAUSE = 12
CMD_DEBUG_STOP = 13
CMD_DEBUG_STEP = 14
CMD_SPEED = 50
CMD_BREAKPOINT = 60
CMD_EDIT_STATE = 70
CMD_BTN_PRESS = 80
CMD_BTN_RELEASE = 90

MSG_EXAMINE = 0
MSG_VRAM = 10
MSG_ERROR = 20
MSG_SOUND_DATA = 30
MSG_SOUND_RESET = 31

CYCLE_SKIP_TIMEOUT_NS = 100e6

class EmulatorProcess:
    def __init__(self, config, cmd_queue, data_queue):
        self._config = config
        self._cmd_queue = cmd_queue
        self._data_queue = data_queue

        self._breakpoints = {}
        self._debug = False
        self._icounter_on_stop = 0

        self._btn_matrix_out = {}
        self._btn_matrix_in = {}

        self._cpu = None
        self._dasm = None
        self._interconnect = None

        self._cycle_time_ns = 0
        self._last_tick = 0
        self._next_display = 0
        self._next_examine = 0

        self._init_config()

    def audio_handler(self, channel, data):
        self._data_queue.put((MSG_SOUND_DATA, channel, data, self._last_tick))

    def _init_config(self):
        try:
            core = self._config["core"]
            self._interconnect = Interconnect()
            self._interconnect.register_audio_forwarder(self)

            self._cpu = cores_map[core]["core"](
                self._config["mask_options"],
                self._config["clock"],
                self._interconnect
            )

            for name, value in self._config.get("peripherals", {}).items():
                if name in peripherals_map:
                    peripherals_map[name](value, self._interconnect)

            self._dasm = cores_map[core]["dasm"](self._config.get("disasm_roots", None))
            self._ui_listing_update()
        except Exception as e:
            self._data_queue.put((MSG_ERROR, str(e)))
            raise

    def _ui_display_update(self):
        self._data_queue.put((MSG_VRAM, self._cpu.get_VRAM()))

    def _ui_listing_update(self):
        self._data_queue.put((MSG_EXAMINE, self._dasm.disassemble(self._cpu.get_ROM())))

    def _ui_examine_update(self):
        self._data_queue.put((MSG_EXAMINE, {
            **self._cpu.examine(),
            "ICTR": self._cpu.istr_counter() - self._icounter_on_stop,
        }))

    def _process_commands(self):
        while True:
            try:
                cmd = self._cmd_queue.get_nowait()
            except:
                break

            op = cmd[0]

            if op == CMD_QUIT:
                self._cmd_queue.cancel_join_thread()
                self._data_queue.cancel_join_thread()
                self._cmd_queue.close()
                self._data_queue.close()
                raise SystemExit

            elif op == CMD_DEBUG:
                cmd_debug = cmd[1]
                self._data_queue.put((MSG_SOUND_RESET,))

                if cmd_debug == CMD_DEBUG_RUN:
                    self._debug = False
                    self._reset_timing()

                elif cmd_debug == CMD_DEBUG_PAUSE:
                    self._debug = True
                    self._ui_display_update()
                    self._ui_examine_update()
                    self._icounter_on_stop = self._cpu.istr_counter()

                elif cmd_debug == CMD_DEBUG_STOP:
                    self._debug = True
                    self._cpu.reset()
                    self._ui_display_update()
                    self._ui_examine_update()
                    self._icounter_on_stop = self._cpu.istr_counter()

                elif cmd_debug == CMD_DEBUG_STEP:
                    self._cpu.clock()
                    self._ui_display_update()
                    self._ui_examine_update()

            elif op == CMD_SPEED:
                self._data_queue.put((MSG_SOUND_RESET,))
                self._cycle_time_ns = self.get_cycle_time_ns() * cmd[1]
                self._reset_timing()

            elif op == CMD_BREAKPOINT:
                _, pc, add = cmd
                if add:
                    self._breakpoints[pc] = True
                else:
                    self._breakpoints.pop(pc, None)

            elif op == CMD_EDIT_STATE:
                state = cmd[1]

                if "BRKPT" in state:
                    pc, add = state["BRKPT"]
                    if add:
                        self._breakpoints[pc] = True
                    else:
                        self._breakpoints.pop(pc, None)

                self._cpu.edit_state(state)
                self._ui_display_update()
                self._ui_examine_update()

            elif op == CMD_BTN_PRESS:
                self._interconnect.emit_input(cmd[1], True)

            elif op == CMD_BTN_RELEASE:
                self._interconnect.emit_input(cmd[1], False)

    def _reset_timing(self):
        now = perf_counter_ns()
        self._last_tick = self._next_display = self._next_examine = now

    def get_cycle_time_ns(self):
        return 1e9 / self._config["clock"]

    def run(self):
        self._cycle_time_ns = self.get_cycle_time_ns()
    
        self._reset_timing()

        next_update = 0

        cpu_clock = self._cpu.clock
        cpu_pc = self._cpu.pc
        emit_clock = self._interconnect.emit_clock

        while True:
            self._process_commands()

            if self._debug:
                sleep(0.005)
                continue

            ns = perf_counter_ns()
            while ns > self._last_tick and ns < next_update:
                cycles = cpu_clock()
                self._last_tick += cycles * self._cycle_time_ns
                emit_clock(cycles)

                if self._breakpoints and cpu_pc() in self._breakpoints:
                    self._debug = True
                    self._data_queue.put((MSG_EXAMINE, {"DEBUG": True}))
                    self._ui_display_update()
                    self._ui_examine_update()
                    self._icounter_on_stop = self._cpu.istr_counter()
                    break

                ns = perf_counter_ns()

            if ns > self._next_display:
                self._next_display += DISPLAY_UPDTE_NS
                next_update = min(self._next_display, self._next_examine)
                self._ui_display_update()

            elif ns > self._next_examine:
                self._next_examine += EXAMINE_UPDTE_NS
                next_update = min(self._next_display, self._next_examine)
                self._ui_examine_update()

            elif (self._last_tick > ns):
                sleep((self._last_tick - ns) / 1e9)

            if (ns - self._last_tick) > CYCLE_SKIP_TIMEOUT_NS:
                self._last_tick = ns
                self._data_queue.put((MSG_SOUND_RESET,))