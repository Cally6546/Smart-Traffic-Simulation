"""
Basic vehicle system for traffic simulation.
"""

import pygame
import random
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Optional

from config.settings import COLORS, VEHICLE, INTERSECTION, DISPLAY


class VehicleType(Enum):
    """Types of vehicles."""
    CAR = "car"
    EMERGENCY = "emergency"
    BUS = "bus"
    TRUCK = "truck"


class VehicleDirection(Enum):
    """Possible directions a vehicle can travel."""
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


@dataclass
class Vehicle:
    """
    A simple vehicle that can move and respond to traffic lights.
    """

    def __init__(self, direction: VehicleDirection, vehicle_type: VehicleType = VehicleType.CAR):
        self.direction = direction
        self.type = vehicle_type
        self.id = random.randint(1000, 9999)

        # Position and movement
        self.x: float = 0.0
        self.y: float = 0.0
        self.speed: float = 0.0
        self.target_speed: float = VEHICLE.MAX_SPEED

        # State
        self.waiting_at_light: bool = False
        self.wait_time: float = 0.0
        self.has_passed: bool = False
        self._passed_counted: bool = False  # Track if we've counted this vehicle

        # Visual
        self.color = self._choose_color()
        self.width = VEHICLE.WIDTH
        self.height = VEHICLE.HEIGHT

        # Set initial position based on direction
        self._set_initial_position()

    def _choose_color(self) -> Tuple[int, int, int]:
        """Choose vehicle color based on type."""
        if self.type == VehicleType.EMERGENCY:
            return COLORS.EMERGENCY_RED
        elif self.type == VehicleType.CAR:
            return random.choice(VEHICLE.COLORS)
        else:
            return COLORS.CAR_BLUE

    def _set_initial_position(self) -> None:
        """Set starting position off-screen based on direction."""
        center_x, center_y = DISPLAY.CENTER
        road_half = INTERSECTION.ROAD_WIDTH // 2
        lane_offset = INTERSECTION.LANE_WIDTH // 2

        if self.direction == VehicleDirection.NORTH:
            self.x = center_x + lane_offset  # Right lane
            self.y = -100  # Above screen
            self.target_speed = VEHICLE.MAX_SPEED
        elif self.direction == VehicleDirection.SOUTH:
            self.x = center_x - lane_offset  # Left lane (from driver's perspective)
            self.y = DISPLAY.HEIGHT + 100  # Below screen
            self.target_speed = VEHICLE.MAX_SPEED
        elif self.direction == VehicleDirection.EAST:
            self.x = DISPLAY.WIDTH + 100  # Right of screen
            self.y = center_y + lane_offset  # Right lane
            self.target_speed = VEHICLE.MAX_SPEED
        elif self.direction == VehicleDirection.WEST:
            self.x = -100  # Left of screen
            self.y = center_y - lane_offset  # Left lane (from driver's perspective)
            self.target_speed = VEHICLE.MAX_SPEED

    def update(self, delta_time: float, light_is_green: bool) -> None:
        """
        Update vehicle position and state.

        Args:
            delta_time: Time since last update in seconds
            light_is_green: Whether the traffic light is green for this direction
        """
        # Update wait time if stopped
        if self.speed < 1.0 and not self.has_passed:
            self.wait_time += delta_time
            self.waiting_at_light = True
        else:
            self.waiting_at_light = False

        # Determine target speed based on traffic light
        if not light_is_green and not self.has_passed:
            # Check if we're approaching the intersection
            distance_to_intersection = self._get_distance_to_intersection()

            if distance_to_intersection < 150:  # Start slowing down
                stop_distance = max(10.0, distance_to_intersection)
                self.target_speed = (stop_distance / 150) * VEHICLE.MAX_SPEED

                if distance_to_intersection < 20:
                    self.target_speed = 0.0  # Stop at line
        else:
            self.target_speed = VEHICLE.MAX_SPEED

        # Apply acceleration/deceleration
        if self.target_speed > self.speed:
            # Accelerate
            self.speed = min(self.speed + VEHICLE.ACCELERATION * delta_time,
                           self.target_speed)
        else:
            # Decelerate
            self.speed = max(self.speed - VEHICLE.DECELERATION * delta_time,
                           self.target_speed)

        # Update position
        self._move(delta_time)

        # Check if passed intersection
        if not self.has_passed:
            self.has_passed = self._has_passed_intersection()

    def _get_distance_to_intersection(self) -> float:
        """Calculate distance to intersection center."""
        center_x, center_y = DISPLAY.CENTER

        if self.direction == VehicleDirection.NORTH:
            return center_y - INTERSECTION.ROAD_WIDTH // 2 - self.y
        elif self.direction == VehicleDirection.SOUTH:
            return self.y - (center_y + INTERSECTION.ROAD_WIDTH // 2)
        elif self.direction == VehicleDirection.EAST:
            return self.x - (center_x + INTERSECTION.ROAD_WIDTH // 2)
        elif self.direction == VehicleDirection.WEST:
            return center_x - INTERSECTION.ROAD_WIDTH // 2 - self.x

    def _has_passed_intersection(self) -> bool:
        """Check if vehicle has passed through the intersection."""
        center_x, center_y = DISPLAY.CENTER
        buffer = 50

        if self.direction == VehicleDirection.NORTH:
            return self.y > center_y + INTERSECTION.ROAD_WIDTH // 2 + buffer
        elif self.direction == VehicleDirection.SOUTH:
            return self.y < center_y - INTERSECTION.ROAD_WIDTH // 2 - buffer
        elif self.direction == VehicleDirection.EAST:
            return self.x < center_x - INTERSECTION.ROAD_WIDTH // 2 - buffer
        elif self.direction == VehicleDirection.WEST:
            return self.x > center_x + INTERSECTION.ROAD_WIDTH // 2 + buffer

    def _move(self, delta_time: float) -> None:
        """Move vehicle based on direction and speed."""
        distance = self.speed * delta_time

        if self.direction == VehicleDirection.NORTH:
            self.y += distance
        elif self.direction == VehicleDirection.SOUTH:
            self.y -= distance
        elif self.direction == VehicleDirection.EAST:
            self.x -= distance
        elif self.direction == VehicleDirection.WEST:
            self.x += distance

    def is_off_screen(self) -> bool:
        """Check if vehicle is completely off screen."""
        buffer = 100

        if self.direction == VehicleDirection.NORTH:
            return self.y > DISPLAY.HEIGHT + buffer
        elif self.direction == VehicleDirection.SOUTH:
            return self.y < -buffer
        elif self.direction == VehicleDirection.EAST:
            return self.x < -buffer
        elif self.direction == VehicleDirection.WEST:
            return self.x > DISPLAY.WIDTH + buffer

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the vehicle."""
        # Create car surface
        car_surface = pygame.Surface((self.width + 4, self.height + 4), pygame.SRCALPHA)

        # Car body
        pygame.draw.rect(car_surface, self.color,
                        (2, 2, self.width, self.height),
                        border_radius=4)

        # Windshield
        pygame.draw.rect(car_surface, (150, 200, 255, 180),
                        (5, 5, self.width - 10, 10),
                        border_radius=2)

        # Wheels
        wheel_color = (20, 20, 20)
        pygame.draw.rect(car_surface, wheel_color, (0, 8, 4, 8))
        pygame.draw.rect(car_surface, wheel_color, (self.width, 8, 4, 8))
        pygame.draw.rect(car_surface, wheel_color, (0, self.height - 16, 4, 8))
        pygame.draw.rect(car_surface, wheel_color, (self.width, self.height - 16, 4, 8))

        # Emergency lights
        if self.type == VehicleType.EMERGENCY:
            flash = pygame.time.get_ticks() // 200 % 2 == 0
            light_color = COLORS.RED if flash else COLORS.CAR_BLUE
            pygame.draw.circle(car_surface, light_color,
                             (self.width // 2 - 5, 6), 3)
            pygame.draw.circle(car_surface, light_color,
                             (self.width // 2 + 5, 6), 3)

        # Rotate based on direction
        rotation = {
            VehicleDirection.NORTH: 0,
            VehicleDirection.SOUTH: 180,
            VehicleDirection.EAST: 90,
            VehicleDirection.WEST: -90
        }[self.direction]

        if rotation != 0:
            car_surface = pygame.transform.rotate(car_surface, rotation)

        # Draw to main surface
        surface.blit(car_surface,
                    (int(self.x - car_surface.get_width() // 2),
                     int(self.y - car_surface.get_height() // 2)))


# Test the vehicle system
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY.WIDTH, DISPLAY.HEIGHT))
    pygame.display.set_caption("Vehicle Test")
    clock = pygame.time.Clock()

    from core.intersection import IntersectionRenderer
    intersection = IntersectionRenderer()

    # Create test vehicles
    vehicles = [
        Vehicle(VehicleDirection.NORTH),
        Vehicle(VehicleDirection.SOUTH, VehicleType.EMERGENCY),
        Vehicle(VehicleDirection.EAST),
        Vehicle(VehicleDirection.WEST)
    ]

    # Position them for testing
    center_x, center_y = DISPLAY.CENTER
    lane_offset = INTERSECTION.LANE_WIDTH // 2

    vehicles[0].x = center_x + lane_offset
    vehicles[0].y = center_y - 100

    vehicles[1].x = center_x - lane_offset
    vehicles[1].y = center_y + 100

    vehicles[2].x = center_x + 100
    vehicles[2].y = center_y + lane_offset

    vehicles[3].x = center_x - 100
    vehicles[3].y = center_y - lane_offset

    print("🚗 Vehicle Test Starting...")
    print(f"Created {len(vehicles)} vehicles")
    print("SPACE: Move vehicles | ESC: Quit")

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Move all vehicles
                    for vehicle in vehicles:
                        vehicle.update(delta_time, light_is_green=True)

        screen.fill(COLORS.NIGHT_SKY)
        intersection.render(screen)

        # Draw vehicles
        for vehicle in vehicles:
            vehicle.draw(screen)

        # Instructions
        font = pygame.font.SysFont('Arial', 24)
        text = font.render("Press SPACE to move vehicles", True, (255, 255, 200))
        screen.blit(text, (20, 20))

        pygame.display.flip()

    pygame.quit()
    print("✅ Vehicle test completed!")
