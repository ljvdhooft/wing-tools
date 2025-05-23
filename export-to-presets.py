import argparse
import json
from datetime import datetime
import os


def export_presets(dir, data, type, io=None):
    os.makedirs(f"{dir}/{type}", exist_ok=True)
    for i in data:
        chn = data[i]

        if "conn" in chn["in"] and chn["in"]["conn"]["grp"] == "OFF":
            continue

        # base preset
        preset = {
            "type": "chpreset.8",
            "creator_fw": "2.0-0-g6617206f:release",
            "creator_sn": "S220800180BV2",
            "creator_model": "ngc-full",
            "creator_version": "SX45-XU2",
            "creator_name": "WING-TOOLS",
            "created": dt,
            "source_channel": i,
            "info_text": chn["name"],
            "scopes_content": " ++++++++++++++",
            "scopes_main": "++++",
            "scopes_send": "++++++++++++++++++++++++",
            "target_fx": [0, 0],
        }

        # append channel data to preset
        preset["ch_data"] = chn

        file_name = f'{type}/{i.zfill(2)} - {chn["name"]}.{type}'
        if 'clink' in chn and chn['clink'] and io:
            ch_grp = chn['in']['conn']['grp']
            ch_in = chn['in']['conn']['in']

            if ch_grp in ["BUS", "MAIN", "MTX"]:
                file_name = f'{type}/{i.zfill(2)}.{type}'
            else:
                io_in = io['in'][str(ch_grp)][str(ch_in)]
                name = io_in['name']
                file_name = f'{type}/{i.zfill(2)} - {name}.{type}'
        file_path = os.path.join(dir, file_name)

        # export the preset
        with open(file_path, "w") as json_file:
            json.dump(preset, json_file, indent=4)
        print(f"{type} : Saved {file_name}")


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input')
parser.add_argument("-o", "--output")
args = parser.parse_args()

dir = args.output
if not dir:
    raise Exception('please define output.')
os.makedirs(dir, exist_ok=True)


with open(args.input) as f:
    snap = json.load(f)

    io = snap['ae_data']['io']
    chs = snap['ae_data']['ch']
    auxes = snap['ae_data']['aux']
    buses = snap['ae_data']['bus']
    mains = snap['ae_data']['main']
    mtxs = snap['ae_data']['mtx']

    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    export_presets(dir, chs, "chn", io)
    export_presets(dir, auxes, "aux", io)
    export_presets(dir, buses, "bus")
    export_presets(dir, mains, "main")
    export_presets(dir, mtxs, "mtx")
