import os
import subprocess
from pathlib import Path

from config import DNS, IP
from deploy import deploy


def nginx_init() -> None:
    if IP == None or DNS == None:
        print("IP/DNS Environment variables not set!")
        print("Exiting Nginx init function.")
        return
    rootcert_path = Path.home() / ".local" / "share" / "mkcert"
    project_dir = Path(__file__).parent
    user = os.getlogin()
    subprocess.run(
        [
            "sudo",
            "mkdir",
            "-p",
            "/var/www/blue",
            "/var/www/green",
            "/etc/nginx/certs",
            "/etc/nginx/logs",
            "/etc/nginx/tealflip",
        ],
        check=False,
        text=True,
        shell=False,
    )
    subprocess.run(
        [
            "sudo",
            "useradd",
            "--system",
            "--user-group",
            "--no-create-home",
            "--shell",
            "/usr/bin/nologin",
            "nginx",
        ],
        check=False,
        text=True,
        shell=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["sudo", "chown", "-R", f"{user}:{user}", "/var/www"],
        check=False,
        text=True,
        shell=False,
        stdout=subprocess.DEVNULL,
    )
    subprocess.run(
        ["sudo", "chown", "-R", f"{user}:{user}", "/etc/nginx/tealflip"],
        check=False,
        text=True,
        shell=False,
        stdout=subprocess.DEVNULL,
    )
    subprocess.run(
        ["mkcert", "-install"],
        check=False,
        text=True,
        shell=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        [
            "mkcert",
            "-cert-file",
            "cert.pem",
            "-key-file",
            "key.pem",
            f"{DNS}",
            f"{IP}",
            "localhost",
        ],
        check=False,
        text=True,
        shell=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        [
            "sudo",
            "mv",
            f"{project_dir}/cert.pem",
            f"{project_dir}/key.pem",
            "/etc/nginx/certs",
        ],
        check=False,
        text=True,
        shell=False,
    )
    print(
        f"Copy rootCA pub key in {rootcert_path}/rootCA.pem and add it to your Browser Certificates"
    )

    os.environ["DNS"] = DNS
    nginx_conf_text = (
        Path(f"{project_dir}/nginx_template.conf").read_text().replace("${DNS}", DNS)
    )

    subprocess.run(
        ["sudo", "tee", "/etc/nginx/nginx.conf"],
        input=nginx_conf_text,
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )

    deploy()
