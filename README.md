# Falcon Host API To LEEF

A Python script that connects to falcon host's public streaming API and outputs into LEEF format to be consumed by QRadar SIEM.

# Configuration

The configuration file included title FH_LEEF.config contains the following settings which should be configured according to your environment and specific use cases.

* __api_url__ - This is the URL to the public falcon host API endpoint
* api_username - username of account with API access
* api_password - password of account with API access
* offset - this is automatically updated by the script in order to keep track of where to reconnect in the stream 
* json_to_file - a boolean value either set to true or false to output API results to json in a local text file
* leef_to_file - a boolean value either set to true or false to output API results to LEEF format in a local text file
* send_over_syslog - a boolean to enable transmission of events over syslog
* syslog_host - hostname or IP address of syslog server, this will likely be your SIEM's log collector
* syslog_port - port to receive syslog events on
* syslog_protocol - can be set to tcp or udp depending on your syslog server configuration
* read_timeout - in seconds, amount of time wait before timing out when no events are being sent from the API.
* connection_timeout - in seconds, amount of time to connect to API before timing out (default is 30)
* error_log - path to local file for logging al script errors
* activity_log - path to local file for logging all script activity
