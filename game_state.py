"""
game_state.py

Core GameState class for King John 1205.
Maintains complete game state including resources, relationships, and history.
"""

from typing import Dict, List, Any, Optional, Tuple
import copy

from calendar import Date
from data.locations import format_location_name


class GameState:
    """
    Maintains complete game state for King John 1205.

    The GameState class stores all game data including the current date,
    king's location, resources (treasury, authority, etc.), baronial
    relationships, regional stability, state flags, event history, and
    active event chains.

    Attributes:
        current_date: Date object representing current in-game date
        location: String ID of current location
        traveling_to: Optional destination if currently traveling
        travel_days_remaining: Days left in current journey
        treasury: Integer amount of gold marks available
        royal_authority: Int 0-100 representing king's power
        military_readiness: Int 0-100 representing military preparedness
        papal_relations: Int -100 to +100 representing relationship with Pope
        barons: Dict mapping baron names to relationship values (0-100)
        regions: Dict mapping region names to stability values (0-100)
        flags: Dict storing game state flags
        event_history: List of event records
        active_chains: List of active multi-day event chains
        days_played: Total days advanced
        days_since_negative_treasury: Counter for bankruptcy check

    Example:
        >>> game_state = GameState()
        >>> game_state.advance_day()
        >>> game_state.treasury -= 500
        >>> game_state.apply_consequences({"resources": {"authority": 5}})
    """

    # Starting values
    STARTING_TREASURY = 8000
    STARTING_AUTHORITY = 65
    STARTING_MILITARY = 60
    STARTING_PAPAL = 40

    def __init__(self):
        """Initialize game state with starting values for 1205."""
        # Time and Location
        self.current_date = Date(1205, 1, 1)
        self.location = "winchester"  # Start at Winchester
        self.traveling_to: Optional[str] = None
        self.travel_days_remaining = 0

        # Primary Resources
        self.treasury = self.STARTING_TREASURY
        self.royal_authority = self.STARTING_AUTHORITY
        self.military_readiness = self.STARTING_MILITARY
        self.papal_relations = self.STARTING_PAPAL

        # Baronial Relationships (0-100, starting values based on historical relationships)
        self.barons: Dict[str, int] = {
            "william_marshal": 70,      # Loyal but cautious
            "william_longespee": 75,    # Half-brother, very loyal
            "william_de_braose": 60,    # Starting to decline historically
            "geoffrey_fitzpeter": 70,   # Loyal justiciar
            "roger_de_lacy": 60,        # Northern lord, moderate
            "robert_de_vieuxpont": 60,  # Northern baron
            "william_de_stuteville": 55, # Yorkshire magnate
            "hugh_de_neville": 65       # Chief Forester
        }

        # Regional Stability (0-100)
        self.regions: Dict[str, int] = {
            "southern_england": 75,   # Core domain, most stable
            "northern_england": 60,   # Less direct control
            "welsh_marches": 55,      # Frequent border issues
            "scotland_border": 60,    # Uneasy peace
            "ireland": 55,            # English holdings tenuous
            "continental": 50         # Just lost Normandy
        }

        # State Flags (for tracking player choices and story progression)
        self.flags: Dict[str, Any] = {
            "invasion_launched": False,
            "invasion_success": None,
            "archbishop_elected": None,
            "de_braose_fallen": False,
            "hostages_taken": [],
            "historical_path": True,  # Tracks if following history
        }

        # Event History (will store EventRecord objects)
        self.event_history: List[Dict[str, Any]] = []

        # Active Multi-Day Chains (will store EventChain data)
        self.active_chains: List[Dict[str, Any]] = []

        # Metadata
        self.days_played = 0
        self.days_since_negative_treasury = 0
        self.difficulty = "normal"

    def advance_day(self) -> None:
        """
        Advance calendar by one day and handle travel.

        Updates the current date, tracks days played, and processes
        any ongoing travel. When travel is complete, updates location.
        """
        self.current_date.increment()
        self.days_played += 1

        # Track negative treasury for bankruptcy
        if self.treasury < 0:
            self.days_since_negative_treasury += 1
        else:
            self.days_since_negative_treasury = 0

        # Handle travel
        if self.traveling_to:
            self.travel_days_remaining -= 1
            if self.travel_days_remaining <= 0:
                self.location = self.traveling_to
                self.traveling_to = None
                self.travel_days_remaining = 0

    def start_travel(self, destination: str, days: int) -> None:
        """
        Begin travel to a new location.

        Args:
            destination: Location ID to travel to
            days: Number of days the journey will take
        """
        self.traveling_to = destination
        self.travel_days_remaining = days

    def get_average_baronial_loyalty(self) -> float:
        """
        Calculate average of all baron relationships.

        Returns:
            Float representing average baronial loyalty (0-100)
        """
        if not self.barons:
            return 0.0
        return sum(self.barons.values()) / len(self.barons)

    def get_kingdom_stability(self) -> float:
        """
        Calculate weighted average regional stability.

        Southern England counts double as it's the royal heartland.

        Returns:
            Float representing overall kingdom stability (0-100)
        """
        weights = {
            "southern_england": 2.0,   # Core region counts double
            "northern_england": 1.0,
            "welsh_marches": 1.0,
            "scotland_border": 0.5,    # Less critical
            "ireland": 0.5,            # Distant
            "continental": 1.0
        }

        total = sum(
            self.regions.get(region, 0) * weight
            for region, weight in weights.items()
        )
        total_weight = sum(weights.values())

        return total / total_weight if total_weight > 0 else 0.0

    def check_game_over(self) -> Tuple[bool, Optional[str]]:
        """
        Check if game over conditions are met.

        Returns:
            Tuple of (is_game_over: bool, reason: Optional[str])

        Game over occurs if:
        - Treasury negative for 30+ days (bankruptcy)
        - Royal authority < 10 (civil war)
        - Average baronial loyalty < 15 (mass rebellion)
        - All regions < 25 stability (kingdom collapse)
        """
        # Bankruptcy check
        if self.treasury < 0 and self.days_since_negative_treasury > 30:
            return (True, "bankruptcy")

        # Authority collapse
        if self.royal_authority < 10:
            return (True, "civil_war")

        # Mass baronial rebellion
        if self.get_average_baronial_loyalty() < 15:
            return (True, "mass_rebellion")

        # Kingdom-wide collapse
        if all(stability < 25 for stability in self.regions.values()):
            return (True, "kingdom_collapse")

        return (False, None)

    def apply_consequences(self, consequences: Dict[str, Any]) -> None:
        """
        Apply event consequences to game state.

        Processes a consequences dictionary and updates game state
        accordingly. Handles resource changes, relationship changes,
        regional stability changes, and flag updates. Values are
        clamped to valid ranges.

        Args:
            consequences: Dictionary with keys:
                - "resources": Dict of resource name -> change amount
                - "relationships": Dict of baron name -> change amount
                - "regions": Dict of region name -> change amount
                - "flags": Dict of flag name -> new value

        Raises:
            TypeError: If consequences is not a dictionary

        Example:
            >>> consequences = {
            ...     "resources": {"treasury": -500, "authority": 5},
            ...     "relationships": {"william_marshal": -10}
            ... }
            >>> game_state.apply_consequences(consequences)
        """
        if not isinstance(consequences, dict):
            raise TypeError("Consequences must be a dictionary")

        # Apply resource changes
        if "resources" in consequences:
            for resource, change in consequences["resources"].items():
                self._apply_resource_change(resource, change)

        # Apply relationship changes
        if "relationships" in consequences:
            for baron, change in consequences["relationships"].items():
                if baron in self.barons:
                    self.barons[baron] = clamp(
                        self.barons[baron] + change, 0, 100
                    )

        # Apply regional changes
        if "regions" in consequences:
            for region, change in consequences["regions"].items():
                if region in self.regions:
                    self.regions[region] = clamp(
                        self.regions[region] + change, 0, 100
                    )

        # Apply flag changes
        if "flags" in consequences:
            for flag, value in consequences["flags"].items():
                self.flags[flag] = value

    def _apply_resource_change(self, resource: str, change: int) -> None:
        """
        Apply a change to a specific resource.

        Handles different resource types appropriately:
        - treasury: No clamping (can go negative temporarily)
        - Others: Clamped to valid ranges

        Args:
            resource: Resource name
            change: Amount to change by
        """
        if resource == "treasury":
            self.treasury += change
        elif resource == "authority":
            self.royal_authority = clamp(
                self.royal_authority + change, 0, 100
            )
        elif resource == "military":
            self.military_readiness = clamp(
                self.military_readiness + change, 0, 100
            )
        elif resource == "papal":
            self.papal_relations = clamp(
                self.papal_relations + change, -100, 100
            )

    def get_resource_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all current resources.

        Returns:
            Dictionary with all resource values
        """
        return {
            "treasury": self.treasury,
            "royal_authority": self.royal_authority,
            "military_readiness": self.military_readiness,
            "papal_relations": self.papal_relations,
            "average_baronial_loyalty": self.get_average_baronial_loyalty(),
            "kingdom_stability": self.get_kingdom_stability()
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize game state to dictionary for saving.

        Returns:
            Dictionary containing complete game state
        """
        return {
            "version": "1.0",
            "date": self.current_date.to_dict(),
            "location": self.location,
            "traveling_to": self.traveling_to,
            "travel_days_remaining": self.travel_days_remaining,
            "treasury": self.treasury,
            "royal_authority": self.royal_authority,
            "military_readiness": self.military_readiness,
            "papal_relations": self.papal_relations,
            "barons": self.barons.copy(),
            "regions": self.regions.copy(),
            "flags": self.flags.copy(),
            "event_history": copy.deepcopy(self.event_history),
            "active_chains": copy.deepcopy(self.active_chains),
            "days_played": self.days_played,
            "days_since_negative_treasury": self.days_since_negative_treasury,
            "difficulty": self.difficulty
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameState':
        """
        Deserialize game state from dictionary.

        Args:
            data: Dictionary containing saved game state

        Returns:
            GameState object restored from save data

        Raises:
            KeyError: If required keys are missing
            ValueError: If data is invalid
        """
        state = cls()

        # Restore date
        state.current_date = Date.from_dict(data["date"])

        # Restore location and travel
        state.location = data["location"]
        state.traveling_to = data.get("traveling_to")
        state.travel_days_remaining = data.get("travel_days_remaining", 0)

        # Restore resources
        state.treasury = data["treasury"]
        state.royal_authority = data["royal_authority"]
        state.military_readiness = data["military_readiness"]
        state.papal_relations = data["papal_relations"]

        # Restore relationships and regions
        state.barons = data["barons"].copy()
        state.regions = data["regions"].copy()

        # Restore flags and history
        state.flags = data["flags"].copy()
        state.event_history = copy.deepcopy(data.get("event_history", []))
        state.active_chains = copy.deepcopy(data.get("active_chains", []))

        # Restore metadata
        state.days_played = data.get("days_played", 0)
        state.days_since_negative_treasury = data.get("days_since_negative_treasury", 0)
        state.difficulty = data.get("difficulty", "normal")

        return state

    def __str__(self) -> str:
        """String representation for debugging."""
        return (
            f"GameState({self.current_date.format_short()}, "
            f"{format_location_name(self.location)}, "
            f"Treasury: {self.treasury})"
        )

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"GameState(date={self.current_date}, "
            f"location='{self.location}', "
            f"treasury={self.treasury})"
        )


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp a value between minimum and maximum.

    Args:
        value: Value to clamp
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        Clamped value

    Example:
        >>> clamp(150, 0, 100)
        100
        >>> clamp(-10, 0, 100)
        0
        >>> clamp(50, 0, 100)
        50
    """
    return max(min_value, min(max_value, value))


# Testing code
if __name__ == "__main__":
    print("=== Testing GameState Class ===\n")

    # Test initialization
    state = GameState()
    print(f"Initial state: {state}")
    print(f"Date: {state.current_date.format_long()}")
    print(f"Location: {format_location_name(state.location)}")
    print(f"Treasury: {state.treasury} marks")
    print(f"Royal Authority: {state.royal_authority}/100")
    print(f"Military Readiness: {state.military_readiness}/100")
    print(f"Papal Relations: {state.papal_relations}/100")
    print()

    # Test derived metrics
    print("=== Testing Derived Metrics ===\n")
    avg_loyalty = state.get_average_baronial_loyalty()
    kingdom_stability = state.get_kingdom_stability()
    print(f"Average Baronial Loyalty: {avg_loyalty:.1f}/100")
    print(f"Kingdom Stability: {kingdom_stability:.1f}/100")
    print()

    # Test consequence application
    print("=== Testing Consequence Application ===\n")
    consequences = {
        "resources": {
            "treasury": -500,
            "authority": 5,
            "military": -10
        },
        "relationships": {
            "william_marshal": -10,
            "william_longespee": 5
        },
        "regions": {
            "southern_england": 3
        }
    }

    print("Applying consequences:")
    print(f"  Treasury: -500")
    print(f"  Authority: +5")
    print(f"  Military: -10")
    print(f"  William Marshal: -10")
    print(f"  William Longespée: +5")
    print(f"  Southern England: +3")
    print()

    old_treasury = state.treasury
    old_authority = state.royal_authority
    state.apply_consequences(consequences)

    print(f"Treasury: {old_treasury} → {state.treasury}")
    print(f"Authority: {old_authority} → {state.royal_authority}")
    print(f"William Marshal: {state.barons['william_marshal']}/100")
    print(f"Southern England: {state.regions['southern_england']}/100")
    print()

    # Test clamping
    print("=== Testing Value Clamping ===\n")
    state.royal_authority = 95
    state.apply_consequences({"resources": {"authority": 20}})
    print(f"Authority at 95, add 20 → {state.royal_authority} (clamped to 100)")

    state.military_readiness = 5
    state.apply_consequences({"resources": {"military": -20}})
    print(f"Military at 5, subtract 20 → {state.military_readiness} (clamped to 0)")
    print()

    # Test day advancement
    print("=== Testing Day Advancement ===\n")
    state = GameState()
    initial_date = str(state.current_date)
    print(f"Initial: {initial_date}")
    state.advance_day()
    print(f"After advance: {state.current_date}")
    print(f"Days played: {state.days_played}")
    print()

    # Test travel
    print("=== Testing Travel System ===\n")
    state.start_travel("york", 5)
    print(f"Started travel to York (5 days)")
    print(f"Traveling to: {format_location_name(state.traveling_to)}")
    print(f"Days remaining: {state.travel_days_remaining}")

    for day in range(5):
        state.advance_day()
        if state.traveling_to:
            print(f"Day {day + 1}: Traveling... ({state.travel_days_remaining} days left)")
        else:
            print(f"Day {day + 1}: Arrived at {format_location_name(state.location)}")
    print()

    # Test game over conditions
    print("=== Testing Game Over Conditions ===\n")
    state = GameState()

    # Test bankruptcy
    state.treasury = -1000
    state.days_since_negative_treasury = 31
    is_over, reason = state.check_game_over()
    print(f"Treasury negative for 31 days: Game Over = {is_over}, Reason = {reason}")

    # Test civil war
    state = GameState()
    state.royal_authority = 5
    is_over, reason = state.check_game_over()
    print(f"Authority at 5: Game Over = {is_over}, Reason = {reason}")

    # Test normal state
    state = GameState()
    is_over, reason = state.check_game_over()
    print(f"Normal state: Game Over = {is_over}, Reason = {reason}")
    print()

    # Test serialization
    print("=== Testing Serialization ===\n")
    state = GameState()
    state.treasury = 7000
    state.flags["invasion_launched"] = True
    state.advance_day()

    save_data = state.to_dict()
    print(f"Serialized version: {save_data['version']}")
    print(f"Serialized date: {save_data['date']}")
    print(f"Serialized treasury: {save_data['treasury']}")

    restored = GameState.from_dict(save_data)
    print(f"Restored treasury: {restored.treasury}")
    print(f"Restored date: {restored.current_date}")
    print(f"Restored flag: invasion_launched = {restored.flags['invasion_launched']}")
    assert restored.treasury == 7000
    assert restored.flags["invasion_launched"] == True
    print("Serialization: OK")
    print()

    print("=== All Tests Passed ===")
