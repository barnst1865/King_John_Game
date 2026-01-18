# King John 1205: Technical Design Document

**Version:** 1.0
**Date:** January 18, 2026
**Language:** Python 3.9+
**Architecture:** Object-Oriented, Event-Driven

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Main Game Loop                         │
│                      (main.py)                              │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┬──────────────┬─────────────┐
        ▼                     ▼              ▼             ▼
┌───────────────┐    ┌──────────────┐  ┌─────────┐  ┌──────────┐
│  Game State   │◄───│ Event System │  │   UI    │  │ Calendar │
│ (resources,   │    │ (event mgr,  │  │ Display │  │  System  │
│  relationships)│    │  consequences)│  │         │  │          │
└───────┬───────┘    └──────┬───────┘  └────┬────┘  └────┬─────┘
        │                   │                │            │
        │                   │                │            │
        ▼                   ▼                ▼            ▼
┌───────────────┐    ┌──────────────┐  ┌─────────┐  ┌──────────┐
│  Save/Load    │    │   Data       │  │ Input   │  │ Location │
│   Manager     │    │   Files      │  │ Handler │  │  Travel  │
└───────────────┘    └──────────────┘  └─────────┘  └──────────┘
```

### 1.2 Module Overview

**Core Modules:**
- `main.py` - Entry point, main menu, game loop coordination
- `game_state.py` - GameState class, resource management, state persistence
- `events.py` - Event classes, EventManager, event processing
- `calendar.py` - Date tracking, medieval calendar, time progression
- `ui.py` - Display functions, input handling, formatting
- `advisors.py` - Advisor system, consultation mechanics
- `location.py` - Location data, travel system

**Data Modules:**
- `data/historical_events.py` - 60 historical anchor events
- `data/triggered_events.py` - 40 conditional events
- `data/event_templates.py` - 30 reusable event templates
- `data/random_events.py` - 50 random event pool
- `data/chains.py` - 20 multi-day event chains
- `data/characters.py` - Baron/advisor data and personalities
- `data/locations.py` - Location information, travel distances

**Utility Modules:**
- `utils/text_utils.py` - Text formatting, color support, wrapping
- `utils/game_logic.py` - Consequence calculations, condition checking
- `utils/validation.py` - Data validation, error checking

**Save Directory:**
- `saves/` - JSON save files (auto + manual slots)

---

## 2. Core Data Structures

### 2.1 GameState Class

The central object holding all game state.

```python
class GameState:
    """
    Maintains complete game state including date, resources,
    relationships, flags, and history.
    """

    def __init__(self):
        # Time and Location
        self.current_date: Date = Date(1205, 1, 1)
        self.location: str = "Winchester"
        self.traveling_to: Optional[str] = None
        self.travel_days_remaining: int = 0

        # Primary Resources
        self.treasury: int = 8000  # Starting marks
        self.royal_authority: int = 65
        self.military_readiness: int = 60
        self.papal_relations: int = 40

        # Baronial Relationships (dict: name -> value 0-100)
        self.barons: Dict[str, int] = {
            "william_marshal": 70,
            "william_longespee": 75,
            "william_de_braose": 60,
            "geoffrey_fitzpeter": 70,
            "roger_de_lacy": 60,
            "robert_de_vieuxpont": 60,
            "william_de_stuteville": 55,
            "hugh_de_neville": 65
        }

        # Regional Stability (dict: region -> value 0-100)
        self.regions: Dict[str, int] = {
            "southern_england": 75,
            "northern_england": 60,
            "welsh_marches": 55,
            "scotland_border": 60,
            "ireland": 55,
            "continental": 50
        }

        # State Flags (dict: flag_name -> bool or value)
        self.flags: Dict[str, Any] = {
            "invasion_launched": False,
            "archbishop_elected": None,  # None, "john_de_gray", or "stephen_langton"
            "de_braose_fallen": False,
            "hostages_taken": [],
            # ... many more flags
        }

        # Event History
        self.event_history: List[EventRecord] = []

        # Active Multi-Day Chains
        self.active_chains: List[EventChain] = []

        # Metadata
        self.days_played: int = 0
        self.score: int = 0
        self.difficulty: str = "normal"

    def advance_day(self) -> None:
        """Advance calendar by one day, handle travel."""
        self.current_date.increment()
        self.days_played += 1

        if self.traveling_to:
            self.travel_days_remaining -= 1
            if self.travel_days_remaining <= 0:
                self.location = self.traveling_to
                self.traveling_to = None

    def get_average_baronial_loyalty(self) -> float:
        """Calculate average of all baron relationships."""
        return sum(self.barons.values()) / len(self.barons)

    def get_kingdom_stability(self) -> float:
        """Calculate weighted average regional stability."""
        weights = {
            "southern_england": 2.0,  # Core region counts double
            "northern_england": 1.0,
            "welsh_marches": 1.0,
            "scotland_border": 0.5,
            "ireland": 0.5,
            "continental": 1.0
        }
        total = sum(self.regions[r] * weights[r] for r in self.regions)
        total_weight = sum(weights.values())
        return total / total_weight

    def check_game_over(self) -> Tuple[bool, Optional[str]]:
        """
        Check if game over conditions met.
        Returns (is_over, reason)
        """
        if self.treasury < 0 and self.days_since_negative_treasury > 30:
            return (True, "bankruptcy")

        if self.royal_authority < 10:
            return (True, "civil_war")

        if self.get_average_baronial_loyalty() < 15:
            return (True, "mass_rebellion")

        if all(stability < 25 for stability in self.regions.values()):
            return (True, "kingdom_collapse")

        return (False, None)

    def apply_consequences(self, consequences: Dict[str, Any]) -> None:
        """Apply event consequences to game state."""
        # Resource changes
        if "resources" in consequences:
            for resource, change in consequences["resources"].items():
                if resource == "treasury":
                    self.treasury += change
                elif resource == "authority":
                    self.royal_authority = clamp(
                        self.royal_authority + change, 0, 100
                    )
                # ... etc for all resources

        # Relationship changes
        if "relationships" in consequences:
            for baron, change in consequences["relationships"].items():
                if baron in self.barons:
                    self.barons[baron] = clamp(
                        self.barons[baron] + change, 0, 100
                    )

        # Regional changes
        if "regions" in consequences:
            for region, change in consequences["regions"].items():
                if region in self.regions:
                    self.regions[region] = clamp(
                        self.regions[region] + change, 0, 100
                    )

        # Flag changes
        if "flags" in consequences:
            for flag, value in consequences["flags"].items():
                self.flags[flag] = value

    def to_dict(self) -> Dict[str, Any]:
        """Serialize game state to dictionary for saving."""
        return {
            "date": self.current_date.to_dict(),
            "location": self.location,
            "traveling_to": self.traveling_to,
            "travel_days_remaining": self.travel_days_remaining,
            "treasury": self.treasury,
            "royal_authority": self.royal_authority,
            "military_readiness": self.military_readiness,
            "papal_relations": self.papal_relations,
            "barons": self.barons,
            "regions": self.regions,
            "flags": self.flags,
            "event_history": [e.to_dict() for e in self.event_history],
            "active_chains": [c.to_dict() for c in self.active_chains],
            "days_played": self.days_played,
            "score": self.score,
            "difficulty": self.difficulty
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameState':
        """Deserialize game state from dictionary."""
        state = cls()
        # Restore all fields from data...
        return state
```

### 2.2 Date Class

```python
class Date:
    """
    Medieval calendar date with feast day tracking.
    """

    # Days per month in 1205 (no leap year)
    DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    MONTH_NAMES = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    DAY_NAMES = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    ]

    # Important feast days (month, day, name)
    FEAST_DAYS = [
        (1, 1, "Circumcision of Christ"),
        (1, 6, "Epiphany"),
        (3, 25, "Annunciation"),
        # Easter is moveable - calculated separately
        (6, 24, "Nativity of St. John the Baptist"),
        (8, 15, "Assumption of Mary"),
        (9, 29, "Michaelmas"),
        (11, 1, "All Saints"),
        (12, 25, "Christmas"),
        (12, 26, "St. Stephen's Day"),
        # ... more feast days
    ]

    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day
        self._validate()

    def _validate(self):
        """Ensure date is valid."""
        if not (1 <= self.month <= 12):
            raise ValueError(f"Invalid month: {self.month}")
        if not (1 <= self.day <= self.DAYS_IN_MONTH[self.month - 1]):
            raise ValueError(f"Invalid day: {self.day}")

    def increment(self) -> None:
        """Advance date by one day."""
        self.day += 1
        if self.day > self.DAYS_IN_MONTH[self.month - 1]:
            self.day = 1
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1

    def day_of_week(self) -> str:
        """Calculate day of week using Zeller's congruence."""
        # Implementation...
        return self.DAY_NAMES[dow_index]

    def day_of_year(self) -> int:
        """Return day number 1-365."""
        return sum(self.DAYS_IN_MONTH[:self.month-1]) + self.day

    def is_feast_day(self) -> Optional[str]:
        """Return feast day name if today is a feast, else None."""
        for month, day, name in self.FEAST_DAYS:
            if self.month == month and self.day == day:
                return name
        # Check Easter and moveable feasts...
        return None

    def format_long(self) -> str:
        """Format as 'Thursday, May 31, 1205'."""
        return f"{self.day_of_week()}, {self.MONTH_NAMES[self.month-1]} {self.day}, {self.year}"

    def format_short(self) -> str:
        """Format as 'Day 152 - May 31, 1205'."""
        return f"Day {self.day_of_year()} - {self.MONTH_NAMES[self.month-1]} {self.day}, {self.year}"

    def to_dict(self) -> Dict[str, int]:
        return {"year": self.year, "month": self.month, "day": self.day}

    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> 'Date':
        return cls(data["year"], data["month"], data["day"])
