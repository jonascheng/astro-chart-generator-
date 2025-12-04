"""Core astrological calculation logic using pyswisseph."""

from typing import List, Tuple
import swisseph as swe

from src.models import (
    Aspect,
    ChartData,
    House,
    Planet,
    Point,
)

"""十二星座名稱陣列，依照黃道順序排列"""
# Zodiac signs
ZODIAC_SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

"""行星對應 pyswisseph 的編號，方便查詢行星位置"""
# Planet identifiers for pyswisseph
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

"""主要相位及其度數與容許誤差（orb），依 FR-005 規範"""
# Major aspects with their degrees and orbs (per FR-005)
MAJOR_ASPECTS = {
    0: ("Conjunction", 8),
    60: ("Sextile", 6),
    90: ("Square", 8),
    120: ("Trine", 8),
    180: ("Opposition", 8),
}

"""主要城市的地理座標（緯度、經度），用於出生地查詢"""
# Geolocation data for major cities (lat, lon)
CITY_COORDS = {
    ("new york", "usa"): (40.7128, -74.0060),
    ("los angeles", "usa"): (34.0522, -118.2437),
    ("london", "uk"): (51.5074, -0.1278),
    ("paris", "france"): (48.8566, 2.3522),
    ("sydney", "australia"): (-33.8688, 151.2093),
    ("tokyo", "japan"): (35.6762, 139.6503),
    ("berlin", "germany"): (52.5200, 13.4050),
    ("madrid", "spain"): (40.4168, -3.7038),
}


def _get_city_coordinates(city: str, country: str) -> Tuple[float, float]:
    """
    取得指定城市的緯度與經度

    目前採用硬編碼查表，正式環境可改用地理 API
    """
    key = (city.lower(), country.lower())
    if key in CITY_COORDS:
        return CITY_COORDS[key]

    # Default fallback (Greenwich Observatory)
    return (51.4769, 0.0000)


