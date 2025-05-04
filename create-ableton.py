# from ableton_set_builder import AbletonSetBuilder, ColorsDir
import json
import argparse

from ableton_set_builder import AbletonSetBuilder

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

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input")
parser.add_argument("-o", "--output")
args = parser.parse_args()

with open(args.input) as f:
    snap = json.load(f)

tracks = []

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
    if src['mode'] == "ST":
        if int(out) % 2:
            continue
        prev = (int(out) - 1)
        prev_dst_grp = usb_outs[str(prev)]["grp"]
        if prev_dst_grp != "OFF":
            prev_dst_in = usb_outs[str(prev)]["in"]
            prev_src = snap["ae_data"]["io"]["in"][str(prev_dst_grp)][str(prev_dst_in)]
            if src != prev_src:
                continue
            input = f"{int(out) - 1}/{out}"
    tracks.append(dict(input=input, name=src["name"], color=ableton_color_name))

builder = AbletonSetBuilder('templates/live-12.xml')

for track in tracks:
    builder.create_audio_track(track['name'], track['color'], track['input'], track['input'], "in", 12)

builder.build_als('output')
