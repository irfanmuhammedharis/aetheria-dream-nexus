# apps/backend/services/analysis_engine.py
import sys
import os
from datetime import datetime
from typing import Dict, List
import hashlib
import json

# Add packages to path - use absolute path resolution
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
repo_root = os.path.dirname(os.path.dirname(backend_dir))
sys.path.insert(0, os.path.join(repo_root, 'packages', 'shared-schema', 'src'))

from schemas import (
    DecagonAnalysisObject,
    ShadowWeaveNode,
    NakshatraSnapshot,
    ArabicLot,
    DashaPeriod,
    SomaticResonance,
    FirdariaPhase,
    Planet,
    Nakshatra,
    InputModality,
    PsychologicalPressure
)

# Import time_keeper from same directory
from time_keeper import (
    calculate_julian_day,
    get_planet_position,
    calculate_nakshatra,
    calculate_ascendant,
    lot_of_fortune,
    lot_of_spirit,
    is_day_chart,
    calculate_firdaria
)

import swisseph as swe


class DecagonAnalyzer:
    """
    Orchestrates the 10-dimensional analysis of a dream + birth data.
    All astronomical calculations are deterministic (Swiss Ephemeris).
    """
    
    def __init__(self):
        self.version = "1.0.0"
    
    def analyze(self, dream_content: str, birth_datetime: datetime, birth_lat: float, birth_lon: float, current_datetime: datetime, user_id: str) -> DecagonAnalysisObject:
        """
        Main analysis method - composes all 10 dimensions.
        
        Args:
            dream_content: The dream narrative
            birth_datetime: User's birth date/time (UT)
            birth_lat: Birth latitude
            birth_lon: Birth longitude
            current_datetime: When dream occurred
            user_id: User ID for checksum
        
        Returns:
            DecagonAnalysisObject with all 10 analysis dimensions
        """
        # Calculate Julian Days
        birth_jd = calculate_julian_day(birth_datetime)
        current_jd = calculate_julian_day(current_datetime)
        
        # Get natal positions
        natal_moon = get_planet_position(birth_jd, swe.MOON)
        natal_asc = calculate_ascendant(birth_jd, birth_lat, birth_lon)
        
        # Get current (transit) positions
        transit_sun = get_planet_position(current_jd, swe.SUN)
        transit_moon = get_planet_position(current_jd, swe.MOON)
        transit_mercury = get_planet_position(current_jd, swe.MERCURY)
        transit_venus = get_planet_position(current_jd, swe.VENUS)
        transit_mars = get_planet_position(current_jd, swe.MARS)
        transit_jupiter = get_planet_position(current_jd, swe.JUPITER)
        transit_saturn = get_planet_position(current_jd, swe.SATURN)
        
        current_asc = calculate_ascendant(current_jd, birth_lat, birth_lon)
        
        # Calculate day/night chart
        is_day = is_day_chart(transit_sun, current_asc)
        
        # Calculate age
        age = (current_datetime - birth_datetime).days / 365.25
        
        # ========================================================================
        # DIMENSION 1: Shadow-Weave (Jungian Archetypal Analysis)
        # ========================================================================
        shadow_weave = self._analyze_shadow_weave(dream_content, transit_moon, natal_moon)
        
        # ========================================================================
        # DIMENSION 2: Celestial Transit (Current planetary pressures)
        # ========================================================================
        celestial_transits = self._analyze_celestial_transits(
            transit_sun, transit_moon, transit_mercury, transit_venus,
            transit_mars, transit_jupiter, transit_saturn
        )
        
        # ========================================================================
        # DIMENSION 3: Nakshatra Snapshot (27 Lunar Mansions)
        # ========================================================================
        nakshatra_snapshot = self._analyze_nakshatra(transit_moon)
        
        # ========================================================================
        # DIMENSION 4: Arabic Lots (Hermetic Fortune/Spirit)
        # ========================================================================
        arabic_lots = self._analyze_arabic_lots(current_asc, transit_sun, transit_moon, is_day)
        
        # ========================================================================
        # DIMENSION 5: Dasha Period (Vedic Planetary Periods)
        # ========================================================================
        dasha_period = self._analyze_dasha(age)
        
        # ========================================================================
        # DIMENSION 6: Somatic Resonance (Biometric stub - real HRV in production)
        # ========================================================================
        somatic_resonance = self._analyze_somatic_resonance()
        
        # ========================================================================
        # DIMENSION 7: Ancestral Ghost (Archetypal inheritance - stub)
        # ========================================================================
        ancestral_ghost = None  # Optional - not implemented yet
        
        # ========================================================================
        # DIMENSION 8: Collective Ripple (Cultural zeitgeist - stub)
        # ========================================================================
        collective_ripple = None  # Optional - requires Pinecone cohort search
        
        # ========================================================================
        # DIMENSION 9: Digital Doppelganger (AI reflection - stub)
        # ========================================================================
        digital_doppelganger = None  # Optional
        
        # ========================================================================
        # DIMENSION 10: Firdaria Phase (Persian Time-Lords)
        # ========================================================================
        firdaria_phase = self._analyze_firdaria(age, is_day)
        
        # Generate deterministic checksum
        checksum_data = f"{user_id}:{dream_content}:{birth_jd}:{current_jd}"
        checksum = hashlib.sha256(checksum_data.encode()).hexdigest()[:16]
        
        return DecagonAnalysisObject(
            analysis_id=f"DEC-{checksum}",
            timestamp=current_datetime,
            shadow_weave=shadow_weave,
            celestial_transit=celestial_transits,
            nakshatra_snapshot=nakshatra_snapshot,
            arabic_lot=arabic_lots,
            dasha_period=dasha_period,
            somatic_resonance=somatic_resonance,
            ancestral_ghost=ancestral_ghost,
            collective_ripple=collective_ripple,
            digital_doppelganger=digital_doppelganger,
            firdaria_phase=firdaria_phase
        )
    
    def _analyze_shadow_weave(self, dream_content: str, transit_moon: float, natal_moon: float) -> List[ShadowWeaveNode]:
        """Jungian archetypal analysis (simplified stub - real LLM analysis in production)"""
        # In production: Use LLM to extract archetypal symbols
        # For now: Return hardcoded example based on moon position
        
        # Moon in Ashlesha (serpent) - shadow confrontation theme
        if 104 <= transit_moon <= 116.67:
            return [
                ShadowWeaveNode(
                    archetype_id="SHADOW",
                    activation_strength=0.85,
                    integration_status="CONFRONTATION",
                    symbolic_fragments=["serpent", "basement", "flood", "darkness"],
                    mythological_resonance="Naga mythology: serpent as guardian of unconscious depths"
                )
            ]
        
        # Default fallback
        return [
            ShadowWeaveNode(
                archetype_id="SELF",
                activation_strength=0.5,
                integration_status="UNCONSCIOUS",
                symbolic_fragments=["dream", "night", "vision"],
                mythological_resonance="Generic archetypal activation"
            )
        ]
    
    def _analyze_celestial_transits(self, sun, moon, mercury, venus, mars, jupiter, saturn) -> List[Dict]:
        """Map current planetary positions to psychological pressures"""
        transits = []
        
        transits.append({
            "planet": Planet.SUN.value,
            "longitude": sun,
            "house_position": int(sun / 30) + 1,  # Simplified house
            "pressure_type": PsychologicalPressure.FLOW.value,
            "intensity": 0.7
        })
        
        transits.append({
            "planet": Planet.MOON.value,
            "longitude": moon,
            "house_position": int(moon / 30) + 1,
            "pressure_type": PsychologicalPressure.FRICTION.value,
            "intensity": 0.9
        })
        
        transits.append({
            "planet": Planet.SATURN.value,
            "longitude": saturn,
            "house_position": int(saturn / 30) + 1,
            "pressure_type": PsychologicalPressure.RESTRICTION.value,
            "intensity": 0.6
        })
        
        return transits
    
    def _analyze_nakshatra(self, moon_longitude: float) -> NakshatraSnapshot:
        """Calculate current Nakshatra from Moon position"""
        name, pada, deity, theme = calculate_nakshatra(moon_longitude)
        
        # Map name string to enum
        nakshatra_enum = Nakshatra[name.upper().replace(" ", "_")]
        
        # Determine ruling planet (Vimshottari rulership)
        ruling_planet_map = {
            0: Planet.KETU, 1: Planet.VENUS, 2: Planet.SUN, 3: Planet.MOON,
            4: Planet.MARS, 5: Planet.RAHU, 6: Planet.JUPITER, 7: Planet.SATURN,
            8: Planet.MERCURY
        }
        nakshatra_index = list(Nakshatra).index(nakshatra_enum)
        ruling_planet = ruling_planet_map[nakshatra_index % 9]
        
        return NakshatraSnapshot(
            nakshatra=nakshatra_enum,
            pada=pada,
            ruling_planet=ruling_planet,
            deity=deity,
            archetypal_theme=theme
        )
    
    def _analyze_arabic_lots(self, asc: float, sun: float, moon: float, is_day: bool) -> List[ArabicLot]:
        """Calculate Arabic Lots/Parts"""
        fortune = lot_of_fortune(asc, sun, moon, is_day)
        spirit = lot_of_spirit(asc, sun, moon, is_day)
        
        return [
            ArabicLot(
                lot_name="Lot of Fortune",
                longitude=fortune,
                house_position=int(fortune / 30) + 1,
                hermetic_meaning="Material fortune, body, physical manifestation"
            ),
            ArabicLot(
                lot_name="Lot of Spirit",
                longitude=spirit,
                house_position=int(spirit / 30) + 1,
                hermetic_meaning="Spiritual fortune, soul, divine will"
            )
        ]
    
    def _analyze_dasha(self, age: float) -> DashaPeriod:
        """Calculate Vimshottari Dasha (simplified - full calculation needs natal Moon Nakshatra)"""
        # In production: Calculate exact dasha balance from natal Moon
        # For now: Simplified planetary period assignment
        
        total_cycle = 120  # Vimshottari = 120 years
        dasha_sequence = [
            (Planet.KETU, 7), (Planet.VENUS, 20), (Planet.SUN, 6),
            (Planet.MOON, 10), (Planet.MARS, 7), (Planet.RAHU, 18),
            (Planet.JUPITER, 16), (Planet.SATURN, 19), (Planet.MERCURY, 17)
        ]
        
        age_in_cycle = age % total_cycle
        cursor = 0
        
        for planet, duration in dasha_sequence:
            if cursor <= age_in_cycle < cursor + duration:
                return DashaPeriod(
                    maha_dasha_lord=planet,
                    antardasha_lord=planet,  # Simplified - should be sub-period
                    start_date=datetime.now(),  # Stub
                    end_date=datetime.now(),  # Stub
                    karmic_theme=f"{planet.value} period: Karmic lessons of {planet.value}"
                )
            cursor += duration
        
        # Fallback
        return DashaPeriod(
            maha_dasha_lord=Planet.SUN,
            antardasha_lord=Planet.SUN,
            start_date=datetime.now(),
            end_date=datetime.now(),
            karmic_theme="Solar period: Authority, self-expression"
        )
    
    def _analyze_somatic_resonance(self) -> SomaticResonance:
        """Biometric analysis stub - real HRV data in production"""
        return SomaticResonance(
            hrv_snapshot=[0.5 + (i % 10) * 0.05 for i in range(100)],  # Mock sine wave
            biometric_context={"sleep_phase": "REM", "heart_rate_avg": 65},
            body_map_activations={"chest": 0.7, "throat": 0.4, "solar_plexus": 0.6}
        )
    
    def _analyze_firdaria(self, age: float, is_day: bool) -> FirdariaPhase:
        """Persian time-lord system"""
        firdaria_data = calculate_firdaria(age, is_day)
        
        return FirdariaPhase(
            ruling_planet=Planet(firdaria_data["ruling_planet"]),
            start_age=firdaria_data["start_age"],
            end_age=firdaria_data["end_age"],
            current_phase=True,
            archetypal_task=firdaria_data["archetypal_task"]
        )
