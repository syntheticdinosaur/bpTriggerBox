# Small Module to communicate with the BrainProducts Triggerbox PLUS via USB (COM-Port)
# Author: Joshua Woller
import serial
import time
import threading

class BPTriggerBox:
    """
    BPTriggerBox - A class for managing binary triggers through a serial port.
    Attributes:
        instances (list): A list to store instances of the BPTriggerBox class.

    Methods:
        close_all_ports():
            Closes all open serial ports associated with instances of BPTriggerBox.

        __init__(config: dict):
            Initializes a new BPTriggerBox instance with the provided configuration.

            Parameters:
                config (dict): A dictionary containing serial port configuration parameters.
                    - "port": The serial port to connect to.
                    - "baudrate": Baud rate for the serial connection.
                    - "timeout": Timeout duration for serial communication.
                    - "exclusive": Whether to open the port exclusively.

        send_trigger(trigger_value: int = 1):
            Writes a trigger value to the serial port.

            Parameters:
                trigger_value (int): The binary value to be sent (default is 1).

        reset(close_only: bool = False):
            Resets the serial port by flushing input and output buffers, closing the port,
            and optionally reopening it.

            Parameters:
                close_only (bool): If True, only closes the port without reopening (default is False).
    """
    instances = []

    @classmethod
    def close_all_ports(cls):
        """
        Closes all open serial ports associated with instances of BPTriggerBox.
        """
        if cls.instances:
            for instance in cls.instances:
                instance._interface.close()

    def __init__(self,
                 port_config:dict =  {"port": 'COM8',
                                       "baudrate": 2_000_000,
                                       "timeout": None,
                                       "exclusive": True},
                 pulsewidth: float = 0.005):
        """
        Initializes a new BPTriggerBox instance with the provided configuration.

        Parameters:
            config (dict): A dictionary containing serial port configuration parameters.
                - "port": The serial port to connect to.
                - "baudrate": Baud rate for the serial connection.
                NOTE: For TriggerBox PLUS, the baudrate needs to be 2_000_000.
                - "timeout": Timeout duration for serial communication.
                - "exclusive": Whether to open the port exclusively.
            pulsewidth: Pulse width of trigger pulse in seconds
        """
        self._interface = serial.Serial(
            port=port_config["port"],
            baudrate=port_config["baudrate"],
            timeout=port_config["timeout"],
            exclusive=port_config["exclusive"]
        )
        self.pw = pulsewidth
        self.__class__.instances.append(self)
        self._interface.write(bytes([0]))

    def send(self, trigger_value: int = 1):
        """
        Writes a trigger value to the serial port.

        Parameters:
            trigger_value (int): The value to be sent (default is 1).
        """
        assert isinstance(trigger_value, int), f"Trigger value must be integer, but was of type {str(type(trigger_value))}."
        assert 0 < trigger_value < 255 ,f"Trigger must be a positive integer between 1 and 254, but was {trigger_value}."
        self._interface.write(bytes([trigger_value]))
        time.sleep(self.pw)
        self._interface.write(bytes([0]))

    def reset_port(self, close_only=False):
        """
        Resets the serial port by flushing input and output buffers, closing the port,
        and optionally reopening it.

        Parameters:
            close_only (bool): If True, only closes the port without reopening (default is False).
        """
        if not self._interface.is_open:
            self._interface.open()
        self._interface.flushInput()
        self._interface.flushOutput()
        self._interface.close()
        if not close_only:
            self._interface.open()
        

def main(config = {"port": 'COM8',
                        "baudrate": 2_000_000,
                        "timeout": None,
                        "exclusive": True}):
    """ Function to test triggerBox implementation"""        
   
    trigger = BPTriggerBox(port_config = config)
    
    """ Send Trigger 1."""
    trigger.send(1)
    time.sleep(3)
    """ Send Trigger 200."""
    trigger.send(200)
    time.sleep(3)
    """ Send Trigger 50."""
    trigger.send(50)
    
    
if __name__ == "main":
    main()
