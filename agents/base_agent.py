from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for all agents in the energy system"""
    
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.status = "initialized"
        self.log_messages = []
        
    def log_action(self, action: str) -> None:
        """Log agent actions"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'agent_id': self.agent_id,
            'action': action
        }
        self.log_messages.append(log_entry)
        logger.info(f"[{self.agent_id}] {action}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            'agent_id': self.agent_id,
            'type': self.agent_type,
            'status': self.status,
            'log_count': len(self.log_messages)
        }
    
    def send_message(self, recipient_id: str, message_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a message to send to another agent"""
        return {
            'sender_id': self.agent_id,
            'recipient_id': recipient_id,
            'message_type': message_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }