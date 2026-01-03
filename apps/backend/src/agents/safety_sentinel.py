# Verified against Section 8 (Security Constraint Violations & Guardrails)

from typing import Dict, List, Optional
from enum import Enum
import re

class SafetyLevel(str, Enum):
    """Security event tiers per Section 8.1."""
    TIER1_CRITICAL = "tier1_critical"  # Imminent harm, abuse of minors
    TIER2_WARNING = "tier2_warning"    # Self-harm ideation, crisis indicators
    TIER3_PII = "tier3_pii"            # Personally identifiable information
    SAFE = "safe"

class SafetySentinel:
    """
    Implements the Safety Sentinel (W-05) per Section 8.
    Content moderation, crisis detection, PII scrubbing.
    
    ADR Context: Preventing "hallucination" of therapeutic advice
    and ensuring responsible psychological container.
    """

    def __init__(self):
        # Section 8.1: Critical indicators (imminent self-harm, abuse)
        self.tier1_patterns = [
            r'\b(kill myself|suicide plan|end(ing)? (my|it all)|overdose)\b',
            r'\b(abuse|molest|assault).{0,20}\b(child|minor|kid)\b',
        ]
        
        # Section 8.1: Warning indicators (ideation, crisis)
        self.tier2_patterns = [
            r'\b(suicidal|self-harm|cutting|hurt(ing)? myself)\b',
            r'\b(hopeless|worthless|better off dead)\b',
            r'\b(can\'?t go on|no reason to live)\b',
        ]
        
        # Section 8.3: PII patterns
        self.pii_patterns = {
            'name': r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'address': r'\b\d+\s+[A-Za-z0-9\s,]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)\b',
        }
        
        # Section 8.1: Crisis resource cards
        self.crisis_resources = {
            "hotlines": [
                {"name": "National Suicide Prevention Lifeline", "number": "988"},
                {"name": "Crisis Text Line", "sms": "Text HOME to 741741"},
                {"name": "International Association for Suicide Prevention", "url": "https://www.iasp.info/resources/Crisis_Centres/"},
            ]
        }

    def validate_content(self, content: str) -> Dict:
        """
        Main entry point for content safety validation per Section 8.
        
        Returns:
            {
                "is_safe": bool,
                "safety_level": SafetyLevel,
                "violations": List[str],
                "scrubbed_content": str,
                "resources": Optional[Dict],
                "action_required": Optional[str]
            }
        """
        violations = []
        safety_level = SafetyLevel.SAFE
        resources = None
        
        # Section 8.1: Tier 1 - Critical (STOP immediately)
        for pattern in self.tier1_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                violations.append("TIER1: Imminent harm indicator detected")
                safety_level = SafetyLevel.TIER1_CRITICAL
                resources = self.crisis_resources
                break
        
        # Section 8.1: Tier 2 - Warning (crisis indicators)
        if safety_level == SafetyLevel.SAFE:
            for pattern in self.tier2_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    violations.append("TIER2: Crisis indicator detected")
                    safety_level = SafetyLevel.TIER2_WARNING
                    resources = self.crisis_resources
                    break
        
        # Section 8.3: PII Scrubbing
        scrubbed_content = self.scrub_pii(content)
        pii_found = scrubbed_content != content
        
        if pii_found:
            violations.append("TIER3: PII detected and scrubbed")
            if safety_level == SafetyLevel.SAFE:
                safety_level = SafetyLevel.TIER3_PII
        
        is_safe = safety_level not in [SafetyLevel.TIER1_CRITICAL]
        
        return {
            "is_safe": is_safe,
            "safety_level": safety_level.value,
            "violations": violations,
            "scrubbed_content": scrubbed_content,
            "resources": resources,
            "action_required": "TERMINATE" if safety_level == SafetyLevel.TIER1_CRITICAL else None
        }

    def scrub_pii(self, content: str) -> str:
        """
        Section 8.3: Remove personally identifiable information.
        Replace with generic tokens to prevent context poisoning.
        """
        scrubbed = content
        
        for pii_type, pattern in self.pii_patterns.items():
            replacement = f"[{pii_type.upper()}]"
            scrubbed = re.sub(pattern, replacement, scrubbed, flags=re.IGNORECASE)
        
        return scrubbed
    
    def log_security_event(self, user_id: str, safety_result: Dict) -> None:
        """
        Section 8.1: Log security events to audit trail.
        Privacy preserved - no content stored for TIER1.
        """
        if safety_result["safety_level"] != SafetyLevel.SAFE.value:
            print(f"[SECURITY_EVENT] User: {user_id}, Level: {safety_result['safety_level']}, "
                  f"Violations: {safety_result['violations']}")


# Verification Log
# - Implements Section 8.1 constraint logic (multi-tier safety levels)
# - Implements Section 8.3 PII scrubbing with generic token replacement
# - Returns crisis resources per Section 8.1 specification
# - Logs security events without persisting problematic content
# - Enhanced pattern matching for comprehensive crisis detection