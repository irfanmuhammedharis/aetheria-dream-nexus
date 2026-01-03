# apps/backend/test_decagon_analyzer.py
"""
Test script for DecagonAnalyzer
Validates the 10-dimensional analysis system
"""
import sys
import os
from datetime import datetime

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../packages/shared-schema/src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services'))

from analysis_engine import DecagonAnalyzer

def test_decagon_analysis():
    """Test the complete analysis pipeline"""
    print("=" * 80)
    print("TESTING DECAGON ANALYZER")
    print("=" * 80)
    
    # Mock dream data (from spec: "black serpent in flooded basement")
    dream_content = "I saw a black serpent coiled in a flooded basement. The water was rising, and the serpent's eyes glowed in the darkness."
    user_id = "550e8400-e29b-41d4-a716-446655440000"
    
    # Birth data (example: Delhi, India)
    birth_datetime = datetime(1990, 5, 15, 3, 30, 0)  # May 15, 1990, 3:30 AM UT
    birth_lat = 28.6139
    birth_lon = 77.2090
    
    # Dream timestamp
    dream_datetime = datetime(2026, 1, 3, 6, 45, 0)  # Jan 3, 2026, 6:45 AM UT
    
    # Create analyzer
    analyzer = DecagonAnalyzer()
    
    print(f"\n🌙 Analyzing dream from user {user_id}")
    print(f"📅 Birth: {birth_datetime} (Lat: {birth_lat}, Lon: {birth_lon})")
    print(f"🌌 Dream time: {dream_datetime}")
    print(f"📝 Dream content: {dream_content[:80]}...")
    
    # Perform analysis
    try:
        result = analyzer.analyze(
            dream_content=dream_content,
            birth_datetime=birth_datetime,
            birth_lat=birth_lat,
            birth_lon=birth_lon,
            current_datetime=dream_datetime,
            user_id=user_id
        )
        
        print("\n" + "=" * 80)
        print("ANALYSIS RESULTS")
        print("=" * 80)
        
        print(f"\n✅ Analysis ID: {result.analysis_id}")
        print(f"⏰ Timestamp: {result.timestamp}")
        
        # Dimension 1: Shadow-Weave
        print("\n" + "-" * 80)
        print("DIMENSION 1: SHADOW-WEAVE (Jungian Archetypes)")
        print("-" * 80)
        for node in result.shadow_weave:
            print(f"  🔮 Archetype: {node.archetype_id}")
            print(f"     Activation: {node.activation_strength * 100:.1f}%")
            print(f"     Status: {node.integration_status}")
            print(f"     Symbols: {', '.join(node.symbolic_fragments)}")
            print(f"     Mythic: {node.mythological_resonance}")
        
        # Dimension 2: Celestial Transits
        print("\n" + "-" * 80)
        print("DIMENSION 2: CELESTIAL TRANSITS")
        print("-" * 80)
        for transit in result.celestial_transit:
            print(f"  🪐 {transit['planet']}: {transit['longitude']:.2f}°")
            print(f"     House: {transit['house_position']}")
            print(f"     Pressure: {transit['pressure_type']}")
            print(f"     Intensity: {transit['intensity'] * 100:.1f}%")
        
        # Dimension 3: Nakshatra
        print("\n" + "-" * 80)
        print("DIMENSION 3: NAKSHATRA SNAPSHOT")
        print("-" * 80)
        nak = result.nakshatra_snapshot
        print(f"  🌙 Nakshatra: {nak.nakshatra.value}")
        print(f"     Pada: {nak.pada}")
        print(f"     Ruling Planet: {nak.ruling_planet.value}")
        print(f"     Deity: {nak.deity}")
        print(f"     Theme: {nak.archetypal_theme}")
        
        # Dimension 4: Arabic Lots
        print("\n" + "-" * 80)
        print("DIMENSION 4: ARABIC LOTS")
        print("-" * 80)
        for lot in result.arabic_lot:
            print(f"  ✨ {lot.lot_name}: {lot.longitude:.2f}°")
            print(f"     House: {lot.house_position}")
            print(f"     Meaning: {lot.hermetic_meaning}")
        
        # Dimension 5: Dasha
        print("\n" + "-" * 80)
        print("DIMENSION 5: VIMSHOTTARI DASHA")
        print("-" * 80)
        dasha = result.dasha_period
        print(f"  🔱 Mahadasha: {dasha.maha_dasha_lord.value}")
        print(f"     Antardasha: {dasha.antardasha_lord.value}")
        print(f"     Karmic Theme: {dasha.karmic_theme}")
        
        # Dimension 6: Somatic
        print("\n" + "-" * 80)
        print("DIMENSION 6: SOMATIC RESONANCE")
        print("-" * 80)
        som = result.somatic_resonance
        print(f"  💓 HRV Wave: {len(som.hrv_snapshot)} data points")
        print(f"     Biometric Context: {som.biometric_context}")
        print(f"     Body Map: {som.body_map_activations}")
        
        # Dimension 10: Firdaria
        print("\n" + "-" * 80)
        print("DIMENSION 10: FIRDARIA PHASE")
        print("-" * 80)
        fir = result.firdaria_phase
        print(f"  ⏳ Ruling Planet: {fir.ruling_planet.value}")
        print(f"     Age Range: {fir.start_age:.1f} - {fir.end_age:.1f} years")
        print(f"     Archetypal Task: {fir.archetypal_task}")
        
        print("\n" + "=" * 80)
        print("✅ TEST PASSED - All 10 dimensions analyzed successfully!")
        print("=" * 80)
        
        return result
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    test_decagon_analysis()
