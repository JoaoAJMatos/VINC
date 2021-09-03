# VINC - 0.9.6 :door:
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## :busts_in_silhouette: Python backdoor for windows machines :busts_in_silhouette:

> :warning: _**Attention**_: Project under development :warning:

> :exclamation: The following code is not finished and is under heavy development. **Experimental features are being added every day** :exclamation:

> :exclamation: _**Do not**_ use this code in order to develop a stable bug-free undetectable backdoor :exclamation:

## Description :scroll:

Vinc is a backdoor tool initially developed to spy on Windows machines, giving free access to all kinds of information about the target/s.

## Download vinc

```
git clone https://github.com/JoaoAJMatos/VINC.git
```

## Run vinc

To run VINC's command and control center simply run:

```
python commandCenter.py
```

:exclamation: Although it can be used on any machine, the command and control center was made to run on Linux, therefore some commands may not work and some bugs may occur when running the script on a Windows host :exclamation:

The backdoor can be converted into an executable file in order to be delivered to the target's machine:

```
pip install pyinstaller
```
```
pyinstaller backdoor.py --onefile --noconsole
```

_**Note**_: The final build will change according to the host's architecture. Building the .exe file on a 64-bit machine would make the program unusable when opened on a 32-bit machine.

To run the backdoor double click the .exe file. The connection will be automatically astablished with the server after 15 seconds. If the server is offline, the backdoor will attempt to connect every 15 seconds until a connection is finaly made.

## How it works :gear:

All the machines running vinc will connect to the vinc server automatically and will be able to run commands remotely.
The Command & Control Center (CMD&CTRL) is responsible for both handling the connections (acting as the server) and sending commands.

Every time a machine connects to the server a new Target ID is created. The CMD&CTRL Center can then use that machine's target ID to interact with that specific session of the backdoor.

Commands can also be sent via broadcasting to all the connected machines, giving the attacker the ability to execute commands on every machine **simultainiously**

## Is it detectable? :mag_right:

**YES**! Vinc is considered malicious software by 10 of the 67 most popular anti-virus softwares. All the connections made and packets transmited over the internet can also be traced down to you!

## Screenshots :camera:

## Commands :computer:

Vinc is able to execute commands both in the CMD&CTRL Center and inside a specific backdoor session. **The following tables contain all of the available commands in version _0.9.6_.**

>#### CMD&CTRL Center commands

The following commands can be executed inside the the CMD&CTRL shell:


| **Command** | **Arguments** | **Description** |
| :---------: | :-----------: | :-------------: |
|   `clear`   |   **None**    | Clears the screen |
|   `list-targets`   |   **None**    | Displays all the online backdoor sessions with their corresponding session ID |
|   `using` | **Session ID** | Enters the specified backdoor session
|   `kill`  | **Session ID** | Kills the specified backdoor session
|   `shutdown` | **None** | Kills all the online backdoor sessions and turns off the CMD&CTRL Center
|   `broadcast` | **Command** | Sends the specified command to all online backdoor sessions

>#### Individual backdoor session commands

The following commands can **only** be executed inside an individual backdoor session

| **Command** | **Arguments** | **Description** |
| :---------: | :-----------: | :-------------: |
| `clear` | **None** | Clears the screen |
| `exit` | **None** | Kills and exits the current backdoor session |
| `background` | **None** | Exits the current session and returns to the CMD&CTRL Center |
| `help` | **None** | Lists all the current available commands
| `upload` | **Path** | Uploads the specified file to the targets file system |
| `download` | **Path** | Downloads a file from the targets file system |
| `keylog-start` | **None** | Starts the keylogger at the current backdoor session |
| `keylog-dump` | **None** | Show the keylogger log on the screen |
| `keylog-stop` | **None** | Stops the keylogger at the current backdoor session and delets the keylogger file from the target's fyle system |
| `persistence` | **RegName**, **FileName** | Creates a persistent session inside the target's PC. Every time the target boots the system the backdoor will start |
| `screenshot` | **None** | Takes a screenshot of the current backdoor session screen |
| `stream-start` | **None** | Starts screensharing. Enables the attacker to see what the target is doing in real time |
| `stream-stop` | **None** | Stops screensharing

> #### Additional commands

Vinc is also able to run every Windows command on the target's machine

## Legal Advice :oncoming_police_car:

This repository and **every script** inside it are for educational and testing purposes **only**. The creator nor **any** contributor will be responsible for the consequences of your actions.

:exclamation: Only use vinc with the full consent of the targeted machine's owner :exclamation: 
