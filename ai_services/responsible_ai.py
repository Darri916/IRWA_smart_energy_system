"""
Responsible AI Module
Implements fairness, transparency, explainability, and audit logging
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import logging
from pathlib import Path

from config.settings import Config

logger = logging.getLogger(__name__)


class ResponsibleAI:
    """
    Responsible AI framework for ethical AI deployment
    Covers: Fairness, Explainability, Transparency, Privacy, Audit
    """
    
    def __init__(self):
        self.audit_log = []
        self.bias_checks = []
        self.explainability_enabled = Config.ENABLE_EXPLAINABILITY
        self.audit_enabled = Config.ENABLE_AUDIT_LOGGING
        
        # Ensure audit directory exists
        self.audit_dir = Config.LOGS_DIR / "responsible_ai"
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("✓ Responsible AI framework initialized")
    
    def log_decision(self, decision_data: Dict[str, Any]) -> None:
        """
        Log AI decisions for transparency and audit trail
        """
        if not self.audit_enabled:
            return
        
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'decision_type': decision_data.get('type', 'unknown'),
            'decision': decision_data.get('decision'),
            'confidence': decision_data.get('confidence'),
            'input_data': decision_data.get('input_data', {}),
            'reasoning': decision_data.get('reasoning'),
            'impact': decision_data.get('impact', 'medium'),
            'agent_id': decision_data.get('agent_id'),
            'user_id': decision_data.get('user_id', 'system')
        }
        
        self.audit_log.append(audit_entry)
        
        # Write to file periodically (every 100 entries)
        if len(self.audit_log) % 100 == 0:
            self._write_audit_log()
    
    def explain_decision(self, decision_id: str = None) -> Dict[str, Any]:
        """
        Provide detailed explanation of a decision (Explainability)
        """
        if not self.explainability_enabled:
            return {'message': 'Explainability is disabled'}
        
        # Get last decision if no ID provided
        if decision_id is None and self.audit_log:
            decision = self.audit_log[-1]
        else:
            # Find specific decision
            decision = next(
                (d for d in self.audit_log if d.get('decision_id') == decision_id),
                None
            )
        
        if not decision:
            return {'message': 'Decision not found'}
        
        explanation = {
            'decision': decision.get('decision'),
            'timestamp': decision.get('timestamp'),
            'confidence': decision.get('confidence'),
            'reasoning': decision.get('reasoning'),
            'input_factors': list(decision.get('input_data', {}).keys()),
            'impact_level': decision.get('impact'),
            'agent_responsible': decision.get('agent_id'),
            'explainability_score': self._calculate_explainability_score(decision)
        }
        
        return explanation
    
    def check_bias(self, data: Dict[str, Any], check_type: str = 'general') -> Dict[str, Any]:
        """
        Check for potential biases in data or decisions (Fairness)
        """
        bias_report = {
            'timestamp': datetime.now().isoformat(),
            'check_type': check_type,
            'biases_detected': [],
            'fairness_score': 1.0,
            'recommendations': []
        }
        
        try:
            if check_type == 'geographic':
                # Check for geographic bias
                cities = data.get('cities', [])
                if len(set(cities)) < 3:
                    bias_report['biases_detected'].append({
                        'type': 'geographic_concentration',
                        'severity': 'low',
                        'description': 'Analysis focused on limited geographic areas'
                    })
                    bias_report['fairness_score'] -= 0.1
                    bias_report['recommendations'].append(
                        'Consider expanding analysis to diverse geographic regions'
                    )
            
            elif check_type == 'temporal':
                # Check for temporal bias
                timestamps = data.get('timestamps', [])
                if timestamps:
                    # Check if data is recent enough
                    latest = max(timestamps) if timestamps else None
                    if latest:
                        age_hours = (datetime.now() - datetime.fromisoformat(latest)).total_seconds() / 3600
                        if age_hours > 24:
                            bias_report['biases_detected'].append({
                                'type': 'stale_data',
                                'severity': 'medium',
                                'description': f'Data is {age_hours:.1f} hours old'
                            })
                            bias_report['fairness_score'] -= 0.2
            
            elif check_type == 'data_quality':
                # Check for data quality issues
                if data.get('confidence', 1.0) < 0.7:
                    bias_report['biases_detected'].append({
                        'type': 'low_confidence',
                        'severity': 'medium',
                        'description': 'Predictions have low confidence levels'
                    })
                    bias_report['fairness_score'] -= 0.15
                    bias_report['recommendations'].append(
                        'Improve data quality or wait for more reliable inputs'
                    )
            
            # Check for missing critical data
            required_fields = data.get('required_fields', [])
            missing_fields = [f for f in required_fields if f not in data or data[f] is None]
            if missing_fields:
                bias_report['biases_detected'].append({
                    'type': 'incomplete_data',
                    'severity': 'high',
                    'description': f'Missing critical fields: {", ".join(missing_fields)}'
                })
                bias_report['fairness_score'] -= 0.3
                bias_report['recommendations'].append(
                    'Collect missing data before making critical decisions'
                )
            
            # Overall assessment
            bias_report['fairness_score'] = max(0.0, bias_report['fairness_score'])
            
            if bias_report['fairness_score'] >= 0.8:
                bias_report['overall_assessment'] = 'Fair - minimal bias detected'
            elif bias_report['fairness_score'] >= 0.6:
                bias_report['overall_assessment'] = 'Acceptable - some concerns present'
            else:
                bias_report['overall_assessment'] = 'Concerning - significant bias detected'
            
        except Exception as e:
            logger.error(f"Bias check failed: {e}")
            bias_report['error'] = str(e)
        
        self.bias_checks.append(bias_report)
        return bias_report
    
    def ensure_transparency(self, system_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate transparency report about system capabilities and limitations
        """
        transparency_report = {
            'timestamp': datetime.now().isoformat(),
            'system_capabilities': [],
            'limitations': [],
            'data_sources': [],
            'model_info': {},
            'privacy_measures': []
        }
        
        # Document capabilities
        transparency_report['system_capabilities'] = [
            'Real-time weather data integration',
            '5-day weather forecasting',
            'Energy demand prediction',
            'Grid balancing optimization',
            'Renewable energy potential calculation',
            'AI-powered analysis and recommendations',
            'Explainable decision-making'
        ]
        
        # Document limitations
        transparency_report['limitations'] = [
            'Weather forecasts have decreasing accuracy beyond 3 days',
            'Demand predictions assume historical patterns continue',
            'AI analysis dependent on data quality',
            'System optimized for grid capacities between 1-10 GW',
            'Real-time data may have up to 5-minute delay'
        ]
        
        # Document data sources
        transparency_report['data_sources'] = system_info.get('data_sources', [
            {
                'name': 'OpenWeatherMap API',
                'type': 'Weather Data',
                'update_frequency': '3 hours',
                'reliability': 'High'
            },
            {
                'name': 'Historical Demand Patterns',
                'type': 'Energy Demand',
                'update_frequency': 'Static',
                'reliability': 'Medium'
            }
        ])
        
        # Document AI models
        transparency_report['model_info'] = {
            'llm_provider': system_info.get('llm_provider', 'Unknown'),
            'nlp_capabilities': system_info.get('nlp_capabilities', []),
            'prediction_methods': 'Time-series analysis with weather correlation'
        }
        
        # Document privacy measures
        transparency_report['privacy_measures'] = [
            'No personal user data collected',
            'Geographic data anonymized',
            'Audit logs stored securely',
            'API keys encrypted',
            'Session data cleared after timeout'
        ]
        
        return transparency_report
    
    def privacy_check(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure data privacy and identify any sensitive information
        """
        privacy_report = {
            'timestamp': datetime.now().isoformat(),
            'sensitive_data_found': [],
            'privacy_score': 1.0,
            'recommendations': []
        }
        
        # Check for PII (Personal Identifiable Information)
        pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }
        
        data_str = json.dumps(data)
        
        for pii_type, pattern in pii_patterns.items():
            import re
            if re.search(pattern, data_str):
                privacy_report['sensitive_data_found'].append(pii_type)
                privacy_report['privacy_score'] -= 0.3
                privacy_report['recommendations'].append(
                    f'Remove or anonymize {pii_type} data'
                )
        
        # Check for location precision
        if 'coordinates' in data:
            coords = data['coordinates']
            if coords and len(str(coords.get('lat', ''))) > 6:
                privacy_report['sensitive_data_found'].append('precise_location')
                privacy_report['privacy_score'] -= 0.1
                privacy_report['recommendations'].append(
                    'Consider reducing location precision to city level'
                )
        
        privacy_report['privacy_score'] = max(0.0, privacy_report['privacy_score'])
        privacy_report['compliant'] = privacy_report['privacy_score'] >= 0.8
        
        return privacy_report
    
    def generate_impact_assessment(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess potential impact of a decision on stakeholders
        """
        impact_assessment = {
            'timestamp': datetime.now().isoformat(),
            'decision': decision.get('decision'),
            'stakeholder_impacts': {},
            'risk_level': 'low',
            'mitigation_strategies': []
        }
        
        decision_type = decision.get('type', 'general')
        
        # Assess impact on different stakeholders
        if decision_type == 'grid_balancing':
            impact_assessment['stakeholder_impacts'] = {
                'grid_operators': {
                    'impact': 'high',
                    'description': 'Direct operational implications'
                },
                'consumers': {
                    'impact': 'medium',
                    'description': 'Affects electricity reliability and pricing'
                },
                'environment': {
                    'impact': 'medium',
                    'description': 'Influences carbon emissions'
                },
                'renewable_generators': {
                    'impact': 'high',
                    'description': 'Affects renewable energy utilization'
                }
            }
            
            # Assess risk level
            grid_balance = decision.get('input_data', {}).get('grid_balance', 'BALANCED')
            if grid_balance == 'DEFICIT':
                impact_assessment['risk_level'] = 'high'
                impact_assessment['mitigation_strategies'].append(
                    'Activate emergency reserves immediately'
                )
                impact_assessment['mitigation_strategies'].append(
                    'Implement demand response programs'
                )
            elif grid_balance == 'SURPLUS':
                impact_assessment['risk_level'] = 'low'
                impact_assessment['mitigation_strategies'].append(
                    'Optimize storage charging'
                )
        
        elif decision_type == 'renewable_forecast':
            impact_assessment['stakeholder_impacts'] = {
                'renewable_generators': {
                    'impact': 'high',
                    'description': 'Affects generation planning'
                },
                'grid_operators': {
                    'impact': 'medium',
                    'description': 'Influences balancing requirements'
                }
            }
        
        return impact_assessment
    
    def get_audit_summary(self, last_n: int = 100) -> Dict[str, Any]:
        """
        Get summary of audit log for review
        """
        recent_logs = self.audit_log[-last_n:] if self.audit_log else []
        
        summary = {
            'total_decisions': len(recent_logs),
            'decision_types': {},
            'average_confidence': 0.0,
            'high_impact_decisions': 0,
            'time_range': {}
        }
        
        if not recent_logs:
            return summary
        
        # Analyze decision types
        for log in recent_logs:
            dtype = log.get('decision_type', 'unknown')
            summary['decision_types'][dtype] = summary['decision_types'].get(dtype, 0) + 1
            
            # Count high impact
            if log.get('impact') in ['high', 'critical']:
                summary['high_impact_decisions'] += 1
        
        # Calculate average confidence
        confidences = [log.get('confidence', 0) for log in recent_logs if log.get('confidence')]
        if confidences:
            summary['average_confidence'] = sum(confidences) / len(confidences)
        
        # Time range
        if recent_logs:
            summary['time_range'] = {
                'start': recent_logs[0].get('timestamp'),
                'end': recent_logs[-1].get('timestamp')
            }
        
        return summary
    
    def _calculate_explainability_score(self, decision: Dict) -> float:
        """
        Calculate how well a decision can be explained
        """
        score = 1.0
        
        # Check if reasoning is provided
        if not decision.get('reasoning'):
            score -= 0.4
        elif len(decision.get('reasoning', '')) < 20:
            score -= 0.2
        
        # Check if confidence is provided
        if decision.get('confidence') is None:
            score -= 0.2
        
        # Check if input data is documented
        if not decision.get('input_data'):
            score -= 0.3
        
        return max(0.0, score)
    
    def _write_audit_log(self) -> None:
        """
        Write audit log to file
        """
        try:
            filename = self.audit_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
            
            with open(filename, 'a') as f:
                for entry in self.audit_log[-100:]:  # Write last 100 entries
                    f.write(json.dumps(entry) + '\n')
            
            logger.info(f"Audit log written: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get Responsible AI framework status
        """
        return {
            'explainability_enabled': self.explainability_enabled,
            'audit_enabled': self.audit_enabled,
            'total_decisions_logged': len(self.audit_log),
            'bias_checks_performed': len(self.bias_checks),
            'features': [
                'decision_logging',
                'explainability',
                'bias_detection',
                'transparency_reporting',
                'privacy_protection',
                'impact_assessment'
            ]
        }