```

### 2.3 Event Classes

```python
class Event:
    """
    Represents a single event with choices and consequences.
    """

    def __init__(
        self,
        event_id: str,
        event_type: str,  # "historical", "triggered", "random", "chain"
        title: str,
        description: str,
        choices: List['Choice'],
        date: Optional[Tuple[int, int, int]] = None,  # (year, month, day)
        location: Optional[str] = None,
        conditions: Optional[Dict[str, Any]] = None,
        historical_context: Optional[str] = None,
        historical_outcome: Optional[str] = None
    ):
        self.event_id = event_id
        self.event_type = event_type
        self.title = title
        self.description = description
        self.choices = choices
        self.date = date
        self.location = location
        self.conditions = conditions or {}
        self.historical_context = historical_context
        self.historical_outcome = historical_outcome

    def check_conditions(self, game_state: GameState) -> bool:
        """Check if this event's conditions are met."""
        if not self.conditions:
            return True

        # Check resource requirements
        if "resources" in self.conditions:
            for resource, required_value in self.conditions["resources"].items():
                if hasattr(game_state, resource):
                    current = getattr(game_state, resource)
                    if current < required_value:
                        return False

        # Check flag requirements
        if "flags" in self.conditions:
            for flag, required_value in self.conditions["flags"].items():
                if game_state.flags.get(flag) != required_value:
                    return False

        # Check date requirements
        if "date_after" in self.conditions:
            required_date = Date(*self.conditions["date_after"])
            if game_state.current_date.day_of_year() <= required_date.day_of_year():
                return False

        # Check location requirement
        if "location" in self.conditions:
            if game_state.location != self.conditions["location"]:
                return False

        return True

    def get_available_choices(self, game_state: GameState) -> List['Choice']:
        """Return only choices whose requirements are met."""
        available = []
        for choice in self.choices:
            if choice.check_requirements(game_state):
                available.append(choice)
        return available


