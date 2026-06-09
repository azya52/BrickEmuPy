from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import pyqtSignal, QObject

BAUD_RATE = 115200

class SerialConnection(QObject):
    dataReceived = pyqtSignal(bytes)
    error = pyqtSignal(str)

    def __init__(self,  parent=None):
        super().__init__(parent)
        self._serial_port = QSerialPort()
        self._serial_port.readyRead.connect(self._read_data)
        self._serial_port.errorOccurred.connect(self._on_error)
        self._port_name = None

    def open_port(self, port_name):
        if (self._serial_port.isOpen()):
            self._serial_port.close()
        self._serial_port.setPortName(port_name)
        self._serial_port.setBaudRate(BAUD_RATE)
        if self._serial_port.open(QSerialPort.OpenModeFlag.ReadWrite):
            self._port_name = port_name

    def close_port(self):
        if (self._serial_port.isOpen()):
            self._serial_port.close()
        self._port_name = None

    def send_data(self, data):
        if (self._serial_port.isOpen()):
            self._serial_port.write(data)

    def _read_data(self):
        self.dataReceived.emit(bytes(self._serial_port.readAll()))

    def _on_error(self, error):
        if error != QSerialPort.SerialPortError.NoError:
            self.error.emit(self._serial_port.errorString())
            if (error in (QSerialPort.SerialPortError.ResourceError,
                          QSerialPort.SerialPortError.DeviceNotFoundError)):
                self.close_port()

    def is_connected(self):
        return self._serial_port.isOpen()

    def get_port_name(self):
        return self._port_name

    @staticmethod
    def get_available_ports():
        return [(p.portName(), p.description()) for p in QSerialPortInfo.availablePorts()]