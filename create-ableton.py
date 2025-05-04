# from ableton_set_builder import AbletonSetBuilder, ColorsDir
from enum import Enum
from WingSnap import WingSnap
import json

from ableton_set_builder import AbletonSetBuilder, ColorsDir

colors = {
    1: "sapphire",
    2: "sky_blue",
    3: "cosmic_cobalt",
    4: "cyan",
    5: "forest",
    6: "dollar_bill",
    7: "sunshine_yellow",
    8: "tangerine",
    9: "fire_hydrant_red",
    10: "light_salmon",
    11: "flamingo",
    12: "amethyst"
}

file = 'P.FOH 2024.12.snap'
with open(file) as f:
    snap = json.load(f)

usb_outs = snap['ae_data']['io']['out']['USB']
for out in usb_outs:
    dst_grp = usb_outs[out]["grp"]
    if dst_grp == "OFF":
        continue

    dst_in = usb_outs[out]["in"]
    src = snap['ae_data']['io']['in'][str(dst_grp)][str(dst_in)]
    input = out
    src_color = int(src["col"])
    ableton_color_name = colors[src_color]
    ableton_color_id = ColorsDir[ableton_color_name].value
    if src['mode'] == "ST":
        prev = (int(out) - 1)
        prev_dst_grp = usb_outs[str(prev)]["grp"]
        if prev_dst_grp != "OFF":
            prev_dst_in = usb_outs[str(prev)]["in"]
            prev_src = snap["ae_data"]["io"]["in"][str(prev_dst_grp)][str(prev_dst_in)]
            if src == prev_src:
                continue
            input = f'{out}/{int(out) + 1}'
    print(dict(input=input, name=src["name"], color=ableton_color_id))