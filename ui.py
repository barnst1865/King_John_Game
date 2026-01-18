"""
ui.py

User Interface system for King John 1205.
Handles all terminal display, formatting, and input.
"""

import os
import sys
import textwrap
from typing import Optional

from game_state import GameState
from calendar import get_season, get_weather_flavor
from data.locations import format_location_name


# Optional color support
try:
    import colorama
    colorama.init()
    COLOR_SUPPORT = True
except ImportError:
    COLOR_SUPPORT = False


class Colors:
    """ANSI color codes for terminal display."""
    RESET = "\033[0m" if COLOR_SUPPORT else ""
    RED = "\033[31m" if COLOR_SUPPORT else ""
    GREEN = "\033[32m" if COLOR_SUPPORT else ""
    YELLOW = "\033[33m" if COLOR_SUPPORT else ""
    BLUE = "\033[34m" if COLOR_SUPPORT else ""
    CYAN = "\033[36m" if COLOR_SUPPORT else ""
    MAGENTA = "\033[35m" if COLOR_SUPPORT else ""
    BOLD = "\033[1m" if COLOR_SUPPORT else ""
    DIM = "\033[2m" if COLOR_SUPPORT else ""


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_header() -> None:
    """Display the game title header."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "KING JOHN 1205: A ROYAL CHRONICLE".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()


def display_separator(char: str = "═", width: int = 80) -> None:
    """
    Display a horizontal separator line.

    Args:
        char: Character to use for the line
        width: Width of the line
    """
    print(char * width)


def display_date_location(game_state: GameState) -> None:
    """
    Display current date and location.

    Args:
        game_state: Current game state
    """
    date_str = game_state.current_date.format_long()
    location_str = format_location_name(game_state.location)

    print(f"{Colors.BOLD}Date:{Colors.RESET} {Colors.BLUE}{date_str}{Colors.RESET}")
    print(f"{Colors.BOLD}Location:{Colors.RESET} {Colors.BLUE}{location_str}{Colors.RESET}")

    # Show feast day if applicable
    feast = game_state.current_date.is_feast_day()
    if feast:
        print(f"{Colors.MAGENTA}⛪ Feast Day: {feast}{Colors.RESET}")

    # Show travel status
    if game_state.traveling_to:
        dest_name = format_location_name(game_state.traveling_to)
        print(f"{Colors.YELLOW}🐎 Traveling to {dest_name} "
              f"({game_state.travel_days_remaining} days remaining){Colors.RESET}")

    # Weather flavor
    weather = get_weather_flavor(game_state.current_date)
    print(f"{Colors.DIM}{weather}{Colors.RESET}")
    print()


def display_resource_dashboard(game_state: GameState) -> None:
    """
    Display resource dashboard with all key metrics.

    Args:
        game_state: Current game state
    """
    print(f"{Colors.BOLD}═══ RESOURCES ═══{Colors.RESET}")

    # Primary resources in two columns
    treasury_str = format_treasury(game_state.treasury)
    authority_str = format_stat(game_state.royal_authority)
    military_str = format_stat(game_state.military_readiness)
    papal_str = format_stat(game_state.papal_relations, signed=True)

    print(f"Treasury: {treasury_str}      "
          f"Authority: {authority_str}")
    print(f"Military: {military_str}      "
          f"Papal Relations: {papal_str}")

    # Derived metrics
    avg_loyalty = game_state.get_average_baronial_loyalty()
    kingdom_stability = game_state.get_kingdom_stability()

    print(f"Baronial Loyalty (avg): {format_stat(avg_loyalty)}      "
          f"Kingdom Stability: {format_stat(kingdom_stability)}")
    print()


def display_detailed_status(game_state: GameState) -> None:
    """
    Display detailed status including all barons and regions.

    Args:
        game_state: Current game state
    """
    clear_screen()
    display_header()
    print(f"{Colors.BOLD}═══ DETAILED STATUS ═══{Colors.RESET}\n")

    # Date and location
    print(f"{Colors.BOLD}Date:{Colors.RESET} {game_state.current_date.format_long()}")
    print(f"{Colors.BOLD}Location:{Colors.RESET} {format_location_name(game_state.location)}")
    print(f"{Colors.BOLD}Days Played:{Colors.RESET} {game_state.days_played}")
    print()

    # Resources
    print(f"{Colors.BOLD}RESOURCES:{Colors.RESET}")
    print(f"  Treasury: {format_treasury(game_state.treasury)}")
    print(f"  Royal Authority: {format_stat(game_state.royal_authority)}")
    print(f"  Military Readiness: {format_stat(game_state.military_readiness)}")
    print(f"  Papal Relations: {format_stat(game_state.papal_relations, signed=True)}")
    print()

    # Baronial relationships
    print(f"{Colors.BOLD}BARONIAL RELATIONSHIPS:{Colors.RESET}")
    for baron, value in sorted(game_state.barons.items(), key=lambda x: -x[1]):
        baron_name = baron.replace("_", " ").title()
        print(f"  {baron_name:.<30} {format_stat(value)}")
    avg_loyalty = game_state.get_average_baronial_loyalty()
    print(f"  {Colors.BOLD}Average:{Colors.RESET:.<30} {format_stat(avg_loyalty)}")
    print()

    # Regional stability
    print(f"{Colors.BOLD}REGIONAL STABILITY:{Colors.RESET}")
    for region, value in sorted(game_state.regions.items(), key=lambda x: -x[1]):
        region_name = region.replace("_", " ").title()
        print(f"  {region_name:.<30} {format_stat(value)}")
    kingdom_stability = game_state.get_kingdom_stability()
    print(f"  {Colors.BOLD}Overall (weighted):{Colors.RESET:.<30} {format_stat(kingdom_stability)}")
    print()


def format_treasury(amount: int) -> str:
    """
    Format treasury amount with color coding.

    Args:
        amount: Treasury amount in marks

    Returns:
        Formatted string with color
    """
    if amount > 5000:
        color = Colors.GREEN
    elif amount > 2000:
        color = Colors.YELLOW
    elif amount > 0:
        color = Colors.YELLOW
    else:
        color = Colors.RED

    return f"{color}{amount:,} marks{Colors.RESET}"


def format_stat(value: float, signed: bool = False) -> str:
    """
    Format a stat (0-100 or -100 to +100) with color and visual bar.

    Args:
        value: Stat value
        signed: Whether stat can be negative (like papal relations)

    Returns:
        Formatted string with color and bar
    """
    if signed:
        # For -100 to +100 stats
        if value > 40:
            color = Colors.GREEN
        elif value > -20:
            color = Colors.YELLOW
        else:
            color = Colors.RED

        # Visual bar (20 blocks for -100 to +100 range)
        normalized = (value + 100) / 20  # 0-10 range
        bars = int(normalized)
        bar_display = "▓" * bars + "░" * (10 - bars)

        sign = "+" if value > 0 else ""
        return f"{color}{sign}{int(value)}/100{Colors.RESET} {bar_display}"
    else:
        # For 0-100 stats
        if value > 70:
            color = Colors.GREEN
        elif value > 40:
            color = Colors.YELLOW
        else:
            color = Colors.RED

        # Visual bar (10 blocks)
        bars = int(value / 10)
        bar_display = "▓" * bars + "░" * (10 - bars)

        return f"{color}{int(value)}/100{Colors.RESET} {bar_display}"


def display_text(text: str, width: int = 78, indent: int = 0) -> None:
    """
    Display wrapped text.

    Args:
        text: Text to display
        width: Width to wrap at
        indent: Number of spaces to indent
    """
    indent_str = " " * indent
    wrapped = textwrap.fill(
        text,
        width=width,
        initial_indent=indent_str,
        subsequent_indent=indent_str
    )
    print(wrapped)
    print()


def display_choices(choices: list, prefix: str = "") -> None:
    """
    Display a numbered list of choices.

    Args:
        choices: List of choice strings
        prefix: Optional prefix for each choice
    """
    print(f"{Colors.BOLD}YOUR OPTIONS:{Colors.RESET}")
    print()

    for i, choice in enumerate(choices, 1):
        print(f"  {Colors.BOLD}{i}.{Colors.RESET} {prefix}{choice}")
    print()


def get_player_input(prompt: str = "Your choice: ") -> str:
    """
    Get input from the player.

    Args:
        prompt: Prompt to display

    Returns:
        Player's input as string
    """
    return input(f"{Colors.BOLD}{prompt}{Colors.RESET}").strip()


def get_numeric_choice(min_val: int, max_val: int, prompt: str = "Your choice: ") -> Optional[int]:
    """
    Get a numeric choice from the player within a range.

    Args:
        min_val: Minimum valid value
        max_val: Maximum valid value
        prompt: Prompt to display

    Returns:
        Integer choice, or None if invalid
    """
    try:
        choice = int(get_player_input(prompt))
        if min_val <= choice <= max_val:
            return choice
        else:
            display_error(f"Please enter a number between {min_val} and {max_val}.")
            return None
    except ValueError:
        display_error("Please enter a valid number.")
        return None


def display_error(message: str) -> None:
    """
    Display an error message.

    Args:
        message: Error message to display
    """
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")


def display_success(message: str) -> None:
    """
    Display a success message.

    Args:
        message: Success message to display
    """
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")


def display_warning(message: str) -> None:
    """
    Display a warning message.

    Args:
        message: Warning message to display
    """
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")


def wait_for_continue(prompt: str = "\n[Press Enter to continue...]") -> None:
    """
    Pause and wait for the player to press Enter.

    Args:
        prompt: Prompt to display
    """
    input(f"{Colors.YELLOW}{prompt}{Colors.RESET}")


def confirm_choice(message: str) -> bool:
    """
    Ask player to confirm a choice.

    Args:
        message: Confirmation message

    Returns:
        True if confirmed, False otherwise
    """
    response = get_player_input(f"{message} (y/n): ").lower()
    return response in ['y', 'yes']


def display_resource_changes(old_state: GameState, new_state: GameState) -> None:
    """
    Display what changed between two game states.

    Args:
        old_state: State before changes
        new_state: State after changes
    """
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

    # Military
    if old_state.military_readiness != new_state.military_readiness:
        diff = new_state.military_readiness - old_state.military_readiness
        color = Colors.GREEN if diff > 0 else Colors.RED
        sign = "+" if diff > 0 else ""
        changes.append(f"Military {color}{sign}{diff}{Colors.RESET}")

    # Papal
    if old_state.papal_relations != new_state.papal_relations:
        diff = new_state.papal_relations - old_state.papal_relations
        color = Colors.GREEN if diff > 0 else Colors.RED
        sign = "+" if diff > 0 else ""
        changes.append(f"Papal Relations {color}{sign}{diff}{Colors.RESET}")

    # Baronial relationships
    for baron in old_state.barons:
        if old_state.barons[baron] != new_state.barons[baron]:
            diff = new_state.barons[baron] - old_state.barons[baron]
            color = Colors.GREEN if diff > 0 else Colors.RED
            sign = "+" if diff > 0 else ""
            baron_name = baron.replace("_", " ").title()
            changes.append(f"{baron_name} {color}{sign}{diff}{Colors.RESET}")

    # Regional stability
    for region in old_state.regions:
        if old_state.regions[region] != new_state.regions[region]:
            diff = new_state.regions[region] - old_state.regions[region]
            color = Colors.GREEN if diff > 0 else Colors.RED
            sign = "+" if diff > 0 else ""
            region_name = region.replace("_", " ").title()
            changes.append(f"{region_name} {color}{sign}{diff}{Colors.RESET}")

    if changes:
        for change in changes:
            print(f"  • {change}")
    else:
        print(f"  {Colors.DIM}(No resource changes){Colors.RESET}")

    print()


# Testing code
if __name__ == "__main__":
    print("=== Testing UI System ===\n")

    # Test header
    display_header()
    wait_for_continue()
    clear_screen()

    # Test with game state
    from game_state import GameState
    state = GameState()

    print("=== Testing Date/Location Display ===\n")
    display_date_location(state)
    wait_for_continue()

    print("\n=== Testing Resource Dashboard ===\n")
    display_resource_dashboard(state)
    wait_for_continue()

    print("\n=== Testing Detailed Status ===\n")
    display_detailed_status(state)
    wait_for_continue()

    clear_screen()
    print("\n=== Testing Text Display ===\n")
    long_text = (
        "Your fleet lies at anchor in Portsmouth harbor, fifty galleys and "
        "twice that many transports. The army you've assembled—knights, "
        "serjeants, and Flemish mercenaries—waits aboard or camps on the "
        "shore. Today is Pentecost, the date you set for your great "
        "enterprise: the reconquest of Normandy."
    )
    display_text(long_text)
    wait_for_continue()

    print("\n=== Testing Choices ===\n")
    choices = [
        "Order the fleet to sail immediately",
        "Sail with a reduced force of loyalists only",
        "Cancel the invasion and punish those who refused",
        "Cancel and accept their counsel gracefully"
    ]
    display_choices(choices)

    print("\n=== Testing Messages ===\n")
    display_success("Game saved successfully!")
    display_warning("Treasury is running low.")
    display_error("Invalid choice. Please try again.")
    print()
    wait_for_continue()

    print("\n=== Testing Resource Changes ===\n")
    import copy
    old_state = copy.deepcopy(state)
    state.apply_consequences({
        "resources": {"treasury": -500, "authority": 5},
        "relationships": {"william_marshal": -10},
        "regions": {"southern_england": 3}
    })
    display_resource_changes(old_state, state)
    wait_for_continue()

    print("\n=== All UI Tests Complete ===")
