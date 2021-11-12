import subprocess
from pathlib import Path
import hashlib

ASCP_PORT = 330001


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
    # invoke ascp
    ascp_command = f"ascp -i {privkey} -P {ASCP_PORT} -Q {link} {out_dir}"
    subprocess.run(ascp_command, shell=True)


def check_file(file_path: str, md5: str, blocksize=2 ** 20):
    """
    Checks if the file at the given path has the given md5.
    """
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


def download_and_verify(ascp_dict: dict, privkey: str = None, out_dir: str = "."):
    """
    Downloads the given link and verifies it with the given md5.
    """
    for links, info in ascp_dict.items():
        for link in links:
            invoke_ascp(link, privkey, out_dir)
            check_file(out_dir + "/" + info["filename"], info["md5"])
