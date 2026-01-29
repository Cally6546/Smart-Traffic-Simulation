"""
Fixed vehicle manager with proper spawn rates and alignment.
"""

import pygame
import random
from typing import List, Dict
from enum import Enum

from core.vehicle import Vehicle, VehicleDirection, VehicleType
from config.settings import DISPLAY, INTERSECTION


class SpawnRate(Enum):
    """Different traffic density levels - FIXED RATES."""
    VERY_LOW = 0.003   # Night time - very few cars
    LOW = 0.01         # Normal traffic - occasional cars
    MEDIUM = 0.02      # Busy - steady flow
    HIGH = 0.04        # Rush hour - heavy traffic
    VERY_HIGH = 0.06   # Gridlock - maximum reasonable


class VehicleManager:
    """
    Manages all vehicles in the simulation with fixed spawn rates.
    """

    def __init__(self, traffic_lights):
        self.vehicles: List[Vehicle] = []
        self.traffic_lights = traffic_lights
        self.spawn_timer = 0.0
        self.spawn_rate = SpawnRate.MEDIUM

        # Statistics
        self.total_spawned = 0
        self.total_passed = 0
        self.total_wait_time = 0.0
        self.max_wait_time = 0.0

        # Spawn probabilities per direction (can be adjusted for scenarios)
        self.direction_weights = {
            VehicleDirection.NORTH: 1.0,
            VehicleDirection.SOUTH: 1.0,
            VehicleDirection.EAST: 1.0,
            VehicleDirection.WEST: 1.0
        }

        # Emergency vehicle chance (FIXED: much lower)
        self.emergency_chance = 0.001  # 0.1% chance (1 in 1000) - realistic

    def set_spawn_rate(self, rate: SpawnRate) -> None:
        """Set the vehicle spawn rate."""
        self.spawn_rate = rate
        rate_names = {
            SpawnRate.VERY_LOW: "VERY LOW (night)",
            SpawnRate.LOW: "LOW (light)",
            SpawnRate.MEDIUM: "MEDIUM (normal)",
            SpawnRate.HIGH: "HIGH (rush hour)",
            SpawnRate.VERY_HIGH: "VERY HIGH (gridlock)"
        }
        print(f"🚗 Spawn rate set to: {rate_names[rate]}")

    def set_direction_weights(self, weights: Dict[VehicleDirection, float]) -> None:
        """Adjust which directions get more traffic."""
        self.direction_weights = weights

    def update(self, delta_time: float) -> None:
        """Update all vehicles and handle spawning."""
        # Spawn new vehicles
        self._handle_spawning(delta_time)

        # Update existing vehicles
        self._update_vehicles(delta_time)

        # Remove off-screen vehicles
        self._cleanup_vehicles()

    def _handle_spawning(self, delta_time: float) -> None:
        """Handle spawning new vehicles with proper timing."""
        self.spawn_timer += delta_time

        # Spawn check based on rate - FIXED FORMULA
        # We want about 1 vehicle every few seconds for MEDIUM rate
        spawn_chance = self.spawn_rate.value * delta_time * 30  # Adjusted multiplier

        if random.random() < spawn_chance and len(self.vehicles) < 50:  # Limit to 50 vehicles
            # Choose direction based on weights
            directions = list(self.direction_weights.keys())
            weights = list(self.direction_weights.values())
            direction = random.choices(directions, weights=weights, k=1)[0]

            # Determine vehicle type (emergency vehicles are rare)
            vehicle_type = VehicleType.EMERGENCY if random.random() < self.emergency_chance else VehicleType.CAR

            # Create and add vehicle
            vehicle = Vehicle(direction, vehicle_type)
            self.vehicles.append(vehicle)
            self.total_spawned += 1

            # Log emergency vehicles only
            if vehicle_type == VehicleType.EMERGENCY:
                print(f"🚑 Emergency vehicle spawned from {direction.value}")

    def _update_vehicles(self, delta_time: float) -> None:
        """Update all vehicles."""
        for vehicle in self.vehicles:
            # Check if vehicle's light is green
            light_is_green = self._is_light_green_for_vehicle(vehicle)

            # Update vehicle
            vehicle.update(delta_time, light_is_green)

            # Update statistics (only count once when vehicle passes)
            if vehicle.has_passed and not vehicle._passed_counted:
                self.total_passed += 1
                self.total_wait_time += vehicle.wait_time
                self.max_wait_time = max(self.max_wait_time, vehicle.wait_time)
                vehicle._passed_counted = True  # Mark as counted

    def _is_light_green_for_vehicle(self, vehicle: Vehicle) -> bool:
        """Check if the traffic light is green for this vehicle's direction."""
        if not self.traffic_lights:
            return True

        # Map vehicle direction to traffic light direction
        direction_map = {
            VehicleDirection.NORTH: 'north',
            VehicleDirection.SOUTH: 'south',
            VehicleDirection.EAST: 'east',
            VehicleDirection.WEST: 'west'
        }

        light_direction = direction_map[vehicle.direction]
        light = self.traffic_lights.lights.get(light_direction)

        if not light:
            return True

        # Check if light is green
        is_ns = vehicle.direction in [VehicleDirection.NORTH, VehicleDirection.SOUTH]
        current_phase = self.traffic_lights.current_phase

        # Green if phase matches AND timer is in green period (< 30 seconds)
        if is_ns:
            return current_phase == 'NS' and self.traffic_lights.phase_timer < 30
        else:
            return current_phase == 'EW' and self.traffic_lights.phase_timer < 30

    def _cleanup_vehicles(self) -> None:
        """Remove vehicles that are off screen."""
        initial_count = len(self.vehicles)
        self.vehicles = [v for v in self.vehicles if not v.is_off_screen()]

        removed = initial_count - len(self.vehicles)
        if removed > 10:  # Only log if many were removed
            print(f"Cleaned up {removed} vehicles (had {initial_count}, now {len(self.vehicles)})")

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all vehicles."""
        for vehicle in self.vehicles:
            vehicle.draw(surface)

    def get_statistics(self) -> Dict:
        """Get current statistics."""
        avg_wait = self.total_wait_time / self.total_passed if self.total_passed > 0 else 0

        return {
            'total_spawned': self.total_spawned,
            'total_passed': self.total_passed,
            'current_count': len(self.vehicles),
            'average_wait_time': avg_wait,
            'max_wait_time': self.max_wait_time
        }

    def reset(self) -> None:
        """Reset the vehicle manager."""
        self.vehicles.clear()
        self.total_spawned = 0
        self.total_passed = 0
        self.total_wait_time = 0.0
        self.max_wait_time = 0.0
        self.spawn_timer = 0.0
        print("🔄 Vehicle manager reset")


# Quick test
if __name__ == "__main__":
    print("Testing fixed vehicle manager spawn rates:")
    for rate in SpawnRate:
        print(f"  {rate.name}: {rate.value}")
