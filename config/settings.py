import pygame
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Colors:
    """Named color constants for consistency."""
    # Background
    NIGHT_SKY = (10, 10, 26)
    DAY_SKY = (135, 206, 235)
    ASPHALT = (50, 50, 50)

    # Roads
    ROAD_GRAY = (60, 60, 60)
    INTERSECTION_DARK = (70, 70, 70)

    # Markings
    LANE_YELLOW = (255, 235, 59)
    STOP_WHITE = (255, 255, 255)

    # Traffic Lights
    RED = (255, 50, 50)
    YELLOW = (255, 235, 0)
    GREEN = (50, 255, 50)
    LIGHT_OFF = (40, 40, 40)

    # Vehicles
    CAR_BLUE = (52, 152, 219)
    CAR_GREEN = (46, 204, 113)
    CAR_YELLOW = (241, 196, 15)
    CAR_PURPLE = (155, 89, 182)
    CAR_RED = (231, 76, 60)
    EMERGENCY_RED = (255, 0, 0)

    # UI
    UI_BACKGROUND = (30, 30, 40, 220)  # With alpha
    TEXT_WHITE = (240, 240, 240)
    TEXT_DIM = (180, 180, 180)

@dataclass(frozen=True)
class Display:
    """Display and window configuration."""
    WIDTH: int = 1200
    HEIGHT: int = 800
    FPS: int = 60
    TITLE: str = "Smart Traffic Intersection Simulation"

    # Calculate center for consistent positioning
    @property
    def CENTER(self) -> Tuple[int, int]:
        return (self.WIDTH // 2, self.HEIGHT // 2)

@dataclass(frozen=True)
class Intersection:
    """Intersection geometry and layout."""
    SIZE: int = 600  # Total intersection area
    ROAD_WIDTH: int = 160
    LANE_WIDTH: int = 40
    LANE_COUNT: int = 2  # Lanes per direction

    # Derived properties (calculated from above)
    @property
    def LANE_MARKING_LENGTH(self) -> int:
        return 15

    @property
    def LANE_MARKING_GAP(self) -> int:
        return 10

    @property
    def STOP_LINE_OFFSET(self) -> int:
        return 15

@dataclass(frozen=True)
class VehicleSpecs:
    """Vehicle dimensions and physics."""
    WIDTH: int = 32
    HEIGHT: int = 48
    WHEEL_SIZE: int = 8

    # Physics (pixels per second^2)
    MAX_SPEED: float = 100.0
    ACCELERATION: float = 80.0
    DECELERATION: float = 120.0
    SAFE_FOLLOWING_DISTANCE: int = 60

    # Visual
    COLORS = [
        Colors.CAR_BLUE,
        Colors.CAR_GREEN,
        Colors.CAR_YELLOW,
        Colors.CAR_PURPLE
    ]

@dataclass(frozen=True)
class TrafficLightTiming:
    """Traffic light timing parameters."""
    MIN_GREEN: float = 20.0  # Minimum green time
    MAX_GREEN: float = 60.0  # Maximum green time
    YELLOW_DURATION: float = 3.0
    ALL_RED_CLEARANCE: float = 2.0

    # Detection thresholds
    VEHICLES_FOR_EXTENSION: int = 3
    WAIT_TIME_THRESHOLD: float = 30.0

# Create global instances for easy access
COLORS = Colors()
DISPLAY = Display()
INTERSECTION = Intersection()
VEHICLE = VehicleSpecs()
TIMING = TrafficLightTiming()

# Initialize pygame font module for consistent font loading
pygame.font.init()
FONT_SMALL = pygame.font.SysFont('Arial', 16)
FONT_MEDIUM = pygame.font.SysFont('Arial', 20)
FONT_LARGE = pygame.font.SysFont('Arial', 24, bold=True)
FONT_TITLE = pygame.font.SysFont('Arial', 32, bold=True)

def validate_config() -> None:
    """Validate configuration on startup."""
    assert DISPLAY.WIDTH >= INTERSECTION.SIZE, \
        "Screen width must be at least intersection size"
    assert DISPLAY.HEIGHT >= INTERSECTION.SIZE, \
        "Screen height must be at least intersection size"
    assert INTERSECTION.ROAD_WIDTH > INTERSECTION.LANE_WIDTH * INTERSECTION.LANE_COUNT, \
        "Road must be wider than total lanes"

    print("✅ Configuration validated successfully")

if __name__ == "__main__":
    # Test the configuration
    validate_config()
    print(f"Screen: {DISPLAY.WIDTH}x{DISPLAY.HEIGHT}")
    print(f"Intersection size: {INTERSECTION.SIZE}")
    print(f"Available colors: {len([c for c in dir(COLORS) if not c.startswith('_')])}")
