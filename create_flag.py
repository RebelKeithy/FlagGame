#!/usr/bin/env python3
"""
SVG Flag Template Generator

A modular and extensible script for generating SVG flag templates with various
geometric elements like bars, crosses, circles, stars, moons, rectangles,
triangles and side features.
"""

import argparse
import os
import sys
import random
import math
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass, field


# Country name to ISO 2-letter code mapping
COUNTRY_CODES = {
    "afghanistan": "af", "albania": "al", "algeria": "dz", "andorra": "ad", "angola": "ao",
    "argentina": "ar", "armenia": "am", "australia": "au", "austria": "at", "azerbaijan": "az",
    "bahamas": "bs", "bahrain": "bh", "bangladesh": "bd", "barbados": "bb", "belarus": "by",
    "belgium": "be", "belize": "bz", "benin": "bj", "bhutan": "bt", "bolivia": "bo",
    "bosnia": "ba", "botswana": "bw", "brazil": "br", "brunei": "bn", "bulgaria": "bg",
    "burkina": "bf", "burundi": "bi", "cambodia": "kh", "cameroon": "cm", "canada": "ca",
    "chad": "td", "chile": "cl", "china": "cn", "colombia": "co", "comoros": "km",
    "congo": "cg", "croatia": "hr", "cuba": "cu", "cyprus": "cy", "czechia": "cz",
    "denmark": "dk", "djibouti": "dj", "dominica": "dm", "ecuador": "ec", "egypt": "eg",
    "estonia": "ee", "ethiopia": "et", "fiji": "fj", "finland": "fi", "france": "fr",
    "gabon": "ga", "gambia": "gm", "georgia": "ge", "germany": "de", "ghana": "gh",
    "greece": "gr", "grenada": "gd", "guatemala": "gt", "guinea": "gn", "guyana": "gy",
    "haiti": "ht", "honduras": "hn", "hungary": "hu", "iceland": "is", "india": "in",
    "indonesia": "id", "iran": "ir", "iraq": "iq", "ireland": "ie", "israel": "il",
    "italy": "it", "jamaica": "jm", "japan": "jp", "jordan": "jo", "kazakhstan": "kz",
    "kenya": "ke", "kiribati": "ki", "kosovo": "xk", "kuwait": "kw", "kyrgyzstan": "kg",
    "laos": "la", "latvia": "lv", "lebanon": "lb", "lesotho": "ls", "liberia": "lr",
    "libya": "ly", "lithuania": "lt", "luxembourg": "lu", "madagascar": "mg", "malawi": "mw",
    "malaysia": "my", "maldives": "mv", "mali": "ml", "malta": "mt", "mauritania": "mr",
    "mauritius": "mu", "mexico": "mx", "micronesia": "fm", "moldova": "md", "monaco": "mc",
    "mongolia": "mn", "montenegro": "me", "morocco": "ma", "mozambique": "mz", "myanmar": "mm",
    "namibia": "na", "nauru": "nr", "nepal": "np", "netherlands": "nl", "nicaragua": "ni",
    "niger": "ne", "nigeria": "ng", "norway": "no", "oman": "om", "pakistan": "pk",
    "palau": "pw", "panama": "pa", "paraguay": "py", "peru": "pe", "philippines": "ph",
    "poland": "pl", "portugal": "pt", "qatar": "qa", "romania": "ro", "russia": "ru",
    "rwanda": "rw", "samoa": "ws", "senegal": "sn", "serbia": "rs", "singapore": "sg",
    "slovakia": "sk", "slovenia": "si", "somalia": "so", "spain": "es", "sudan": "sd",
    "suriname": "sr", "sweden": "se", "switzerland": "ch", "syria": "sy", "taiwan": "tw",
    "tajikistan": "tj", "tanzania": "tz", "thailand": "th", "togo": "tg", "tonga": "to",
    "tunisia": "tn", "turkey": "tr", "turkmenistan": "tm", "tuvalu": "tv", "uganda": "ug",
    "ukraine": "ua", "uruguay": "uy", "uzbekistan": "uz", "vanuatu": "vu", "vatican": "va",
    "venezuela": "ve", "vietnam": "vn", "yemen": "ye", "zambia": "zm", "zimbabwe": "zw",
    "north macedonia": "mk",
    # Common alternatives
    "usa": "us", "united states": "us", "uk": "gb", "united kingdom": "gb", "britain": "gb",
    "south korea": "kr", "north korea": "kp", "czech republic": "cz", "dominican republic": "do",
    "central african republic": "cf", "democratic republic of congo": "cd", "east timor": "tl",
    "equatorial guinea": "gq", "ivory coast": "ci", "marshall islands": "mh",
    "papua new guinea": "pg", "saint lucia": "lc", "saudi arabia": "sa", "sierra leone": "sl",
    "solomon islands": "sb", "south africa": "za", "south sudan": "ss", "sri lanka": "lk",
    "trinidad and tobago": "tt", "united arab emirates": "ae"
}

