# VINC v0.9.6
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

> Python backdoor for windows machines :busts_in_silhouette:

> :warning: **Attention**: Project under development

The following code is not finished and is under heavy development. Experimental features are being added every day.

**Do not** use this code in order to develop a stable bug-free undetectable backdoor.

## Description

Vinc is a backdoor tool initially developed to spy on Windows machines, giving free access to all kinds of information about the target.

## How it works

All the machines running vinc will connect to the vinc server automatically and will be able to run commands remotely.
The Command & Control Center (CMD&CTRL) is responsible for both handling the connections (acting as the server) and sending commands.

Every time a machine connects to the server a new Target ID is created. The CMD&CTRL Center can then use that machine's target ID to interact with that specific session of the backdoor.

## Screenshots