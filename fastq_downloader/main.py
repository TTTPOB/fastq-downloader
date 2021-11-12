from helper.rename_files_by_run import write_filename_to_dict, actual_rename
from helper.download_and_verify import download_and_verify
from helper.construct_gsm_dict import infotsv_to_dict, get_link_md5
from helper.merge_files import merge_files
from multiprocessing import Pool
import click


@click.command()
@click.option(
    "--info", "-in", default="info.tsv", help="iinput information file, must be a tsv"
)
@click.option("--out", "-o", default="fastq_downloader_out", help="output directory")
@click.option("--rename", "-r", default=True, help="rename the out putted file or not")
@click.option("--privkey", "-k", default=None, help="private key for downloading")
@click.option(
    "--parallel",
    "-p",
    default=4,
    help="number of accession to download, note the granular of parallel is the first level accesion",
)
@click.option(
    "--merge",
    "-m",
    default=True,
    help="merge the downloaded files or not" + "implies rename",
)
def main(info, out, rename, privkey, parallel, merge):
    if merge:
        rename = True
    infodict = infotsv_to_dict(info)
    infodict = get_link_md5(infodict)
    for acc, subdict in infodict.items():
        infodict[acc] = write_filename_to_dict(subdict)

    p = Pool(parallel)
    ascp_dict_list = [x["ascp"] for x in infodict.values()]
    p.map(lambda x: download_and_verify(x, privkey, out), ascp_dict_list)

    if rename:
        for acc, subdict in infodict.items():
            actual_rename(subdict, out)
    if merge:
        for acc, subdict in infodict.items():
            merge_files(subdict, rename, out)


if __name__ == "__main__":
    main()