# Named colors mapping
NAMED_COLORS = {
    'red': '#ff0000', 'blue': '#0000ff', 'green': '#008000', 'yellow': '#ffff00',
    'orange': '#ffa500', 'purple': '#800080', 'pink': '#ffc0cb', 'brown': '#a52a2a',
    'black': '#000000', 'white': '#ffffff', 'gray': '#808080', 'grey': '#808080',
    'navy': '#000080', 'maroon': '#800000', 'olive': '#808000', 'lime': '#00ff00',
    'aqua': '#00ffff', 'teal': '#008080', 'silver': '#c0c0c0', 'fuchsia': '#ff00ff'
}


class ColorManager:
    """Manages color assignment for flag elements"""

    def __init__(self, colors: Optional[List[str]] = None):
        self.colors = colors or []
        self.index = 0

    def get_next_color(self) -> str:
        """Get the next color in sequence, or random if none left"""
        if self.index < len(self.colors):
            color = self.colors[self.index]
            self.index += 1
            return color
        return self._generate_random_color()

    def reset(self):
        """Reset color index to beginning"""
        self.index = 0

    @staticmethod
    def _generate_random_color() -> str:
        """Generate a random hex color"""
        return f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"

    @staticmethod
    def parse_colors(color_list: List[str]) -> List[str]:
        """Parse and validate color list"""
        if not color_list:
            return []

        colors = []
        for color in color_list:
            # Remove # if present and validate hex
            color = color.lstrip('#')
            if len(color) == 6 and all(c in '0123456789abcdefABCDEF' for c in color):
                colors.append(f"#{color.lower()}")
            elif len(color) == 3 and all(c in '0123456789abcdefABCDEF' for c in color):
                # Expand 3-digit hex to 6-digit
                colors.append(f"#{color[0]*2}{color[1]*2}{color[2]*2}".lower())
            else:
                # Try named colors
                if color.lower() in NAMED_COLORS:
                    colors.append(NAMED_COLORS[color.lower()])
                else:
                    raise ValueError(f"Invalid color: {color}")

        return colors


@dataclass
class FlagDimensions:
    """Flag dimensions container"""
    width: int
    height: int


class FlagElement(ABC):
    """Abstract base class for all flag elements"""

    @abstractmethod
    def render(self, color_manager: ColorManager) -> List[str]:
        """Render the element as SVG strings"""
        pass

    @abstractmethod
    def describe(self) -> str:
        """Return a human-readable description of the element"""
        pass

    @abstractmethod
    def validate(self, dimensions: FlagDimensions) -> Optional[str]:
        """Validate the element against flag dimensions. Returns error message if invalid."""
        pass


@dataclass
class Background(FlagElement):
    """Solid background rectangle"""
    dimensions: FlagDimensions

    def render(self, color_manager: ColorManager) -> List[str]:
        color = color_manager.get_next_color()
        return [f'    <rect class="flag-component" width="{self.dimensions.width}" '
                f'height="{self.dimensions.height}" x="0" y="0" fill="{color}"/>']

    def describe(self) -> str:
        return "background"

    def validate(self, dimensions: FlagDimensions) -> Optional[str]:
        return None


