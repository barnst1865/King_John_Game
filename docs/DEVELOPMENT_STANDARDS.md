# King John 1205: Development Standards

**Version:** 1.0
**Date:** January 18, 2026
**Purpose:** Coding conventions, git practices, testing standards, and development workflow

---

## 1. Code Style and Conventions

### 1.1 Python Style Guide

**Follow PEP 8** with specific project conventions:

**Naming Conventions:**
```python
# Classes: PascalCase
class GameState:
class EventManager:
class WilliamMarshalAdvisor:

# Functions and methods: snake_case
def advance_day():
def get_event_for_day():
def apply_consequences():

# Constants: UPPER_SNAKE_CASE
MAX_TREASURY = 20000
DAYS_IN_YEAR = 365
DEFAULT_AUTHORITY = 65

# Variables: snake_case
game_state = GameState()
event_manager = EventManager()
current_date = Date(1205, 1, 1)

# Private methods/attributes: _leading_underscore
def _validate_date():
self._internal_state = {}
```

**Line Length:**
- Maximum 100 characters (slightly longer than PEP 8's 79)
- Break long lines logically

**Imports:**
```python
# Standard library imports first
import os
import sys
from typing import Dict, List, Optional

# Third-party imports second (if any)
# import colorama

# Local imports last
from game_state import GameState
from events import Event, EventManager
from calendar import Date
```

**Docstrings:**
```python
def apply_consequences(self, consequences: Dict[str, Any]) -> None:
    """
    Apply event consequences to game state.

    Updates resources, relationships, regions, and flags based on
    the provided consequences dictionary.

    Args:
        consequences: Dictionary containing resource changes,
            relationship changes, regional changes, and flag updates.

    Returns:
        None. Modifies game state in place.

    Example:
        consequences = {
            "resources": {"treasury": -500, "authority": 5},
            "relationships": {"william_marshal": -10}
        }
        game_state.apply_consequences(consequences)
    """
    # Implementation...
```

**Type Hints:**
- Use type hints for all function signatures
- Use typing module for complex types

```python
def get_event_for_day(
    self,
    game_state: GameState
) -> Optional[Event]:
    """Get the event for the current day."""
    pass

def calculate_score(
    resources: Dict[str, int],
    relationships: Dict[str, int]
) -> int:
    """Calculate final score from game state."""
    pass
```

### 1.2 Code Organization

**File Structure:**
```
module.py
├── Imports
├── Constants
├── Helper functions (if needed)
├── Main classes
└── Main execution (if __name__ == "__main__")
```

**Class Structure:**
```python
class GameState:
    """Class docstring."""

    # Class constants
    STARTING_TREASURY = 8000

    def __init__(self):
        """Initialize game state."""
        # Instance attributes
        self.treasury = self.STARTING_TREASURY
        # ...

    # Public methods
    def advance_day(self) -> None:
        """Public method docstring."""
        pass

    def apply_consequences(self, consequences: Dict[str, Any]) -> None:
        """Public method docstring."""
        pass

    # Private methods (used internally only)
    def _validate_state(self) -> bool:
        """Private method docstring."""
        pass

    # Special methods last
    def __str__(self) -> str:
        """String representation."""
        return f"GameState(day={self.current_date})"
```

### 1.3 Comments and Documentation

**When to Comment:**
```python
# DO: Explain WHY, not WHAT
# We need to check treasury weekly because daily checks cause
# unnecessary event spam when player is low on funds
if self.days_played % 7 == 0:
    self._check_treasury_status()

# DON'T: State the obvious
# Increment the day by 1
self.day += 1
```

**Complex Logic:**
```python
# DO: Break down complex calculations
# Calculate weighted average regional stability
# Southern England counts double as it's the royal heartland
weights = {
    "southern_england": 2.0,
    "northern_england": 1.0,
    "welsh_marches": 1.0,
    # ...
}
total = sum(self.regions[r] * weights[r] for r in self.regions)
total_weight = sum(weights.values())
return total / total_weight
```

**TODOs:**
```python
# TODO: Implement Easter calculation for moveable feast
# TODO: Add save file compression for smaller file sizes
# FIXME: Event selection can trigger same random event twice
# HACK: Workaround for colorama on Mac - remove when fixed
```

### 1.4 Error Handling

**Use Exceptions Appropriately:**
```python
# For invalid data
def __init__(self, year: int, month: int, day: int):
    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month: {month}")
    if not (1 <= day <= self.DAYS_IN_MONTH[month - 1]):
        raise ValueError(f"Invalid day: {day} for month {month}")

# For file operations
try:
    with open(filepath, 'r') as f:
        save_data = json.load(f)
except FileNotFoundError:
    logging.error(f"Save file not found: {filepath}")
    return None
except json.JSONDecodeError as e:
    logging.error(f"Invalid JSON in save file: {e}")
    return None
```

**Fail Fast:**
```python
# Validate inputs early
def apply_consequences(self, consequences: Dict[str, Any]) -> None:
    if not isinstance(consequences, dict):
        raise TypeError("Consequences must be a dictionary")

    # Then proceed with logic
    # ...
```

**Logging:**
```python
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Use throughout code
logging.info("Game started")
logging.warning("Treasury below 1000 marks")
logging.error("Failed to load event: invalid format")
logging.debug(f"Event triggered: {event.event_id}")
```

---

## 2. Git Workflow and Version Control

### 2.1 Branch Strategy

**Main Development Branch:**
- `claude/king-john-adventure-game-cEQCi`
- All development happens here
- Keep branch up to date
- Never force push

**No Feature Branches (Single Developer):**
- All commits go to main dev branch
- Use descriptive commit messages to track work

### 2.2 Commit Guidelines

**Commit Frequently:**
- Commit working code after each logical unit
- Don't commit broken code
- Aim for 2-5 commits per day of work

**Commit Message Format:**
```
[Phase X, Week Y] Brief description (50 chars or less)

Detailed explanation of changes (if needed):
- Bullet point 1
- Bullet point 2

Testing notes:
- What was tested
- Any known issues
```

**Examples of Good Commits:**
```
[Phase 1, Week 2] Implement GameState class with save/load

- Created complete GameState class with all resources
- Added consequence application logic
- Implemented SaveManager with JSON serialization
- Unit tests pass for save/load round-trip

Testing: Saved and loaded game state at different points,
verified all values preserved correctly.
```

```
[Phase 3, Week 6] Add Pentecost Invasion historical event

- Implemented full event with 4 choice branches
- Tested all choices and consequences
- Added historical context note
- Integrated with event manager

Testing: Played through event multiple times, all paths work.
Known issue: Need to balance consequence values.
```

```
[Phase 5, Week 14] Fix achievement unlock logic

- Fixed bug where achievements unlocked prematurely
- Added validation before unlock
- Updated achievement display UI

Testing: Verified achievements only unlock when conditions met.
Closes issue #12.
```

**Examples of Bad Commits:**
```
[Bad] stuff
[Bad] Fixed things
[Bad] WIP
[Bad] asdfasdf
[Bad] More changes
```

### 2.3 What to Commit

**DO Commit:**
- All source code files (.py)
- Documentation files (.md)
- Configuration files
- README
- Requirements.txt
- Test files
- Example/template data files

**DON'T Commit:**
- Save game files (*.json in saves/)
- Python cache files (__pycache__, *.pyc)
- IDE specific files (.vscode, .idea)
- Personal notes (unless project-relevant)
- Large binary files
- Temporary files

**Create .gitignore:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Project specific
saves/*.json
!saves/.gitkeep
logs/*.log
!logs/.gitkeep
personal_notes.txt

# OS
.DS_Store
Thumbs.db
```

### 2.4 Push Strategy

**Push Regularly:**
- Push at end of each work session
- Push after completing milestone
- Push after significant feature completion

**Before Pushing:**
1. Ensure code runs without errors
2. Run tests (if applicable)
3. Review changes (`git diff`)
4. Verify correct branch
5. Write clear commit message

**Push Command:**
```bash
git add .
git commit -m "[Phase X] Brief description

Detailed changes..."
git push -u origin claude/king-john-adventure-game-cEQCi
```

**Retry Logic for Network Issues:**
If push fails due to network:
1. Wait 2 seconds, retry
2. Wait 4 seconds, retry
3. Wait 8 seconds, retry
4. Wait 16 seconds, final retry
5. If still failing, report issue

---

## 3. Testing Standards

### 3.1 Unit Testing

**Use Python's unittest:**
```python
import unittest
from game_state import GameState

class TestGameState(unittest.TestCase):
    """Test GameState class."""

    def setUp(self):
        """Set up test fixtures."""
        self.game_state = GameState()

    def tearDown(self):
        """Clean up after tests."""
        pass

    def test_initial_treasury(self):
        """Test that treasury initializes correctly."""
        self.assertEqual(self.game_state.treasury, 8000)

    def test_apply_treasury_change(self):
        """Test applying treasury consequences."""
        consequences = {"resources": {"treasury": -500}}
        self.game_state.apply_consequences(consequences)
        self.assertEqual(self.game_state.treasury, 7500)

    def test_treasury_clamping(self):
        """Test that treasury doesn't go below 0."""
        consequences = {"resources": {"treasury": -10000}}
        self.game_state.apply_consequences(consequences)
        self.assertGreaterEqual(self.game_state.treasury, -10000)
        # Note: Negative allowed but tracked for game over

if __name__ == '__main__':
    unittest.main()
```

**Test Coverage Goals:**
- Core systems: 80%+ coverage
- Game logic: 60%+ coverage
- UI: Manual testing (hard to automate terminal UI)
- Content: Manual playtesting

**Run Tests:**
```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests/test_game_state.py

# Run specific test
python -m unittest tests.test_game_state.TestGameState.test_initial_treasury
```

### 3.2 Integration Testing

**Test System Interactions:**
```python
class TestGameLoop(unittest.TestCase):
    """Test full game loop integration."""

    def test_one_day_cycle(self):
        """Test complete day cycle."""
        game_state = GameState()
        event_manager = EventManager()
        event_manager.load_all_events()

        # Simulate one day
        initial_day = game_state.current_date.day
        event = event_manager.get_event_for_day(game_state)

        if event:
            choices = event.get_available_choices(game_state)
            if choices:
                choice = choices[0]
                game_state.apply_consequences(choice.consequences)

        game_state.advance_day()

        # Verify state is valid
        self.assertEqual(game_state.current_date.day, initial_day + 1)
        self.assertIsNotNone(game_state.treasury)
        self.assertFalse(game_state.check_game_over()[0])
```

### 3.3 Manual Testing Checklist

**Before Committing Code:**
- [ ] Code runs without crashes
- [ ] No Python syntax errors
- [ ] Key functionality works as expected
- [ ] No obvious bugs introduced

**Before Milestone Completion:**
- [ ] All milestone features functional
- [ ] Full playthrough of milestone content
- [ ] Save/load tested at milestone
- [ ] No game-breaking bugs
- [ ] UI displays correctly

**Before Release:**
- [ ] Multiple full playthroughs
- [ ] All event types tested
- [ ] All endings reachable
- [ ] Save/load robust
- [ ] Cross-platform testing
- [ ] Performance acceptable

### 3.4 Bug Reporting

**Track Bugs in BUGS.md:**
```markdown
# Known Bugs

## Critical (Must Fix Before Release)
- [ ] Save file corruption when quitting during event resolution
- [ ] Game crashes if treasury goes below -10000

## High Priority (Should Fix)
- [ ] Event can trigger twice if reloading same day
- [ ] Advisor dialogue overlaps with event text

## Medium Priority (Fix If Time)
- [ ] Color display issues on some terminals
- [ ] Minor typo in March 12 event

## Low Priority (Nice To Fix)
- [ ] Journal search is slow with 100+ entries
- [ ] Could use better error message for invalid saves
```

**Bug Report Format:**
```markdown
## Bug: Save file corruption during event

**Priority:** Critical
**Discovered:** 2026-01-20
**Steps to reproduce:**
1. Start game
2. Play to first event
3. Make choice
4. Quit immediately (don't advance day)
5. Load save - file is corrupt

**Expected:** Save file loads correctly
**Actual:** JSON decode error

**Notes:** Issue is with timing of auto-save vs. state update
**Fix:** Move auto-save to after state fully updated
```

---

## 4. Code Review Guidelines

### 4.1 Self-Review Checklist

**Before Marking Code Complete:**
- [ ] Code follows style guide
- [ ] No unused imports or variables
- [ ] All functions have docstrings
- [ ] Type hints present
- [ ] No obvious performance issues
- [ ] Error handling appropriate
- [ ] Tested and working
- [ ] Commented where needed (not obvious code)

### 4.2 Code Quality Indicators

**Good Code:**
- Easy to read and understand
- Clear variable/function names
- Appropriate abstraction level
- DRY (Don't Repeat Yourself)
- Single Responsibility Principle
- Well-documented

**Code Smells to Avoid:**
- Functions longer than 50 lines
- Deeply nested conditionals (>3 levels)
- Magic numbers (use named constants)
- Copy-pasted code
- Unclear variable names (x, tmp, data)
- God objects (classes that do everything)

**Refactoring Triggers:**
- If you write same code twice, extract function
- If function does multiple things, split it
- If conditional is complex, extract to method
- If code is hard to test, refactor for testability

### 4.3 Example: Before and After Refactoring

**Before (Code Smell):**
```python
def process_event(e, gs):
    # Apply consequences
    if "resources" in e["consequences"]:
        for r, v in e["consequences"]["resources"].items():
            if r == "treasury":
                gs.treasury += v
            elif r == "authority":
                gs.royal_authority += v
                if gs.royal_authority > 100:
                    gs.royal_authority = 100
                elif gs.royal_authority < 0:
                    gs.royal_authority = 0
            elif r == "military":
                gs.military_readiness += v
                if gs.military_readiness > 100:
                    gs.military_readiness = 100
                elif gs.military_readiness < 0:
                    gs.military_readiness = 0
            # ... etc
```

**After (Clean Code):**
```python
def apply_consequences(
    self,
    consequences: Dict[str, Any]
) -> None:
    """Apply event consequences to game state."""
    if "resources" in consequences:
        self._apply_resource_changes(consequences["resources"])

    if "relationships" in consequences:
        self._apply_relationship_changes(consequences["relationships"])

    if "regions" in consequences:
        self._apply_regional_changes(consequences["regions"])

def _apply_resource_changes(self, changes: Dict[str, int]) -> None:
    """Apply resource changes with clamping."""
    for resource, change in changes.items():
        if resource == "treasury":
            self.treasury += change
        elif resource in ["royal_authority", "military_readiness", "papal_relations"]:
            current = getattr(self, resource)
            setattr(self, resource, clamp(current + change, 0, 100))
```

---

## 5. Performance Guidelines

### 5.1 Performance Targets

**Acceptable Performance:**
- Game start: < 2 seconds
- Day advancement: < 100ms
- Event display: Instant (<50ms)
- Save operation: < 1 second
- Load operation: < 1 second
- Memory usage: < 50MB

### 5.2 Optimization Tips

**Premature Optimization is Bad, But...**
- Don't optimize before measuring
- Profile before optimizing
- Focus on hot paths (code run frequently)
- Simple code is usually fast enough

**Common Optimizations:**

**1. Cache Expensive Calculations:**
```python
# Bad: Recalculate every time
def get_average_loyalty(self):
    return sum(self.barons.values()) / len(self.barons)

# Good: Cache if called frequently
def get_average_loyalty(self):
    if self._loyalty_cache_dirty:
        self._loyalty_cache = sum(self.barons.values()) / len(self.barons)
        self._loyalty_cache_dirty = False
    return self._loyalty_cache
```

**2. Avoid Repeated Work:**
```python
# Bad: Check same condition multiple times
if event.check_conditions(game_state):
    # ... later in code
    if event.check_conditions(game_state):
        # ...

# Good: Check once, store result
is_valid = event.check_conditions(game_state)
if is_valid:
    # ... later
    if is_valid:
        # ...
```

**3. Use Appropriate Data Structures:**
```python
# Bad: List for membership testing
triggered_events = []
if event_id in triggered_events:  # O(n) lookup

# Good: Set for membership testing
triggered_events = set()
if event_id in triggered_events:  # O(1) lookup
```

### 5.3 Memory Management

**Avoid Memory Leaks:**
- Don't store references to temporary objects
- Clear caches periodically
- Don't accumulate infinite history

**Example:**
```python
# Bad: Unlimited event history
self.event_history.append(record)  # Grows forever

# Good: Limit history size
MAX_HISTORY = 500
self.event_history.append(record)
if len(self.event_history) > MAX_HISTORY:
    self.event_history = self.event_history[-MAX_HISTORY:]
```

---

## 6. Documentation Standards

### 6.1 Code Documentation

**Module Docstrings:**
```python
"""
game_state.py

Contains the GameState class which maintains complete game state
including date, resources, relationships, flags, and history.

This is the central data structure for the entire game. All game
systems interact with GameState to read and modify the state.
"""
```

**Class Docstrings:**
```python
class GameState:
    """
    Maintains complete game state for King John 1205.

    The GameState class stores all game data including the current date,
    king's location, resources (treasury, authority, etc.), baronial
    relationships, regional stability, state flags, event history, and
    active event chains.

    Attributes:
        current_date: Date object representing current in-game date
        treasury: Integer amount of gold marks available
        royal_authority: Int 0-100 representing king's power
        barons: Dict mapping baron names to relationship values (0-100)
        regions: Dict mapping region names to stability values (0-100)
        flags: Dict storing game state flags
        event_history: List of EventRecord objects
        active_chains: List of currently active EventChain objects

    Example:
        >>> game_state = GameState()
        >>> game_state.advance_day()
        >>> game_state.treasury -= 500
        >>> game_state.save("autosave")
    """
```

**Function Docstrings:**
```python
def apply_consequences(
    self,
    consequences: Dict[str, Any]
) -> None:
    """
    Apply event consequences to game state.

    Processes a consequences dictionary and updates game state
    accordingly. Handles resource changes, relationship changes,
    regional stability changes, and flag updates. All values are
    clamped to valid ranges.

    Args:
        consequences: Dictionary with keys:
            - "resources": Dict of resource name -> change amount
            - "relationships": Dict of baron name -> change amount
            - "regions": Dict of region name -> change amount
            - "flags": Dict of flag name -> new value

    Returns:
        None. Modifies game state in place.

    Raises:
        TypeError: If consequences is not a dictionary
        KeyError: If invalid resource/baron/region name provided

    Example:
        >>> consequences = {
        ...     "resources": {"treasury": -500, "authority": 5},
        ...     "relationships": {"william_marshal": -10}
        ... }
        >>> game_state.apply_consequences(consequences)
    """
```

### 6.2 README Files

**Project README (README.md):**
- Project description
- Installation instructions
- How to play
- Features
- Credits
- License

**Module README (if needed):**
- Explanation of module purpose
- Key classes/functions
- Usage examples
- Dependencies

### 6.3 Changelog

**Maintain CHANGELOG.md:**
```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- New achievement system
- Enhanced journal with search

### Changed
- Improved event selection algorithm

### Fixed
- Fixed save file corruption bug

## [0.2.0] - 2026-02-15
### Added
- Vertical slice complete
- 15 historical events
- Advisor system

### Changed
- Rebalanced resource gains/losses

## [0.1.0] - 2026-01-31
### Added
- Core game loop
- Date/calendar system
- Save/load system
- Basic UI
```

---

## 7. Development Environment Setup

### 7.1 Required Tools

**Python:**
```bash
# Verify Python version
python --version  # Should be 3.9+

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies (when added)
pip install -r requirements.txt
```

**Git:**
```bash
# Configure git (if not already)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Clone repository (if needed)
git clone <repository-url>
cd King_John_Game

# Verify correct branch
git branch
# Should show: claude/king-john-adventure-game-cEQCi
```

**Text Editor/IDE:**
- VS Code (recommended, with Python extension)
- PyCharm
- Sublime Text
- Vim/Emacs (if preferred)

### 7.2 Project Structure Setup

```
King_John_Game/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── game_state.py
├── events.py
├── calendar.py
├── ui.py
├── advisors.py
├── location.py
├── data/
│   ├── __init__.py
│   ├── historical_events.py
│   ├── triggered_events.py
│   ├── event_templates.py
│   ├── random_events.py
│   ├── chains.py
│   ├── characters.py
│   └── locations.py
├── utils/
│   ├── __init__.py
│   ├── text_utils.py
│   ├── game_logic.py
│   └── validation.py
├── tests/
│   ├── __init__.py
│   ├── test_game_state.py
│   ├── test_events.py
│   ├── test_calendar.py
│   └── test_integration.py
├── saves/
│   └── .gitkeep
├── docs/
│   ├── GAME_DESIGN_DOCUMENT.md
│   ├── TECHNICAL_DESIGN_DOCUMENT.md
│   ├── PROJECT_ROADMAP.md
│   ├── CONTENT_WRITING_GUIDELINES.md
│   └── DEVELOPMENT_STANDARDS.md
└── logs/
    └── .gitkeep
```

### 7.3 Development Workflow

**Daily Workflow:**
1. Pull latest changes: `git pull origin claude/king-john-adventure-game-cEQCi`
2. Review current task from roadmap
3. Code, following standards
4. Test locally
5. Commit with clear message
6. Push at end of session

**Starting New Feature:**
1. Review design docs
2. Plan implementation approach
3. Write stub functions/classes
4. Implement incrementally
5. Test as you go
6. Document
7. Commit when complete

**Debugging Workflow:**
1. Reproduce bug consistently
2. Add logging/print statements
3. Identify root cause
4. Fix
5. Test fix
6. Commit with bug description in message
7. Update BUGS.md if applicable

---

## 8. Quality Assurance Checklist

### 8.1 Before Every Commit

- [ ] Code follows style guide
- [ ] No syntax errors
- [ ] Code runs without crashes
- [ ] New code has docstrings
- [ ] Obvious bugs fixed
- [ ] Commit message is clear

### 8.2 Before Milestone Completion

- [ ] All milestone features complete
- [ ] Unit tests pass (if applicable)
- [ ] Integration testing done
- [ ] Manual playthrough successful
- [ ] Documentation updated
- [ ] No critical bugs
- [ ] Code reviewed (self-review)
- [ ] Ready for user testing

### 8.3 Before Release

- [ ] All features implemented
- [ ] All critical bugs fixed
- [ ] Full playthroughs completed (3+)
- [ ] Cross-platform testing done
- [ ] Performance acceptable
- [ ] Documentation complete
- [ ] CHANGELOG updated
- [ ] Version number set
- [ ] README polished
- [ ] User-tested and approved

---

## 9. Troubleshooting Common Issues

### 9.1 Git Issues

**Problem: Push fails with 403**
```
Error: 403 forbidden
```
**Solution:** Branch name must start with 'claude/' and match session ID
```bash
git checkout -b claude/king-john-adventure-game-cEQCi
git push -u origin claude/king-john-adventure-game-cEQCi
```

**Problem: Merge conflicts**
**Solution:** Since single developer, shouldn't happen. If it does:
```bash
git pull origin claude/king-john-adventure-game-cEQCi
# Resolve conflicts in files
git add .
git commit -m "Resolve merge conflicts"
git push
```

### 9.2 Python Issues

**Problem: Import errors**
```
ModuleNotFoundError: No module named 'game_state'
```
**Solution:** Ensure you're in correct directory, or add to PYTHONPATH
```bash
# Run from project root
cd King_John_Game
python main.py

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Problem: Encoding issues with unicode characters**
**Solution:** Ensure UTF-8 encoding
```python
# At top of file
# -*- coding: utf-8 -*-

# When opening files
with open(filepath, 'r', encoding='utf-8') as f:
    data = f.read()
```

### 9.3 Testing Issues

**Problem: Tests fail unexpectedly**
**Solution:** Check test isolation, reset state
```python
def setUp(self):
    """Create fresh state for each test."""
    self.game_state = GameState()  # Fresh instance

def tearDown(self):
    """Clean up after test."""
    self.game_state = None
```

---

## 10. Best Practices Summary

### 10.1 Do's

✅ **DO:**
- Write clear, readable code
- Use meaningful names
- Add docstrings and comments
- Test your code
- Commit frequently with clear messages
- Follow the style guide
- Ask questions when uncertain
- Refactor when code smells
- Document decisions
- Keep functions small and focused

### 10.2 Don'ts

❌ **DON'T:**
- Commit broken code
- Use unclear variable names
- Write functions longer than 50 lines
- Copy-paste code (DRY)
- Leave TODO comments forever
- Skip testing
- Ignore warnings/errors
- Prematurely optimize
- Over-engineer
- Force push to shared branch

### 10.3 When In Doubt

**Code Style:** Follow PEP 8 and this document
**Architecture:** Refer to TDD
**Design:** Refer to GDD
**Process:** Refer to Roadmap
**Content:** Refer to Writing Guidelines

**Still Uncertain?**
- Look at existing code for examples
- Consult documentation
- Start simple, refactor later
- Ask for clarification

---

## 11. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-18 | Initial development standards created | Claude & User |

---

**Document Status:** APPROVED
**Next Review:** As issues arise or practices evolve