class Choice:
    """
    Represents one choice within an event.
    """

    def __init__(
        self,
        choice_id: int,
        text: str,
        consequences: Dict[str, Any],
        narrative_outcome: str,
        requirements: Optional[Dict[str, Any]] = None
    ):
        self.choice_id = choice_id
        self.text = text
        self.consequences = consequences
        self.narrative_outcome = narrative_outcome
        self.requirements = requirements or {}

    def check_requirements(self, game_state: GameState) -> bool:
        """Check if player can select this choice."""
        if not self.requirements:
            return True

        # Similar to Event.check_conditions()
        # Check resource requirements, flags, etc.
        return True

    def get_display_text(self, game_state: GameState) -> str:
        """Get choice text with requirement indicators if needed."""
        text = self.text
        if not self.check_requirements(game_state):
            text += " [LOCKED]"
        return text


class EventChain:
    """
    Represents a multi-day event sequence.
    """

    def __init__(
        self,
        chain_id: str,
        name: str,
        events: List[Event],
        start_date: Optional[Date] = None
    ):
        self.chain_id = chain_id
        self.name = name
        self.events = events
        self.start_date = start_date
        self.current_event_index = 0
        self.active = False
        self.flags = {}  # Chain-specific flags

    def start(self, game_state: GameState) -> None:
        """Begin this event chain."""
        self.active = True
        self.start_date = game_state.current_date

    def get_current_event(self) -> Optional[Event]:
        """Get the current event in the chain."""
        if self.active and self.current_event_index < len(self.events):
            return self.events[self.current_event_index]
        return None

    def advance(self) -> None:
        """Move to next event in chain."""
        self.current_event_index += 1
        if self.current_event_index >= len(self.events):
            self.active = False

    def is_complete(self) -> bool:
        """Check if chain has finished."""
        return not self.active or self.current_event_index >= len(self.events)


class EventManager:
    """
    Manages event selection, triggering, and processing.
    """

    def __init__(self):
        self.historical_events: List[Event] = []
        self.triggered_events: List[Event] = []
        self.random_events: List[Event] = []
        self.event_templates: List[Event] = []
        self.chains: List[EventChain] = []

        self.triggered_event_ids: Set[str] = set()  # Track used one-time events

    def load_all_events(self) -> None:
        """Load events from data modules."""
        from data.historical_events import HISTORICAL_EVENTS
        from data.triggered_events import TRIGGERED_EVENTS
        from data.random_events import RANDOM_EVENTS
        from data.event_templates import EVENT_TEMPLATES
        from data.chains import CHAINS

        self.historical_events = HISTORICAL_EVENTS
        self.triggered_events = TRIGGERED_EVENTS
        self.random_events = RANDOM_EVENTS
        self.event_templates = EVENT_TEMPLATES
        self.chains = CHAINS

    def get_event_for_day(self, game_state: GameState) -> Optional[Event]:
        """
        Determine which event should occur today.
        Priority: Active Chain > Historical > Triggered > Random > Template
        """

        # 1. Check active chains first
        for chain in game_state.active_chains:
            if chain.active:
                event = chain.get_current_event()
                if event and event.check_conditions(game_state):
                    return event

        # 2. Check for historical event on this date
        current_date_tuple = (
            game_state.current_date.year,
            game_state.current_date.month,
            game_state.current_date.day
        )
        for event in self.historical_events:
            if event.date == current_date_tuple:
                if event.check_conditions(game_state):
                    return event

        # 3. Check triggered events
        for event in self.triggered_events:
            if event.event_id not in self.triggered_event_ids:
                if event.check_conditions(game_state):
                    self.triggered_event_ids.add(event.event_id)
                    return event

        # 4. Random event (20% chance)
        if random.random() < 0.20:
            eligible_random = [
                e for e in self.random_events
                if e.check_conditions(game_state)
            ]
            if eligible_random:
                return random.choice(eligible_random)

        # 5. Template event (fallback for administrative/routine)
        if random.random() < 0.50:  # 50% chance for routine event
            eligible_templates = [
                e for e in self.event_templates
                if e.check_conditions(game_state)
            ]
            if eligible_templates:
                template = random.choice(eligible_templates)
                # Generate instance from template
                return self.instantiate_template(template, game_state)

        # 6. No event (quiet day)
        return None

    def instantiate_template(
        self,
        template: Event,
        game_state: GameState
    ) -> Event:
        """
        Create a specific event instance from a template.
        Fills in random values for variable parts.
        """
        # Implementation: Replace placeholders with random appropriate values
        # e.g., [PETITIONER_NAME] -> "Sir Geoffrey of Kent"
        return instantiated_event

    def start_chain(self, chain_id: str, game_state: GameState) -> None:
        """Activate a multi-day event chain."""
        for chain in self.chains:
            if chain.chain_id == chain_id:
                chain.start(game_state)
                game_state.active_chains.append(chain)
                break
```

### 2.4 EventRecord Class

```python
class EventRecord:
    """
    Records an event that occurred for history/journal.
    """

    def __init__(
        self,
        date: Date,
        location: str,
        event_id: str,
        event_title: str,
        choice_made: int,
        choice_text: str,
        consequences_summary: str
    ):
        self.date = date
        self.location = location
        self.event_id = event_id
        self.event_title = event_title
        self.choice_made = choice_made
        self.choice_text = choice_text
        self.consequences_summary = consequences_summary

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date.to_dict(),
            "location": self.location,
            "event_id": self.event_id,
            "event_title": self.event_title,
            "choice_made": self.choice_made,
            "choice_text": self.choice_text,
            "consequences_summary": self.consequences_summary
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EventRecord':
        date = Date.from_dict(data["date"])
        return cls(
            date,
            data["location"],
            data["event_id"],
            data["event_title"],
            data["choice_made"],
            data["choice_text"],
            data["consequences_summary"]
        )
```

---

## 3. Game Loop Architecture

### 3.1 Main Game Loop

```python
def main_game_loop(game_state: GameState):
    """
    Primary game loop - one iteration per day.
    """
    event_manager = EventManager()
    event_manager.load_all_events()

    while True:
        # Check for game over
        is_over, reason = game_state.check_game_over()
        if is_over:
            display_game_over(reason, game_state)
            break

        # Check for year end (victory)
        if game_state.current_date.day_of_year() > 365:
            display_year_end(game_state)
            break

        # ===== PHASE 1: Morning Reports =====
        display_morning_reports(game_state)

        # ===== PHASE 2: Decision Time =====
        event = event_manager.get_event_for_day(game_state)

        if event:
            # Present event and get player choice
            chosen_choice = present_event(event, game_state)

            # ===== PHASE 3: Resolution =====
            process_choice(chosen_choice, event, game_state)
        else:
            # Quiet day - offer simple options
            handle_quiet_day(game_state)

        # ===== PHASE 4: Evening Events =====
        handle_evening_phase(game_state, event_manager)

        # Auto-save
        save_game(game_state, "autosave")

        # Advance to next day
        game_state.advance_day()

        # Pause before continuing
        wait_for_continue()
