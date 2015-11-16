#!/usr/bin/env python
#Usage: ./FH-LEEF.py 
import sys, json, base64, signal, socket, os, ConfigParser
import requests
import urllib2
import requests.exceptions
import time, commands
from Mapping import Detection, LoginAuditEvent, ConfigFile


# GLOBAL VARIABLES
abs_cwd = os.path.dirname(os.path.abspath(__file__))
configpath = os.path.join(abs_cwd, "FH_LEEF.config")
config = ConfigFile(configpath)
if config.debug:
    f = open('json.out', 'w') #Raw JSON output for debugging
    LEEF = open('LEEF.out', 'w') #Parsed LEEF output for debugging
EventCount = 0
LastOffset = 0
buffer = ""


def main(argv):
    global LastOffset, config
    LastOffset = config.offset
    connection = StreamManager()
    streams = connection.list()
    for url, token in streams.iteritems():
        connection.open(url, token)
    print "Script Execution Completed"
    shutdown()


def handle_ctrl_c(signal, frame):
    print "Got ctrl+c, going down!"
    shutdown()


def shutdown():
    global f, LEEF
    if config.debug:
        f.close()
        LEEF.close()
    config.update(LastOffset)
    print "Shutting Down"
    os.unlink(pidfile)
    sys.exit(0)


def Logger(message, file):
    log = open(file, 'a')
    currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    log.write("[" + currenttime + "] - " + message + "\n")


class StreamManager(object):
    global config

    def __init__(self):
        self.name = ""
        signal.signal(signal.SIGINT, handle_ctrl_c)

    def list(self):
        streams = {}
        try:
            req = urllib2.Request(config.api_url)
            base64string = base64.encodestring('%s:%s' %
                                               (config.api_username, config.api_password)).replace('\n', '')
            req.add_header('Authorization', "Basic %s" % base64string)
            resp = urllib2.urlopen(req)
            content = resp.read()
            decoded = json.loads(content)
            for stream in decoded['resources']:
                streams[stream['dataFeedURL']] = stream['sessionToken']['token']
        except Exception, e:
            error = "Initial API Connection Failed: " + str(e)
            print error
            Logger(error, config.error_log)
            shutdown()
        return streams

    def open(self, url, token):
        header = {'Authorization': 'Token %s' % token}
        try:
            req = requests.get(url + '&offset=' + config.offset, stream=True,
                               timeout=(config.connection_timeout, config.read_timeout), headers=header)

            for line in req.iter_content(chunk_size=None):
                self.process(line)

        except requests.exceptions.ConnectionError:
            config.update(LastOffset)
            error = "Connection Timeout Error: No events received in the last " + str(config.read_timeout) + " seconds"
            print error
            Logger(error, config.error_log)
            shutdown()

        except Exception as e:
            config.update(LastOffset)
            error = "Error: " + str(e)
            print error
            Logger(error, config.error_log)
            shutdown()

    def process(self, data):
        global buffer, f, EventCount, LastOffset
        signal.signal(signal.SIGINT, handle_ctrl_c)
        buffer = ""
        buffer += data
        if data.endswith('\r\n') and buffer.strip():
            if config.debug:
                f.write(buffer)
            decoded = json.loads(buffer)
            etype = decoded['metadata']['eventType']
            if etype == 'DetectionSummaryEvent':
                event = Detection()
                event.deserialize(buffer)
                if config.debug:
                    Logger(" Loaded " + event.Type + " - " + event.Url, config.activity_log)
            elif etype == 'LoginAuditEvent':
                event = LoginAuditEvent()
                event.deserialize(buffer)
                if config.debug:
                    Logger(" Loaded " + event.Type + " - " + event.UserIP + " - " + event.UserId, config.activity_log)
            else:
                return
            LastOffset = event.Offset

            # CONVERSION TO LEEF FORMAT
            bodyextension = event.converttoleef()
            header = "LEEF:1.0|CrowdStrike|CrowdStrike Falcon Host|1.0|"
            line = header+bodyextension
            line = line.replace('\\', '\\\\')
            line = line.encode('utf-8').strip()
            if config.debug:
                LEEF.write(line+'\n')

            # SEND TO QRADAR VIA SYSLOG
            if config.send_over_syslog:
                if config.protocol == 'tcp':
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((config.syslog_host, config.syslog_port))
                    sock.send(line)
                    sock.shutdown(socket.SHUT_RDWR)
                    sock.close()
                elif config.protocol == 'udp':
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.sendto(line, (config.syslog_host, config.syslog_port))
            print str(EventCount) + " Events Processed"
            EventCount += 1

if __name__ == '__main__':
    abs_cwd = os.path.dirname(os.path.abspath(__file__))
    pid = str(os.getpid())
    pidfile = os.path.join(abs_cwd, "FH_LEEF.pid")

    if os.path.isfile(pidfile):
        pidfileval = commands.getoutput("cat " + pidfile)
        status = commands.getoutput("if ps -p " + pidfileval + " >/dev/null;then echo true;else echo false;fi")
        if status == "true":
            error = "Process is already running under PID %s, exiting" % pidfileval
            print error
            Logger(error, config.error_log)
            sys.exit()
        elif status == "false":
            error = "PID file exists but process not running, creating new file"
            print error
            file(pidfile, 'w').write(pid)
            Logger(error, config.error_log)
    else:
        file(pidfile, 'w').write(pid)
        print "Script successfully initiated"
        if config.debug:
            Logger("Script successfully initiated", config.activity_log)
    main(sys.argv[1:])
