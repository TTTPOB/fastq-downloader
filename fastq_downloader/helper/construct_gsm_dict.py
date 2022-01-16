from .accession_to_links import get_link_md5
import os
import sys
from pathlib import Path
from hashlib import md5
import json


def infotsv_to_dict(tsv_file):
    """
    Converts a tsv file with the following columns:
    acc number, description
    to a dict, with gsmnumber as key
    """
    infodict = {}
    with open(tsv_file, "r") as tsv:
        for line in tsv:
            line = line.strip().split("\t")
            infodict[line[0]] = {"desp": line[1].replace(" ", "_")}
    return infodict


def parse_acc_type(infodict):
    """
    tell if this entry is a gsm accesion or a srx accession
    """
    for acc, info in infodict.items():
        if acc.startswith("SRX"):
            info["type"] = "srx"
        elif acc.startswith("GSM"):
            info["type"] = "gsm"
        else:
            ValueError("I can only eat GSM or SRX acsession number!")
    return infodict


def get_link_md5(infodict):
    for acc, info in infodict.items():
        infodict[acc]["ascp"] = get_link_md5(acc, info["type"])
    return infodict


def breakdown_infotsv(
    info_tsv_path: str, out_dir: str, refresh_acc: bool = False
) -> dict:
    tmp_dir = f"{out_dir}/.tmp"
    if refresh_acc:
        os.remove(Path(tmp_dir))
    infodict = infotsv_to_dict(info_tsv_path)
    infodict = parse_acc_type(infodict)
    Path(tmp_dir).mkdir(exist_ok=True, parents=True)
    for acc, info in infodict.items():
        Path(tmp_dir, "acc_json").mkdir(exist_ok=True, parents=True)
        # check md5 of the file, if not equal, overwrite it
        if Path(tmp_dir, "acc_json", acc + ".json").exists():
            with open(Path(tmp_dir, "acc_json", acc + ".json"), "r") as f:
                print(f"orig file content {f.read()}")
                md5_old = md5(f.read().encode("utf-8")).hexdigest()
                print(f"old md5: {md5_old} for {acc}")
        else:
            md5_old = ""
        # calculate md5 of the json
        json_md5 = md5(json.dumps(info).encode("utf-8")).hexdigest()
        print(f"new md5: {json_md5} for {acc}")
        with open(Path(tmp_dir, "acc_json", f"{acc}.json"), "w") as f:
            # if not equal:
            if md5_old != json_md5:
                # overwrite the file
                f.write(json.dumps(info))
                print(
                    f"overwrite {acc}, file content\n {json.dumps(info)}",
                    file=sys.stderr,
                )
            else:
                # if equal, do nothing
                # but alert the user
                print(f"{acc} is already up to date", file=sys.stderr)
                print(f"old md5 is {md5_old}\nnew md5 is {json_md5}", file=sys.stderr)
                pass
