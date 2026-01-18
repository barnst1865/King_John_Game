"""
save_manager.py

Save/load system for King John 1205.
Handles game state persistence using JSON format.
"""

import json
import os
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any, Union

from game_state import GameState


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class SaveManager:
    """
    Handles saving and loading game state.

    Provides functionality to save game state to JSON files and load
    them back. Supports autosave and multiple manual save slots.

    Attributes:
        SAVE_DIR: Directory for save files
        AUTOSAVE_FILE: Filename for autosave
        MANUAL_SLOTS: Number of manual save slots available
    """

    SAVE_DIR = "saves/"
    AUTOSAVE_FILE = "autosave.json"
    MANUAL_SLOTS = 5

    @staticmethod
    def ensure_save_directory() -> None:
        """
        Create saves directory if it doesn't exist.

        Creates the save directory and ensures it's accessible.
        """
        if not os.path.exists(SaveManager.SAVE_DIR):
            os.makedirs(SaveManager.SAVE_DIR)
            logging.info(f"Created save directory: {SaveManager.SAVE_DIR}")

    @staticmethod
    def save_game(
        game_state: GameState,
        slot: Union[int, str] = "autosave"
    ) -> bool:
        """
        Save game state to file.

        Args:
            game_state: GameState object to save
            slot: "autosave" or int 1-5 for manual slots

        Returns:
            True if save successful, False otherwise

        Example:
            >>> save_manager.save_game(game_state, "autosave")
            True
            >>> save_manager.save_game(game_state, 1)
            True
        """
        SaveManager.ensure_save_directory()

        # Determine filename
        if slot == "autosave":
            filename = SaveManager.AUTOSAVE_FILE
        else:
            if not isinstance(slot, int) or slot < 1 or slot > SaveManager.MANUAL_SLOTS:
                logging.error(f"Invalid save slot: {slot}")
                return False
            filename = f"save_slot_{slot}.json"

        filepath = os.path.join(SaveManager.SAVE_DIR, filename)

        try:
            # Prepare save data with metadata
            save_data = {
                "game_version": "0.1.0",
                "save_version": "1.0",
                "timestamp": datetime.now().isoformat(),
                "game_state": game_state.to_dict()
            }

            # Write to file with pretty printing
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            logging.info(f"Game saved successfully to {filename}")
            return True

        except Exception as e:
            logging.error(f"Failed to save game: {e}")
            return False

    @staticmethod
    def load_game(slot: Union[int, str] = "autosave") -> Optional[GameState]:
        """
        Load game state from file.

        Args:
            slot: "autosave" or int 1-5 for manual slots

        Returns:
            GameState object if successful, None otherwise

        Example:
            >>> state = save_manager.load_game("autosave")
            >>> if state:
            ...     print("Game loaded successfully")
        """
        # Determine filename
        if slot == "autosave":
            filename = SaveManager.AUTOSAVE_FILE
        else:
            if not isinstance(slot, int) or slot < 1 or slot > SaveManager.MANUAL_SLOTS:
                logging.error(f"Invalid save slot: {slot}")
                return None
            filename = f"save_slot_{slot}.json"

        filepath = os.path.join(SaveManager.SAVE_DIR, filename)

        # Check if file exists
        if not os.path.exists(filepath):
            logging.warning(f"Save file not found: {filename}")
            return None

        try:
            # Read save file
            with open(filepath, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            # Version compatibility check
            save_version = save_data.get("save_version", "unknown")
            if save_version != "1.0":
                logging.warning(
                    f"Save file version mismatch: {save_version} vs 1.0. "
                    "Attempting to load anyway..."
                )

            # Restore game state
            game_state = GameState.from_dict(save_data["game_state"])

            logging.info(f"Game loaded successfully from {filename}")
            return game_state

        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in save file: {e}")
            return None
        except KeyError as e:
            logging.error(f"Missing required data in save file: {e}")
            return None
        except Exception as e:
            logging.error(f"Failed to load game: {e}")
            return None

    @staticmethod
    def list_saves() -> List[Dict[str, Any]]:
        """
        List all available save files with metadata.

        Returns:
            List of dictionaries with save info:
                - slot: Save slot identifier
                - timestamp: When save was created
                - date: In-game date
                - location: Current location
                - days_played: Days advanced
                - exists: Whether save file exists

        Example:
            >>> saves = save_manager.list_saves()
            >>> for save in saves:
            ...     print(f"Slot {save['slot']}: {save['date']}")
        """
        saves = []

        SaveManager.ensure_save_directory()

        # Check autosave
        autosave_meta = SaveManager._get_save_metadata("autosave")
        if autosave_meta:
            saves.append({"slot": "autosave", **autosave_meta})

        # Check manual slots
        for slot in range(1, SaveManager.MANUAL_SLOTS + 1):
            slot_meta = SaveManager._get_save_metadata(slot)
            if slot_meta:
                saves.append({"slot": slot, **slot_meta})

        return saves

    @staticmethod
    def _get_save_metadata(slot: Union[int, str]) -> Optional[Dict[str, Any]]:
        """
        Extract metadata from save file without loading full state.

        Args:
            slot: Save slot identifier

        Returns:
            Dictionary with metadata, or None if file doesn't exist
        """
        # Determine filename
        if slot == "autosave":
            filename = SaveManager.AUTOSAVE_FILE
        else:
            filename = f"save_slot_{slot}.json"

        filepath = os.path.join(SaveManager.SAVE_DIR, filename)

        if not os.path.exists(filepath):
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            gs = save_data["game_state"]
            date_data = gs["date"]

            # Format in-game date
            game_date = f"{date_data['month']}/{date_data['day']}/{date_data['year']}"

            # Format location
            from data.locations import format_location_name
            location = format_location_name(gs["location"])

            return {
                "timestamp": save_data.get("timestamp", "Unknown"),
                "date": game_date,
                "location": location,
                "days_played": gs.get("days_played", 0),
                "treasury": gs.get("treasury", 0),
                "exists": True
            }

        except Exception as e:
            logging.error(f"Failed to read metadata from {filename}: {e}")
            return None

    @staticmethod
    def delete_save(slot: Union[int, str]) -> bool:
        """
        Delete a save file.

        Args:
            slot: Save slot to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        # Determine filename
        if slot == "autosave":
            filename = SaveManager.AUTOSAVE_FILE
        else:
            if not isinstance(slot, int) or slot < 1 or slot > SaveManager.MANUAL_SLOTS:
                logging.error(f"Invalid save slot: {slot}")
                return False
            filename = f"save_slot_{slot}.json"

        filepath = os.path.join(SaveManager.SAVE_DIR, filename)

        if not os.path.exists(filepath):
            logging.warning(f"Save file not found: {filename}")
            return False

        try:
            os.remove(filepath)
            logging.info(f"Deleted save file: {filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to delete save file: {e}")
            return False

    @staticmethod
    def save_exists(slot: Union[int, str]) -> bool:
        """
        Check if a save file exists.

        Args:
            slot: Save slot to check

        Returns:
            True if save exists, False otherwise
        """
        if slot == "autosave":
            filename = SaveManager.AUTOSAVE_FILE
        else:
            if not isinstance(slot, int) or slot < 1 or slot > SaveManager.MANUAL_SLOTS:
                return False
            filename = f"save_slot_{slot}.json"

        filepath = os.path.join(SaveManager.SAVE_DIR, filename)
        return os.path.exists(filepath)


# Testing code
if __name__ == "__main__":
    print("=== Testing SaveManager ===\n")

    # Create test game state
    print("Creating test game state...")
    state = GameState()
    state.treasury = 7500
    state.royal_authority = 70
    state.flags["test_flag"] = True
    state.advance_day()
    state.advance_day()
    print(f"State: {state}")
    print(f"Treasury: {state.treasury}")
    print(f"Days played: {state.days_played}")
    print()

    # Test autosave
    print("=== Testing Autosave ===\n")
    success = SaveManager.save_game(state, "autosave")
    print(f"Save successful: {success}")
    assert success, "Autosave failed"

    # Check if file exists
    exists = SaveManager.save_exists("autosave")
    print(f"Autosave exists: {exists}")
    assert exists, "Autosave file not found"
    print()

    # Test loading
    print("=== Testing Load ===\n")
    loaded_state = SaveManager.load_game("autosave")
    assert loaded_state is not None, "Failed to load autosave"
    print(f"Loaded state: {loaded_state}")
    print(f"Treasury: {loaded_state.treasury}")
    print(f"Days played: {loaded_state.days_played}")
    print(f"Test flag: {loaded_state.flags.get('test_flag')}")

    # Verify loaded state matches original
    assert loaded_state.treasury == 7500, "Treasury mismatch"
    assert loaded_state.royal_authority == 70, "Authority mismatch"
    assert loaded_state.days_played == 2, "Days played mismatch"
    assert loaded_state.flags["test_flag"] == True, "Flag mismatch"
    print("Load verification: OK")
    print()

    # Test manual save slots
    print("=== Testing Manual Save Slots ===\n")
    for slot in range(1, 4):
        state.treasury -= 100  # Modify state
        state.advance_day()
        success = SaveManager.save_game(state, slot)
        print(f"Slot {slot} save: {success}")
        assert success, f"Slot {slot} save failed"

    print()

    # Test listing saves
    print("=== Testing List Saves ===\n")
    saves = SaveManager.list_saves()
    print(f"Found {len(saves)} save(s):")
    for save in saves:
        print(f"  Slot {save['slot']}: {save['date']} at {save['location']} "
              f"(Day {save['days_played']}, {save['treasury']} marks)")
    assert len(saves) >= 4, "Not all saves found"
    print()

    # Test loading from slot
    print("=== Testing Load from Slot ===\n")
    slot_2_state = SaveManager.load_game(2)
    assert slot_2_state is not None, "Failed to load slot 2"
    print(f"Loaded from slot 2: {slot_2_state}")
    print(f"Days played: {slot_2_state.days_played}")
    print()

    # Test delete
    print("=== Testing Delete Save ===\n")
    deleted = SaveManager.delete_save(3)
    print(f"Deleted slot 3: {deleted}")
    assert deleted, "Delete failed"

    exists = SaveManager.save_exists(3)
    print(f"Slot 3 exists after delete: {exists}")
    assert not exists, "Slot 3 still exists"
    print()

    # Test invalid slot
    print("=== Testing Invalid Slot ===\n")
    success = SaveManager.save_game(state, 10)  # Invalid slot
    print(f"Save to slot 10 (invalid): {success}")
    assert not success, "Should have failed"

    loaded = SaveManager.load_game(0)  # Invalid slot
    print(f"Load from slot 0 (invalid): {loaded}")
    assert loaded is None, "Should have returned None"
    print()

    # Clean up test saves
    print("=== Cleaning Up ===\n")
    for slot in ["autosave", 1, 2]:
        if SaveManager.save_exists(slot):
            SaveManager.delete_save(slot)
            print(f"Deleted {slot}")
    print()

    print("=== All Tests Passed ===")
