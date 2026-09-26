import subprocess
from sys import argv


def main():
    str_arg = argv[1]
    if "tealflip" in subprocess.getoutput(f"ls {str_arg}"):
        print(True)
    # print(output.stdout)


if __name__ == "__main__":
    main()
