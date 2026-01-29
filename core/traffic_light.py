"""
Advanced traffic light system with realistic visual effects.
No external assets needed - pure PyGame graphics.
"""

import pygame
import math
from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, List, Optional
from datetime import datetime

from config.settings import COLORS


class LightPhase(Enum):
    """Traffic light phases."""
    RED = auto()
    RED_AMBER = auto()  # Red + Yellow (some countries)
    GREEN = auto()
    AMBER = auto()      # Yellow
    OFF = auto()


class LightAnimation:
    """Handles light animations and effects."""

    @staticmethod
    def create_glow_surface(radius: int, color: Tuple[int, int, int], intensity: float = 1.0) -> pygame.Surface:
        """Create a glow effect surface."""
        size = radius * 4
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        # Create gradient glow
        for r in range(radius * 2, 0, -1):
            alpha = int(100 * intensity * (1 - r / (radius * 2)))
            if alpha > 0:
                pygame.draw.circle(surface, (*color, alpha),
                                 (size // 2, size // 2), r)

        return surface

    @staticmethod
    def create_lens_flare(pos: Tuple[int, int], color: Tuple[int, int, int]) -> List[Tuple[Tuple[int, int], float]]:
        """Create lens flare points for realistic light effect."""
        flares = []
        base_color = color

        # Main flare
        flares.append((pos, 1.0))

        # Secondary flares (offset positions)
        offsets = [(5, -5), (-5, 5), (8, 0), (0, 8)]
        for i, offset in enumerate(offsets):
            intensity = 0.3 - (i * 0.05)
            if intensity > 0:
                flare_pos = (pos[0] + offset[0], pos[1] + offset[1])
                flares.append((flare_pos, intensity))

        return flares


@dataclass
class TrafficLightConfig:
    """Configuration for traffic light appearance."""
    pole_color: Tuple[int, int, int] = (50, 50, 50)
    pole_highlight: Tuple[int, int, int] = (100, 100, 100)
    housing_color: Tuple[int, int, int] = (40, 40, 40)
    housing_highlight: Tuple[int, int, int] = (80, 80, 80)
    housing_shadow: Tuple[int, int, int] = (20, 20, 20)
    bezel_color: Tuple[int, int, int] = (60, 60, 60)
    bezel_highlight: Tuple[int, int, int] = (100, 100, 100)

    # Light colors with enhanced vibrancy
    red_light: Tuple[int, int, int] = (255, 50, 50)
    amber_light: Tuple[int, int, int] = (255, 200, 50)
    green_light: Tuple[int, int, int] = (50, 255, 50)
    off_light: Tuple[int, int, int] = (30, 30, 30)

    # Dimensions
    pole_width: int = 12
    pole_height: int = 60
    housing_width: int = 45
    housing_height: int = 135
    light_radius: int = 14
    light_spacing: int = 35
    bezel_thickness: int = 6
    shadow_offset: int = 3


class AdvancedTrafficLight:
    """
    Advanced traffic light with realistic 3D effects, animations, and polish.
    """

    def __init__(self, x: int, y: int, direction: str):
        self.x = x
        self.y = y
        self.direction = direction.lower()  # 'north', 'south', 'east', 'west'
        self.phase = LightPhase.RED
        self.config = TrafficLightConfig()

        # Animation state
        self.pulse_intensity = 0.0
        self.pulse_speed = 3.0
        self.last_update = datetime.now()

        # Create cached surfaces for performance
        self._cached_surfaces = {}
        self._needs_redraw = True

        # Emergency mode (for ambulance priority)
        self.emergency_override = False
        self.emergency_flash = False
        self.flash_timer = 0

    def set_phase(self, phase: LightPhase) -> None:
        """Set the light phase."""
        if self.phase != phase:
            self.phase = phase
            self._needs_redraw = True

    def set_emergency(self, active: bool) -> None:
        """Set emergency override mode."""
        self.emergency_override = active
        self._needs_redraw = True

    def update(self, delta_time: float) -> None:
        """Update animations."""
        # Pulse animation for active lights
        self.pulse_intensity = (math.sin(pygame.time.get_ticks() * 0.001 * self.pulse_speed) * 0.2) + 0.8

        # Emergency flash
        if self.emergency_override:
            self.flash_timer += delta_time
            self.emergency_flash = (math.sin(self.flash_timer * 10) > 0)
            self._needs_redraw = True

    def _get_light_colors(self) -> List[Tuple[int, int, int]]:
        """Get colors for each light based on current phase."""
        if self.emergency_override and self.emergency_flash:
            # Emergency flash - all lights bright red
            return [self.config.red_light] * 3

        colors = [self.config.off_light, self.config.off_light, self.config.off_light]

        if self.phase == LightPhase.RED:
            colors[0] = self.config.red_light
        elif self.phase == LightPhase.RED_AMBER:
            colors[0] = self.config.red_light
            colors[1] = self.config.amber_light
        elif self.phase == LightPhase.GREEN:
            colors[2] = self.config.green_light
        elif self.phase == LightPhase.AMBER:
            colors[1] = self.config.amber_light

        return colors

    def _create_housing_surface(self) -> pygame.Surface:
        """Create the 3D-looking housing surface."""
        width = self.config.housing_width
        height = self.config.housing_height

        # Create surface with alpha for shadows
        surface = pygame.Surface((width + self.config.shadow_offset * 2,
                                height + self.config.shadow_offset * 2),
                               pygame.SRCALPHA)

        # Draw shadow (offset)
        shadow_rect = pygame.Rect(
            self.config.shadow_offset,
            self.config.shadow_offset,
            width,
            height
        )
        pygame.draw.rect(surface, (*self.config.housing_shadow, 150),
                        shadow_rect, border_radius=8)

        # Draw main housing with 3D effect
        main_rect = pygame.Rect(0, 0, width, height)

        # Base color
        pygame.draw.rect(surface, self.config.housing_color,
                        main_rect, border_radius=8)

        # 3D highlight (top/left)
        highlight_points = [
            (0, 0),
            (width, 0),
            (width - 10, 10),
            (10, 10),
            (10, height - 10),
            (0, height)
        ]
        pygame.draw.polygon(surface, self.config.housing_highlight, highlight_points)

        # 3D shadow (bottom/right)
        shadow_points = [
            (width, 0),
            (width, height),
            (0, height),
            (10, height - 10),
            (width - 10, height - 10),
            (width - 10, 10)
        ]
        pygame.draw.polygon(surface, self.config.housing_shadow, shadow_points)

        # Bezel around lights
        bezel_rect = pygame.Rect(
            self.config.bezel_thickness,
            self.config.bezel_thickness,
            width - self.config.bezel_thickness * 2,
            height - self.config.bezel_thickness * 2
        )
        pygame.draw.rect(surface, self.config.bezel_color,
                        bezel_rect,
                        border_radius=6,
                        width=self.config.bezel_thickness)

        # Bezel highlight
        pygame.draw.line(surface, self.config.bezel_highlight,
                        (self.config.bezel_thickness * 2, self.config.bezel_thickness * 2),
                        (width - self.config.bezel_thickness * 2, self.config.bezel_thickness * 2),
                        2)

        return surface

    def _draw_pole(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Draw a realistic pole."""
        pole_w = self.config.pole_width
        pole_h = self.config.pole_height

        # Shadow
        pygame.draw.rect(surface, (*self.config.pole_color[:3], 100),
                        (x - pole_w // 2 + 2, y + 2, pole_w, pole_h),
                        border_radius=3)

        # Main pole with 3D effect
        pole_rect = pygame.Rect(x - pole_w // 2, y, pole_w, pole_h)
        pygame.draw.rect(surface, self.config.pole_color, pole_rect, border_radius=3)

        # Pole highlight (left side)
        highlight_rect = pygame.Rect(x - pole_w // 2, y, pole_w // 2, pole_h)
        pygame.draw.rect(surface, self.config.pole_highlight, highlight_rect, border_radius=3)

        # Pole base (wider at bottom)
        base_width = pole_w + 8
        base_points = [
            (x - base_width // 2, y + pole_h),
            (x + base_width // 2, y + pole_h),
            (x + pole_w // 2, y + pole_h + 10),
            (x - pole_w // 2, y + pole_h + 10)
        ]
        pygame.draw.polygon(surface, self.config.pole_color, base_points)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the advanced traffic light."""
        # Check cache
        cache_key = f"{self.phase.value}_{self.emergency_flash}"
        if not self._needs_redraw and cache_key in self._cached_surfaces:
            cached = self._cached_surfaces[cache_key]
            surface.blit(cached["surface"], cached["rect"])
            return

        # Create new surface
        width = self.config.housing_width + self.config.shadow_offset * 2
        height = self.config.housing_height + self.config.shadow_offset * 2 + self.config.pole_height

        # Create surface for this light
        light_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Draw based on direction
        if self.direction in ['north', 'south']:
            self._draw_vertical_light(light_surface)
        else:
            self._draw_horizontal_light(light_surface)

        # Cache the result
        self._cached_surfaces[cache_key] = {
            "surface": light_surface,
            "rect": pygame.Rect(self.x - width // 2, self.y - height // 2, width, height)
        }
        self._needs_redraw = False

        # Draw to main surface
        surface.blit(light_surface, (self.x - width // 2, self.y - height // 2))

    def _draw_vertical_light(self, surface: pygame.Surface) -> None:
        """Draw vertical traffic light (north/south facing)."""
        # Draw pole (at bottom center)
        pole_x = surface.get_width() // 2
        pole_y = surface.get_height() - self.config.pole_height
        self._draw_pole(surface, pole_x, pole_y)

        # Draw housing (above pole)
        housing_y = pole_y - self.config.housing_height + self.config.shadow_offset
        housing_surf = self._create_housing_surface()
        surface.blit(housing_surf, (self.config.shadow_offset, housing_y))

        # Draw lights
        light_colors = self._get_light_colors()
        housing_center_x = surface.get_width() // 2

        for i, color in enumerate(light_colors):
            light_y = housing_y + self.config.shadow_offset + self.config.bezel_thickness * 2 + \
                     (i * self.config.light_spacing)

            # Light position
            light_pos = (housing_center_x, light_y)

            # Draw light with effects
            self._draw_light_with_effects(surface, light_pos, color, i == 2)  # Green is bottom

    def _draw_horizontal_light(self, surface: pygame.Surface) -> None:
        """Draw horizontal traffic light (east/west facing)."""
        # Rotate the surface for horizontal display
        rotated_surface = pygame.Surface((surface.get_height(), surface.get_width()), pygame.SRCALPHA)

        # Draw as vertical first
        temp_surface = pygame.Surface((surface.get_height(), surface.get_width()), pygame.SRCALPHA)
        temp_light = AdvancedTrafficLight(0, 0, 'north')
        temp_light.config = self.config
        temp_light.phase = self.phase
        temp_light.emergency_override = self.emergency_override
        temp_light.emergency_flash = self.emergency_flash
        temp_light._draw_vertical_light(temp_surface)

        # Rotate based on direction
        if self.direction == 'east':
            rotated = pygame.transform.rotate(temp_surface, -90)
        else:  # west
            rotated = pygame.transform.rotate(temp_surface, 90)

        # Copy to main surface
        surface.blit(rotated, (0, 0))

    def _draw_light_with_effects(self, surface: pygame.Surface,
                                pos: Tuple[int, int],
                                color: Tuple[int, int, int],
                                is_bottom: bool = False) -> None:
        """Draw a single light with glow and lens effects."""
        # Check if light is on (not off color)
        is_on = color != self.config.off_light

        # Draw light lens
        lens_radius = self.config.light_radius
        lens_color = color if is_on else self.config.off_light

        # Lens with glass effect
        pygame.draw.circle(surface, lens_color, pos, lens_radius)

        # Glass highlight (top-left)
        if is_on:
            highlight_pos = (pos[0] - lens_radius // 3, pos[1] - lens_radius // 3)
            pygame.draw.circle(surface, (255, 255, 255, 100), highlight_pos, lens_radius // 3)

        # Glow effect for active lights
        if is_on:
            intensity = self.pulse_intensity if not self.emergency_flash else 1.0

            # Create and draw glow
            glow_surf = LightAnimation.create_glow_surface(lens_radius, color, intensity)
            surface.blit(glow_surf,
                        (pos[0] - glow_surf.get_width() // 2,
                         pos[1] - glow_surf.get_height() // 2))

            # Lens flare for extra realism
            if intensity > 0.7:
                flares = LightAnimation.create_lens_flare(pos, color)
                for flare_pos, flare_intensity in flares:
                    flare_alpha = int(150 * flare_intensity * intensity)
                    pygame.draw.circle(surface, (*color, flare_alpha),
                                     flare_pos, lens_radius // 2)


class TrafficLightSystem:
    """
    Manages all traffic lights at an intersection with coordinated timing.
    """

    def __init__(self, center_x: int, center_y: int, road_width: int):
        self.center_x = center_x
        self.center_y = center_y
        self.road_width = road_width

        # Create lights at each approach
        offset = road_width // 2 + 40

        self.lights = {
            'north': AdvancedTrafficLight(center_x + 25, center_y - offset, 'north'),
            'south': AdvancedTrafficLight(center_x - 25, center_y + offset, 'south'),
            'east': AdvancedTrafficLight(center_x + offset, center_y + 25, 'east'),
            'west': AdvancedTrafficLight(center_x - offset, center_y - 25, 'west')
        }

        # Timing
        self.current_phase = 'NS'  # 'NS' or 'EW'
        self.phase_timer = 0.0
        self.green_duration = 30.0
        self.yellow_duration = 3.0
        self.all_red_duration = 2.0

        # Emergency state
        self.emergency_active = False
        self.emergency_direction = None

    def update(self, delta_time: float) -> None:
        """Update all lights and timing."""
        self.phase_timer += delta_time

        # Update animations for all lights
        for light in self.lights.values():
            light.update(delta_time)

        # Handle emergency override
        if self.emergency_active:
            self._handle_emergency()
            return

        # Normal phase cycling
        self._update_normal_phases()

    def _update_normal_phases(self) -> None:
        """Update normal traffic light phases."""
        # Determine which lights should be green
        if self.current_phase == 'NS':
            active_lights = ['north', 'south']
            opposite_lights = ['east', 'west']
        else:
            active_lights = ['east', 'west']
            opposite_lights = ['north', 'south']

        # Set phases based on timer
        if self.phase_timer < self.green_duration:
            # Green for active direction
            for direction in active_lights:
                self.lights[direction].set_phase(LightPhase.GREEN)
            for direction in opposite_lights:
                self.lights[direction].set_phase(LightPhase.RED)

        elif self.phase_timer < self.green_duration + self.yellow_duration:
            # Yellow for active direction
            for direction in active_lights:
                self.lights[direction].set_phase(LightPhase.AMBER)

        elif self.phase_timer < self.green_duration + self.yellow_duration + self.all_red_duration:
            # All red during clearance
            for light in self.lights.values():
                light.set_phase(LightPhase.RED)

        else:
            # Switch phases
            self.current_phase = 'EW' if self.current_phase == 'NS' else 'NS'
            self.phase_timer = 0.0

    def _handle_emergency(self) -> None:
        """Handle emergency vehicle priority."""
        # Determine which lights should be green for emergency vehicle
        if self.emergency_direction in ['north', 'south']:
            emergency_phase = 'NS'
            opposite_phase = 'EW'
        else:
            emergency_phase = 'EW'
            opposite_phase = 'NS'

        # Set emergency priority
        if self.current_phase != emergency_phase:
            # Switch to emergency phase quickly
            self.current_phase = emergency_phase
            self.phase_timer = self.green_duration - 5.0  # Force quick switch

        # Set all lights to emergency flash except the emergency direction
        for direction, light in self.lights.items():
            light.set_emergency(True)
            if direction == self.emergency_direction:
                light.set_phase(LightPhase.GREEN)
            else:
                light.set_phase(LightPhase.RED)

    def set_emergency(self, direction: Optional[str] = None) -> None:
        """Activate or deactivate emergency mode."""
        self.emergency_active = (direction is not None)
        self.emergency_direction = direction

        if not self.emergency_active:
            for light in self.lights.values():
                light.set_emergency(False)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all traffic lights."""
        for light in self.lights.values():
            light.draw(surface)

    def get_time_until_change(self) -> float:
        """Get seconds until next phase change."""
        total_cycle = self.green_duration + self.yellow_duration + self.all_red_duration
        return max(0, total_cycle - self.phase_timer)


# Test the advanced traffic lights
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from config.settings import DISPLAY

    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Advanced Traffic Lights Demo")
    clock = pygame.time.Clock()

    # Create light system
    light_system = TrafficLightSystem(500, 350, 160)

    # Demo lights in corners
    demo_lights = [
        AdvancedTrafficLight(200, 150, 'north'),
        AdvancedTrafficLight(800, 150, 'south'),
        AdvancedTrafficLight(200, 550, 'east'),
        AdvancedTrafficLight(800, 550, 'west'),
    ]

    # Set different phases for demo
    demo_lights[0].set_phase(LightPhase.RED)
    demo_lights[1].set_phase(LightPhase.GREEN)
    demo_lights[2].set_phase(LightPhase.AMBER)
    demo_lights[3].set_phase(LightPhase.RED_AMBER)
    demo_lights[3].set_emergency(True)

    running = True
    last_time = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - last_time) / 1000.0
        last_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Toggle emergency
                    if light_system.emergency_active:
                        light_system.set_emergency(None)
                    else:
                        light_system.set_emergency('north')
                elif event.key == pygame.K_1:
                    light_system.current_phase = 'NS'
                    light_system.phase_timer = 0
                elif event.key == pygame.K_2:
                    light_system.current_phase = 'EW'
                    light_system.phase_timer = 0

        # Update
        light_system.update(delta_time)
        for light in demo_lights:
            light.update(delta_time)

        # Draw
        screen.fill((20, 25, 35))  # Dark blue-gray background

        # Draw grid for reference
        for x in range(0, 1000, 50):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 700), 1)
        for y in range(0, 700, 50):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (1000, y), 1)

        # Draw demo lights
        for light in demo_lights:
            light.draw(screen)

        # Draw main intersection lights
        light_system.draw(screen)

        # Draw intersection
        pygame.draw.rect(screen, (60, 60, 60),
                        (500 - 80, 350 - 80, 160, 160))

        # Draw info
        font = pygame.font.SysFont('Arial', 22)

        info_lines = [
            "ADVANCED TRAFFIC LIGHTS DEMO",
            f"Phase: {light_system.current_phase}",
            f"Time to change: {light_system.get_time_until_change():.1f}s",
            f"Emergency mode: {'ON' if light_system.emergency_active else 'OFF'}",
            "",
            "CONTROLS:",
            "SPACE: Toggle emergency mode",
            "1: Set NS green",
            "2: Set EW green",
            "ESC: Quit",
            "",
            "Demo lights show:",
            "1. Red  2. Green  3. Amber  4. Emergency Red+Amber"
        ]

        for i, line in enumerate(info_lines):
            color = (220, 220, 255) if i < 5 else (180, 180, 220)
            text = font.render(line, True, color)
            screen.blit(text, (20, 20 + i * 26))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("✅ Advanced traffic lights demo completed!")
