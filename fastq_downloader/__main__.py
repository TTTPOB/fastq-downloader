#!/usr/bin/env python3
from .helper.rename_files_by_run import write_filename_to_dict, actual_rename
from .helper.download_and_verify import download_and_verify, invoke_ascp
from .helper.construct_gsm_dict import (
    infotsv_to_dict,
    get_link_md5,
    parse_acc_type,
    breakdown_infotsv as breakdown_infotsv_func,
)
from .helper.merge_files import merge_files
from multiprocessing import Pool
import importlib.resources as pkg_resources
from . import snakemake
import subprocess
from pathlib import Path
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--info", "-in", default="info.tsv", help="iinput information file, must be a tsv"
)
@click.option("--out", "-o", default=".", help="output directory")
@click.option("--rename", "-r", default=True, help="rename the out putted file or not")
@click.option("--privkey", "-k", default=None, help="private key for downloading")
@click.option(
    "--parallel",
    "-p",
    default=4,
    help="number of accession to download, note the granular of parallel is the first level accesion(gsm/srx)",
)
@click.option(
    "--parallel2",
    "-pp",
    default=4,
    help="number of accession to download, note the granular of parallel is the second level accesion(srr)",
)
@click.option(
    "--merge",
    "-m",
    default=True,
    help="merge the downloaded files or not" + "implies rename",
)
def vanilla(info, out, rename, privkey, parallel, merge, parallel2):
    if merge:
        rename = True
    infodict = infotsv_to_dict(info)
    infodict = parse_acc_type(infodict)
    infodict = get_link_md5(infodict)
    for acc, subdict in infodict.items():
        infodict[acc] = write_filename_to_dict(subdict)

    p = Pool(parallel)
    ascp_dict_list = [x["ascp"] for x in infodict.values()]
    p.starmap(
        download_and_verify,
        zip(
            ascp_dict_list,
            [privkey] * len(ascp_dict_list),
            [out] * len(ascp_dict_list),
            [parallel2] * len(ascp_dict_list),
        ),
    )

    if rename:
        for acc, subdict in infodict.items():
            actual_rename(subdict, out)
    if merge:
        for acc, subdict in infodict.items():
            merge_files(subdict, out)


@click.option(
    "--info", "-i", default="info.tsv", help="iinput information file, must be a tsv"
)
@click.option("--out", "-o", default=".", help="output directory")
@click.option(
    "--refresh_acc",
    "-r",
    default=False,
    help="refresh the accession number parse result, \
    note this will trigger the input file timestamp change thus \
    triggers re-evaluation of all snakemake downloads",
)
@click.option(
    "--threads",
    "-t",
    default=4,
    help="threads snamekame using",
)
@click.option(
    "--download-backend",
    "--backend",
    default="ascp",
    help="backend to use for downloading, \
    currently only supports ascp, and wget",
)
@click.option(
    "--snakemake_options",
    "-s",
    default="",
    help="options passed to snakemake",
)
@cli.command()
def smk(info, out, refresh_acc, threads, snakemake_options, download_backend):
    try:
        snakemake_path = (
            subprocess.check_output(["which", "snakemake"]).decode("utf-8").strip()
        )
        if not Path(snakemake_path).exists():
            FileNotFoundError("snakemake not found in path, please install it.")
    except subprocess.CalledProcessError:
        FileNotFoundError("snakemake not found in path, please install it.")
    with pkg_resources.path(snakemake, "Snakefile") as snakefile_path:
        command_list = [
            "snakemake",
            "-s",
            f"{snakefile_path}",
            "-j",
            f"{threads}",
            "--config",
            f"infotsv={info}",
            f"output_dir={out}",
            f"refresh_acc={refresh_acc}",
            f"download_backend={download_backend}",
            "--reason",
            "--keep-going",
            snakemake_options,
        ]
        command_string = " ".join(command_list)
        subprocess.run(command_string, shell=True)


@cli.command()
@click.option(
    "--infotsv", "-i", default="info.tsv", help="iinput information file, must be a tsv"
)
@click.option("--out-dir", "-o", default=".", help="output directory")
@click.option(
    "--refresh-acc",
    "-r",
    default=False,
    help="refresh the accession number parse result",
)
def breakdown_infotsv(infotsv, out_dir, refresh_acc):
    breakdown_infotsv_func(infotsv, out_dir, refresh_acc)


def main():
    cli()


if __name__ == "__main__":
    main()