@dataclass
class Bars(FlagElement):
    """Horizontal or vertical bars"""
    dimensions: FlagDimensions
    orientation: str  # 'horizontal' or 'vertical'
    count: int
    widths: Optional[List[int]] = None  # Custom widths/heights for each bar

    def render(self, color_manager: ColorManager) -> List[str]:
        elements = []

        if self.orientation == 'horizontal':
            if self.widths:
                # Use custom heights
                current_y = 0
                for i, height in enumerate(self.widths):
                    color = color_manager.get_next_color()
                    elements.append(f'    <rect class="flag-component" width="{self.dimensions.width}" '
                                  f'height="{height}" x="0" y="{current_y}" fill="{color}"/>')
                    current_y += height
            else:
                # Equal division
                bar_height = self.dimensions.height // self.count
                remainder = self.dimensions.height % self.count

                for i in range(self.count):
                    y = i * bar_height
                    current_height = bar_height + (1 if i < remainder else 0)
                    if i >= remainder:
                        y += remainder

                    color = color_manager.get_next_color()
                    elements.append(f'    <rect class="flag-component" width="{self.dimensions.width}" '
                                  f'height="{current_height}" x="0" y="{y}" fill="{color}"/>')

        else:  # vertical
            if self.widths:
                # Use custom widths
                current_x = 0
                for i, width in enumerate(self.widths):
                    color = color_manager.get_next_color()
                    elements.append(f'    <rect class="flag-component" width="{width}" '
                                  f'height="{self.dimensions.height}" x="{current_x}" y="0" fill="{color}"/>')
                    current_x += width
            else:
                # Equal division
                bar_width = self.dimensions.width // self.count
                remainder = self.dimensions.width % self.count

                for i in range(self.count):
                    x = i * bar_width
                    current_width = bar_width + (1 if i < remainder else 0)
                    if i >= remainder:
                        x += remainder

                    color = color_manager.get_next_color()
                    elements.append(f'    <rect class="flag-component" width="{current_width}" '
                                  f'height="{self.dimensions.height}" x="{x}" y="0" fill="{color}"/>')

        return elements

    def describe(self) -> str:
        if self.widths:
            if self.orientation == 'vertical':
                widths_str = ",".join(map(str, self.widths))
                return f"{len(self.widths)} vertical bars (widths: {widths_str})"
            else:
                heights_str = ",".join(map(str, self.widths))
                return f"{len(self.widths)} horizontal bars (heights: {heights_str})"
        else:
            if self.orientation == 'vertical':
                bar_width = self.dimensions.width // self.count
                return f"{self.count} vertical bars ({bar_width} units wide each)"
            else:
                bar_height = self.dimensions.height // self.count
                return f"{self.count} horizontal bars ({bar_height} units tall each)"

    def validate(self, dimensions: FlagDimensions) -> Optional[str]:
        if self.widths:
            if len(self.widths) < 2:
                return f"{self.orientation.capitalize()} bars must have >= 2 widths specified"

            total = sum(self.widths)
            expected = dimensions.height if self.orientation == 'horizontal' else dimensions.width

            if total != expected:
                return f"{self.orientation.capitalize()} bar widths sum to {total}, but flag dimension is {expected}"

            if any(w <= 0 for w in self.widths):
                return f"{self.orientation.capitalize()} bar widths must be > 0"
        else:
            if self.count < 2:
                return f"{self.orientation.capitalize()} bars must be >= 2"

            if self.orientation == 'vertical' and dimensions.width % self.count != 0:
                return f"Warning: Width {dimensions.width} doesn't divide evenly by {self.count} bars."
            elif self.orientation == 'horizontal' and dimensions.height % self.count != 0:
                return f"Warning: Height {dimensions.height} doesn't divide evenly by {self.count} bars."

        return None


@dataclass
class Side(FlagElement):
    """Side feature (bar, triangle, or trapezoid)"""
    dimensions: FlagDimensions
    width: int
    right_edge_length: int
    position: str = 'left'  # 'left' or 'right'

    def render(self, color_manager: ColorManager) -> List[str]:
        color = color_manager.get_next_color()

        # Determine shape type based on dimensions
        if self.right_edge_length == self.dimensions.height:
            # Bar (rectangle)
            if self.position == 'left':
                return [f'    <rect class="flag-component" width="{self.width}" '
                       f'height="{self.dimensions.height}" x="0" y="0" fill="{color}"/>']
            else:  # right
                x_pos = self.dimensions.width - self.width
                return [f'    <rect class="flag-component" width="{self.width}" '
                       f'height="{self.dimensions.height}" x="{x_pos}" y="0" fill="{color}"/>']

        elif self.right_edge_length == 0:
            # Triangle
            if self.position == 'left':
                # Triangle pointing right, tip at vertical center
                center_y = self.dimensions.height // 2
                points = f"0,0 {self.width},{center_y} 0,{self.dimensions.height}"
            else:  # right
                # Triangle pointing left, tip at vertical center
                center_y = self.dimensions.height // 2
                x_base = self.dimensions.width - self.width
                points = f"{self.dimensions.width},0 {x_base},{center_y} {self.dimensions.width},{self.dimensions.height}"

            return [f'    <polygon class="flag-component" points="{points}" fill="{color}"/>']

        else:
            # Trapezoid
            if self.position == 'left':
                # Left trapezoid
                top_y = (self.dimensions.height - self.right_edge_length) // 2
                bottom_y = top_y + self.right_edge_length
                points = f"0,0 {self.width},{top_y} {self.width},{bottom_y} 0,{self.dimensions.height}"
            else:  # right
                # Right trapezoid
                top_y = (self.dimensions.height - self.right_edge_length) // 2
                bottom_y = top_y + self.right_edge_length
                x_base = self.dimensions.width - self.width
                points = f"{self.dimensions.width},0 {x_base},{top_y} {x_base},{bottom_y} {self.dimensions.width},{self.dimensions.height}"

            return [f'    <polygon class="flag-component" points="{points}" fill="{color}"/>']

    def describe(self) -> str:
        if self.right_edge_length == self.dimensions.height:
            shape_type = "bar"
        elif self.right_edge_length == 0:
            shape_type = "triangle"
        else:
            shape_type = "trapezoid"

        return f"{self.position} {shape_type} (width {self.width}, right edge {self.right_edge_length})"

    def validate(self, dimensions: FlagDimensions) -> Optional[str]:
        if self.width < 1:
            return "Side width must be >= 1"
        if self.width >= dimensions.width:
            return f"Side width {self.width} must be less than flag width {dimensions.width}"
        if self.right_edge_length < 0:
            return "Side right edge length must be >= 0"
        if self.right_edge_length > dimensions.height:
            return f"Side right edge length {self.right_edge_length} must be <= flag height {dimensions.height}"
        if self.position not in ['left', 'right']:
            return "Side position must be 'left' or 'right'"
        return None


