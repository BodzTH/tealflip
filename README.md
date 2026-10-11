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
```shell
git clone https://github.com/BodzTH/tealflip.git
cd tealflip
```

### 2. Initialize the tool

Make sure your working directory at tealflip directory then run:
```shell
./tealflip init
```
The above command will initialize necessary services, environment variables, and nginx. It will also ask for Repo URL , Server IP, DNS, and Project git managed path.
