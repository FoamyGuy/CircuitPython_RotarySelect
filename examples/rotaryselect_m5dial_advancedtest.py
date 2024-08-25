# SPDX-FileCopyrightText: Copyright (c) 2024 Tim C
#
# SPDX-License-Identifier: MIT
"""
Demonstrates the usage of RotarySelect Widget made to run on the M5 Dial device.
"""

import board
import displayio
import rotaryio
import terminalio
import vectorio
from adafruit_display_text.bitmap_label import Label

from rotaryselect import RotarySelect

encoder = rotaryio.IncrementalEncoder(board.ENC_B, board.ENC_A)
last_position = None

SCREEN_RADIUS = 120

main_group = displayio.Group()

bg_palette = displayio.Palette(1)
bg_palette[0] = 0xFFFFFF
bg_circle = vectorio.Circle(pixel_shader=bg_palette, radius=120, x=120, y=120)
# main_group.append(bg_circle)


SELECT_INDICATOR_RADIUS = 40 // 2

board.DISPLAY.root_group = main_group

items_list = []

circles = [
    "vectorio.Circle,0xff00ff,17,Strawberry",
    "vectorio.Circle,0xffff00,17,Pear",
    "vectorio.Circle,0x00ffff,17,Apple",
    "vectorio.Circle,0x00ff00,17,Cherry",
]

things = ["Peach", "Pineapple", "Orange", "Pumpkin", "Banana", "Melon", "Blueberry", "Cranberry"]
for i in range(8):
    items_list.append(f"circle_icons/circle_icon_{i + 1}.png,{things[i]}")

for circle in circles:
    items_list.append(circle)

selected_lbl = Label(terminalio.FONT, text="", scale=2)
selected_lbl.anchor_point = (0.5, 0.5)
selected_lbl.anchored_position = (board.DISPLAY.width // 2, board.DISPLAY.height // 2)

# Outline Style Indicator
rotary_select = RotarySelect(
    120,
    120,
    94,
    items_list,
    indicator_r=44 // 2,
    indicator_color=0xFFFFFF,
    indicator_stroke=3,
    label=selected_lbl,
)


# Dot Style Indicator
# rotary_select = RotarySelect(
#     120,
#     120,
#     94,
#     items_list,
#     indicator_r=8 // 2,
#     indicator_color=0xFFFFFF,
#     indicator_type=RotarySelect.INDICATOR_TYPE_INNER_DOT,
#     indicator_offset=26,
#     label=selected_lbl,
# )


main_group.append(rotary_select)
main_group.append(selected_lbl)

while True:
    position = encoder.position
    if last_position is None or position != last_position:
        delta = position - last_position if last_position is not None else position
        if delta > 0:
            rotary_select.move_selection_up()
        else:
            rotary_select.move_selection_down()
        print(position)

    last_position = position
