# from ableton_set_builder import AbletonSetBuilder, ColorsDir
import json
import argparse
import os

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

cwd = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input")
parser.add_argument("-g", "--output-group", default='USB', choices=['USB', 'CRD', 'MOD', 'A', 'B', 'C'])
parser.add_argument("-v", "--verbose", action="count", default=0)
args = parser.parse_args()

with open(args.input) as f:
    snap = json.load(f)

tracks = []
output_group = args.output_group
outs = snap["ae_data"]["io"]["out"][output_group]
for out in outs:
    dst_grp = outs[out]["grp"]
    if dst_grp == "OFF":
        continue

    dst_in = outs[out]["in"]
    if not str(dst_grp) in snap['ae_data']['io']['in']:
        continue
    src = snap['ae_data']['io']['in'][str(dst_grp)][str(dst_in)]
    input = out
    src_color = int(src["col"])
    ableton_color_name = colors[src_color]
    if src['mode'] == "ST":
        if int(out) % 2:
            continue
        prev = (int(out) - 1)
        prev_dst_grp = outs[str(prev)]["grp"]
        if prev_dst_grp != "OFF":
            prev_dst_in = outs[str(prev)]["in"]
            prev_src = snap["ae_data"]["io"]["in"][str(prev_dst_grp)][str(prev_dst_in)]
            if src != prev_src:
                continue
            input = f"{int(out) - 1}/{out}"
    tracks.append(dict(input=input, name=src["name"], color=ableton_color_name))

if args.verbose:
    print(json.dumps(tracks, indent=2))

if not tracks:
    exit()

builder = AbletonSetBuilder(f'{cwd}/templates/live-12.xml')

for track in tracks:
    builder.create_audio_track(track['name'], track['color'], track['input'], track['input'], "in", 12)

builder.build_als(f'/tmp/{args.input}.als')

os.system(f"open '/Applications/Ableton Live 12 Suite.app/' '/tmp/{args.input}.als'")
