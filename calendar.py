"""
calendar.py

Medieval calendar system for King John 1205.
Handles date tracking, feast days, and day-of-week calculations.
"""

from typing import Dict, List, Optional, Tuple


class Date:
    """
    Medieval calendar date with feast day tracking.

    Represents a specific date in the medieval calendar system,
    handling day/month/year tracking, feast days, and day of week
    calculations using historical methods.

    Attributes:
        year: Integer year (1205 for our game)
        month: Integer month (1-12)
        day: Integer day (1-31 depending on month)

    Example:
        >>> date = Date(1205, 1, 1)
        >>> print(date.format_long())
        'Saturday, January 1, 1205'
        >>> date.increment()
        >>> print(date.day)
        2
    """

    # Days per month (1205 is not a leap year)
    DAYS_IN_MONTH: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    MONTH_NAMES: List[str] = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    DAY_NAMES: List[str] = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    ]

    # Important feast days: (month, day, name)
    FEAST_DAYS: List[Tuple[int, int, str]] = [
        (1, 1, "Circumcision of Christ / New Year"),
        (1, 6, "Epiphany"),
        (2, 2, "Candlemas / Purification of Mary"),
        (3, 25, "Annunciation / Lady Day"),
        # Easter is moveable - calculated separately (April 17, 1205)
        (4, 17, "Easter Sunday"),
        (5, 26, "Ascension Day"),
        (6, 5, "Pentecost / Whitsunday"),
        (6, 24, "Nativity of St. John the Baptist / Midsummer"),
        (8, 15, "Assumption of Mary"),
        (9, 29, "Michaelmas / Feast of St. Michael"),
        (10, 28, "Feast of St. Simon and St. Jude"),
        (11, 1, "All Saints' Day"),
        (11, 11, "Feast of St. Martin"),
        (11, 30, "Feast of St. Andrew"),
        (12, 25, "Christmas / Nativity of Christ"),
        (12, 26, "St. Stephen's Day"),
        (12, 27, "Feast of St. John the Evangelist"),
        (12, 28, "Feast of the Holy Innocents"),
    ]

    def __init__(self, year: int, month: int, day: int):
        """
        Initialize a date.

        Args:
            year: Year (should be 1205 for this game)
            month: Month (1-12)
            day: Day (1-31 depending on month)

        Raises:
            ValueError: If date values are invalid
        """
        self.year = year
        self.month = month
        self.day = day
        self._validate()

    def _validate(self) -> None:
        """
        Ensure date is valid.

        Raises:
            ValueError: If month or day is out of valid range
        """
        if not (1 <= self.month <= 12):
            raise ValueError(f"Invalid month: {self.month}. Must be 1-12.")

        max_day = self.DAYS_IN_MONTH[self.month - 1]
        if not (1 <= self.day <= max_day):
            raise ValueError(
                f"Invalid day: {self.day}. "
                f"Month {self.month} has {max_day} days."
            )

    def increment(self) -> None:
        """
        Advance date by one day.

        Handles month and year rollovers automatically.
        """
        self.day += 1

        # Check if we've exceeded days in current month
        if self.day > self.DAYS_IN_MONTH[self.month - 1]:
            self.day = 1
            self.month += 1

            # Check if we've exceeded months in year
            if self.month > 12:
                self.month = 1
                self.year += 1

    def day_of_week(self) -> str:
        """
        Calculate day of week using Zeller's congruence.

        Returns:
            String name of the day of week

        Note:
            Uses Zeller's congruence algorithm adapted for
            the Gregorian/Julian calendar transition period.
        """
        # Zeller's congruence algorithm
        # For Julian calendar (pre-1582)
        year = self.year
        month = self.month
        day = self.day

        # Adjust for Zeller's: Jan/Feb are months 13/14 of previous year
        if month < 3:
            month += 12
            year -= 1

        # Zeller's formula (Julian calendar variant)
        h = (
            day +
            ((13 * (month + 1)) // 5) +
            year +
            (year // 4) +
            5
        ) % 7

        # Convert Zeller's result to standard weekday
        # Zeller: 0=Sat, 1=Sun, 2=Mon, ... 6=Fri
        # We want: 0=Mon, 1=Tue, ... 6=Sun
        day_index = (h + 5) % 7

        return self.DAY_NAMES[day_index]

    def day_of_year(self) -> int:
        """
        Return day number within the year (1-365).

        Returns:
            Integer day of year (1 = Jan 1, 365 = Dec 31)
        """
        return sum(self.DAYS_IN_MONTH[:self.month - 1]) + self.day

    def is_feast_day(self) -> Optional[str]:
        """
        Check if today is a feast day.

        Returns:
            Name of feast day if today is a feast, None otherwise
        """
        for month, day, name in self.FEAST_DAYS:
            if self.month == month and self.day == day:
                return name
        return None

    def format_long(self) -> str:
        """
        Format date in long form.

        Returns:
            String like "Thursday, May 31, 1205"
        """
        return (
            f"{self.day_of_week()}, "
            f"{self.MONTH_NAMES[self.month - 1]} {self.day}, "
            f"{self.year}"
        )

    def format_short(self) -> str:
        """
        Format date in short form with day of year.

        Returns:
            String like "Day 152 - May 31, 1205"
        """
        return (
            f"Day {self.day_of_year()} - "
            f"{self.MONTH_NAMES[self.month - 1]} {self.day}, "
            f"{self.year}"
        )

    def to_dict(self) -> Dict[str, int]:
        """
        Serialize date to dictionary for saving.

        Returns:
            Dictionary with year, month, day keys
        """
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day
        }

    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> 'Date':
        """
        Deserialize date from dictionary.

        Args:
            data: Dictionary with year, month, day keys

        Returns:
            Date object
        """
        return cls(data["year"], data["month"], data["day"])

    def __str__(self) -> str:
        """String representation."""
        return self.format_short()

    def __repr__(self) -> str:
        """Developer representation."""
        return f"Date({self.year}, {self.month}, {self.day})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another Date."""
        if not isinstance(other, Date):
            return NotImplemented
        return (
            self.year == other.year and
            self.month == other.month and
            self.day == other.day
        )


def get_season(date: Date) -> str:
    """
    Determine the season for a given date.

    Uses medieval/astronomical seasons:
    - Spring: March 21 - June 20
    - Summer: June 21 - September 22
    - Autumn: September 23 - December 20
    - Winter: December 21 - March 20

    Args:
        date: Date object

    Returns:
        String: "spring", "summer", "autumn", or "winter"
    """
    month = date.month
    day = date.day

    if (month == 3 and day >= 21) or month == 4 or month == 5 or (month == 6 and day <= 20):
        return "spring"
    elif (month == 6 and day >= 21) or month == 7 or month == 8 or (month == 9 and day <= 22):
        return "summer"
    elif (month == 9 and day >= 23) or month == 10 or month == 11 or (month == 12 and day <= 20):
        return "autumn"
    else:
        return "winter"


def get_weather_flavor(date: Date) -> str:
    """
    Generate season-appropriate weather flavor text.

    Provides atmospheric description based on season.

    Args:
        date: Date object

    Returns:
        String describing weather/atmosphere
    """
    season = get_season(date)

    flavors = {
        "spring": [
            "The spring air is crisp and fresh.",
            "New growth appears on the trees.",
            "Rain showers pass through the countryside.",
            "The days grow longer and warmer."
        ],
        "summer": [
            "The summer sun beats down warmly.",
            "Long days perfect for travel and campaigning.",
            "Heat shimmers over the fields.",
            "The countryside is green and lush."
        ],
        "autumn": [
            "Autumn leaves fall in golden drifts.",
            "The harvest is being gathered in.",
            "Cool winds blow from the north.",
            "The days grow shorter and colder."
        ],
        "winter": [
            "Winter cold grips the land.",
            "Frost covers the ground each morning.",
            "Travel is difficult in the mud and cold.",
            "The nights are long and dark."
        ]
    }

    # Simple selection based on day of year for variety
    import random
    random.seed(date.day_of_year())  # Consistent for same date
    return random.choice(flavors[season])


# Testing code
if __name__ == "__main__":
    print("=== Testing Date Class ===\n")

    # Test basic date creation
    date = Date(1205, 1, 1)
    print(f"Created: {date}")
    print(f"Long format: {date.format_long()}")
    print(f"Day of year: {date.day_of_year()}")
    print(f"Season: {get_season(date)}")
    print(f"Weather: {get_weather_flavor(date)}")

    # Test feast day
    feast = date.is_feast_day()
    if feast:
        print(f"Feast day: {feast}")
    print()

    # Test date incrementing
    print("=== Testing Date Incrementing ===\n")
    date = Date(1205, 1, 31)
    print(f"Start: {date}")
    date.increment()
    print(f"After increment: {date}")
    assert date.month == 2 and date.day == 1
    print("Month rollover: OK")
    print()

    # Test year rollover
    date = Date(1205, 12, 31)
    print(f"Start: {date}")
    date.increment()
    print(f"After increment: {date}")
    assert date.year == 1206 and date.month == 1 and date.day == 1
    print("Year rollover: OK")
    print()

    # Test Easter date
    easter = Date(1205, 4, 17)
    print(f"Easter 1205: {easter.format_long()}")
    print(f"Feast: {easter.is_feast_day()}")
    print()

    # Test Pentecost (important in game)
    pentecost = Date(1205, 6, 5)
    print(f"Pentecost 1205: {pentecost.format_long()}")
    print(f"Feast: {pentecost.is_feast_day()}")
    print()

    # Test Christmas
    christmas = Date(1205, 12, 25)
    print(f"Christmas 1205: {christmas.format_long()}")
    print(f"Feast: {christmas.is_feast_day()}")
    print(f"Season: {get_season(christmas)}")
    print()

    # Test serialization
    print("=== Testing Serialization ===\n")
    date = Date(1205, 6, 5)
    data = date.to_dict()
    print(f"Serialized: {data}")
    restored = Date.from_dict(data)
    print(f"Restored: {restored}")
    assert date == restored
    print("Serialization: OK")
    print()

    print("=== All Tests Passed ===")
