#!/usr/bin/env python3
import httpx
import json
import re
from bs4 import BeautifulSoup as bs
from lxml import etree as ET


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
    json_url = f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={srr}&result=read_run&format=json"
    json_text = httpx.get(json_url).text
    srr_info = json.loads(json_text)

    ftp_links = srr_info[0]["fastq_ftp"].split(";")
    fastq_md5 = srr_info[0]["fastq_md5"].split(";")
    ascp_links = [
        link.replace("ftp.sra.ebi.ac.uk/", "era-fasp@fasp.sra.ebi.ac.uk:")
        for link in ftp_links
    ]

    return zip(ascp_links, fastq_md5)


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
