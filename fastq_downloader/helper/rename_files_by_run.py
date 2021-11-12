from pathlib import Path
import shutil


def if_paired(orig_names: list):
    paired_or_not = ["_" in name for name in orig_names]
    if len(set(paired_or_not)) != 1:
        ValueError("Not all files are paired or unpaired reads")
    if all(paired_or_not):
        return True
    else:
        return False


def write_filename_to_dict(subdict: dict):
    ascp_dict = subdict["ascp"]
    desp = subdict["desp"]
    link_list = ascp_dict.keys()
    orig_names = [Path(link).name for link in link_list]
    paired = if_paired(orig_names)
    if paired:
        srrlist = list([name.split("_")[0] for name in orig_names])
    else:
        srrlist = list([name.split(".")[0] for name in orig_names])
    count_run = len(set(srrlist))
    srr2run_map = dict(zip(set(srrlist), range(1, count_run + 1)))
    new_name = [
        orig_name.replace(srr, f"{desp}_run{srr2run_map[srr]}")
        for orig_name, srr in zip(orig_names, srrlist)
    ]
    new_name = [name.replace("_1", "_R1") for name in new_name]
    new_name = [name.replace("_2", "_R2") for name in new_name]
    for ascp_link, orig_name, new_name in zip(link_list, orig_names, new_name):
        ascp_dict[ascp_link]["orig_name"] = orig_name
        ascp_dict[ascp_link]["new_name"] = new_name
    subdict["ascp"] = ascp_dict
    subdict["paired"] = paired
    return subdict


def actual_rename(info_dict: dict, out: str):
    ascp_dict = info_dict["ascp"]
    orig_name_list = [x["orig_name"] for x in ascp_dict.values()]
    new_name_list = [x["new_name"] for x in ascp_dict.values()]
    for orig_name, new_name in zip(orig_name_list, new_name_list):
        orig_path = Path(out, orig_name)
        new_path = Path(out, new_name)
        shutil.move(orig_path, new_path)
