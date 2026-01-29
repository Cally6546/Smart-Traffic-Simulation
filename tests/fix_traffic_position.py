#!/usr/bin/env python3
# fix_traffic_position.py
# Clean test to adjust traffic light positions
# RUN THIS FROM PROJECT ROOT: python3 fix_traffic_position.py

import pygame
import sys
import os

# Setup path - IMPORTANT: This file should be in project root
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from config.settings import DISPLAY, COLORS, INTERSECTION
    from core.intersection import IntersectionRenderer
    print("✅ Modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Current directory: {current_dir}")
    print("Files in directory:")
    for item in os.listdir(current_dir):
        print(f"  {item}")
    sys.exit(1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY.WIDTH, DISPLAY.HEIGHT))
    pygame.display.set_caption("Adjust Traffic Light Positions")
    clock = pygame.time.Clock()

    # Create intersection
    intersection = IntersectionRenderer()
    center_x, center_y = DISPLAY.CENTER

    print("=" * 50)
    print("ADJUST TRAFFIC LIGHT POSITIONS")
    print("=" * 50)
    print(f"Center: ({center_x}, {center_y})")
    print(f"Road width: {INTERSECTION.ROAD_WIDTH}")
    print(f"Stop line offset: {INTERSECTION.STOP_LINE_OFFSET}")

    # STARTING positions - we'll adjust these
    test_positions = {
        'north': {
            'x': center_x + 25,
            'y': center_y - 100,
            'color': (255, 255, 0)  # Yellow
        },
        'south': {
            'x': center_x - 25,
            'y': center_y + 100,
            'color': (255, 165, 0)  # Orange
        },
        'east': {
            'x': center_x + 100,
            'y': center_y + 25,
            'color': (0, 255, 255)  # Cyan
        },
        'west': {
            'x': center_x - 100,
            'y': center_y - 25,
            'color': (200, 0, 255)  # Purple
        }
    }

    print("\nCurrent test positions:")
    for dir_name, pos in test_positions.items():
        print(f"  {dir_name}: ({pos['x']}, {pos['y']})")

    print("\nCONTROLS:")
    print("  N/S/E/W: Select which light to move")
    print("  Arrow keys: Move selected light")
    print("  ENTER: Print final positions")
    print("  ESC: Exit")
    print("\nMove the markers until they look right!")

    selected = 'north'  # Which light we're adjusting

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_n:
                    selected = 'north'
                    print(f"Selected: NORTH")
                elif event.key == pygame.K_s:
                    selected = 'south'
                    print(f"Selected: SOUTH")
                elif event.key == pygame.K_e:
                    selected = 'east'
                    print(f"Selected: EAST")
                elif event.key == pygame.K_w:
                    selected = 'west'
                    print(f"Selected: WEST")
                elif event.key == pygame.K_UP:
                    test_positions[selected]['y'] -= 5
                    print(f"{selected}: y = {test_positions[selected]['y']}")
                elif event.key == pygame.K_DOWN:
                    test_positions[selected]['y'] += 5
                    print(f"{selected}: y = {test_positions[selected]['y']}")
                elif event.key == pygame.K_LEFT:
                    test_positions[selected]['x'] -= 5
                    print(f"{selected}: x = {test_positions[selected]['x']}")
                elif event.key == pygame.K_RIGHT:
                    test_positions[selected]['x'] += 5
                    print(f"{selected}: x = {test_positions[selected]['x']}")
                elif event.key == pygame.K_RETURN:
                    # Print final positions
                    print("\n" + "=" * 50)
                    print("FINAL POSITIONS (copy these):")
                    print("=" * 50)
                    for dir_name, pos in test_positions.items():
                        print(f"'{dir_name}': ({pos['x']}, {pos['y']}),")
                    print("=" * 50)

        # Draw
        screen.fill(COLORS.NIGHT_SKY)
        intersection.render(screen)

        # Draw stop lines for reference (BRIGHT color)
        offset = INTERSECTION.STOP_LINE_OFFSET
        r = INTERSECTION.ROAD_WIDTH // 2

        # North stop line
        pygame.draw.line(screen, (0, 255, 255),  # Bright cyan
                        (center_x - r, center_y - r - offset),
                        (center_x + r, center_y - r - offset), 4)

        # South stop line
        pygame.draw.line(screen, (0, 255, 255),
                        (center_x - r, center_y + r + offset),
                        (center_x + r, center_y + r + offset), 4)

        # East stop line
        pygame.draw.line(screen, (0, 255, 255),
                        (center_x + r + offset, center_y - r),
                        (center_x + r + offset, center_y + r), 4)

        # West stop line
        pygame.draw.line(screen, (0, 255, 255),
                        (center_x - r - offset, center_y - r),
                        (center_x - r - offset, center_y + r), 4)

        # Draw test positions
        for dir_name, pos in test_positions.items():
            x, y, color = pos['x'], pos['y'], pos['color']

            # Draw marker (bigger if selected)
            if dir_name == selected:
                # Selected marker - white and bigger
                pygame.draw.circle(screen, (255, 255, 255), (x, y), 12)
                pygame.draw.circle(screen, color, (x, y), 10)
                pygame.draw.circle(screen, (255, 255, 255), (x, y), 6)
            else:
                # Normal marker
                pygame.draw.circle(screen, color, (x, y), 8)
                pygame.draw.circle(screen, (255, 255, 255), (x, y), 8, 2)

            # Crosshair inside
            pygame.draw.line(screen, (255, 255, 255), (x-6, y), (x+6, y), 2)
            pygame.draw.line(screen, (255, 255, 255), (x, y-6), (x, y+6), 2)

            # Label
            font = pygame.font.SysFont('Arial', 18, bold=True)
            label = font.render(dir_name.upper(), True,
                              (255, 255, 255) if dir_name == selected else color)
            screen.blit(label, (x - 25, y - 35))

            # Coordinates
            coord_font = pygame.font.SysFont('Arial', 14)
            coords = coord_font.render(f"({x}, {y})", True, (200, 200, 200))
            screen.blit(coords, (x - 30, y + 25))

        # Instructions
        font = pygame.font.SysFont('Arial', 22)
        instructions = [
            "ADJUST TRAFFIC LIGHT POSITIONS",
            "",
            f"SELECTED: {selected.upper()} (N/S/E/W to change)",
            "Arrow keys: Move selected light",
            "ENTER: Print final positions",
            "ESC: Exit",
            "",
            "Place markers where lights should be:",
            "• Right side of each approach",
            "• Just before stop line (cyan line)",
            "• Facing approaching traffic"
        ]

        for i, text in enumerate(instructions):
            if i == 0:
                color = (255, 255, 200)
                text_surface = font.render(text, True, color)
                screen.blit(text_surface, (DISPLAY.WIDTH // 2 - 250, 20))
            elif i == 2:
                color = (255, 200, 100)
                text_surface = font.render(text, True, color)
                screen.blit(text_surface, (DISPLAY.WIDTH // 2 - 150, 60))
            else:
                color = (200, 220, 255)
                text_surface = font.render(text, True, color)
                screen.blit(text_surface, (20, 100 + (i-3) * 25))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("\n✅ Done! Copy the positions above.")

if __name__ == "__main__":
    main()
