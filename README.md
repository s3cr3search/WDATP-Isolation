# WDATP-Isolation

Introduction <br/>
This how to guide aim is to show how to utilize the Windows Defender mass isolation scripts.

Prerequisites
- Python is installed on your machine
- You have the WDATP machine-IDs of the machines you wish to isolate
- Your internal DNS is pointing to an external DNS server
- Both python packages (pandas & inquirer) are installed
- A csv file called Machine_list.csv (In the same folder location as the scripts)
- An Azure App with permissions to isolate machines

How-to
1. Enter app credentials to scripts
2. Run script to isolate.
3. Select type of isolation
4. Add a comment (This is needed for the sript to run)
