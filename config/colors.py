from dataclasses import dataclass

@dataclass(frozen=True)
class Colors:
    # --- Background & Environment ---
    NIGHT_SKY = (10, 15, 30)
    DAY_SKY = (135, 206, 235)
    ASPHALT = (50, 50, 50)

    # --- Roads & Intersection ---
    ROAD_GRAY = (60, 60, 60)
    ROAD_DARK = (40, 45, 60)
    ROAD_LIGHT = (60, 65, 80)
    INTERSECTION_DARK = (70, 70, 70)  # Fixed the missing attribute

    # --- Markings ---
    LANE_YELLOW = (255, 235, 59)
    LANE_MARKER = (220, 220, 150)
    STOP_WHITE = (255, 255, 255)

    # --- Traffic Lights ---
    RED = (220, 60, 60)
    RED_DARK = (180, 40, 40)
    YELLOW = (255, 200, 50)
    GREEN = (50, 200, 50)
    LIGHT_OFF = (40, 40, 40)

    # --- Brand Colors (For UIManager) ---
    BRAND_PRIMARY = (0, 102, 204)
    BRAND_ACCENT = (0, 255, 204)
    BRAND_LIGHT = (200, 230, 255)

    # --- UI Elements ---
    UI_BACKGROUND = (20, 25, 40, 220)
    UI_PANEL = (30, 35, 50, 230)
    UI_PANEL_DARK = (20, 22, 35, 240)
    TEXT_WHITE = (240, 245, 255)
    TEXT_DIM = (180, 190, 210)
    TEXT_HIGHLIGHT = (100, 180, 255)
    TEXT_SUCCESS = (100, 220, 100)
    TEXT_WARNING = (255, 180, 60)
    ACCENT_EMERGENCY = (255, 80, 100)

    # --- Vehicles ---
    CAR_BLUE = (52, 152, 219)
    CAR_GREEN = (46, 204, 113)
    CAR_YELLOW = (241, 196, 15)
    CAR_PURPLE = (155, 89, 182)
    CAR_RED = (231, 76, 60)
    EMERGENCY_RED = (255, 0, 0)

COLORS = Colors()
