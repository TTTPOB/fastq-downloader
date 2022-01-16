import subprocess
from pathlib import Path
import hashlib
from multiprocessing import Pool

ASCP_PORT = 33001


def invoke_ascp(link: str, privkey: str = None, out_dir: str = "."):
    """
    Invokes the ascp command with the given private key and link.
    """
    # try to get path to ascp binary
    ascp_bin_path = subprocess.check_output(["which", "ascp"]).decode("utf-8").strip()
    if ascp_bin_path == "":
        raise Exception("ascp binary not found")
    ascp_bin_path = Path(ascp_bin_path)
    # if privkey are not provided, use infered one
    if privkey is None:
        privkey = ascp_bin_path.parent.parent / "etc" / "asperaweb_id_dsa.openssh"
    if not privkey.exists():
        raise Exception("private key not found")
    orig_name = Path(link).name
    # invoke ascp
    ascp_command = f"ascp -i {privkey} -P {ASCP_PORT} -Q {link} ./{out_dir}/{orig_name}"
    subprocess.run(ascp_command, shell=True)


def invoke_wget(link: str, out_dir: str = "."):
    """
    Invokes the wget command with the given link.
    """
    # try to get path to wget binary
    wget_bin_path = subprocess.check_output(["which", "wget"]).decode("utf-8").strip()
    if wget_bin_path == "":
        raise Exception("wget binary not found")
    wget_bin_path = Path(wget_bin_path)
    # file name
    file_name = Path(link).name
    # invoke wget
    wget_command = f"wget -O {Path(out_dir)/file_name} {link}"
    subprocess.run(wget_command, shell=True)


def check_file(file_path: str, md5: str, blocksize=2 ** 20):
    """
    Checks if the file at the given path has the given md5.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise Exception("file not found")
    with open(file_path, "rb") as f:
        m = hashlib.md5()
        with open(file_path, "rb") as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                m.update(buf)
        file_md5 = m.hexdigest()
    if file_md5 != md5:
        raise Exception("md5 does not match")


def download_and_verify__(link: str, info: dict, privkey: str, out_dir: str):
    if link.startswith("ftp"):
        invoke_wget(link, out_dir)
        check_file(out_dir + "/" + Path(link).name, info["md5"])
    elif link.startswith("era-fasp"):
        invoke_ascp(link, privkey, out_dir)
        check_file(out_dir + "/" + Path(link).name, info["md5"])
    else:
        raise Exception("I can only download ftp or era-fasp(ascp) links")


def download_and_verify(
    ascp_dict: dict, privkey: str = None, out_dir: str = ".", parallel2: int = 4
):
    """
    Downloads the given link and verifies it with the given md5.
    """
    # p = Pool(parallel2)
    # p.starmap(
    #     download_and_verify__,
    #     zip(
    #         ascp_dict.keys(),
    #         ascp_dict.values(),
    #         [privkey] * len(ascp_dict.keys()),
    #         [out_dir] * len(ascp_dict.keys()),
    #     )
    # )
    for link, info, privkey, out_dir in zip(
        ascp_dict.keys(),
        ascp_dict.values(),
        [privkey] * len(ascp_dict.keys()),
        [out_dir] * len(ascp_dict.keys()),
    ):
        download_and_verify__(link, info, privkey, out_dir)
