<div align="center">

# $\color{#2a9d8f}{\textsf{TealFlip}}$

### $\color{#4a7fd4}{\textsf{Blue}}\ \color{#ffffff}{\textsf{⇄}}\ \color{#3fa66b}{\textsf{Green}}\ \color{#ffffff}{\textsf{Deployment Tool}}$

![Nginx](https://img.shields.io/badge/Nginx-black?style=flat&logo=Nginx&logoColor=green)
![Git](https://img.shields.io/badge/Git-black?style=flat&logo=Git)
![Python](https://img.shields.io/badge/Python-black?style=flat&logo=Python)
</div>



`tealflip` is an automation tool that uses blue/green deployment technique to automate service's deployments/updates while maintaining __99%__ uptime.

## Motivation
If you have a home server and you are concerned with the uptime of your services or having a painful time deploying a new commit, this might be the right tool (hopefully).

## The Problem
I have a service that runs inside a container on my old laptop, every time I want to deploy a new commit to the service, I do the following:

1. SSH to the laptop
2. Navigate to project directory
3. `git pull`
4. Shutdown the container 
5. Run the container again.
6. Hope it does not crash.

## Solution
One of the solutions I picked, is to automate deployments with $\color{#4a7fd4}{\textsf{Blue}}\$ / $\color{#3fa66b}{\textsf{Green}}\$ deployment technique, Below is an example how it works: 

Status: __Active__ Slot: $\color{#4a7fd4}{\textsf{Blue}}\$ __Commit__: B, __Idle__ Slot: $\color{#3fa66b}{\textsf{Green}}\$ __Commit__: A 

1. Watch latest remote git commits
2. Deploy new healthy commit on new Active slot, __Commit__: C

    __Active__ Slot: $\color{#3fa66b}{\textsf{Green}}\$ __Commit__: C, __Idle__ Slot: $\color{#4a7fd4}{\textsf{Blue}}\$ __Commit__: B

3. Rollback in case active slot has bugs

    __Active__ Slot: $\color{#4a7fd4}{\textsf{Blue}}\$ __Commit__: B, __Idle__ Slot: $\color{#3fa66b}{\textsf{Green}}\$ __Commit__: C 

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
This will make a copy of the files in `templates/` and place it in `variables/` directory, this separation is important as the __data__ in `variables/` must be preserved. As you may have saw the output message you need to set configuration variables for your git, machine,  and project.

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

## Subcommands
`status`: Displays idle/active slots commit hash\
`deploy`: Deploys new commit version and switches to latest healthy commit\
`rollback`: Rolls back to healthy idle slot\
`watch`: Watches for latest remote git commits

## Coming 
- Interactive selection rolling back to any healthy commit in commits history
- Automate container deployments

> [!NOTE]
> You can test TealFlip with simple index.html as in [TealFlip Demo](https://github.com/BodzTH/tealflip-demo).\
> TealFlip is under development, fully functional blue/green deployment for a container is not yet implemented.