```

### 3.2 Phase Functions

```python
def display_morning_reports(game_state: GameState):
    """
    Phase 1: Display date, location, resources, and any overnight reports.
    """
    ui.clear_screen()
    ui.display_header()
    ui.display_date_location(game_state)
    ui.display_resource_dashboard(game_state)

    # Check for special reports
    reports = generate_morning_reports(game_state)
    if reports:
        ui.display_reports(reports)

    ui.display_separator()


def present_event(event: Event, game_state: GameState) -> Choice:
    """
    Phase 2: Display event and get player's choice.
    Returns the chosen Choice object.
    """
    ui.display_event_header(event.title)
    ui.display_text(event.description)

    # Show historical context option
    if event.historical_context:
        ui.display_hint("[Type 'H' for historical context]")

    # Display choices
    available_choices = event.get_available_choices(game_state)

    # Add meta-choices
    available_choices.append(
        Choice(-1, "Consult advisors", {}, "", None)
    )
    available_choices.append(
        Choice(-2, "Review status", {}, "", None)
    )

    while True:
        ui.display_choices(available_choices, game_state)

        player_input = ui.get_player_input()

        # Handle special inputs
        if player_input.upper() == 'H' and event.historical_context:
            ui.display_historical_context(event.historical_context)
            continue

        if player_input.upper() == 'J':
            display_journal(game_state)
            continue

        try:
            choice_index = int(player_input) - 1
            if 0 <= choice_index < len(available_choices):
                chosen = available_choices[choice_index]

                # Handle meta-choices
                if chosen.choice_id == -1:
                    consult_advisors(event, game_state)
                    continue
                elif chosen.choice_id == -2:
                    display_detailed_status(game_state)
                    continue

                # Confirm choice if significant
                if is_major_decision(chosen):
                    if not ui.confirm_choice(chosen.text):
                        continue

                return chosen
            else:
                ui.display_error("Invalid choice number.")
        except ValueError:
            ui.display_error("Please enter a number.")


def process_choice(
    choice: Choice,
    event: Event,
    game_state: GameState
) -> None:
    """
    Phase 3: Apply consequences and show results.
    """
    ui.clear_screen()
    ui.display_separator()

    # Display narrative outcome
    ui.display_text(choice.narrative_outcome)
    ui.display_separator()

    # Calculate and display consequences
    old_state = copy.deepcopy(game_state)
    game_state.apply_consequences(choice.consequences)

    # Show resource changes
    display_resource_changes(old_state, game_state)

    # Show relationship changes
    display_relationship_changes(old_state, game_state)

    # Show advisor reactions if significant
    display_advisor_reactions(choice, game_state)

    # Record in history
    record = create_event_record(event, choice, game_state)
    game_state.event_history.append(record)

    # Check for triggered consequences
    check_triggered_consequences(choice, game_state)

    ui.display_separator()
    ui.wait_for_continue()


def handle_evening_phase(
    game_state: GameState,
    event_manager: EventManager
) -> None:
    """
    Phase 4: Random events, chain progression, travel updates.
    """
    # Advance any active chains
    for chain in game_state.active_chains:
        if chain.should_advance():
            chain.advance()

    # Travel progress
    if game_state.traveling_to:
        ui.display_travel_progress(game_state)

    # Evening random event (low probability)
    if random.random() < 0.05:
        evening_event = event_manager.get_random_evening_event(game_state)
        if evening_event:
            present_event(evening_event, game_state)
