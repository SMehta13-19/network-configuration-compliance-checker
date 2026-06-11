"""
Device Connector Module - Handles SSH connections to network devices
"""
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DeviceConnector:
    """Handles SSH connections to network devices with retry logic"""
    
    def __init__(self, device_info, max_retries=2):
        self.device_info = device_info
        self.connection = None
        self.max_retries = max_retries
        self.hostname = device_info.get('host', device_info.get('ip', 'Unknown'))
        
    def connect(self):
        """Establish SSH connection to device with retry logic"""
        for attempt in range(self.max_retries):
            try:
                # Prepare device parameters for Netmiko
                device_params = {
                    'device_type': self.device_info.get('device_type', 'cisco_ios'),
                    'host': self.device_info.get('host', self.device_info.get('ip')),
                    'username': self.device_info.get('username'),
                    'password': self.device_info.get('password'),
                    'port': int(self.device_info.get('port', 22)),
                    'timeout': 10,
                    'session_timeout': 30,
                    'conn_timeout': 10
                }
                
                # Remove None values
                device_params = {k: v for k, v in device_params.items() if v is not None}
                
                # Add enable secret if provided
                if 'secret' in self.device_info and self.device_info['secret']:
                    device_params['secret'] = self.device_info['secret']
                
                logger.info(f"Attempting to connect to {self.hostname} (attempt {attempt + 1}/{self.max_retries})")
                self.connection = ConnectHandler(**device_params)
                
                # Enter enable mode if secret is provided and device type supports it
                if 'secret' in device_params and 'cisco' in device_params['device_type']:
                    try:
                        self.connection.enable()
                    except:
                        logger.debug(f"Enable mode not supported or already enabled on {self.hostname}")
                
                logger.info(f"✓ Successfully connected to {self.hostname}")
                return True
                
            except NetmikoTimeoutException:
                logger.error(f"Timeout connecting to {self.hostname} - check IP/connectivity")
                if attempt < self.max_retries - 1:
                    time.sleep(2)
                
            except NetmikoAuthenticationException:
                logger.error(f"Authentication failed for {self.hostname} - check credentials")
                return False
                
            except Exception as e:
                logger.error(f"Unexpected error connecting to {self.hostname}: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(2)
        
        return False
    
    def send_command(self, command, delay_factor=1, max_loops=100):
        """Send command and return output"""
        if not self.connection:
            raise Exception(f"Not connected to {self.hostname}")
        
        try:
            logger.debug(f"Sending command to {self.hostname}: {command[:50]}...")
            output = self.connection.send_command(
                command, 
                delay_factor=delay_factor,
                max_loops=max_loops,
                expect_string=r'[>#]'
            )
            return output
        except Exception as e:
            logger.error(f"Command '{command[:50]}...' failed on {self.hostname}: {str(e)}")
            return None
    
    def disconnect(self):
        """Close SSH connection"""
        if self.connection:
            try:
                self.connection.disconnect()
                logger.info(f"Disconnected from {self.hostname}")
            except:
                pass