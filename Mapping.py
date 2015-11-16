import time, sys, json, ConfigParser


class FalconEvent:
    def __init__(self):

        def deserialize(self, data):
            return NotImplemented()


class Detection(FalconEvent):

    def __init__(self):
        self.Type = "DetectionSummaryEvent"
        self.Url = ""
        self.ProcessStartTime = ""
        self.Offset = ""
        self.DetectName = ""
        self.UserName = ""
        self.Hostname = ""
        self.Domain = ""
        self.FileName = ""
        self.FilePath = ""
        self.Severity = ""
        self.FileHash = ""

    def deserialize(self, data):
        decoded = json.loads(data)
        self.Url = decoded['event']['FalconHostLink']
        self.ProcessStartTime = str(time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.gmtime(min(decoded['event']['ProcessStartTime'], sys.maxint))))
        self.Offset = decoded['metadata']['offset']
        self.DetectName = decoded['event']['DetectName']
        self.UserName = decoded['event']['UserName']
        self.Severity = decoded['event']['Severity']
        self.Hostname = decoded['event']['ComputerName']
        self.Domain = decoded['event']['MachineDomain']
        self.FileName = decoded['event']['FileName']
        self.FilePath = decoded['event']['FilePath']
        self.FileHash = decoded['event']['SHA256String']
        return self

    def converttoleef(self):
        body = "Detection|"
        extension = ""
        extension += "devTimeFormat="+"yyyy-MM-dd HH:mm:ss Z\t"
        extension += "devTime=" + self.ProcessStartTime + "\t"
        extension += "offset=" + str(self.Offset) + "\t"
        extension += "sev=" + str(self.Severity) + "\t"
        extension += "cat=" + self.Type + "\t"
        extension += "detectName=" + self.DetectName + "\t"
        extension += "userName=" + self.UserName + "\t"
        extension += "identHostName=" + self.Hostname + "\t"
        extension += "domain=" + self.Domain + "\t"
        extension += "fileName=" + self.FileName + "\t"
        extension += "filePath=" + self.FilePath + "\t"
        extension += "fileHash=" + self.FileHash + "\t"
        extension += "url=" + self.Url + "\t"
        return body+extension


class LoginAuditEvent(FalconEvent):

    def __init__(self):
        self.Type = "LoginAuditEvent"
        self.LoginTime = ""
        self.Offset = ""
        self.UserId = ""
        self.UserIP = ""
        self.Operation = ""
        self.ServiceName = ""
        self.Success = ""

    def deserialize(self, data):
        decoded = json.loads(data)
        self.LoginTime = str(time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.gmtime(min(decoded['event']['LoginTime'] / 1000, sys.maxint))))
        self.Offset = decoded['metadata']['offset']
        self.UserId = decoded['event']['UserId']
        self.UserIP = decoded['event']['UserIp']
        self.Operation = decoded['event']['OperationName']
        self.ServiceName = decoded['event']['ServiceName']
        self.Success = decoded['event']['Success']
        return self

    def converttoleef(self):
        body = self.Operation + "|"
        extension = ""
        extension += "devTimeFormat="+"yyyy-MM-dd HH:mm:ss Z\t"
        extension += "devTime=" + self.LoginTime + "\t"
        extension += "offset=" + str(self.Offset) + "\t"
        extension += "sev=1"+'\t'
        extension += "cat=" + self.Type + "\t"
        extension += "userName=" + self.UserId + "\t"
        extension += "identSrc=" + self.UserIP + "\t"
        return body+extension


class ConfigFile(object):
    def __init__(self, name):
        config = ConfigParser.ConfigParser()
        config.read(name)
        self.name = name
        self.api_url = config.get('settings', 'api_url')
        self.api_username = config.get('settings', 'api_username')
        self.api_password = config.get('settings', 'api_password')
        self.offset = config.get('settings', 'offset')
        self.syslog_host = config.get('settings', 'syslog_host')
        self.syslog_port = config.getint('settings', 'syslog_port')
        self.read_timeout = config.getint('settings', 'read_timeout')
        self.connection_timeout = config.getint('settings', 'connection_timeout')
        self.send_over_syslog = config.getboolean('settings', 'send_over_syslog')
        self.protocol = config.get('settings', 'syslog_protocol')
        self.error_log = config.get('settings', 'error_log')
        self.activity_log = config.get('settings', 'activity_log')
        self.debug = config.getboolean('settings', 'debug')

    def update(self, lastoffset):
        config = ConfigParser.ConfigParser(allow_no_value=True)
        config.read(self.name)
        config.set('settings', 'offset', lastoffset)
        config_file = open(self.name, 'w')
        config.write(config_file)
        config_file.close()