```

---

## 4. Save/Load System

### 4.1 Save Manager

```python
class SaveManager:
    """
    Handles saving and loading game state.
    """

    SAVE_DIR = "saves/"
    AUTOSAVE_FILE = "autosave.json"
    MANUAL_SLOTS = 5

    @staticmethod
    def ensure_save_directory():
        """Create saves directory if it doesn't exist."""
        if not os.path.exists(SaveManager.SAVE_DIR):
            os.makedirs(SaveManager.SAVE_DIR)

    @staticmethod
    def save_game(
        game_state: GameState,
        slot: Union[int, str] = "autosave"
    ) -> bool:
        """
        Save game state to file.
        slot: "autosave" or int 1-5 for manual slots.
        Returns True if successful.
        """
        SaveManager.ensure_save_directory()

        if slot == "autosave":
            filename = SaveManager.AUTOSAVE_FILE
        else:
            filename = f"save_slot_{slot}.json"

        filepath = os.path.join(SaveManager.SAVE_DIR, filename)

        try:
            save_data = {
                "version": "1.0",
                "timestamp": datetime.now().isoformat(),
                "game_state": game_state.to_dict()
            }

            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)

            return True
        except Exception as e:
            logging.error(f"Save failed: {e}")
            return False

    @staticmethod
    def load_game(slot: Union[int, str] = "autosave") -> Optional[GameState]:
        """
        Load game state from file.
        Returns GameState object if successful, None otherwise.
        """
        if slot == "autosave":
            filename = SaveManager.AUTOSAVE_FILE
        else:
            filename = f"save_slot_{slot}.json"

        filepath = os.path.join(SaveManager.SAVE_DIR, filename)

        if not os.path.exists(filepath):
            return None

        try:
            with open(filepath, 'r') as f:
                save_data = json.load(f)

            # Version compatibility check
            if save_data["version"] != "1.0":
                logging.warning("Save file version mismatch")
                # Could attempt migration here

            game_state = GameState.from_dict(save_data["game_state"])
            return game_state

        except Exception as e:
            logging.error(f"Load failed: {e}")
            return None

    @staticmethod
    def list_saves() -> List[Dict[str, Any]]:
        """
        List all available save files with metadata.
        Returns list of dicts with save info.
        """
        saves = []

        # Check autosave
        if os.path.exists(os.path.join(SaveManager.SAVE_DIR, SaveManager.AUTOSAVE_FILE)):
            metadata = SaveManager._get_save_metadata("autosave")
            if metadata:
                saves.append({"slot": "autosave", **metadata})

        # Check manual slots
        for slot in range(1, SaveManager.MANUAL_SLOTS + 1):
            metadata = SaveManager._get_save_metadata(slot)
            if metadata:
                saves.append({"slot": slot, **metadata})

        return saves

    @staticmethod
    def _get_save_metadata(slot: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Extract metadata from save file without loading full state."""
        if slot == "autosave":
            filename = SaveManager.AUTOSAVE_FILE
        else:
            filename = f"save_slot_{slot}.json"

        filepath = os.path.join(SaveManager.SAVE_DIR, filename)

        if not os.path.exists(filepath):
            return None

        try:
            with open(filepath, 'r') as f:
                save_data = json.load(f)

            gs = save_data["game_state"]
            return {
                "timestamp": save_data["timestamp"],
                "date": f"{gs['date']['month']}/{gs['date']['day']}/{gs['date']['year']}",
                "location": gs["location"],
                "days_played": gs["days_played"]
            }
        except Exception:
            return None
```

---

## 5. UI System

### 5.1 Display Functions

```python
# ui.py

import os
import sys
from typing import List, Dict, Any

# Optional color support
try:
    import colorama
    colorama.init()
    COLOR_SUPPORT = True
except ImportError:
    COLOR_SUPPORT = False


class Colors:
    """ANSI color codes."""
    RESET = "\033[0m" if COLOR_SUPPORT else ""
    RED = "\033[31m" if COLOR_SUPPORT else ""
    GREEN = "\033[32m" if COLOR_SUPPORT else ""
    YELLOW = "\033[33m" if COLOR_SUPPORT else ""
    BLUE = "\033[34m" if COLOR_SUPPORT else ""
    CYAN = "\033[36m" if COLOR_SUPPORT else ""
    MAGENTA = "\033[35m" if COLOR_SUPPORT else ""
    BOLD = "\033[1m" if COLOR_SUPPORT else ""


def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_header():
    """Display game title header."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "KING JOHN 1205: A ROYAL CHRONICLE".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()


def display_separator():
    """Display horizontal line separator."""
    print("═" * 80)


def display_date_location(game_state: GameState):
    """Display current date and location."""
    date_str = game_state.current_date.format_long()
    location_str = game_state.location.replace("_", " ").title()

    print(f"{Colors.BOLD}Date:{Colors.RESET} {Colors.BLUE}{date_str}{Colors.RESET}")
    print(f"{Colors.BOLD}Location:{Colors.RESET} {Colors.BLUE}{location_str}{Colors.RESET}")

    # Show feast day if applicable
    feast = game_state.current_date.is_feast_day()
    if feast:
        print(f"{Colors.MAGENTA}Feast Day: {feast}{Colors.RESET}")

    print()


def display_resource_dashboard(game_state: GameState):
    """Display all resources in compact dashboard."""
    print(f"{Colors.BOLD}═══ RESOURCES ═══{Colors.RESET}")

    # Primary resources
    print(f"Treasury: {format_treasury(game_state.treasury)}  "
          f"Authority: {format_stat(game_state.royal_authority)}  "
          f"Military: {format_stat(game_state.military_readiness)}")
    print(f"Papal Relations: {format_stat(game_state.papal_relations, signed=True)}")

    # Averages
    avg_loyalty = game_state.get_average_baronial_loyalty()
    kingdom_stability = game_state.get_kingdom_stability()
    print(f"Baronial Loyalty (avg): {format_stat(avg_loyalty)}  "
          f"Kingdom Stability: {format_stat(kingdom_stability)}")

    print()


def format_treasury(amount: int) -> str:
    """Format treasury with color coding."""
    color = Colors.GREEN if amount > 5000 else (
        Colors.YELLOW if amount > 2000 else Colors.RED
    )
    return f"{color}{amount:,} marks{Colors.RESET}"


def format_stat(value: float, signed: bool = False) -> str:
    """Format stat 0-100 with color and bar."""
    if value > 70:
        color = Colors.GREEN
    elif value > 40:
        color = Colors.YELLOW
    else:
        color = Colors.RED

    # Visual bar (10 blocks)
    bars = int(value / 10)
    bar_display = "▓" * bars + "░" * (10 - bars)

    if signed:
        # For -100 to +100 stats like papal relations
        display_value = int(value)
        sign = "+" if display_value > 0 else ""
        return f"{color}{sign}{display_value}/100{Colors.RESET} {bar_display}"
    else:
        return f"{color}{int(value)}/100{Colors.RESET} {bar_display}"


def display_text(text: str, width: int = 78):
    """Display wrapped text."""
    import textwrap
    wrapped = textwrap.fill(text, width=width)
    print(wrapped)
    print()


def display_choices(choices: List[Choice], game_state: GameState):
    """Display numbered list of choices."""
    print(f"{Colors.BOLD}YOUR OPTIONS:{Colors.RESET}")
    print()

    for i, choice in enumerate(choices, 1):
        display_text = choice.get_display_text(game_state)
        available = choice.check_requirements(game_state)

        if available:
            print(f"  {Colors.BOLD}{i}.{Colors.RESET} {display_text}")
        else:
            print(f"  {Colors.BOLD}{i}.{Colors.RESET} {Colors.RED}{display_text}{Colors.RESET}")

    print()


def get_player_input(prompt: str = "Your choice: ") -> str:
    """Get input from player."""
    return input(f"{Colors.BOLD}{prompt}{Colors.RESET}").strip()


def wait_for_continue():
    """Pause and wait for player to press Enter."""
    input(f"\n{Colors.YELLOW}[Press Enter to continue...]{Colors.RESET}")


def display_resource_changes(old_state: GameState, new_state: GameState):
    """Show what changed after a decision."""
    print(f"{Colors.BOLD}CONSEQUENCES:{Colors.RESET}")

    changes = []

    # Treasury
    if old_state.treasury != new_state.treasury:
        diff = new_state.treasury - old_state.treasury
        color = Colors.GREEN if diff > 0 else Colors.RED
        sign = "+" if diff > 0 else ""
        changes.append(f"Treasury {color}{sign}{diff:,} marks{Colors.RESET}")

    # Authority
    if old_state.royal_authority != new_state.royal_authority:
        diff = new_state.royal_authority - old_state.royal_authority
        color = Colors.GREEN if diff > 0 else Colors.RED
        sign = "+" if diff > 0 else ""
        changes.append(f"Authority {color}{sign}{diff}{Colors.RESET}")

    # ... similar for all resources

    if changes:
        for change in changes:
            print(f"  • {change}")
    else:
        print("  (No immediate resource changes)")

    print()


# ... many more UI functions ...
```

---

## 6. Advisor System

```python
# advisors.py

class Advisor:
    """Base class for advisor personalities."""

    def __init__(
        self,
        name: str,
        role: str,
        personality_traits: List[str],
        expertise_areas: List[str]
    ):
        self.name = name
        self.role = role
        self.personality_traits = personality_traits
        self.expertise_areas = expertise_areas

    def get_advice(
        self,
        event: Event,
        game_state: GameState
    ) -> str:
        """
        Generate advice for an event.
        Override in subclasses for specific personalities.
        """
        return "I defer to your judgment, my lord."

    def get_relationship(self, game_state: GameState) -> int:
        """Get current relationship value with this advisor."""
        # Map advisor to baron if applicable
        return 50  # Default


class WilliamMarshalAdvisor(Advisor):
    """William Marshal - cautious, honorable military advisor."""

    def __init__(self):
        super().__init__(
            "William Marshal",
            "Military Advisor",
            ["cautious", "honorable", "experienced"],
            ["military", "diplomacy", "chivalry"]
        )

    def get_advice(self, event: Event, game_state: GameState) -> str:
        """Generate Marshal-specific advice."""

        # Example: For invasion decision
        if event.event_id == "pentecost_invasion":
            if game_state.military_readiness < 75:
                return (
                    f"{Colors.CYAN}Marshal counsels:{Colors.RESET} "
                    "My lord, our forces are not yet ready for such an "
                    "undertaking. Philip commands superior numbers. I urge "
                    "caution and further preparation."
                )
            elif game_state.get_average_baronial_loyalty() < 60:
                return (
                    f"{Colors.CYAN}Marshal counsels:{Colors.RESET} "
                    "Sire, the barons are not united behind this venture. "
                    "To force the issue risks rebellion at home while we "
                    "fight abroad. We must secure England first."
                )
            else:
                return (
                    f"{Colors.CYAN}Marshal counsels:{Colors.RESET} "
                    "My lord, though the risk is great, our preparations "
                    "are sound. If we strike boldly, we may yet recover "
                    "what was lost. I will serve as you command."
                )

        # Default advice
        return self._generate_generic_advice(event, game_state)

    def _generate_generic_advice(
        self,
        event: Event,
        game_state: GameState
    ) -> str:
        """Generate generic advice based on situation."""
        # Implementation...
        return "I trust your judgment in this matter, sire."


# Similar classes for other advisors:
# - GeoffreyFitzPeterAdvisor (administrative)
# - JohnDeGrayAdvisor (church)
# - IntelligenceOfficer (neutral reporter)
# - QueenIsabellaAdvisor (family/social)


class AdvisorSystem:
    """Manages all advisors."""

    def __init__(self):
        self.advisors = {
            "marshal": WilliamMarshalAdvisor(),
            "fitzpeter": GeoffreyFitzPeterAdvisor(),
            "de_gray": JohnDeGrayAdvisor(),
            "intelligence": IntelligenceOfficer(),
            "isabella": QueenIsabellaAdvisor()
        }

    def consult_all(self, event: Event, game_state: GameState):
        """Get advice from all advisors on an event."""
        print(f"\n{Colors.BOLD}═══ CONSULTING ADVISORS ═══{Colors.RESET}\n")

        for advisor_id, advisor in self.advisors.items():
            relationship = advisor.get_relationship(game_state)

            # Advisors with low relationship may refuse or be terse
            if relationship < 30:
                advice = f"{advisor.name} declines to counsel you."
            else:
                advice = advisor.get_advice(event, game_state)

            print(advice)
            print()

        wait_for_continue()
```

---

## 7. Data File Format

### 7.1 Event Data Structure (Python initially, JSON later)

```python
# data/historical_events.py

from events import Event, Choice

# Example historical event
PENTECOST_INVASION = Event(
    event_id="pentecost_invasion",
    event_type="historical",
    title="The Pentecost Fleet",
    date=(1205, 6, 5),
    location="Portsmouth",
    description="""
Your fleet lies at anchor in Portsmouth harbor, fifty galleys and
twice that many transports. The army you've assembled—knights,
serjeants, and Flemish mercenaries—waits aboard or camps on the
shore. Today is Pentecost, the date you set for your great
enterprise: the reconquest of Normandy.

Yet your tent is heavy with tension. This morning, William Marshal
and several great barons came to you with grave concerns. They
speak of leaving England defenseless, of their own Norman lands
already lost, of the risk of Philip's superior forces. Some refuse
outright to sail.

Marshal stands before you: "My lord, I counsel caution. We have
not the strength to hold Normandy even if we take it. Better to
secure England first."

Your half-brother Longespée counters: "We must strike now, before
Philip consolidates! Give the order to sail, sire."
    """.strip(),
    choices=[
        Choice(
            choice_id=1,
            text="Order the fleet to sail immediately - You are King, they will obey",
            requirements={"resources": {"royal_authority": 70, "military_readiness": 75}},
            consequences={
                "resources": {
                    "treasury": -2000,
                    "royal_authority": 10,
                    "military_readiness": -20
                },
                "relationships": {
                    "william_marshal": -15,
                    "william_longespee": +10
                },
                "regions": {
                    "southern_england": -10
                },
                "flags": {
                    "invasion_launched": True,
                    "invasion_success": True
                }
            },
            narrative_outcome="""
You rise to your full height. "We sail at dawn. Those who refuse
will answer for their disobedience." The tent falls silent. Marshal's
face is grim, but he bows. "As you command, my lord."

Over the next days, your fleet crosses the Channel. Against the odds,
your bold strike catches Philip off-guard. You reclaim several key
fortresses in Normandy. Yet the campaign drains your treasury, and
news from England speaks of baronial discontent...

[Branch: Invasion Success - events change for July-September]
            """.strip()
        ),
        Choice(
            choice_id=2,
            text="Sail with a reduced force of loyalists only",
            requirements=None,
            consequences={
                "resources": {
                    "treasury": -800,
                    "royal_authority": -5,
                    "military_readiness": -10
                },
                "relationships": {
                    "william_longespee": +5,
                    "william_marshal": -5
                },
                "flags": {
                    "invasion_launched": True,
                    "invasion_success": False
                }
            },
            narrative_outcome="""
You make a calculated decision. "Those loyal to their king will sail.
The rest may remain and explain themselves later." Longespée leads
the expedition with a smaller but dedicated force.

The campaign achieves limited success in Poitou, but lacks the
strength for Normandy. Philip remains entrenched. Still, you've
shown you will not be deterred, and your continental allies take heart.
            """.strip()
        ),
        Choice(
            choice_id=3,
            text="Cancel the invasion and punish those who refused",
            requirements=None,
            consequences={
                "resources": {
                    "treasury": -300,
                    "royal_authority": 5,
                    "military_readiness": -15
                },
                "relationships": {
                    "william_marshal": -10,
                    "william_de_braose": -8
                },
                "regions": {
                    "northern_england": -5
                },
                "flags": {
                    "invasion_launched": False,
                    "barons_punished": True
                }
            },
            narrative_outcome="""
Your rage boils over. "So be it. The invasion is cancelled. But those
who refused their king will pay scutage double." You demand hostages
from the recalcitrant barons.

Your authority is maintained, but at a cost. The barons comply, but
resentment festers. They whisper that you are becoming a tyrant. The
seeds of future rebellion are sown.
            """.strip()
        ),
        Choice(
            choice_id=4,
            text="Cancel and accept their counsel gracefully (Historical path)",
            requirements=None,
            consequences={
                "resources": {
                    "royal_authority": -10,
                    "military_readiness": -5
                },
                "relationships": {
                    "william_marshal": +5
                },
                "flags": {
                    "invasion_launched": False,
                    "historical_path_pentecost": True
                }
            },
            narrative_outcome="""
You exhale slowly. Pride wars with pragmatism, and pragmatism wins.
"Very well. We will not sail under such circumstances. Let the fleet
be disbanded for now."

Marshal looks relieved. The other barons bow gratefully. You have
kept the peace with your magnates, but your grand design lies in ruins.
History will judge whether this was wisdom or weakness.

[Historical path - events proceed as they did in actual 1205]
            """.strip()
        )
    ],
    historical_context="""
Historically, King John cancelled the invasion of Normandy at Pentecost
1205 due to baronial refusal to serve. Many of his nobles had already
lost their Norman lands and saw no reason to risk life and treasure for
a lost cause. Only a small force under William Longespée sailed to Poitou
later that year. This failure to act contributed to John's reputation and
increased baronial resentment over heavy taxation with no results. The
tensions from 1205 would eventually explode into open rebellion and
Magna Carta in 1215.

Source: W.L. Warren, "King John", pp. 142-147
    """.strip(),
    historical_outcome="invasion_cancelled"
)


# Collect all historical events in a list
HISTORICAL_EVENTS = [
    PENTECOST_INVASION,
    # ... 59 more events
]
```

### 7.2 Migration to JSON

```json
{
  "event_id": "pentecost_invasion",
  "event_type": "historical",
  "title": "The Pentecost Fleet",
  "date": [1205, 6, 5],
  "location": "Portsmouth",
  "description": "Your fleet lies at anchor...",
  "choices": [
    {
      "choice_id": 1,
      "text": "Order the fleet to sail immediately...",
      "requirements": {
        "resources": {
          "royal_authority": 70,
          "military_readiness": 75
        }
      },
      "consequences": {
        "resources": {
          "treasury": -2000,
          "royal_authority": 10,
          "military_readiness": -20
        },
        "relationships": {
          "william_marshal": -15,
          "william_longespee": 10
        },
        "regions": {
          "southern_england": -10
        },
        "flags": {
          "invasion_launched": true,
          "invasion_success": true
        }
      },
      "narrative_outcome": "You rise to your full height..."
    }
  ],
  "historical_context": "Historically, King John cancelled...",
  "historical_outcome": "invasion_cancelled"
}
```

---

## 8. Testing Strategy

### 8.1 Unit Tests

```python
# tests/test_game_state.py

import unittest
from game_state import GameState
from calendar import Date

class TestGameState(unittest.TestCase):

    def setUp(self):
        self.game_state = GameState()

    def test_initial_values(self):
        """Test that game state initializes with correct values."""
        self.assertEqual(self.game_state.treasury, 8000)
        self.assertEqual(self.game_state.royal_authority, 65)
        self.assertEqual(len(self.game_state.barons), 8)

    def test_advance_day(self):
        """Test that day advances correctly."""
        initial_day = self.game_state.current_date.day
        self.game_state.advance_day()
        self.assertEqual(self.game_state.current_date.day, initial_day + 1)

    def test_apply_consequences(self):
        """Test that consequences modify state correctly."""
        consequences = {
            "resources": {"treasury": -500, "authority": 5},
            "relationships": {"william_marshal": -10}
        }
        self.game_state.apply_consequences(consequences)

        self.assertEqual(self.game_state.treasury, 7500)
        self.assertEqual(self.game_state.royal_authority, 70)
        self.assertEqual(self.game_state.barons["william_marshal"], 60)

    def test_check_game_over_bankruptcy(self):
        """Test that bankruptcy triggers game over."""
        self.game_state.treasury = -1000
        self.game_state.days_since_negative_treasury = 31
        is_over, reason = self.game_state.check_game_over()

        self.assertTrue(is_over)
        self.assertEqual(reason, "bankruptcy")

    def test_save_load_roundtrip(self):
        """Test that saving and loading preserves state."""
        self.game_state.treasury = 5000
        self.game_state.flags["test_flag"] = True

        save_dict = self.game_state.to_dict()
        loaded_state = GameState.from_dict(save_dict)

        self.assertEqual(loaded_state.treasury, 5000)
        self.assertTrue(loaded_state.flags["test_flag"])


# tests/test_events.py

class TestEvent(unittest.TestCase):

    def test_event_condition_checking(self):
        """Test that event conditions are evaluated correctly."""
        event = Event(
            event_id="test",
            event_type="triggered",
            title="Test Event",
            description="Test",
            choices=[],
            conditions={"resources": {"royal_authority": 70}}
        )

        game_state = GameState()
        game_state.royal_authority = 60
        self.assertFalse(event.check_conditions(game_state))

        game_state.royal_authority = 75
        self.assertTrue(event.check_conditions(game_state))

    # More event tests...


# tests/test_calendar.py

class TestDate(unittest.TestCase):

    def test_date_increment(self):
        """Test that dates increment correctly including month rollovers."""
        date = Date(1205, 1, 31)
        date.increment()
        self.assertEqual(date.month, 2)
        self.assertEqual(date.day, 1)

    def test_feast_day_detection(self):
        """Test that feast days are detected."""
        christmas = Date(1205, 12, 25)
        self.assertEqual(christmas.is_feast_day(), "Christmas")

        normal_day = Date(1205, 5, 15)
        self.assertIsNone(normal_day.is_feast_day())

    # More calendar tests...
```

### 8.2 Integration Tests

```python
# tests/test_integration.py

class TestGameLoop(unittest.TestCase):

    def test_full_day_cycle(self):
        """Test that a complete day cycle functions without errors."""
        game_state = GameState()
        event_manager = EventManager()
        event_manager.load_all_events()

        # Simulate one day
        event = event_manager.get_event_for_day(game_state)
        if event:
            available_choices = event.get_available_choices(game_state)
            if available_choices:
                choice = available_choices[0]
                game_state.apply_consequences(choice.consequences)

        game_state.advance_day()

        # Verify state is still valid
        self.assertEqual(game_state.current_date.day, 2)
        self.assertIsNotNone(game_state.treasury)

    def test_save_load_integration(self):
        """Test that save/load works in game context."""
        game_state = GameState()
        game_state.advance_day()
        game_state.treasury -= 1000

        SaveManager.save_game(game_state, "test_slot")
        loaded_state = SaveManager.load_game("test_slot")

        self.assertEqual(loaded_state.current_date.day, game_state.current_date.day)
        self.assertEqual(loaded_state.treasury, game_state.treasury)
```

### 8.3 Playtesting Checklist

**Milestone 1 Testing:**
- [ ] Day advances correctly
- [ ] Resources display accurately
- [ ] One event can be completed
- [ ] Consequences apply correctly
- [ ] Save/load works

**Milestone 2 Testing:**
- [ ] Multiple events flow naturally
- [ ] All event types trigger appropriately
- [ ] Advisor system functions
- [ ] Resource balance feels right
- [ ] No soft-locks or dead-ends

**Milestone 3 Testing:**
- [ ] Full year playthrough completable
- [ ] All major historical events work
- [ ] Multiple endings reachable
- [ ] Performance acceptable (no lag)
- [ ] Save files robust

**Milestone 4 Testing:**
- [ ] UI polished and readable
- [ ] No typos or grammatical errors
- [ ] Balance testing (difficulty)
- [ ] Edge case testing (extreme resource values)
- [ ] Cross-platform testing

---

## 9. Performance Considerations

### 9.1 Optimization Targets

**Memory:**
- Game state: <5 MB
- Event data: <10 MB loaded
- Total runtime memory: <50 MB

**Speed:**
- Game load: <2 seconds
- Save operation: <1 second
- Event processing: <100ms
- UI updates: Instant

### 9.2 Potential Bottlenecks

**Event Loading:**
- Solution: Lazy load event data, only load categories as needed
- Cache frequently accessed events

**Save File Size:**
- Solution: Compress save data (gzip)
- Only store necessary state

**UI Rendering:**
- Solution: Minimize screen clears
- Buffer output before displaying

---

## 10. Future Technical Enhancements

### 10.1 Web Port Architecture

When porting to web:

**Backend (Optional):**
- Python Flask or FastAPI for game logic
- Or fully client-side JavaScript

**Frontend:**
- React or Vue.js for UI
- CSS styled like illuminated manuscript
- Canvas or SVG for maps

**Data:**
- JSON events served via API or bundled
- LocalStorage for saves
- Optional: Cloud saves with accounts

### 10.2 Modding Support

**To enable modding:**
- Fully externalize event data to JSON
- Document JSON schema
- Event validation tools
- Mod loading system
- Community event repository

### 10.3 Advanced Features

**Analytics:**
- Track player choices across playthroughs
- Popular paths and outcomes
- Difficulty metrics

**Procedural Content:**
- Procedurally generated minor events
- Name/location generators for templates
- Random event parameter variation

---

## 11. Dependencies and Requirements

### 11.1 Python Requirements

```
# requirements.txt
# No external dependencies for Phase 1-5
# Optional:
colorama>=0.4.6  # For Windows color support (optional)
```

### 11.2 Development Tools

- Python 3.9+
- Git for version control
- Text editor / IDE
- pytest for testing (optional)

### 11.3 Deployment

**Python Executable:**
- Use PyInstaller to create standalone executable
- Bundle all data files

**Web Deployment:**
- Static hosting (GitHub Pages, Netlify)
- Or dynamic with backend (Heroku, AWS)

---

## 12. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-18 | Initial TDD created | Claude & User |

---

**Document Status:** APPROVED FOR DEVELOPMENT
**Next Review:** After Milestone 1 implementation