@dataclass
class Cross(FlagElement):
    """Cross element"""
    dimensions: FlagDimensions
    center_x: int
    center_y: int
    width: int

    def render(self, color_manager: ColorManager) -> List[str]:
        half_width = self.width // 2

        # Cross polygon points (extending to edges)
        cross_points = [
            (self.center_x - half_width, 0),
            (self.center_x + half_width, 0),
            (self.center_x + half_width, self.center_y - half_width),
            (self.dimensions.width, self.center_y - half_width),
            (self.dimensions.width, self.center_y + half_width),
            (self.center_x + half_width, self.center_y + half_width),
            (self.center_x + half_width, self.dimensions.height),
            (self.center_x - half_width, self.dimensions.height),
            (self.center_x - half_width, self.center_y + half_width),
            (0, self.center_y + half_width),
            (0, self.center_y - half_width),
            (self.center_x - half_width, self.center_y - half_width)
        ]

        points_str = " ".join([f"{x},{y}" for x, y in cross_points])
        color = color_manager.get_next_color()
        return [f'    <polygon class="flag-component" points="{points_str}" fill="{color}"/>']

    def describe(self) -> str:
        return f"cross at ({self.center_x},{self.center_y}) width {self.width}"

    def validate(self, dimensions: FlagDimensions) -> Optional[str]:
        if self.width < 1:
            return "Cross width must be >= 1"
        if not (0 <= self.center_x < dimensions.width and 0 <= self.center_y < dimensions.height):
            return "Cross center point must be within SVG bounds"
        return None


@dataclass
class Canton(FlagElement):
    """Canton (top-left rectangular overlay)"""
    width: int
    height: int

    def render(self, color_manager: ColorManager) -> List[str]:
        color = color_manager.get_next_color()
        return [f'    <rect class="flag-component" width="{self.width}" '
                f'height="{self.height}" x="0" y="0" fill="{color}"/>']

    def describe(self) -> str:
        return f"canton ({self.width}x{self.height})"

    def validate(self, dimensions: FlagDimensions) -> Optional[str]:
        if self.width < 1:
            return "Canton width must be >= 1"
        if self.height < 1:
            return "Canton height must be >= 1"
        if self.width >= dimensions.width:
            return f"Canton width {self.width} must be less than flag width {dimensions.width}"
        if self.height >= dimensions.height:
            return f"Canton height {self.height} must be less than flag height {dimensions.height}"
        return None


@dataclass
class Circle(FlagElement):
    """Circle element"""
    center_x: int
    center_y: int
    radius: int

    def render(self, color_manager: ColorManager) -> List[str]:
        color = color_manager.get_next_color()
        return [f'    <circle class="flag-component" cx="{self.center_x}" '
                f'cy="{self.center_y}" r="{self.radius}" fill="{color}"/>']

    def describe(self) -> str:
        return f"circle at ({self.center_x},{self.center_y}) radius {self.radius}"

    def validate(self, dimensions: FlagDimensions) -> Optional[str]:
        if self.radius < 1:
            return "Circle radius must be >= 1"
        if not (0 <= self.center_x < dimensions.width and 0 <= self.center_y < dimensions.height):
            return "Circle center point must be within SVG bounds"
        return None


@dataclass
class Star(FlagElement):
    """5-pointed star element"""
    center_x: float
    center_y: float
    radius: float
    angle: float

    def render(self, color_manager: ColorManager) -> List[str]:
        points = []
        inner_radius = self.radius * 0.4

        for i in range(10):
            current_radius = self.radius if i % 2 == 0 else inner_radius
            point_angle = math.radians(self.angle + i * 36 - 90)

            x = self.center_x + current_radius * math.cos(point_angle)
            y = self.center_y + current_radius * math.sin(point_angle)
            points.append((x, y))

        points_str = " ".join([f"{x:.2f},{y:.2f}" for x, y in points])
        color = color_manager.get_next_color()
        return [f'    <polygon class="flag-component" points="{points_str}" fill="{color}"/>']

    def describe(self) -> str:
        return f"star at ({self.center_x},{self.center_y}) radius {self.radius} angle {self.angle}°"

    def validate(self, dimensions: FlagDimensions) -> Optional[str]:
        if self.radius < 1:
            return "Star radius must be >= 1"
        if not (0 <= self.center_x < dimensions.width and 0 <= self.center_y < dimensions.height):
            return "Star center point must be within SVG bounds"
        return None


