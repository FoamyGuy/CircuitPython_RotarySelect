# SPDX-FileCopyrightText: Copyright (c) 2024 Tim C
#
# SPDX-License-Identifier: MIT
"""
Minimal example that demonstrates RotarySelect widget.
Made to run on any device with built-in display at least 240px large.
Automatic selection advancement so as not to need any other hardware
integration or requirements.
"""

import time

import board
import displayio
import terminalio
import vectorio
from adafruit_display_text.bitmap_label import Label

from rotaryselect import RotarySelect

last_position = None

SCREEN_RADIUS = 120

main_group = displayio.Group()

board.DISPLAY.root_group = main_group

items_list = []

items_list = [
    "vectorio.Circle,0xff00ff,17,Strawberry",
    "vectorio.Circle,0xffff00,17,Pineapple",
    "vectorio.Circle,0x00ffff,17,Apple",
    "vectorio.Circle,0x00ff00,17,Pear",
    "vectorio.Circle,0xff0000,17,Cherry",
    "vectorio.Circle,0x0000ff,17,Blueberry",
    "vectorio.Circle,0xff9900,17,Orange",
]

selected_lbl = Label(terminalio.FONT, text="", scale=2)
selected_lbl.anchor_point = (0.5, 0.5)
selected_lbl.anchored_position = (120, 120)

# Outline Style Indicator
rotary_select = RotarySelect(
    120,
    120,
    94,
    items_list,
    indicator_r=45 // 2,
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
#     indicator_type=RotarySelect.INDICATOR_TYPE_DOT,
#     indicator_offset=26,
#     label=selected_lbl,
# )


main_group.append(rotary_select)
main_group.append(selected_lbl)

while True:
    rotary_select.move_selection_up()
    time.sleep(1)
