"""
Intersection rendering and logic.
Clean, focused module that only handles the intersection.
"""

import pygame
import sys
import os
from typing import Tuple
from dataclasses import dataclass

# Add parent directory to path so we can import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config.settings import COLORS, DISPLAY, INTERSECTION, FONT_SMALL
except ImportError as e:
    print(f"❌ Failed to import config: {e}")
    print("Make sure you have config/settings.py")
    sys.exit(1)


@dataclass
class IntersectionMetrics:
    """Track metrics for the intersection."""
    total_cars_passed: int = 0
    average_wait_time: float = 0.0
    max_wait_time: float = 0.0


class IntersectionRenderer:
    """
    Handles rendering of the intersection.
    Separated from logic for clean architecture.
    """

    def __init__(self):
        self.center_x, self.center_y = DISPLAY.CENTER

    def render(self, surface: pygame.Surface) -> None:
        """Render the complete intersection."""
        self._draw_roads(surface)
        self._draw_intersection_area(surface)
        self._draw_lane_markings(surface)
        self._draw_stop_lines(surface)
        self._draw_street_names(surface)

    def _draw_roads(self, surface: pygame.Surface) -> None:
        """Draw the vertical and horizontal roads."""
        # Vertical road (Main Street)
        vertical_road = pygame.Rect(
            self.center_x - INTERSECTION.ROAD_WIDTH // 2,
            0,
            INTERSECTION.ROAD_WIDTH,
            DISPLAY.HEIGHT
        )
        pygame.draw.rect(surface, COLORS.ROAD_GRAY, vertical_road)

        # Horizontal road (1st Avenue)
        horizontal_road = pygame.Rect(
            0,
            self.center_y - INTERSECTION.ROAD_WIDTH // 2,
            DISPLAY.WIDTH,
            INTERSECTION.ROAD_WIDTH
        )
        pygame.draw.rect(surface, COLORS.ROAD_GRAY, horizontal_road)

    def _draw_intersection_area(self, surface: pygame.Surface) -> None:
        """Draw the intersection square where roads cross."""
        intersection_rect = pygame.Rect(
            self.center_x - INTERSECTION.ROAD_WIDTH // 2,
            self.center_y - INTERSECTION.ROAD_WIDTH // 2,
            INTERSECTION.ROAD_WIDTH,
            INTERSECTION.ROAD_WIDTH
        )
        pygame.draw.rect(surface, COLORS.INTERSECTION_DARK, intersection_rect)

    def _draw_lane_markings(self, surface: pygame.Surface) -> None:
        """Draw dashed lane markings."""
        # Vertical center line (dashed)
        dash_length = INTERSECTION.LANE_MARKING_LENGTH
        dash_gap = INTERSECTION.LANE_MARKING_GAP

        for y in range(0, DISPLAY.HEIGHT, dash_length + dash_gap):
            if y < self.center_y - INTERSECTION.ROAD_WIDTH // 2 or y > self.center_y + INTERSECTION.ROAD_WIDTH // 2:
                start = (self.center_x, y)
                end = (self.center_x, min(y + dash_length, DISPLAY.HEIGHT))
                pygame.draw.line(surface, COLORS.LANE_YELLOW, start, end, 2)

        # Horizontal center line (dashed)
        for x in range(0, DISPLAY.WIDTH, dash_length + dash_gap):
            if x < self.center_x - INTERSECTION.ROAD_WIDTH // 2 or x > self.center_x + INTERSECTION.ROAD_WIDTH // 2:
                start = (x, self.center_y)
                end = (min(x + dash_length, DISPLAY.WIDTH), self.center_y)
                pygame.draw.line(surface, COLORS.LANE_YELLOW, start, end, 2)

    def _draw_stop_lines(self, surface: pygame.Surface) -> None:
        """Draw stop lines at each approach."""
        offset = INTERSECTION.STOP_LINE_OFFSET

        # North stop line
        north_line = [
            (self.center_x - INTERSECTION.ROAD_WIDTH // 2, self.center_y - INTERSECTION.ROAD_WIDTH // 2 - offset),
            (self.center_x + INTERSECTION.ROAD_WIDTH // 2, self.center_y - INTERSECTION.ROAD_WIDTH // 2 - offset)
        ]
        pygame.draw.line(surface, COLORS.STOP_WHITE, *north_line, 4)

        # South stop line
        south_line = [
            (self.center_x - INTERSECTION.ROAD_WIDTH // 2, self.center_y + INTERSECTION.ROAD_WIDTH // 2 + offset),
            (self.center_x + INTERSECTION.ROAD_WIDTH // 2, self.center_y + INTERSECTION.ROAD_WIDTH // 2 + offset)
        ]
        pygame.draw.line(surface, COLORS.STOP_WHITE, *south_line, 4)

        # East stop line
        east_line = [
            (self.center_x + INTERSECTION.ROAD_WIDTH // 2 + offset, self.center_y - INTERSECTION.ROAD_WIDTH // 2),
            (self.center_x + INTERSECTION.ROAD_WIDTH // 2 + offset, self.center_y + INTERSECTION.ROAD_WIDTH // 2)
        ]
        pygame.draw.line(surface, COLORS.STOP_WHITE, *east_line, 4)

        # West stop line
        west_line = [
            (self.center_x - INTERSECTION.ROAD_WIDTH // 2 - offset, self.center_y - INTERSECTION.ROAD_WIDTH // 2),
            (self.center_x - INTERSECTION.ROAD_WIDTH // 2 - offset, self.center_y + INTERSECTION.ROAD_WIDTH // 2)
        ]
        pygame.draw.line(surface, COLORS.STOP_WHITE, *west_line, 4)

    def _draw_street_names(self, surface: pygame.Surface) -> None:
        """Draw street names."""
        # Main Street (vertical)
        main_street_text = FONT_SMALL.render("Main Street", True, COLORS.TEXT_WHITE)

        # North label
        north_rect = main_street_text.get_rect(center=(self.center_x, 40))
        surface.blit(main_street_text, north_rect)

        # South label
        south_rect = main_street_text.get_rect(center=(self.center_x, DISPLAY.HEIGHT - 60))
        surface.blit(main_street_text, south_rect)

        # 1st Avenue (horizontal)
        first_avenue_text = FONT_SMALL.render("1st Avenue", True, COLORS.TEXT_WHITE)

        # Rotated for vertical text
        rotated_text = pygame.transform.rotate(first_avenue_text, 90)

        # West label
        west_rect = rotated_text.get_rect(center=(40, self.center_y))
        surface.blit(rotated_text, west_rect)

        # East label
        rotated_text_east = pygame.transform.rotate(first_avenue_text, -90)
        east_rect = rotated_text_east.get_rect(center=(DISPLAY.WIDTH - 40, self.center_y))
        surface.blit(rotated_text_east, east_rect)


# Test the intersection renderer
if __name__ == "__main__":
    print("🧪 Testing intersection renderer...")

    pygame.init()
    screen = pygame.display.set_mode((DISPLAY.WIDTH, DISPLAY.HEIGHT))
    pygame.display.set_caption("Intersection Test")
    clock = pygame.time.Clock()

    renderer = IntersectionRenderer()
    print(f"✅ Renderer created. Center: ({renderer.center_x}, {renderer.center_y})")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(COLORS.NIGHT_SKY)
        renderer.render(screen)

        # Instructions
        font = pygame.font.SysFont('Arial', 24)
        text = font.render("Press ESC to quit", True, COLORS.TEXT_WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("✅ Intersection renderer test completed!")
