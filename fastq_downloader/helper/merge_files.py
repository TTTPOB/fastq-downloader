import shutil
from pathlib import Path


def merge_files(subdict, out):
    ascp_dict = subdict["ascp"]
    desp = subdict["desp"]
    if subdict["paired"]:
        merged_file_name = {
            "R1": f"{desp}_R1.fastq.gz",
            "R2": f"{desp}_R2.fastq.gz",
        }
        separated_files = [x["new_name"] for x in ascp_dict.values()]
        separated_files = {
            "R1": [Path(out, x) for x in separated_files if "R1" in x],
            "R1": [Path(out, x) for x in separated_files if "R2" in x],
        }
        for mate in ["R1", "R2"]:
            if len(separated_files[mate]) == 1:
                shutil.copy(separated_files[mate][0], Path(out, merged_file_name[mate]))
            with open(Path(out, merged_file_name[mate]), "wb") as outfile:
                for f in separated_files[mate]:
                    shutil.copyfileobj(open(f, "rb"), outfile)

    else:
        merged_file_name = f"{desp}.fastq.gz"
        separated_files = [x["new_name"] for x in ascp_dict.values()]
        separated_files = [Path(out, x) for x in separated_files]
        if len(separated_files) == 1:
            shutil.copy(separated_files[0], Path(out, merged_file_name))
        with open(Path(out, merged_file_name), "wb") as outfile:
            for f in separated_files:
                shutil.copyfileobj(open(f, "rb"), outfile)
