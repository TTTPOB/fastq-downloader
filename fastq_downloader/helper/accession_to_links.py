#!/usr/bin/env python3
import httpx
import json
import re
from bs4 import BeautifulSoup as bs
from lxml import etree as ET
from pathlib import Path
import re


def srx2srr(srx: str):
    srx_link = f"https://www.ncbi.nlm.nih.gov/sra/{srx}[accn]?report=FullXml"
    srx_page = bs(httpx.get(srx_link).text, "html.parser")

    srx_xml = srx_page.select("#ResultView")
    srx_xml = srx_xml[0].text
    # ignore invalid characters in xml by using "recover"
    # I don't know how to report this error to ncbi but
    # SRX764940 has invalid characters in xml
    parser = ET.XMLParser(recover=True)
    srx_xml = ET.XML(srx_xml, parser=parser)

    srr_list = srx_xml.findall(f".//*RUN")
    srr_list = [srr.attrib["accession"] for srr in srr_list]

    return srr_list


def srr2link_md5(srr: str) -> zip:
    """
    using ebi json query api to get the download link for a srr
    """
    json_url = f"https://www.ebi.ac.uk/ena/portal/api/filereport"
    json_fields = [
        "library_layout",
        "run_alias",
        "fastq_bytes",
        "fastq_md5",
        "fastq_aspera",
    ]
    data = {
        "accession": srr,
        "result": "read_run",
        "format": "json",
        "fields": ",".join(json_fields),
    }
    json_text = httpx.get(json_url, params=data).text
    srr_info = json.loads(json_text)[0]
    library_layout = srr_info["library_layout"]
    md5list = srr_info["fastq_md5"].split(";")
    ascp_links = srr_info["fastq_aspera"].split(";")

    # filter out invalid links, which means not matched with library_layout
    valid_links = []
    valid_md5 = []
    for md5, ascp_link in zip(md5list, ascp_links):
        if library_layout == "PAIRED":
            if ascp_link.endswith("_1.fastq.gz") or ascp_link.endswith("_2.fastq.gz"):
                valid_links.append(ascp_link)
                valid_md5.append(md5)
        elif library_layout == "SINGLE":
            if ascp_link.endswith(".fastq.gz"):
                valid_links.append(ascp_link)
                valid_md5.append(md5)
        else:
            raise ValueError(f"library_layout {library_layout} is not supported")

    valid_links = [f"era-fasq@{link}" for link in valid_links]

    return zip(valid_links, valid_md5)


def gsm2srx(gsm: str):
    gsm_url = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gsm}&targ=self&form=xml&view=quick"

    gsm_xml = httpx.get(gsm_url).content
    gsm_xml = ET.fromstring(gsm_xml)
    namespace = gsm_xml.tag.split("}")[0] + "}"

    srx_list = gsm_xml.findall(f"{namespace}Sample/{namespace}Relation[@type='SRA']")
    srx_list = [srx.attrib["target"] for srx in srx_list]
    srx_list = [re.search("SRX.*$", srx).group(0) for srx in srx_list]

    return srx_list


def ascp_links_list2dict(ascp_links: list):
    ascp_dict = {}
    for link, md5 in ascp_links:
        ascp_dict[link] = {"md5": md5}
    return ascp_dict


def srx2link_md5(srx: str):
    """
    first get srx related srr, then get related links
    """
    srr_list = srx2srr(srx)
    ascp_links = []
    for srr in srr_list:
        ascp_links += srr2link_md5(srr)
    ascp_dict = ascp_links_list2dict(ascp_links)
    return ascp_dict


def gsm2link_md5(gsm: str):
    """
    first get gsm related srx acession, and then get srx related srr, then get related links
    """
    srx_list = gsm2srx(gsm)
    if len(srx_list) != 1:
        ValueError(f"gsm {gsm} has {len(srx_list)} srx, excepted 1")
    srx = srx_list[0]
    ascp_dict = srx2link_md5(srx)
    return ascp_dict


if __name__ == "__main__":
    t1 = srx2link_md5("SRX764940")
    print(t1)