@dataclass
class Moon(FlagElement):
    """Crescent moon element"""
    moon_x: float
    moon_y: float
    moon_radius: float
    mask_dx: float
    mask_dy: float
    mask_radius: float
    element_id: int = field(default=0)

    def render(self, color_manager: ColorManager) -> List[str]:
        mask_id = f"moon-mask-{self.element_id}"
        mask_center_x = self.moon_x + self.mask_dx
        mask_center_y = self.moon_y + self.mask_dy

        mask_def = f'''    <defs>
        <mask id="{mask_id}">
            <circle cx="{self.moon_x}" cy="{self.moon_y}" r="{self.moon_radius}" fill="white"/>
            <circle cx="{mask_center_x}" cy="{mask_center_y}" r="{self.mask_radius}" fill="black"/>
        </mask>
    </defs>'''

        color = color_manager.get_next_color()
        moon_circle = f'    <circle class="flag-component" cx="{self.moon_x}" cy="{self.moon_y}" '
        moon_circle += f'r="{self.moon_radius}" fill="{color}" mask="url(#{mask_id})"/>'

        return [mask_def, moon_circle]

    def describe(self) -> str:
        return (f"moon at ({self.moon_x},{self.moon_y}) radius {self.moon_radius} "
                f"mask ({self.mask_dx},{self.mask_dy}) mask_radius {self.mask_radius}")

    def validate(self, dimensions: FlagDimensions) -> Optional[str]:
        if self.moon_radius < 1:
            return "Moon radius must be >= 1"
        if self.mask_radius < 1:
            return "Moon mask radius must be >= 1"
        if not (0 <= self.moon_x < dimensions.width and 0 <= self.moon_y < dimensions.height):
            return "Moon center point must be within SVG bounds"
        return None


@dataclass
class Rect(FlagElement):
    """Simple rectangle element"""
    x: int
    y: int
    width: int
    height: int

    def render(self, color_manager: ColorManager) -> List[str]:
        color = color_manager.get_next_color()
        return [
            f'    <rect class="flag-component" x="{self.x}" y="{self.y}" '
            f'width="{self.width}" height="{self.height}" fill="{color}"/>'
        ]

    def describe(self) -> str:
        return f"rect {self.width}x{self.height} at ({self.x},{self.y})"

    def validate(self, dimensions: FlagDimensions) -> Optional[str]:
        if self.width < 1 or self.height < 1:
            return "Rectangle width and height must be >= 1"
        if not (0 <= self.x < dimensions.width and 0 <= self.y < dimensions.height):
            return "Rectangle origin must be within SVG bounds"
        if self.x + self.width > dimensions.width or self.y + self.height > dimensions.height:
            return "Rectangle exceeds flag bounds"
        return None


@dataclass
class Triangle(FlagElement):
    """Triangle element defined by three points"""
    x1: int
    y1: int
    x2: int
    y2: int
    x3: int
    y3: int

    def render(self, color_manager: ColorManager) -> List[str]:
        color = color_manager.get_next_color()
        points = f"{self.x1},{self.y1} {self.x2},{self.y2} {self.x3},{self.y3}"
        return [f'    <polygon class="flag-component" points="{points}" fill="{color}"/>']

    def describe(self) -> str:
        return f"triangle ({self.x1},{self.y1})-({self.x2},{self.y2})-({self.x3},{self.y3})"

    def validate(self, dimensions: FlagDimensions) -> Optional[str]:
        for x, y in [(self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)]:
            if not (0 <= x <= dimensions.width and 0 <= y <= dimensions.height):
                return "Triangle points must be within SVG bounds"
        return None


class ElementCollection:
    """Manages multiple elements of the same type"""

    def __init__(self, element_type: str, elements: List[FlagElement]):
        self.element_type = element_type
        self.elements = elements

    def render(self, color_manager: ColorManager) -> List[str]:
        result = []
        for element in self.elements:
            result.extend(element.render(color_manager))
        return result

    def describe(self) -> str:
        if len(self.elements) == 1:
            return self.elements[0].describe()
        return f"{len(self.elements)} {self.element_type}s"

    def validate(self, dimensions: FlagDimensions) -> List[str]:
        errors = []
        for i, element in enumerate(self.elements):
            error = element.validate(dimensions)
            if error:
                errors.append(f"{self.element_type.capitalize()} {i+1}: {error}")
        return errors


