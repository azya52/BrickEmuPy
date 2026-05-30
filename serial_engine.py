import threading
import queue
import serial
import time


class SerialEngine:
    """Non-blocking Serial I/O engine (singleton pattern like audio_engine)"""
    
    def __init__(self):
        self._port = "COM1"
        self._baudrate = 115200
        self._timeout = 0.1
        
        self._serial = None
        self._running = False
        self._rx_queue = queue.Queue()
        self._rx_thread = None
        self._lock = threading.Lock()
    
    def configure(self, port, baudrate):
        """Configure serial port settings (non-blocking)"""
        with self._lock:
            self._port = port
            self._baudrate = baudrate
    
    def connect(self):
        """Open serial connection (non-blocking attempt)"""
        self.disconnect()
        time.sleep(0.1)
        
        try:
            with self._lock:
                self._serial = serial.Serial(
                    port=self._port,
                    baudrate=self._baudrate,
                    timeout=self._timeout,
                    write_timeout=self._timeout
                )
                self._running = True
        except (serial.SerialException, FileNotFoundError):
            self._serial = None
            self._running = False
            return False
        
        self._rx_thread = threading.Thread(target=self._read_thread, daemon=True)
        self._rx_thread.start()
        return True
    
    def disconnect(self):
        """Close serial connection"""
        self._running = False
        if self._rx_thread:
            self._rx_thread.join(timeout=1.0)
        
        with self._lock:
            if self._serial:
                try:
                    self._serial.close()
                except Exception:
                    pass
                self._serial = None
    
    def _read_thread(self):
        """Background thread for reading serial data (non-blocking)"""
        while self._running:
            try:
                with self._lock:
                    if not self._serial or not self._running:
                        break
                    data = self._serial.read(256)
                
                if data:
                    self._rx_queue.put(data)
            except (serial.SerialException, OSError):
                break
            except Exception:
                time.sleep(0.001)
    
    def send(self, data):
        """Send data to serial port (non-blocking)"""
        if not self.is_connected():
            return False
        
        try:
            with self._lock:
                if not self._serial or not self._running:
                    return False
                
                if isinstance(data, bytes):
                    self._serial.write(data)
                elif isinstance(data, (list, tuple)):
                    self._serial.write(bytes(data))
                else:
                    self._serial.write(str(data).encode())
            return True
        except (serial.SerialException, OSError):
            return False
    
    def receive(self):
        """Get all queued received data without blocking"""
        data = b""
        try:
            while True:
                chunk = self._rx_queue.get_nowait()
                data += chunk
        except queue.Empty:
            pass
        return data
    
    def is_connected(self):
        """Check if serial port is open"""
        with self._lock:
            return self._serial is not None and self._serial.is_open and self._running


_serial_engine = None

def getSerialEngine():
    """Get or create singleton serial engine"""
    global _serial_engine
    if _serial_engine is None:
        _serial_engine = SerialEngine()
    return _serial_engine