def _degrees_to_zodiac_sign(degrees: float) -> str:
    """將度數（0-360）轉換為星座名稱"""
    sign_index = int(degrees // 30)
    return ZODIAC_SIGNS[sign_index % 12]


def _degrees_to_sign_components(degrees: float) -> Tuple[str, int, int]:
    """
    將度數（0-360）轉換為星座、度、分

    回傳：(星座名稱, 星座內度數, 星座內分)
    """
    sign_index = int(degrees // 30)
    sign = ZODIAC_SIGNS[sign_index % 12]

    # Get degrees within sign (0-29)
    degrees_in_sign = degrees % 30
    degree_part = int(degrees_in_sign)

    # Get minutes within degree (0-59)
    minute_part = int((degrees_in_sign - degree_part) * 60)

    return sign, degree_part, minute_part


def _calculate_jd(date_str: str, time_str: str) -> float:
    """
    根據日期與時間計算儒略日（Julian Day）

    Args:
        date_str: 日期（YYYY-MM-DD）
        time_str: 時間（HH:MM:SS）

    Returns:
        儒略日數值
    """
    year, month, day = map(int, date_str.split("-"))
    time_parts = time_str.split(":")
    hour = int(time_parts[0])
    minute = int(time_parts[1])
    second = int(time_parts[2]) if len(time_parts) > 2 else 0

    # Convert to decimal hour
    time_decimal = hour + minute / 60.0 + second / 3600.0

    # Calculate Julian Day
    jd = swe.julday(year, month, day, time_decimal)
    return jd


def get_planet_positions(
    date_str: str,
    time_str: str,
    latitude: float,
    longitude: float,
    house_cusps: List[float],
) -> List[Planet]:
    """
    計算指定日期、時間、地點的行星位置

    Args:
        date_str: 日期（YYYY-MM-DD）
        time_str: 時間（HH:MM:SS）
        latitude: 緯度
        longitude: 經度
        house_cusps: 12宮分界度數列表

    Returns:
        Planet 物件列表
    """
    jd = _calculate_jd(date_str, time_str)

    positions = []

    for planet_name, planet_id in PLANETS.items():
        # Calculate planet position
        coords, ret_flag = swe.calc_ut(jd, planet_id)
        lon, lat, distance, speed_lon, speed_lat, speed_dist = coords

        # Normalize longitude to 0-360 range
        lon = lon % 360

        # Get zodiac sign with degree and minute
        sign, degree, minute = _degrees_to_sign_components(lon)

        # Determine house placement
        house = _get_house_for_position(lon, house_cusps)

        positions.append(
            Planet(
                name=planet_name,
                longitude=lon,
                sign=sign,
                degree=degree,
                minute=minute,
                house=house,
            )
        )

    return positions


def get_astrological_points(
    date_str: str,
    time_str: str,
    latitude: float,
    longitude: float,
) -> List[Point]:
    """
    計算占星四大點（上升、下降、中天、天底）

    Args:
        date_str: 日期（YYYY-MM-DD）
        time_str: 時間（HH:MM:SS）
        latitude: 緯度
        longitude: 經度

    Returns:
        Point 物件列表（ASC, DSC, MC, IC）
    """
    jd = _calculate_jd(date_str, time_str)

    # Calculate houses to get ASC and MC
    houses, ascmc = swe.houses_ex(jd, latitude, longitude, b"P")

    points = []

    # Ascendant (ASC)
    asc_lon = ascmc[0] % 360
    asc_sign, asc_degree, asc_minute = _degrees_to_sign_components(asc_lon)
    points.append(
        Point(
            name="Ascendant",
            longitude=asc_lon,
            sign=asc_sign,
            degree=asc_degree,
            minute=asc_minute,
        )
    )

    # Descendant (DSC) - opposite of ASC
    dsc_lon = (asc_lon + 180) % 360
    dsc_sign, dsc_degree, dsc_minute = _degrees_to_sign_components(dsc_lon)
    points.append(
        Point(
            name="Descendant",
            longitude=dsc_lon,
            sign=dsc_sign,
            degree=dsc_degree,
            minute=dsc_minute,
        )
    )

    # Midheaven (MC)
    mc_lon = ascmc[1] % 360
    mc_sign, mc_degree, mc_minute = _degrees_to_sign_components(mc_lon)
    points.append(
        Point(
            name="Midheaven",
            longitude=mc_lon,
            sign=mc_sign,
            degree=mc_degree,
            minute=mc_minute,
        )
    )

    # Imum Coeli (IC) - opposite of MC
    ic_lon = (mc_lon + 180) % 360
    ic_sign, ic_degree, ic_minute = _degrees_to_sign_components(ic_lon)
    points.append(
        Point(
            name="Imum Coeli",
            longitude=ic_lon,
            sign=ic_sign,
            degree=ic_degree,
            minute=ic_minute,
        )
    )

    return points


def get_house_cusps(
    date_str: str,
    time_str: str,
    latitude: float,
    longitude: float,
) -> List[House]:
    """
    計算指定日期、時間、地點的十二宮分界

    Args:
        date_str: 日期（YYYY-MM-DD）
        time_str: 時間（HH:MM:SS）
        latitude: 緯度
        longitude: 經度

    Returns:
        House 物件列表（12宮）
    """
    jd = _calculate_jd(date_str, time_str)

    # Calculate houses (Placidus houses)
    houses, ascmc = swe.houses_ex(jd, latitude, longitude, b"P")

    cusps = []

    for house_num in range(1, 13):
        lon = houses[house_num - 1]
        lon = lon % 360

        sign, degree, minute = _degrees_to_sign_components(lon)

        cusps.append(
            House(
                number=house_num,
                longitude=lon,
                sign=sign,
            )
        )

    return cusps


def _get_house_for_position(
    planet_lon: float,
    house_cusps: List[float],
) -> int:
    """
    根據行星度數判斷其所屬宮位

    Args:
        planet_lon: 行星度數（0-360）
        house_cusps: 12宮分界度數列表

    Returns:
        宮位編號（1-12）
    """
    # Find which house the planet is in by checking angles
    for i in range(12):
        current_cusp = house_cusps[i]
        next_cusp = house_cusps[(i + 1) % 12]

        # Handle wraparound at 0/360
        if i == 11:  # Between house 12 and 1
            if planet_lon >= current_cusp or planet_lon < next_cusp:
                return (i % 12) + 1
        else:
            if current_cusp <= next_cusp:
                if current_cusp <= planet_lon < next_cusp:
                    return i + 1
            else:  # Wraparound case
                if planet_lon >= current_cusp or planet_lon < next_cusp:
                    return i + 1

    return 1  # Default to house 1


def get_aspects(
    planets: List[Planet],
    points: List[Point],
) -> List[Aspect]:
    """
    計算行星與占星點之間的主要相位

    Args:
        planets: Planet 物件列表
        points: Point 物件列表

    Returns:
        Aspect 物件列表
    """
    aspects = []

    # Combine all bodies for aspect calculation
    all_bodies = []
    for planet in planets:
        all_bodies.append((planet.name, planet.longitude))
    for point in points:
        all_bodies.append((point.name, point.longitude))

    # Check all body pairs
    for i in range(len(all_bodies)):
        for j in range(i + 1, len(all_bodies)):
            name1, lon1 = all_bodies[i]
            name2, lon2 = all_bodies[j]

            # Calculate angle difference
            diff = abs(lon1 - lon2)
            # Use smallest angle
            angle_diff = min(diff, 360 - diff)

            # Check for major aspects
            aspect_items = MAJOR_ASPECTS.items()
            for aspect_angle, (aspect_type, orb_tolerance) in aspect_items:
                # Check if angle matches aspect within orb
                angular_offset = abs(angle_diff - aspect_angle)

                if angular_offset <= orb_tolerance:
                    aspects.append(
                        Aspect(
                            planet1=name1,
                            planet2=name2,
                            type=aspect_type,
                            orb=angular_offset,
                        )
                    )
                    break  # Each pair has at most one aspect

    return aspects


def calculate_natal_chart(
    date_str: str,
    time_str: str,
    country: str,
    city: str,
) -> ChartData:
    """
    計算完整的出生星盤（本命盤）

    Args:
        date_str: 出生日期（YYYY-MM-DD）
        time_str: 出生時間（HH:MM:SS）
        country: 出生國家
        city: 出生城市

    Returns:
        ChartData 物件，包含行星、占星點、宮位、相位
    """
    # Get coordinates for the city
    latitude, longitude = _get_city_coordinates(city, country)

    # Calculate houses first (needed for planet house placement)
    houses = get_house_cusps(date_str, time_str, latitude, longitude)
    house_cusps = [h.longitude for h in houses]

    # Calculate positions
    planets = get_planet_positions(
        date_str, time_str, latitude, longitude, house_cusps
    )
    points = get_astrological_points(date_str, time_str, latitude, longitude)
    aspects = get_aspects(planets, points)

    return ChartData(
        planets=planets,
        points=points,
        houses=houses,
        aspects=aspects,
    )
