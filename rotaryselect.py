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

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""
import math
import os

# imports
from displayio import Group, Palette, TileGrid
import vectorio
import adafruit_imageload
from adafruit_display_shapes.circle import Circle

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/foamyguy/CircuitPython_RotarySelect.git"


class RotarySelect(Group):
    def __init__(self, x, y, radius, items,
                 indicator_color=0x0000ff,
                 indicator_r=40 // 2,
                 indicator_stroke=4,
                 icon_transparency_index=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.points = RotarySelect.points_around_circle(x, y, radius, len(items))
        self.items = items
        self.icon_transparency_index = icon_transparency_index
        self.indicator_color = indicator_color
        self.indicator_r = indicator_r
        self.indicator_stroke = indicator_stroke
        self._selected_index = 0
        self.icons = []
        self.icon_palettes = []

        for i, point in enumerate(self.points):
            cur_item = items[i]

            if cur_item.startswith("vectorio.Circle"):
                parts = cur_item.split(",")
                palette = Palette(1)
                palette[0] = int(parts[1], 16)
                self.icon_palettes.append(palette)
                circle = vectorio.Circle(pixel_shader=palette, radius=int(parts[2]), x=int(point[0]), y=int(point[1]))
                self.icons.append(circle)
                self.append(circle)

            else:  # assume icon image file
                # load item icon

                image, palette = adafruit_imageload.load(cur_item)
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

        self.indicator = Circle(0, 0, self.indicator_r, fill=None, outline=self.indicator_color,
                                stroke=self.indicator_stroke)
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
        self.indicator.x = int(self.points[self.selected_index][0]) - self.indicator_r - 1
        self.indicator.y = int(self.points[self.selected_index][1]) - self.indicator_r - 1

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
