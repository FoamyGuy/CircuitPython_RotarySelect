# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 Tim C for foamyguy
#
# SPDX-License-Identifier: MIT
"""
`rotaryselect`
================================================================================

A circular rotary selection widget


* Author(s): Tim C

Implementation Notes
--------------------

**Hardware:**

  "* `M5 Dial <https://www.adafruit.com/product/5966>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

import math
import os

import adafruit_imageload
import vectorio
from adafruit_display_shapes.circle import Circle

# imports
from displayio import Group, Palette, TileGrid
from micropython import const

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/foamyguy/CircuitPython_RotarySelect.git"


class RotarySelect(Group):
    INDICATOR_TYPE_OUTLINE = const(0)
    INDICATOR_TYPE_DOT = const(1)

    CONFIG_ICONFILE = const(0)
    CONFIG_CIRCLE_COLOR = const(1)
    CONFIG_CIRCLE_RADIUS = const(2)
    CONFIG_CIRCLE_LABEL = const(3)

    CONFIG_ICON_LABEL = const(1)

    def __init__(  # noqa: PLR0913, PLR0915, Too many arguments, Too many statements
        self,
        x,
        y,
        radius,
        items,
        indicator_color=0x0000FF,
        indicator_r=40 // 2,
        indicator_stroke=4,
        indicator_type=INDICATOR_TYPE_OUTLINE,
        indicator_offset=0,
        icon_transparency_index=None,
        label=None,
        **kwargs,
    ):
        # noqa:
        """

        :param x: X pixel coordinate location of the center of the RotarySelect
        :param y: Y pixel coordinate location of the center of the RotarySelect
        :param radius: Distance away from center point to draw the icons or circles
        :param items: List of item configuration values
        :param indicator_color: Hex color for the indicator
        :param indicator_r: Radius of the indicator in pixels
        :param indicator_stroke: Size in pixels of the outline circle
        :param indicator_offset: Offset of the indicator in pixels
        :param indicator_type: The type of indicator to use. Valid values are
            INDICATOR_TYPE_OUTLINE, and INDICATOR_TYPE_DOT
        :param icon_transparency_index: A color index to set to transparent on the icon
            palette(s)
        :param label: Label object that will have its text property updated to show
            the currently selected item label.
        :param kwargs: Any kwargs belonging to displayio.Group
        """
        super().__init__(**kwargs)
        self.points = RotarySelect.points_around_circle(x, y, radius, len(items))
        self.indicator_points = RotarySelect.points_around_circle(
            x, y, radius - indicator_offset, len(items)
        )
        self.items = items
        self.icon_transparency_index = icon_transparency_index
        self.indicator_color = indicator_color
        self.indicator_r = indicator_r
        self.indicator_stroke = indicator_stroke

        self._selected_index = 0
        self.icons = []
        self.icon_palettes = []
        self.label_strings = []
        self.label = label

        for i, point in enumerate(self.points):
            cur_item = items[i]

            if cur_item.startswith("vectorio.Circle"):
                parts = cur_item.split(",")
                if len(parts) < 3:
                    raise ValueError(
                        "Circle item config must contain at least 3 values. "
                        "example: 'vectorio.Circle,0x00ff00,17'"
                    )

                palette = Palette(1)
                palette[0] = int(parts[1], 16)
                self.icon_palettes.append(palette)
                circle = vectorio.Circle(
                    pixel_shader=palette, radius=int(parts[2]), x=int(point[0]), y=int(point[1])
                )
                self.icons.append(circle)
                self.append(circle)
                if len(parts) >= 4:
                    self.label_strings.append(parts[3])
                else:
                    self.label_strings.append("")

            else:  # assume icon image file
                # load item icon
                parts = cur_item.split(",")
                image, palette = adafruit_imageload.load(parts[RotarySelect.CONFIG_ICONFILE])
                self.icon_palettes.append(palette)
                # print(f"p[0]: {palette.}")
                # palette.make_transparent(0xffffff)
                if icon_transparency_index is not None:
                    palette.make_transparent(icon_transparency_index)

                tile_grid = TileGrid(image, pixel_shader=palette)
                self.icons.append((image, tile_grid))
                print(f"x: {int(point[0])}, y: {int(point[1])}")
                tile_grid.x = int(point[0]) - tile_grid.tile_width // 2
                tile_grid.y = int(point[1]) - tile_grid.tile_height // 2
                self.append(tile_grid)

                if len(parts) >= 2:
                    self.label_strings.append(parts[1])
                else:
                    self.label_strings.append("")

        if indicator_type == RotarySelect.INDICATOR_TYPE_OUTLINE:
            self.indicator = Circle(
                0,
                0,
                self.indicator_r,
                fill=None,
                outline=self.indicator_color,
                stroke=self.indicator_stroke,
            )
        elif indicator_type == RotarySelect.INDICATOR_TYPE_DOT:
            self.indicator = Circle(0, 0, self.indicator_r, fill=self.indicator_color)
        else:
            raise ValueError("Invalid indicator type")

        self.append(self.indicator)
        self._update_indicator()

    @staticmethod
    def points_around_circle(circle_x, circle_y, r, point_count):
        points = []
        for i in range(point_count):
            x = circle_x + r * math.cos(2 * math.pi * i / point_count)
            y = circle_y + r * math.sin(2 * math.pi * i / point_count)
            points.append((x, y))
        return points

    def _update_indicator(self):
        self.indicator.x = (
            int(self.indicator_points[self._selected_index][0]) - self.indicator_r - 1
        )
        self.indicator.y = (
            int(self.indicator_points[self._selected_index][1]) - self.indicator_r - 1
        )
        if self.label is not None:
            self.label.text = self.label_strings[self._selected_index]

    @property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, new_index):
        self._selected_index = new_index
        self._update_indicator()

    def move_selection_down(self):
        """
        Move the selection indicator down 1 space
        :return: None
        """
        self.selected_index = (self.selected_index - 1) % len(self.items)

    def move_selection_up(self):
        """
        Move the selection indicator up 1 space
        :return: None
        """
        self.selected_index = (self.selected_index + 1) % len(self.items)
