"""
locations.py

Location data and travel system for King John 1205.
Contains information about castles, cities, and travel distances.
"""

from typing import Dict, List, Tuple


# Location categories
LOCATION_TYPES = {
    "castle": "Royal Castle",
    "palace": "Royal Palace",
    "city": "City",
    "monastery": "Monastery/Abbey",
    "manor": "Royal Manor",
    "port": "Port/Harbor"
}


# Major locations King John visited in 1205
# Format: location_id: (display_name, type, region, description)
LOCATIONS: Dict[str, Tuple[str, str, str, str]] = {
    # Southern England - Core royal domain
    "westminster": (
        "Westminster",
        "palace",
        "southern_england",
        "The seat of royal government and chancery, home to Westminster Palace and Abbey."
    ),
    "winchester": (
        "Winchester",
        "castle",
        "southern_england",
        "Ancient capital of England, royal treasury, and major stronghold."
    ),
    "windsor": (
        "Windsor",
        "castle",
        "southern_england",
        "Favored royal residence with extensive hunting grounds along the Thames."
    ),
    "portsmouth": (
        "Portsmouth",
        "port",
        "southern_england",
        "Major naval base and embarkation point for continental campaigns."
    ),
    "portchester": (
        "Portchester",
        "castle",
        "southern_england",
        "Coastal fortress near Portsmouth, ancient Roman fort converted to royal castle."
    ),
    "guildford": (
        "Guildford",
        "castle",
        "southern_england",
        "Royal castle and hunting lodge south of London."
    ),
    "marlborough": (
        "Marlborough",
        "castle",
        "southern_england",
        "Important royal castle in Wiltshire, center of Savernake Forest."
    ),
    "clarendon": (
        "Clarendon",
        "palace",
        "southern_england",
        "Royal hunting lodge and palace near Salisbury, a favorite residence."
    ),
    "woodstock": (
        "Woodstock",
        "palace",
        "southern_england",
        "Ancestral royal palace in Oxfordshire with extensive deer parks."
    ),
    "oxford": (
        "Oxford",
        "city",
        "southern_england",
        "Important town with royal castle, growing center of learning."
    ),
    "reading": (
        "Reading",
        "monastery",
        "southern_england",
        "Major Benedictine abbey on the Thames, royal burials."
    ),
    "canterbury": (
        "Canterbury",
        "city",
        "southern_england",
        "Seat of the Archbishop, England's premier religious center."
    ),
    "dover": (
        "Dover",
        "castle",
        "southern_england",
        "Key fortress guarding the shortest crossing to France."
    ),

    # Northern England
    "york": (
        "York",
        "city",
        "northern_england",
        "Major northern city, seat of archbishop, strategic stronghold."
    ),
    "nottingham": (
        "Nottingham",
        "castle",
        "northern_england",
        "Powerful Midlands fortress, gateway to the north."
    ),
    "northampton": (
        "Northampton",
        "castle",
        "northern_england",
        "Important Midlands stronghold and administrative center."
    ),
    "lincoln": (
        "Lincoln",
        "city",
        "northern_england",
        "Major cathedral city and commercial center."
    ),

    # Welsh Marches
    "gloucester": (
        "Gloucester",
        "city",
        "welsh_marches",
        "Gateway to Wales, important administrative and military center."
    ),
    "bristol": (
        "Bristol",
        "port",
        "welsh_marches",
        "Major western port city, center of trade with Ireland and Wales."
    ),
    "shrewsbury": (
        "Shrewsbury",
        "castle",
        "welsh_marches",
        "Key fortress controlling the Welsh borderlands."
    ),
    "ludlow": (
        "Ludlow",
        "castle",
        "welsh_marches",
        "Marcher stronghold in Shropshire."
    ),

    # Other locations
    "abingdon": (
        "Abingdon",
        "monastery",
        "southern_england",
        "Abbey town on the Thames between Oxford and Reading."
    ),
    "silverstone": (
        "Silverstone",
        "manor",
        "northern_england",
        "Royal manor in Northamptonshire."
    ),
    "burbage": (
        "Burbage",
        "manor",
        "southern_england",
        "Royal manor in Savernake Forest near Marlborough."
    ),
    "hinton": (
        "Hinton",
        "monastery",
        "southern_england",
        "Carthusian priory in Somerset."
    ),
    "lambeth": (
        "Lambeth",
        "palace",
        "southern_england",
        "Archbishop's palace across the Thames from Westminster."
    ),
    "ludgershall": (
        "Ludgershall",
        "castle",
        "southern_england",
        "Royal castle and hunting lodge in Wiltshire."
    ),
}


