import os
import subprocess
from pathlib import Path


def nginx_init(ip: str | None, dns: str | None) -> None:
    if ip == None or dns == None:
        print("IP/DNS Environment variables not set!")
        print("Exiting Nginx init function.")
        return
    rootcert_path = Path.home() / ".local" / "share" / "mkcert"
    subprocess.run(
        ["sudo", "mkdir", "-p", "/var/www"], check=False, text=True, shell=False
    )
    subprocess.run(
        ["sudo", "mkdir", "-p", "/etc/nginx/certs"], check=False, text=True, shell=False
    )
    subprocess.run(
        ["sudo", "mkdir", "-p", "/etc/nginx/logs"], check=False, text=True, shell=False
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
    )
    subprocess.run(
        ["sudo", "chown", "-R", "nginx:nginx", "/var/www"],
        check=False,
        text=True,
        shell=False,
    )
    subprocess.run(["mkcert", "-install"], check=False, text=True, shell=False)
    subprocess.run(
        [
            "mkcert",
            "-cert-file",
            "cert.pem",
            "-key-file",
            "key.pem",
            f"{dns}",
            f"{ip}",
            "localhost",
        ],
        check=False,
        text=True,
        shell=False,
    )
    subprocess.run(
        ["sudo", "mv", "cert.pem", "key.pem", "/etc/nginx/certs"],
        check=False,
        text=True,
        shell=False,
    )
    subprocess.run(
        ["cp", f"{rootcert_path}/rootCA.pem", "./"], check=False, text=True, shell=False
    )

    os.environ["DNS"] = dns
    nginx_conf_text = Path("nginx_template.conf").read_text().replace("${DNS}", dns)

    subprocess.run(
        ["sudo", "tee", "/etc/nginx/nginx.conf"],
        input=nginx_conf_text,
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )
