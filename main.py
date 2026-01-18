"""
main.py

Main game loop for King John 1205.
Entry point and game flow control.
"""

import sys
import copy
from typing import Optional

from game_state import GameState
from save_manager import SaveManager
import ui
from ui import Colors
from data.locations import format_location_name


def main():
    """Main entry point for the game."""
    ui.clear_screen()
    ui.display_header()

    print(f"{Colors.CYAN}Welcome to King John 1205: A Royal Chronicle{Colors.RESET}\n")
    print("Experience a pivotal year in medieval English history.")
    print("Make decisions, manage resources, and shape the fate of a kingdom.")
    print()

    main_menu()


def main_menu():
    """Display and handle the main menu."""
    while True:
        ui.display_separator()
        print(f"{Colors.BOLD}MAIN MENU{Colors.RESET}\n")

        print("1. New Game")
        print("2. Continue Game (autosave)")
        print("3. Load Game")
        print("4. About")
        print("5. Exit")
        print()

        choice = ui.get_numeric_choice(1, 5)

        if choice == 1:
            if confirm_new_game():
                start_new_game()
                break
        elif choice == 2:
            if continue_game():
                break
        elif choice == 3:
            if load_game_menu():
                break
        elif choice == 4:
            show_about()
        elif choice == 5:
            confirm_exit()
            break


def confirm_new_game() -> bool:
    """
    Confirm starting a new game.

    Returns:
        True if confirmed, False otherwise
    """
    print()
    print("Starting a new game will begin on January 1, 1205.")
    print("You are King John of England, and the year ahead is pivotal.")
    print()

    return ui.confirm_choice("Begin new game?")


def start_new_game():
    """Initialize and start a new game."""
    ui.clear_screen()
    ui.display_header()

    print(f"{Colors.BOLD}═══ PROLOGUE ═══{Colors.RESET}\n")

    prologue = """
January 1, 1205. Winchester.

The Christmas court has dispersed, but the weight of the crown remains heavy
on your shoulders. Last year's losses still sting—Normandy fallen to Philip
of France, your continental empire crumbling, and the mocking nickname
"Softsword" echoing in your ears.

Yet you are determined. This year, you will rebuild your strength, reclaim
what was lost, and prove yourself a true Plantagenet king. Your treasury
is strained, your barons restless, but you have plans—grand plans to
restore your glory.

The new year stretches before you. 365 days to change history.
    """

    ui.display_text(prologue.strip())
    ui.wait_for_continue()

    # Create new game state
    game_state = GameState()

    # Start game loop
    game_loop(game_state)


def continue_game() -> bool:
    """
    Continue from autosave.

    Returns:
        True if game loaded, False if no autosave exists
    """
    if not SaveManager.save_exists("autosave"):
        ui.display_error("No autosave found. Please start a new game or load from a save slot.")
        ui.wait_for_continue()
        return False

    game_state = SaveManager.load_game("autosave")
    if game_state:
        ui.display_success("Game loaded from autosave.")
        ui.wait_for_continue()
        game_loop(game_state)
        return True
    else:
        ui.display_error("Failed to load autosave.")
        ui.wait_for_continue()
        return False


def load_game_menu() -> bool:
    """
    Display load game menu.

    Returns:
        True if game loaded, False otherwise
    """
    ui.clear_screen()
    ui.display_header()

    print(f"{Colors.BOLD}═══ LOAD GAME ═══{Colors.RESET}\n")

    saves = SaveManager.list_saves()

    if not saves:
        ui.display_warning("No saved games found.")
        ui.wait_for_continue()
        return False

    print("Available saves:\n")
    for i, save in enumerate(saves, 1):
        slot = save['slot']
        date = save['date']
        location = save['location']
        days = save['days_played']
        treasury = save['treasury']

        slot_str = f"Slot {slot}" if isinstance(slot, int) else "Autosave"
        print(f"{i}. {slot_str:.<15} {date} at {location}")
        print(f"   Day {days}, Treasury: {treasury:,} marks")
        print()

    print(f"{len(saves) + 1}. Cancel")
    print()

    choice = ui.get_numeric_choice(1, len(saves) + 1)

    if choice and choice <= len(saves):
        slot = saves[choice - 1]['slot']
        game_state = SaveManager.load_game(slot)
        if game_state:
            ui.display_success(f"Game loaded from {slot}.")
            ui.wait_for_continue()
            game_loop(game_state)
            return True
        else:
            ui.display_error("Failed to load game.")
            ui.wait_for_continue()

    return False


