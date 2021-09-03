# VINC - 0.9.6
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

> :busts_in_silhouette: Python backdoor for windows machines :busts_in_silhouette:

> :warning: _**Attention**_: Project under development :warning:

The following code is not finished and is under heavy development. **Experimental features are being added every day**.

_**Do not**_ use this code in order to develop a stable bug-free undetectable backdoor.

## Description

Vinc is a backdoor tool initially developed to spy on Windows machines, giving free access to all kinds of information about the target/s.

## How it works

All the machines running vinc will connect to the vinc server automatically and will be able to run commands remotely.
The Command & Control Center (CMD&CTRL) is responsible for both handling the connections (acting as the server) and sending commands.

Every time a machine connects to the server a new Target ID is created. The CMD&CTRL Center can then use that machine's target ID to interact with that specific session of the backdoor.

Commands can also be sent via broadcasting to all the connected machines, giving the attacker the ability to execute commands on every machine **simultainiously**

## Screenshots

## Commands

Vinc is able to execute commands both in the CMD&CTRL Center and inside a specific backdoor session. **The following tables contain all of the available commands in version _0.9.6_.**

#### CMD&CTRL Center commands

| **Command** | **Arguments** | **Description** |
| ----------- | ------------- | --------------- |
|   `clear`   |   **None**    | Clears the screen |
|   `list-targets`   |   **None**    | Displays all the online backdoor sessions with their corresponding session ID |
|   `using` | **Session ID** | Enters the specified backdoor session