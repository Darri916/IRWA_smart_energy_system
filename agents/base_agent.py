from datetime import datetime
from typing import Dict, Any, List, Optional
import logging
import uuid
import json
from enum import Enum

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent operational status"""
    INITIALIZED = "initialized"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    IDLE = "idle"


class MessageType(Enum):
    """Message types for agent communication"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"
    ACKNOWLEDGMENT = "acknowledgment"


class BaseAgent:
    """
    Enhanced base class for all agents with MCP-style communication
    and responsible AI features
    """
    
    def __init__(self, agent_id: str, agent_type: str, capabilities: List[str] = None):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.capabilities = capabilities or []
        self.status = AgentStatus.INITIALIZED
        self.log_messages = []
        self.message_queue = []
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        
        # Metrics for monitoring
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0.0
        }
        
        # Responsible AI tracking
        self.decision_log = []
        
        logger.info(f"Agent {self.agent_id} ({self.agent_type}) initialized")
        self.status = AgentStatus.IDLE
    
    def log_action(self, action: str, level: str = "info", metadata: Dict = None) -> None:
        """Enhanced logging with metadata"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'action': action,
            'level': level,
            'metadata': metadata or {}
        }
        
        self.log_messages.append(log_entry)
        self.last_active = datetime.now()
        
        # Log to system logger
        log_method = getattr(logger, level.lower(), logger.info)
        log_method(f"[{self.agent_id}] {action}")
    
    def log_decision(self, decision: str, reasoning: str, confidence: float, 
                     input_data: Dict = None, impact: str = "medium") -> None:
        """
        Log decisions for explainability and audit trail (Responsible AI)
        """
        decision_entry = {
            'timestamp': datetime.now().isoformat(),
            'decision': decision,
            'reasoning': reasoning,
            'confidence': confidence,
            'input_data': input_data or {},
            'impact': impact,
            'agent_id': self.agent_id
        }
        
        self.decision_log.append(decision_entry)
        self.log_action(f"Decision: {decision}", metadata={'confidence': confidence})
    
    def create_message(self, recipient_id: str, message_type: MessageType, 
                       data: Dict[str, Any], priority: int = 5) -> Dict[str, Any]:
        """
        Create a structured message following MCP-style protocol
        
        Args:
            recipient_id: Target agent ID
            message_type: Type of message
            data: Message payload
            priority: Message priority (1-10, 10 highest)
        """
        message = {
            'message_id': str(uuid.uuid4()),
            'sender_id': self.agent_id,
            'sender_type': self.agent_type,
            'recipient_id': recipient_id,
            'message_type': message_type.value,
            'priority': priority,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'requires_response': message_type == MessageType.REQUEST
        }
        
        self.log_action(f"Message created for {recipient_id}", metadata={
            'message_id': message['message_id'],
            'type': message_type.value
        })
        
        return message
    
    def send_message(self, recipient_id: str, message_type: MessageType, 
                     data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message to another agent"""
        message = self.create_message(recipient_id, message_type, data)
        self.message_queue.append(message)
        return message
    
    def receive_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process received message and generate response
        """
        self.log_action(f"Received message from {message.get('sender_id')}", 
                       metadata={'message_id': message.get('message_id')})
        
        # Acknowledge receipt
        acknowledgment = self.create_message(
            message['sender_id'],
            MessageType.ACKNOWLEDGMENT,
            {'original_message_id': message['message_id']}
        )
        
        return acknowledgment
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status"""
        return {
            'agent_id': self.agent_id,
            'type': self.agent_type,
            'status': self.status.value,
            'capabilities': self.capabilities,
            'created_at': self.created_at.isoformat(),
            'last_active': self.last_active.isoformat(),
            'log_count': len(self.log_messages),
            'message_queue_size': len(self.message_queue),
            'metrics': self.metrics,
            'decision_count': len(self.decision_log)
        }
    
    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        """Get recent log entries"""
        return self.log_messages[-count:]
    
    def get_decision_history(self, count: int = 5) -> List[Dict]:
        """Get recent decision history for explainability"""
        return self.decision_log[-count:]
    
    def update_metrics(self, success: bool, response_time: float) -> None:
        """Update agent performance metrics"""
        self.metrics['total_requests'] += 1
        
        if success:
            self.metrics['successful_requests'] += 1
        else:
            self.metrics['failed_requests'] += 1
        
        # Update average response time
        total = self.metrics['total_requests']
        current_avg = self.metrics['average_response_time']
        self.metrics['average_response_time'] = (
            (current_avg * (total - 1) + response_time) / total
        )
    
    def set_status(self, status: AgentStatus) -> None:
        """Update agent status"""
        old_status = self.status
        self.status = status
        self.log_action(f"Status changed: {old_status.value} -> {status.value}")
    
    def reset(self) -> None:
        """Reset agent state"""
        self.message_queue.clear()
        self.status = AgentStatus.IDLE
        self.log_action("Agent reset")
    
    def explain_last_decision(self) -> Optional[Dict]:
        """
        Return explanation of last decision (Responsible AI - Explainability)
        """
        if not self.decision_log:
            return None
        
        last_decision = self.decision_log[-1]
        return {
            'decision': last_decision['decision'],
            'reasoning': last_decision['reasoning'],
            'confidence': last_decision['confidence'],
            'timestamp': last_decision['timestamp'],
            'factors_considered': list(last_decision['input_data'].keys())
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get agent health status for monitoring"""
        uptime = (datetime.now() - self.created_at).total_seconds()
        success_rate = (
            self.metrics['successful_requests'] / self.metrics['total_requests'] * 100
            if self.metrics['total_requests'] > 0 else 100
        )
        
        return {
            'agent_id': self.agent_id,
            'healthy': self.status not in [AgentStatus.ERROR],
            'status': self.status.value,
            'uptime_seconds': round(uptime, 2),
            'uptime_hours': round(uptime / 3600, 2),
            'success_rate': round(success_rate, 2),
            'avg_response_time_ms': round(self.metrics['average_response_time'] * 1000, 2),
            'total_requests': self.metrics['total_requests'],
            'failed_requests': self.metrics['failed_requests'],
            'last_active': self.last_active.isoformat()
        }
    
    def __repr__(self) -> str:
        return f"<{self.agent_type}(id={self.agent_id}, status={self.status.value})>"
