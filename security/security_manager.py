"""
Security Manager
Implements authentication, encryption, input validation, and session management
"""

import hashlib
import secrets
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging
import jwt
from cryptography.fernet import Fernet
import base64

from config.settings import Config

logger = logging.getLogger(__name__)


class SecurityManager:
    """
    Comprehensive security manager for the energy system
    """
    
    def __init__(self):
        self.sessions = {}
        self.failed_attempts = {}
        self.blocked_ips = set()
        
        # Initialize encryption
        self.cipher_suite = None
        self._init_encryption()
        
        logger.info("✓ Security Manager initialized")
    
    def _init_encryption(self):
        """Initialize encryption cipher"""
        try:
            # Generate or use existing encryption key
            key = Config.SECRET_KEY.encode()
            # Ensure key is 32 bytes for Fernet
            key = base64.urlsafe_b64encode(hashlib.sha256(key).digest())
            self.cipher_suite = Fernet(key)
            logger.info("✓ Encryption initialized")
        except Exception as e:
            logger.error(f"Encryption initialization failed: {e}")
    
    # ==================== Session Management ====================
    
    def create_session(self, user_id: str = 'anonymous', ip_address: str = None) -> Dict[str, Any]:
        """Create a new user session"""
        try:
            session_id = secrets.token_urlsafe(32)
            
            session = {
                'session_id': session_id,
                'user_id': user_id,
                'ip_address': ip_address,
                'created_at': datetime.now(),
                'last_activity': datetime.now(),
                'expires_at': datetime.now() + timedelta(seconds=Config.SESSION_TIMEOUT),
                'is_active': True,
                'data': {}
            }
            
            self.sessions[session_id] = session
            
            # Clean up old sessions
            self._cleanup_expired_sessions()
            
            logger.info(f"Session created: {session_id[:8]}... for user {user_id}")
            
            return {
                'session_id': session_id,
                'expires_at': session['expires_at'].isoformat(),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Session creation failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def validate_session(self, session_id: str) -> Dict[str, Any]:
        """Validate if session is active and not expired"""
        if session_id not in self.sessions:
            return {'valid': False, 'reason': 'Session not found'}
        
        session = self.sessions[session_id]
        
        if not session['is_active']:
            return {'valid': False, 'reason': 'Session inactive'}
        
        if datetime.now() > session['expires_at']:
            self.terminate_session(session_id)
            return {'valid': False, 'reason': 'Session expired'}
        
        # Update last activity
        session['last_activity'] = datetime.now()
        
        return {
            'valid': True,
            'user_id': session['user_id'],
            'created_at': session['created_at'].isoformat()
        }
    
    def terminate_session(self, session_id: str) -> bool:
        """Terminate a session"""
        if session_id in self.sessions:
            self.sessions[session_id]['is_active'] = False
            del self.sessions[session_id]
            logger.info(f"Session terminated: {session_id[:8]}...")
            return True
        return False
    
    def _cleanup_expired_sessions(self):
        """Remove expired sessions"""
        expired = []
        for sid, session in self.sessions.items():
            if datetime.now() > session['expires_at']:
                expired.append(sid)
        
        for sid in expired:
            self.terminate_session(sid)
        
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired sessions")
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions"""
        return len(self.sessions)
    
    # ==================== Input Validation & Sanitization ====================
    
    def validate_city_input(self, city: str) -> Dict[str, Any]:
        """Validate city name input"""
        if not city or not isinstance(city, str):
            return {'valid': False, 'error': 'City must be a non-empty string'}
        
        # Remove any special characters, keep only letters, spaces, hyphens
        sanitized = re.sub(r'[^a-zA-Z\s\-]', '', city)
        
        if len(sanitized) < 2:
            return {'valid': False, 'error': 'City name too short'}
        
        if len(sanitized) > 50:
            return {'valid': False, 'error': 'City name too long'}
        
        return {
            'valid': True,
            'sanitized': sanitized.strip(),
            'original': city
        }
    
    def validate_numeric_input(self, value: Any, min_val: float = None, 
                               max_val: float = None, name: str = 'value') -> Dict[str, Any]:
        """Validate numeric input"""
        try:
            numeric_value = float(value)
            
            if min_val is not None and numeric_value < min_val:
                return {'valid': False, 'error': f'{name} must be >= {min_val}'}
            
            if max_val is not None and numeric_value > max_val:
                return {'valid': False, 'error': f'{name} must be <= {max_val}'}
            
            return {
                'valid': True,
                'value': numeric_value
            }
            
        except (ValueError, TypeError):
            return {'valid': False, 'error': f'{name} must be a number'}
    
    def sanitize_text_input(self, text: str, max_length: int = 1000) -> str:
        """Sanitize text input to prevent injection attacks"""
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove script tags and content
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove SQL injection patterns
        sql_patterns = [
            r"(\bUNION\b|\bSELECT\b|\bDROP\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b)",
            r"(--|;|'|\"|\/\*|\*\/)"
        ]
        
        for pattern in sql_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Limit length
        text = text[:max_length]
        
        return text.strip()
    
    def validate_api_key(self, api_key: str, service: str = 'general') -> Dict[str, Any]:
        """Validate API key format"""
        if not api_key or not isinstance(api_key, str):
            return {'valid': False, 'error': 'Invalid API key format'}
        
        # Check minimum length
        if len(api_key) < 20:
            return {'valid': False, 'error': 'API key too short'}
        
        # Check for valid characters (alphanumeric, dashes, underscores)
        if not re.match(r'^[a-zA-Z0-9\-_]+$', api_key):
            return {'valid': False, 'error': 'API key contains invalid characters'}
        
        return {'valid': True, 'service': service}
    
    # ==================== Rate Limiting ====================
    
    def check_rate_limit(self, identifier: str, limit: int = 100, 
                        window_seconds: int = 60) -> Dict[str, Any]:
        """Check if identifier has exceeded rate limit"""
        current_time = datetime.now()
        
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = []
        
        # Remove old attempts outside window
        self.failed_attempts[identifier] = [
            attempt for attempt in self.failed_attempts[identifier]
            if (current_time - attempt).seconds < window_seconds
        ]
        
        attempt_count = len(self.failed_attempts[identifier])
        
        if attempt_count >= limit:
            return {
                'allowed': False,
                'reason': 'Rate limit exceeded',
                'retry_after': window_seconds
            }
        
        # Record this attempt
        self.failed_attempts[identifier].append(current_time)
        
        return {
            'allowed': True,
            'remaining': limit - attempt_count - 1
        }
    
    def block_ip(self, ip_address: str, duration_minutes: int = 15):
        """Block an IP address temporarily"""
        self.blocked_ips.add((ip_address, datetime.now() + timedelta(minutes=duration_minutes)))
        logger.warning(f"IP blocked: {ip_address} for {duration_minutes} minutes")
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """Check if IP is blocked"""
        current_time = datetime.now()
        
        # Remove expired blocks
        self.blocked_ips = {
            (ip, expiry) for ip, expiry in self.blocked_ips
            if expiry > current_time
        }
        
        return any(ip == ip_address for ip, _ in self.blocked_ips)
    
    # ==================== Encryption & Hashing ====================
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            if self.cipher_suite:
                encrypted = self.cipher_suite.encrypt(data.encode())
                return encrypted.decode()
            else:
                logger.warning("Encryption not available, returning plain data")
                return data
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return data
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            if self.cipher_suite:
                decrypted = self.cipher_suite.decrypt(encrypted_data.encode())
                return decrypted.decode()
            else:
                logger.warning("Decryption not available, returning data as-is")
                return encrypted_data
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return encrypted_data
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${pwd_hash}"
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            salt, pwd_hash = hashed.split('$')
            test_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return test_hash == pwd_hash
        except:
            return False
    
    # ==================== JWT Token Management ====================
    
    def generate_token(self, user_id: str, expires_in: int = 3600) -> str:
        """Generate JWT token"""
        try:
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=expires_in),
                'iat': datetime.utcnow()
            }
            
            token = jwt.encode(payload, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
            return token
            
        except Exception as e:
            logger.error(f"Token generation failed: {e}")
            return None
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
            return {
                'valid': True,
                'user_id': payload['user_id'],
                'exp': payload['exp']
            }
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'error': 'Invalid token'}
    
    # ==================== Security Audit ====================
    
    def generate_security_report(self) -> Dict[str, Any]:
        """Generate security status report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'active_sessions': self.get_active_sessions_count(),
            'blocked_ips': len(self.blocked_ips),
            'rate_limited_identifiers': len(self.failed_attempts),
            'encryption_enabled': self.cipher_suite is not None,
            'security_features': [
                'Session Management',
                'Input Validation',
                'Rate Limiting',
                'IP Blocking',
                'Data Encryption',
                'JWT Authentication',
                'SQL Injection Prevention',
                'XSS Protection'
            ]
        }
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security-related events"""
        logger.warning(f"SECURITY EVENT: {event_type} - {details}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get security manager status"""
        return {
            'active_sessions': self.get_active_sessions_count(),
            'blocked_ips': len(self.blocked_ips),
            'encryption_available': self.cipher_suite is not None,
            'max_sessions': Config.MAX_SESSIONS,
            'session_timeout': Config.SESSION_TIMEOUT
        }
