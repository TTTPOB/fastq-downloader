from .accession_to_links import get_link_md5


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
