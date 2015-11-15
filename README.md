# Falcon Host API To LEEF

A Python script that connects to falcon host's public streaming API and outputs into LEEF format to be consumed by QRadar SIEM.

# Configuration

The configuration file included title FH_LEEF.config contains the following settings which should be configured according to your environment and specific use cases.

* __api_url__ - This is the URL to the public falcon host API endpoint
* __api_username__ - username of account with API access
* __api_password__ - password of account with API access
* __offset__ - this is automatically updated by the script in order to keep track of where to reconnect in the stream 
* __json_to_file__ - a boolean value either set to true or false to output API results to json in a local text file
* __leef_to_file__ - a boolean value either set to true or false to output API results to LEEF format in a local text file
* __send_over_syslog__ - a boolean to enable transmission of events over syslog
* __syslog_host__ - hostname or IP address of syslog server, this will likely be your SIEM's log collector
* __syslog_port__ - port to receive syslog events on
* __syslog_protocol__ - can be set to tcp or udp depending on your syslog server configuration
* __read_timeout__ - in seconds, amount of time wait before timing out when no events are being sent from the API.
* __connection_timeout__ - in seconds, amount of time to connect to API before timing out (default is 30)
* __error_log__ - path to local file for logging al script errors
* __activity_log__ - path to local file for logging all script activity

# Modules

## Mapping ##

There are two modules apart of this project.  The Mapping module contains the data structures to manage the mapping of different event types from API.  In the event any field titles change within the API or LEEF schemas, simply update the mapping file accordingly.



