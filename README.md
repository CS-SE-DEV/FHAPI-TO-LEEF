# Falcon Host API To LEEF

A Python script that connects to falcon host's public streaming API and outputs into LEEF format to be consumed by QRadar SIEM.  Optionally the events can be convereted to LEEF and pushed via syslog to QRadar.

# Deployment

In order to run this program you will need a system with Python 2.X installed.  You can either download the files directly through your browser and transfer them to your server, or clone the files using git.  The program also uses the python requests library, this must be installed for the script to run successfully.  

1. Install requests by running either pip install requests or easy_install requests
2. Run command git clone https://github.com/CS-SE-DEV/Falcon-Host-API-To-LEEF.git to download files to local system.
3. Ensure FH_LEEF.py has executable permissions by running chmod +x FH_LEEF.py
4. Update FH_LEEF.config file with the appropriate settings
5. Run script by typing ./FH_LEEF.py

# Configuration

The configuration file included title FH_LEEF.config contains the following settings which should be configured according to your environment and specific use cases.

* __api_url__ - This is the URL to the public falcon host API endpoint
* __api_username__ - username of account with API access
* __api_password__ - password of account with API access
* __offset__ - this is automatically updated by the script in order to keep track of the last event processed
* __json_to_file__ - a boolean value indicating whether  to output API results to JSON in a local text file
* __leef_to_file__ - a boolean value indicating whether to output API results to LEEF format in a local text file
* __send_over_syslog__ - a boolean to enable transmission of events over syslog
* __syslog_host__ - hostname or IP address of syslog server, this will likely be your SIEM's log collector
* __syslog_port__ - port to receive syslog events on
* __syslog_protocol__ - can be set to tcp or udp depending on your syslog server configuration
* __read_timeout__ - in seconds, amount of time wait before timing out when no events are being sent from the API.
* __connection_timeout__ - in seconds, amount of time to connect to API before timing out (default is 30)
* __error_log__ - path to local file for logging al script errors
* __activity_log__ - path to local file for logging all script activity

## Mapping ##

There are two modules apart of this project.  The Mapping module contains the data structures and deserializtion logic for all data models used in the script.  In the event a field titles change in the API or LEEF schema, simply update the information in the mapping file.  Including additional fields or adding new event types to capture/convert can be accomplished by updating the mapping file accordingly.


