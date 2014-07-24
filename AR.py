"""This module provides most common functions for AccuRev.
   Authors: Anastasia Panchenko, Oleksandr Chyrkov
"""

import subprocess

class ARException(Exception):
    """Exception thrown by AR in case of some AccuRev exceptions"""
    
    def __init__(self, value):
        Exception.__init__(self)
        
    def __str__(self):
        return str(self.value)

class AccuRev:
    """"Use this class for getting AccuRev info (host, port, user),
        connection to server, login/logout commands.
        """
    
    def run(self, *args, **kwargs):
        "Runs raw AccuRev commands"
        cmd = subprocess.Popen("accurev %s" % ' '.join(args),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        stdout, stderr = cmd.communicate()
        retcode = cmd.returncode
        
        if retcode:
            raise ARException(stderr)
        
        return stdout, stderr, retcode
    
    def login(self, *args):
        self.run("login", *args)
    
    def logout(self):
        self.run("logout")
    
    def info(self):
        params = {
                  "Principal"     : "",
                  "Host"          : "",
                  "Server name"   : "",
                  "Port"          : "",
                  "DB Encoding"   : "",
                  "ACCUREV_BIN"   : "",
                  "Client time"   : "",
                  "Server time"   : "",
                  "Depot"         : "",
                  "Workspace/ref" : "",
                  "Basis"         : "",
                  "Top"           : "",
                  }
        
        info = self.run("info", "-v")[0].splitlines()
        for k, v in params.items():
            params[k] = [i.split(k + ":")[1].strip() for i in info if k in i]
            print k, params[k]


if __name__ == '__main__':
    pass    