class FlagGenerator:
    """Main flag generator class"""

    # Element rendering order (background first, then overlays)
    RENDER_ORDER = [
        'background',
        'bars',
        'sides',
        'canton',
        'crosses',
        'circles',
        'rects',
        'triangles',
        'stars',
        'moons'
    ]

    def __init__(self, dimensions: FlagDimensions, colors: Optional[List[str]] = None):
        self.dimensions = dimensions
        self.color_manager = ColorManager(colors)
        self.elements: Dict[str, Any] = {}
        self.descriptions: List[str] = []

    def add_background(self):
        """Add a solid background"""
        self.elements['background'] = Background(self.dimensions)
        self.descriptions.append("background")

    def add_bars(self, orientation: str, count: int, widths: Optional[List[int]] = None):
        """Add horizontal or vertical bars"""
        bars = Bars(self.dimensions, orientation, count, widths)
        self.elements['bars'] = bars
        self.descriptions.append(bars.describe())

    def add_canton(self, width: int, height: int):
        """Add a canton (top-left rectangular overlay)"""
        canton = Canton(width, height)
        self.elements['canton'] = canton
        self.descriptions.append(canton.describe())

    def add_sides(self, sides_data: List[Tuple[int, int, str]]):
        """Add one or more side features"""
        sides = [Side(self.dimensions, width, right_edge, pos) for width, right_edge, pos in sides_data]
        self.elements['sides'] = ElementCollection('side', sides)
        self.descriptions.append(self.elements['sides'].describe())

    def add_crosses(self, crosses_data: List[Tuple[int, int, int]]):
        """Add one or more crosses"""
        crosses = [Cross(self.dimensions, x, y, w) for x, y, w in crosses_data]
        self.elements['crosses'] = ElementCollection('cross', crosses)
        self.descriptions.append(self.elements['crosses'].describe())

    def add_circles(self, circles_data: List[Tuple[int, int, int]]):
        """Add one or more circles"""
        circles = [Circle(x, y, r) for x, y, r in circles_data]
        self.elements['circles'] = ElementCollection('circle', circles)
        self.descriptions.append(self.elements['circles'].describe())

    def add_rects(self, rects_data: List[Tuple[int, int, int, int]]):
        """Add one or more rectangles"""
        rects = [Rect(x, y, w, h) for x, y, w, h in rects_data]
        self.elements['rects'] = ElementCollection('rect', rects)
        self.descriptions.append(self.elements['rects'].describe())

    def add_triangles(self, triangles_data: List[Tuple[int, int, int, int, int, int]]):
        """Add one or more triangles"""
        triangles = [Triangle(x1, y1, x2, y2, x3, y3) for x1, y1, x2, y2, x3, y3 in triangles_data]
        self.elements['triangles'] = ElementCollection('triangle', triangles)
        self.descriptions.append(self.elements['triangles'].describe())

    def add_stars(self, stars_data: List[Tuple[float, float, float, float]]):
        """Add one or more stars"""
        stars = [Star(x, y, r, a) for x, y, r, a in stars_data]
        self.elements['stars'] = ElementCollection('star', stars)
        self.descriptions.append(self.elements['stars'].describe())

    def add_moons(self, moons_data: List[Tuple[float, float, float, float, float, float]]):
        """Add one or more moons"""
        moons = [Moon(x, y, r, dx, dy, mr, i)
                 for i, (x, y, r, dx, dy, mr) in enumerate(moons_data)]
        self.elements['moons'] = ElementCollection('moon', moons)
        self.descriptions.append(self.elements['moons'].describe())

    def validate(self) -> List[str]:
        """Validate all elements"""
        errors = []
        warnings = []

        for element_type, element in self.elements.items():
            if isinstance(element, FlagElement):
                result = element.validate(self.dimensions)
                if result:
                    if result.startswith("Warning:"):
                        warnings.append(result)
                    else:
                        errors.append(result)
            elif isinstance(element, ElementCollection):
                results = element.validate(self.dimensions)
                for result in results:
                    if result.startswith("Warning:"):
                        warnings.append(result)
                    else:
                        errors.append(result)

        return errors, warnings

    def generate_svg(self) -> str:
        """Generate the complete SVG content"""
        svg_header = f'<svg viewBox="0 0 {self.dimensions.width} {self.dimensions.height}" xmlns="http://www.w3.org/2000/svg">'
        svg_footer = '</svg>'

        elements = []

        # Render elements in the correct order
        for element_type in self.RENDER_ORDER:
            if element_type in self.elements:
                element = self.elements[element_type]
                if isinstance(element, FlagElement):
                    elements.extend(element.render(self.color_manager))
                elif isinstance(element, ElementCollection):
                    elements.extend(element.render(self.color_manager))

        return '\n'.join([svg_header] + elements + [svg_footer])

    def get_description(self) -> str:
        """Get a human-readable description of the flag"""
        return " + ".join(self.descriptions)


