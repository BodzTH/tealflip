import subprocess
from pathlib import Path


def nginx_init(ip: str | None, dns: str | None, project: str | None) -> None:
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
        ["sudo", "mv", "*.pem", "/etc/nginx/certs"], check=False, text=True, shell=False
    )
    subprocess.run(
        ["cp", f"{rootcert_path}/rootCA.pem", "./"], check=False, text=True, shell=False
    )
    subprocess.run(
        ["sudo", "cp", "-r", f"{project}/*.{{html,css}}", "/var/www/"],
        check=False,
        text=True,
        shell=False,
    )
    subprocess.run(
        ["sudo", "cp", "./nginx.conf", "/etc/nginx/nginx.conf"],
        check=False,
        text=True,
        shell=False,
    )