def show_about():
    """Display information about the game."""
    ui.clear_screen()
    ui.display_header()

    print(f"{Colors.BOLD}═══ ABOUT ═══{Colors.RESET}\n")

    about_text = """
King John 1205: A Royal Chronicle is a historical text-based adventure game
set during a pivotal year in medieval England.

The year 1205 saw King John attempting to recover from the devastating loss
of Normandy, planning military campaigns, navigating baronial tensions, and
dealing with church politics. Your decisions will shape history—will you
follow the historical path, or forge a new destiny?

Features:
• Day-by-day simulation of the entire year 1205
• Resource management (treasury, authority, military, papal relations)
• Relationship tracking with 8 key barons
• Regional stability across 6 regions
• Historical events based on documented sources
• Multiple endings based on your choices

Version: 0.1.0-dev (Phase 1: Core Systems)
Development Status: Milestone 1 - Complete Day Cycle

For more information, see the documentation in the docs/ directory.
    """

    ui.display_text(about_text.strip())
    ui.wait_for_continue()


def confirm_exit():
    """Confirm exiting the game."""
    print()
    if ui.confirm_choice("Are you sure you want to exit?"):
        print(f"\n{Colors.CYAN}Thank you for playing King John 1205.{Colors.RESET}")
        print("May history remember your reign wisely.\n")
        sys.exit(0)


def game_loop(game_state: GameState):
    """
    Main game loop.

    Handles the multi-phase daily structure and game flow.

    Args:
        game_state: Current game state
    """
    while True:
        # Check for game over
        is_over, reason = game_state.check_game_over()
        if is_over:
            handle_game_over(game_state, reason)
            break

        # Check for year end (victory)
        if game_state.current_date.day_of_year() > 365:
            handle_year_end(game_state)
            break

        # ===== PHASE 1: Morning Reports =====
        display_morning_reports(game_state)

        # ===== PHASE 2: Decision Time =====
        # For Milestone 1, we'll use a placeholder event
        event_occurred = handle_daily_event(game_state)

        # ===== PHASE 3: Resolution =====
        # (Handled within handle_daily_event for now)

        # ===== PHASE 4: Evening/End of Day =====
        handle_end_of_day(game_state)

        # Auto-save
        SaveManager.save_game(game_state, "autosave")

        # Advance to next day
        game_state.advance_day()


def display_morning_reports(game_state: GameState):
    """
    Phase 1: Display morning reports.

    Args:
        game_state: Current game state
    """
    ui.clear_screen()
    ui.display_header()

    # Date and location
    ui.display_date_location(game_state)

    # Resource dashboard
    ui.display_resource_dashboard(game_state)

    ui.display_separator()


def handle_daily_event(game_state: GameState) -> bool:
    """
    Phase 2: Handle the day's main event.

    For Milestone 1, this uses a simple placeholder event system.

    Args:
        game_state: Current game state

    Returns:
        True if an event occurred, False otherwise
    """
    # Placeholder event - will be replaced with real event system in Phase 2
    event = get_placeholder_event(game_state)

    if event:
        display_event(event, game_state)
        choice = get_event_choice(event)
        if choice:
            process_event_choice(event, choice, game_state)
            return True

    return False


def get_placeholder_event(game_state: GameState) -> Optional[dict]:
    """
    Get a placeholder event for testing.

    This is a simplified event system for Milestone 1.
    Will be replaced with full event system in Phase 2.

    Args:
        game_state: Current game state

    Returns:
        Event dictionary or None
    """
    # Every few days, show a sample event
    if game_state.days_played % 3 == 0:
        return {
            "title": "A Petition from the Merchants",
            "description": f"""
A delegation of merchants from {format_location_name(game_state.location)}
requests an audience. They seek a royal charter to establish a new market,
offering 200 marks for the privilege.

Your chancellor notes that granting this would increase trade and please the
townspeople, but some of your barons might see it as favoring merchants over
the nobility.
            """.strip(),
            "choices": [
                {
                    "id": 1,
                    "text": "Grant the charter and accept the payment",
                    "consequences": {
                        "resources": {"treasury": 200},
                        "regions": {game_state.location.replace("_", " "): 3}
                    }
                },
                {
                    "id": 2,
                    "text": "Grant the charter but waive the fee (generous gesture)",
                    "consequences": {
                        "resources": {"authority": 3},
                        "regions": {game_state.location.replace("_", " "): 5}
                    }
                },
                {
                    "id": 3,
                    "text": "Refuse the petition",
                    "consequences": {
                        "resources": {"authority": 1},
                        "regions": {game_state.location.replace("_", " "): -2}
                    }
                }
            ]
        }

    return None


def display_event(event: dict, game_state: GameState):
    """
    Display an event to the player.

    Args:
        event: Event dictionary
        game_state: Current game state
    """
    print(f"{Colors.BOLD}═══ {event['title'].upper()} ═══{Colors.RESET}\n")
    ui.display_text(event['description'])
    ui.display_separator("─")


