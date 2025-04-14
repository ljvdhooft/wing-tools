# from ableton_set_builder import AbletonSetBuilder, ColorsDir
from enum import Enum
from WingSnap import WingSnap
import json

class ColorsDir(Enum):
    salmon = 0
    frank_orange = 1
    dirty_gold = 2
    lemonade = 3
    lime = 4
    highlighter_green = 5
    bianchi = 6
    turquiose = 7
    sky_blue = 8
    sapphire = 9
    periwinkle = 10
    orchid = 11
    magenta = 12
    white = 13
    fire_hydrant_red = 14
    tangerine = 15
    sand = 16
    sunshine_yellow = 17
    terminal_green = 18
    forest = 19
    tiffany_blue = 20
    cyan = 21
    cerulean = 22
    united_nations_blue = 23
    amethyst = 24
    iris = 25
    flamingo = 26
    aluminium = 27
    terracotta = 28
    light_salmon = 29
    whiskey = 30
    canary = 31
    primrose = 32
    wild_willow = 33
    dark_sea_green = 34
    honeydew = 35
    pale_turquiose = 36
    light_periwinkle = 37
    fog = 38
    dull_lavender = 39
    whisper = 40
    silver_chalice = 41
    dusty_pink = 42
    barley_corn = 43
    pale_oyster = 44
    dark_khaki = 45
    pistachio = 46
    dollar_bill = 47
    neptune = 48
    nepal = 49
    polo_blue = 50
    vista_blue = 51
    amethyst_smoke = 52
    lilac = 53
    turkish_rose = 54
    steel = 55
    medium_carmine = 56
    red_orche = 57
    coffee = 58
    durian_yellow = 59
    pomelo_green = 60
    apple = 61
    aquamarine = 62
    sea_blue = 63
    cosmic_cobalt = 64
    dark_sapphire = 65
    plump_purple = 66
    purpureus = 67
    fuchsia_rose = 68
    eclipse = 69

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