# Travel distances in days between major locations
# Format: (from, to): days_travel
TRAVEL_TIMES: Dict[Tuple[str, str], int] = {
    # London area interconnections
    ("westminster", "windsor"): 1,
    ("westminster", "guildford"): 1,
    ("westminster", "canterbury"): 2,
    ("westminster", "dover"): 2,
    ("westminster", "oxford"): 2,
    ("westminster", "reading"): 1,
    ("windsor", "oxford"): 1,
    ("windsor", "woodstock"): 1,
    ("oxford", "woodstock"): 1,

    # Southern routes
    ("winchester", "westminster"): 2,
    ("winchester", "portsmouth"): 1,
    ("winchester", "portchester"): 1,
    ("winchester", "clarendon"): 1,
    ("winchester", "marlborough"): 1,
    ("portsmouth", "portchester"): 0,  # Adjacent
    ("marlborough", "clarendon"): 1,
    ("marlborough", "oxford"): 1,

    # North-south routes
    ("westminster", "northampton"): 2,
    ("oxford", "northampton"): 1,
    ("northampton", "nottingham"): 2,
    ("nottingham", "york"): 2,
    ("westminster", "york"): 5,  # Long journey

    # Western routes
    ("oxford", "gloucester"): 2,
    ("gloucester", "bristol"): 1,
    ("gloucester", "shrewsbury"): 2,
    ("bristol", "winchester"): 3,

    # Kent
    ("canterbury", "dover"): 1,
    ("westminster", "canterbury"): 2,
}


def get_travel_time(from_location: str, to_location: str) -> int:
    """
    Calculate travel time between two locations.

    Checks both forward and reverse lookups in TRAVEL_TIMES.
    If no direct route exists, estimates based on a simple heuristic.

    Args:
        from_location: Starting location ID
        to_location: Destination location ID

    Returns:
        Number of days required for travel

    Note:
        Same location returns 0 days.
        Unknown routes estimate 3 days (average).
    """
    if from_location == to_location:
        return 0

    # Check direct route
    if (from_location, to_location) in TRAVEL_TIMES:
        return TRAVEL_TIMES[(from_location, to_location)]

    # Check reverse route (distance is same both ways)
    if (to_location, from_location) in TRAVEL_TIMES:
        return TRAVEL_TIMES[(to_location, from_location)]

    # Unknown route - return estimated time
    # In a full implementation, could use more sophisticated estimation
    return 3


def get_location_info(location_id: str) -> Dict[str, str]:
    """
    Get detailed information about a location.

    Args:
        location_id: Location identifier

    Returns:
        Dictionary with location details (name, type, region, description)

    Raises:
        KeyError: If location_id not found
    """
    if location_id not in LOCATIONS:
        raise KeyError(f"Unknown location: {location_id}")

    name, loc_type, region, description = LOCATIONS[location_id]

    return {
        "id": location_id,
        "name": name,
        "type": LOCATION_TYPES[loc_type],
        "type_id": loc_type,
        "region": region,
        "description": description
    }


def get_locations_in_region(region: str) -> List[str]:
    """
    Get all locations in a specific region.

    Args:
        region: Region identifier (southern_england, northern_england, etc.)

    Returns:
        List of location IDs in that region
    """
    return [
        loc_id
        for loc_id, (_, _, loc_region, _) in LOCATIONS.items()
        if loc_region == region
    ]


def format_location_name(location_id: str) -> str:
    """
    Get formatted display name for a location.

    Args:
        location_id: Location identifier

    Returns:
        Display name string

    Example:
        >>> format_location_name("westminster")
        'Westminster'
    """
    if location_id in LOCATIONS:
        return LOCATIONS[location_id][0]
    return location_id.replace("_", " ").title()


# Testing code
if __name__ == "__main__":
    print("=== Testing Location System ===\n")

    # Test location info
    info = get_location_info("westminster")
    print(f"Location: {info['name']}")
    print(f"Type: {info['type']}")
    print(f"Region: {info['region']}")
    print(f"Description: {info['description']}")
    print()

    # Test travel times
    print("=== Testing Travel Times ===\n")
    routes = [
        ("westminster", "windsor"),
        ("westminster", "york"),
        ("winchester", "portsmouth"),
        ("portsmouth", "portchester"),
    ]

    for from_loc, to_loc in routes:
        days = get_travel_time(from_loc, to_loc)
        from_name = format_location_name(from_loc)
        to_name = format_location_name(to_loc)
        print(f"{from_name} to {to_name}: {days} day(s)")
    print()

    # Test reverse route
    days_forward = get_travel_time("westminster", "york")
    days_reverse = get_travel_time("york", "westminster")
    print(f"Westminster to York: {days_forward} days")
    print(f"York to Westminster: {days_reverse} days")
    assert days_forward == days_reverse
    print("Reverse routes: OK")
    print()

    # Test region listing
    print("=== Testing Region Listing ===\n")
    southern_locs = get_locations_in_region("southern_england")
    print(f"Southern England locations ({len(southern_locs)}):")
    for loc in southern_locs[:5]:  # Show first 5
        print(f"  - {format_location_name(loc)}")
    print(f"  ... and {len(southern_locs) - 5} more")
    print()

    # Test unknown route estimation
    print("=== Testing Unknown Route ===\n")
    unknown_time = get_travel_time("york", "dover")
    print(f"York to Dover (no direct route): {unknown_time} days (estimated)")
    print()

    print("=== All Tests Passed ===")
