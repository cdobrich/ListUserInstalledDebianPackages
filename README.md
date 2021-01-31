# List User Installed Debian Packages

List all packages manually installed (by users, by admin/root, or both), as determined by the Debian package system.

## Methodology
First we query the Debian package system (dpkg) status file, to determine which packages are listed as currently installed. Second, we parse one or more sources for lists of manually installed files. Lastly, we  return the intersection of the list of manually installed packages against the currently installed packages.

> Reasoning: This is done because without comparing against current dpkg status simply listing manually installed files from logs may give false positives by not account for any later removed packages.

Result: Display a list of manually installed packages, not dependencies. This does not include pre-installed packages and system packages.


## Option Modes
There are 3 modes available for how to use this program. Execute the program on the command-line with the --help option to see more details.

1. Parse the log files in /var/log/apt/history.log*, returning only results from that data source.

2. Query the program apt-mark which is available in most modern Apt systems and only parse the output results from that data source.

> NOTE: Using Mode (2) 'apt-mark' generally gives a more complete list than Mode (1). Apt-mark includes packages which were manually installed via use of the 'dpkg' system directly by users. Further, Mode (2) includes      manually installed packages even by root/admin.

3. Perform options #1 and #2, then combine both sets of the results.

Mode 3 is the default and will be run if no specifying arguments are provided.

## Debian Package

There is a folder called 'ListUserInstalledPackages' which contains the 'DEBIAN' package info directory (including its 'control' file), for potential Debian-package generation. Here are the simple steps to generate a debian package file:

1. Copy the python file into the 'opt/' directory.

> cp ListUserInstalledPackages.py ListUserInstalledPackages/opt/
 
2. Run this command at the top of the repository:

dpkg-deb --build ListUserInstalledPackages

This will create a deb file with the name of the target build directory. In this example, it will be named 'ListUserInstalledPackages.deb'.

### Code Nodes

Some of this code could be separated into callable functions, but in the interests of development time and keeping the code simple, they have not been separated.

Names of variables have been made unique to clarify and avoid shadow-naming confusion.

Author: Clifton Dobrich

Date: 2021-01-17
