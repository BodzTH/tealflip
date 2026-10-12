<!-- ![Nginx](https://img.shields.io/badge/Nginx-black?style=flat&logo=Nginx&logoColor=green)
![Git](https://img.shields.io/badge/Git-black?style=flat&logo=Git)
![Python](https://img.shields.io/badge/Python-black?style=flat&logo=Python)
 -->

<div align="center">
  <h1 align="center">TealFlip</h1>
  <h3>Blue/Green Deployment Tool</h3>
</div>

`tealflip` is an automation tool that uses blue/green deployment technique to automate service's deployments/updates while maintaining __99%__ uptime.

## Motivation
If you have a home server and you are concerned with the uptime of your services or having a painful time deploying new updates, this might be the right tool (hopefully).

## The Problem
I have a service running inside a podman container on my old laptop, each time I want to update something in that service I have to ssh to the laptop and:

1. `git pull` 
2. Shutdown the podman 
3. Run the podman again.
4. Hope it does not crash.
5. Repeat.

## Installation

### 1. Clone the repository
Clone tealflip repo __on the machine__  you want to manage, clone it with:
```shell
git clone https://github.com/BodzTH/tealflip.git
cd tealflip
```

### 2. Set Configurations
Make sure your working directory at `tealflip/` directory then run:
```shell
./tealflip -t
```
This will make a copy of the files in `templates/` and place it in `variables/` directory, this separation is important as the __data__ in `variables/` must be preserved.<br>  
As you may have saw the output message you need to set configuration variables for your git, machine,  and project.<br>
Set the following configuration variables in `variables/config.py`:
- REPO_URL (Remote Git Repository)
- IP (The local IP of your machine)
- DNS (A domain name for your machine preferably a [example].local)
- PROJECT_PATH (Absolute Path of the project managed with same REPO_URL remote git)

> [!WARNING]
> Do not run `./tealflip -t` after setting your configuration variables, this will override what you set with `templates/` if you haven't __initialized__ tealflip.

### 3. Initialize the tool

After you make sure you have set the right configurations, run the following command:
```shell
./tealflip init
```
The above command will initialize necessary services, environment variables, and Nginx. Now you can run `tealflip` command from any path in your machine.
  
