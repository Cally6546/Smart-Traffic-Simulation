import pygame
from .colors import COLORS
from .geometry import DISPLAY, INTERSECTION, VEHICLE

# --- Brand & Project Information ---
# This dictionary is required by your UIManager
BRAND_INFO = {
    "group_name": "INNOHUB KE",
    "creator": "Calson",
    "version": "v2.1.0-AI",
    "description": "Smart Traffic Intelligence System"
}

# --- Font Configurations ---
pygame.font.init()

# Use a fallback to 'Arial' if 'Segoe UI' isn't on your HP EliteBook (Linux/Ubuntu)
def get_font(name, size, bold=False):
    try:
        return pygame.font.SysFont(name, size, bold=bold)
    except:
        return pygame.font.SysFont('Arial', size, bold=bold)

FONT_SMALL = get_font('Segoe UI', 14)
FONT_MEDIUM = get_font('Segoe UI', 18)
FONT_SUBTITLE = get_font('Segoe UI', 20)      # Required by UIManager
FONT_LARGE = get_font('Segoe UI', 24, bold=True)
FONT_TITLE = get_font('Segoe UI', 32, bold=True) # Required by UIManager

# --- Validation Logic ---
def validate_config():
    """Checks for logical errors in dimensions."""
    try:
        assert DISPLAY.WIDTH >= 600, "Display too narrow"
        assert INTERSECTION.ROAD_WIDTH > 0, "Road width must be positive"
        # Ensure the road actually fits on the screen
        assert INTERSECTION.ROAD_WIDTH < DISPLAY.HEIGHT, "Road wider than screen height"
        print("✅ Configuration validated")
    except AssertionError as e:
        print(f"❌ Config Error: {e}")

if __name__ == "__main__":
    validate_config()
    print(f"Loaded Brand: {BRAND_INFO['group_name']}")