def get_country_code(country_name: str) -> Optional[str]:
    """Convert country name to ISO 2-letter code"""
    return COUNTRY_CODES.get(country_name.lower())


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        description='Generate SVG flag templates',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Examples:
  %(prog)s laos -x 18 -y 15              # 18x15 solid rectangle
  %(prog)s france -x 18 -y 15 --vertical 3       # 18x15 with 3 equal vertical bars
  %(prog)s germany -x 21 -y 14 --horizontal 3    # 21x14 with 3 equal horizontal bars
  %(prog)s colombia -x 30 -y 18 --horizontal "9,6,3" -c yellow blue red  # Colombia with custom heights
  %(prog)s custom -x 24 -y 16 --vertical "8,6,10" -c red white blue  # Custom vertical bar widths
  %(prog)s italy -x 30 -y 20 --vertical 3 -c green white red  # Italian flag colors
  %(prog)s usa -x 30 -y 20 --horizontal 13 --canton 12 7 --star 6 3 2 0 -c red white blue white  # US-style flag
  %(prog)s malaysia -x 28 -y 14 --horizontal 14 --canton 14 7 -c red white blue  # Malaysia-style flag
  %(prog)s england -x 30 -y 20 --cross 15 10 6 -c white red  # White background, red cross
  %(prog)s japan -x 30 -y 20 --circle 15 10 8 -c white red   # White background, red circle
  %(prog)s turkey -x 30 -y 20 --moon 15 10 6 3 -1 -c red white  # Red background, white crescent
  %(prog)s madagascar -x 30 -y 20 --side 10 20 left -c white red green  # Left bar (Madagascar style)
  %(prog)s sudan -x 30 -y 20 --side 15 0 left -c blue yellow black red  # Left triangle (Sudan style)
  %(prog)s kuwait -x 30 -y 20 --side 8 10 left -c green white red black  # Left trapezoid (Kuwait style)
  %(prog)s complex -x 40 -y 30 --star 10 10 4 0 --moon 30 20 5 2 -2 -c navy white yellow  # Star and moon
  %(prog)s rectdemo -x 20 -y 15 --rect 5 5 10 5 -c white red  # Add a rectangle
  %(prog)s tridemo -x 20 -y 15 --triangle 0 0 10 15 20 0 -c blue white yellow  # Add a triangle
        '''
    )

    parser.add_argument('country', help='Country name')
    parser.add_argument('-x', '--width', type=int, required=True, help='SVG width in units')
    parser.add_argument('-y', '--height', type=int, required=True, help='SVG height in units')
    parser.add_argument('-v', '--vertical', type=str, metavar='BARS_OR_WIDTHS',
                       help='Create vertical bars. Use single number for equal bars (e.g., --vertical 3) '
                            'or comma-separated numbers for custom widths (e.g., --vertical "10,8,12")')
    parser.add_argument('--horizontal', type=str, metavar='BARS_OR_HEIGHTS',
                       help='Create horizontal bars. Use single number for equal bars (e.g., --horizontal 3) '
                            'or comma-separated numbers for custom heights (e.g., --horizontal "8,12,8")')
    parser.add_argument('--canton', nargs=2, type=int, metavar=('WIDTH', 'HEIGHT'),
                       help='Create a canton (top-left rectangle overlay) with specified width and height')
    parser.add_argument('--side', action='append', nargs=3,
                       metavar=('WIDTH', 'RIGHT_EDGE_LENGTH', 'POSITION'),
                       help='Create a side feature (width right_edge_length position). '
                            'right_edge_length=height creates a bar, =0 creates a triangle, '
                            'other values create a trapezoid. position must be "left" or "right". '
                            'Can be used multiple times.')
    parser.add_argument('--cross', action='append', nargs=3, type=int,
                       metavar=('CENTER_X', 'CENTER_Y', 'WIDTH'),
                       help='Create a cross (center_x center_y width). Can be used multiple times.')
    parser.add_argument('--circle', action='append', nargs=3, type=int,
                       metavar=('CENTER_X', 'CENTER_Y', 'RADIUS'),
                       help='Create a circle (center_x center_y radius). Can be used multiple times.')
    parser.add_argument('--star', action='append', nargs=4, type=float,
                       metavar=('CENTER_X', 'CENTER_Y', 'RADIUS', 'ANGLE'),
                       help='Create a 5-pointed star (center_x center_y radius angle_degrees). Can be used multiple times.')
    parser.add_argument('--moon', action='append', nargs=6, type=float,
                       metavar=('CENTER_X', 'CENTER_Y', 'RADIUS', 'MASK_DX', 'MASK_DY', 'MASK_RADIUS'),
                       help='Create a crescent moon (center_x center_y radius mask_dx mask_dy mask_radius). Can be used multiple times.')
    parser.add_argument('--rect', action='append', nargs=4, type=int,
                       metavar=('X', 'Y', 'WIDTH', 'HEIGHT'),
                       help='Create a rectangle (x y width height). Can be used multiple times.')
    parser.add_argument('--triangle', action='append', nargs=6, type=int,
                       metavar=('X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3'),
                       help='Create a triangle using three points. Can be used multiple times.')
    parser.add_argument('-c', '--colors', nargs='+', metavar='COLOR',
                       help='Specify colors (hex codes, 3/6 digits, or named colors)')
    parser.add_argument('-o', '--output', help='Output directory (default: ./public/flags/)')

    return parser


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()

    # Validate mutually exclusive bar orientations
    if args.vertical and args.horizontal:
        print("Error: Cannot specify both --vertical and --horizontal", file=sys.stderr)
        return 1

    # Parse bar arguments
    vertical_count = None
    vertical_widths = None
    horizontal_count = None
    horizontal_heights = None

    if args.vertical:
        try:
            # Handle comma-separated values or single value
            if ',' in args.vertical:
                vertical_values = [int(x.strip()) for x in args.vertical.split(',')]
                vertical_count = len(vertical_values)
                vertical_widths = vertical_values
            else:
                vertical_count = int(args.vertical)
        except ValueError:
            print("Error: All vertical bar values must be integers", file=sys.stderr)
            return 1

    if args.horizontal:
        try:
            # Handle comma-separated values or single value
            if ',' in args.horizontal:
                horizontal_values = [int(x.strip()) for x in args.horizontal.split(',')]
                horizontal_count = len(horizontal_values)
                horizontal_heights = horizontal_values
            else:
                horizontal_count = int(args.horizontal)
        except ValueError:
            print("Error: All horizontal bar values must be integers", file=sys.stderr)
            return 1

    # Parse colors if provided
    colors = None
    if args.colors:
        try:
            colors = ColorManager.parse_colors(args.colors)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    # Parse side arguments if provided
    sides_data = []
    if args.side:
        for side_args in args.side:
            try:
                width = float(side_args[0])
                right_edge_length = float(side_args[1])
                position = side_args[2].lower()

                if position not in ['left', 'right']:
                    print(f"Error: Side position must be 'left' or 'right', got '{position}'", file=sys.stderr)
                    return 1

                sides_data.append((width, right_edge_length, position))
            except ValueError as e:
                print(f"Error: Invalid side arguments: {e}", file=sys.stderr)
                return 1

    # Parse rectangle arguments if provided
    rects_data = []
    if args.rect:
        for rect_args in args.rect:
            rects_data.append(tuple(rect_args))

    # Parse triangle arguments if provided
    triangles_data = []
    if args.triangle:
        for tri_args in args.triangle:
            triangles_data.append(tuple(tri_args))

    # Get country code
    country_code = get_country_code(args.country)
    if not country_code:
        print(f"Error: Country '{args.country}' not found. Please check the spelling.", file=sys.stderr)
        return 1

    # Create flag generator
    dimensions = FlagDimensions(args.width, args.height)
    generator = FlagGenerator(dimensions, colors)

    # Check if we need a background (when using overlays)
    needs_background = bool(
        args.cross or args.circle or args.star or args.moon or
        rects_data or triangles_data or sides_data or args.canton
    )

    # Add elements
    if args.vertical:
        generator.add_bars('vertical', vertical_count, vertical_widths)
    elif args.horizontal:
        generator.add_bars('horizontal', horizontal_count, horizontal_heights)
    elif needs_background:
        generator.add_background()
    else:
        # Default solid rectangle
        generator.add_background()
        generator.descriptions[-1] = "solid rectangle"

    # Add side features
    if sides_data:
        generator.add_sides(sides_data)

    if rects_data:
        generator.add_rects(rects_data)

    if triangles_data:
        generator.add_triangles(triangles_data)

    # Add canton
    if args.canton:
        generator.add_canton(args.canton[0], args.canton[1])

    # Add overlay elements
    if args.cross:
        generator.add_crosses(args.cross)

    if args.circle:
        generator.add_circles(args.circle)

    if args.star:
        generator.add_stars(args.star)

    if args.moon:
        generator.add_moons(args.moon)

    # Validate all elements
    errors, warnings = generator.validate()

    # Print warnings
    for warning in warnings:
        print(warning)

    # Exit on errors
    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)
        return 1

    # Generate SVG
    svg_content = generator.generate_svg()

    # Create output directory and write file
    output_dir = args.output or './public/flags/'
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{country_code}.svg"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w') as f:
        f.write(svg_content)

    # Print summary
    print(f"Created: {filepath}")
    print(f"Template: {args.width}x{args.height} {generator.get_description()}")


if __name__ == '__main__':
    sys.exit(main() or 0)