import pygame
from dataclasses import dataclass
from .colors import COLORS

@dataclass(frozen=True)
class Display:
    WIDTH: int = 1200
    HEIGHT: int = 800
    FPS: int = 60
    @property
    def CENTER(self): return (self.WIDTH // 2, self.HEIGHT // 2)

@dataclass(frozen=True)
class Intersection:
    ROAD_WIDTH: int = 400
    LANE_WIDTH: int = 60
    SIDEWALK_WIDTH: int = 40
    STOP_LINE_OFFSET: int = 15
    SIZE: int = 800

    @property
    def LANE_MARKING_LENGTH(self) -> int: return 15
    @property
    def LANE_MARKING_GAP(self) -> int: return 10
    @property
    def CROSSWALK_WIDTH(self) -> int: return 20

@dataclass(frozen=True)
class VehicleSpecs:
    WIDTH: int = 32
    HEIGHT: int = 48
    MAX_SPEED: float = 100.0
    ACCELERATION: float = 80.0
    DECELERATION: float = 120.0
    SAFE_DISTANCE: int = 60

    @property
    def COLORS(self): # Fixed: Removed extra parentheses
        return [
            (52, 152, 219),  # Blue
            (46, 204, 113),  # Green
            (241, 196, 15),  # Yellow
            (155, 89, 182),  # Purple
            (231, 76, 60)    # Red
        ]

# --- Instantiation ---
DISPLAY = Display()
INTERSECTION = Intersection()
VEHICLE = VehicleSpecs()
