"""Mock data for testing without live devices"""

MOCK_DEVICE_RESPONSES = {
    "show ip ssh": """
SSH Enabled - version 2.0
Authentication methods: publickey,password
Authentication Retries: 3
""",
    "show running-config | include service password-encryption": "service password-encryption",
    "show running-config | include banner": "banner motd ^C Unauthorized access prohibited ^C",
    "show running-config | include exec-timeout": "exec-timeout 10 0",
    "show running-config | include snmp-server community": "snmp-server community MySecret RW"
}

class MockDeviceConnector:
    """Mock connector for testing"""
    
    def __init__(self, device_info):
        self.device_info = device_info
        self.responses = MOCK_DEVICE_RESPONSES
    
    def connect(self):
        return True
    
    def send_command(self, command):
        # Return mock response or None if not found
        return self.responses.get(command, "")
    
    def disconnect(self):
        pass