"""
Hospital Registry Module

Purpose:
- Maintain trusted hospital metadata
- Support city-based selection
- Provide booking websites, OPD fee, Google Maps links
- Enable cost alignment via hospital tier
"""

# =====================================================
# HOSPITAL REGISTRY DATA
# =====================================================
HOSPITAL_REGISTRY = {
    "bangalore": {
        "apollo": {
            "display_name": "Apollo Hospitals, Bangalore",
            "tier": "premium",
            "cost_multiplier": 1.25,
            "opd_fee": "₹800 – ₹1,200",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Apollo_Hospitals_Logo.svg",
            "google_maps": "https://www.google.com/maps/search/Apollo+Hospitals+Bangalore",
            "booking_websites": [
                "https://www.apollohospitals.com/book-appointment/",
                "https://www.practo.com/apollo-hospitals-bangalore",
                "https://www.mfine.co/apollo-hospitals"
            ]
        },

        "fortis": {
            "display_name": "Fortis Hospital, Bangalore",
            "tier": "premium",
            "cost_multiplier": 1.15,
            "opd_fee": "₹700 – ₹1,000",
            "logo": "https://upload.wikimedia.org/wikipedia/en/8/8a/Fortis_Healthcare_logo.svg",
            "google_maps": "https://www.google.com/maps/search/Fortis+Hospital+Bangalore",
            "booking_websites": [
                "https://www.fortishealthcare.com/book-an-appointment",
                "https://www.practo.com/fortis-hospital-bangalore"
            ]
        },

        "manipal": {
            "display_name": "Manipal Hospital, Bangalore",
            "tier": "standard",
            "cost_multiplier": 1.0,
            "opd_fee": "₹500 – ₹800",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Manipal_Hospitals_logo.png",
            "google_maps": "https://www.google.com/maps/search/Manipal+Hospital+Bangalore",
            "booking_websites": [
                "https://www.manipalhospitals.com/book-an-appointment/",
                "https://www.practo.com/manipal-hospitals-bangalore"
            ]
        },

        "narayana": {
            "display_name": "Narayana Health, Bangalore",
            "tier": "standard",
            "cost_multiplier": 0.9,
            "opd_fee": "₹400 – ₹700",
            "logo": "https://upload.wikimedia.org/wikipedia/en/3/3f/Narayana_Health_logo.svg",
            "google_maps": "https://www.google.com/maps/search/Narayana+Health+Bangalore",
            "booking_websites": [
                "https://www.narayanahealth.org/book-an-appointment",
                "https://www.practo.com/narayana-health-bangalore"
            ]
        }
    }
}


# =====================================================
# HELPER FUNCTIONS
# =====================================================
def find_hospital(city: str, hospital_name: str):
    """
    Match hospital from extracted hospital name and city.

    Args:
        city (str): Selected city (lowercase)
        hospital_name (str): Hospital name from report

    Returns:
        dict or None: Hospital metadata if found
    """
    if not hospital_name or not city:
        return None

    city = city.lower()
    hospital_name = hospital_name.lower()

    hospitals = HOSPITAL_REGISTRY.get(city, {})

    for key, data in hospitals.items():
        if key in hospital_name:
            return data

    return None


def get_fallback_hospitals(city: str, limit: int = 2):
    """
    Return fallback hospitals for a city.

    Args:
        city (str): Selected city
        limit (int): Number of hospitals to return

    Returns:
        list: Hospital metadata list
    """
    city = city.lower()
    hospitals = list(HOSPITAL_REGISTRY.get(city, {}).values())
    return hospitals[:limit]