def get_event_choice(event: dict) -> Optional[dict]:
    """
    Get the player's choice for an event.

    Args:
        event: Event dictionary

    Returns:
        Chosen option dictionary or None
    """
    choices = event['choices']
    choice_texts = [c['text'] for c in choices]

    ui.display_choices(choice_texts)

    # Add meta options
    print(f"{len(choices) + 1}. View detailed status")
    print(f"{len(choices) + 2}. Pass (no action)")
    print()

    choice_num = ui.get_numeric_choice(1, len(choices) + 2)

    if choice_num:
        if choice_num <= len(choices):
            return choices[choice_num - 1]
        elif choice_num == len(choices) + 1:
            ui.display_detailed_status(GameState)  # Placeholder
            ui.wait_for_continue()
            return get_event_choice(event)  # Re-prompt
        else:
            return None  # Pass

    return None


def process_event_choice(event: dict, choice: dict, game_state: GameState):
    """
    Process the player's choice and apply consequences.

    Args:
        event: Event dictionary
        choice: Chosen option
        game_state: Current game state
    """
    ui.clear_screen()
    ui.display_separator()

    # Display choice made
    print(f"{Colors.BOLD}You chose:{Colors.RESET} {choice['text']}\n")

    # Apply consequences
    old_state = copy.deepcopy(game_state)
    game_state.apply_consequences(choice['consequences'])

    # Show what changed
    ui.display_resource_changes(old_state, game_state)

    ui.display_separator()
    ui.wait_for_continue()


def handle_end_of_day(game_state: GameState):
    """
    Phase 4: Handle end of day activities.

    Args:
        game_state: Current game state
    """
    # For Milestone 1, just a simple summary
    print(f"\n{Colors.DIM}Day {game_state.days_played + 1} ends. "
          f"The realm continues...{Colors.RESET}\n")
    ui.wait_for_continue("Press Enter to advance to the next day...")


def handle_game_over(game_state: GameState, reason: str):
    """
    Handle game over condition.

    Args:
        game_state: Final game state
        reason: Reason for game over
    """
    ui.clear_screen()
    ui.display_header()

    print(f"{Colors.RED}{Colors.BOLD}═══ GAME OVER ═══{Colors.RESET}\n")

    messages = {
        "bankruptcy": "Your treasury has been empty for too long. Unable to pay "
                     "your troops or maintain the realm, your authority collapses. "
                     "The barons rise in rebellion, and your reign ends in chaos.",

        "civil_war": "Your royal authority has diminished to nothing. The barons "
                    "no longer recognize your rule. Civil war erupts, and you are "
                    "forced to flee into exile.",

        "mass_rebellion": "The great barons of England have united against you. "
                         "With their loyalty lost, they march on London and demand "
                         "your abdication. Your reign is over.",

        "kingdom_collapse": "Every region of your kingdom is in turmoil. Unable to "
                           "maintain order anywhere, the realm descends into anarchy. "
                           "Your kingship ends in complete failure."
    }

    message = messages.get(reason, "The game has ended.")
    ui.display_text(message)

    # Show final stats
    print(f"{Colors.BOLD}Final Statistics:{Colors.RESET}")
    print(f"  Days Ruled: {game_state.days_played}")
    print(f"  Final Treasury: {game_state.treasury:,} marks")
    print(f"  Final Authority: {game_state.royal_authority}/100")
    print()

    ui.wait_for_continue()

    # Return to main menu
    main_menu()


def handle_year_end(game_state: GameState):
    """
    Handle reaching the end of the year (victory).

    Args:
        game_state: Final game state
    """
    ui.clear_screen()
    ui.display_header()

    print(f"{Colors.GREEN}{Colors.BOLD}═══ YEAR END: DECEMBER 31, 1205 ═══{Colors.RESET}\n")

    end_text = """
You have survived the year 1205. As the Christmas season draws to a close
and the new year beckons, you reflect on the challenges faced and overcome.

Though the road ahead remains uncertain, you have maintained your crown and
your kingdom through a difficult year. History will record your decisions,
and the future of England remains in your hands.
    """

    ui.display_text(end_text.strip())

    # Show final stats
    print(f"{Colors.BOLD}Final Statistics:{Colors.RESET}")
    print(f"  Days Ruled: {game_state.days_played}")
    print(f"  Treasury: {ui.format_treasury(game_state.treasury)}")
    print(f"  Royal Authority: {ui.format_stat(game_state.royal_authority)}")
    print(f"  Average Baronial Loyalty: {ui.format_stat(game_state.get_average_baronial_loyalty())}")
    print(f"  Kingdom Stability: {ui.format_stat(game_state.get_kingdom_stability())}")
    print()

    # Simple scoring for Milestone 1
    score = calculate_simple_score(game_state)
    print(f"{Colors.BOLD}Final Score: {score}{Colors.RESET}")
    print()

    ui.wait_for_continue()

    # Return to main menu
    main_menu()


def calculate_simple_score(game_state: GameState) -> int:
    """
    Calculate a simple score for Milestone 1.

    Args:
        game_state: Final game state

    Returns:
        Integer score
    """
    score = 0
    score += game_state.treasury // 10
    score += game_state.royal_authority * 5
    score += int(game_state.get_average_baronial_loyalty() * 3)
    score += int(game_state.get_kingdom_stability() * 3)
    return score


if __name__ == "__main__":
    main()
