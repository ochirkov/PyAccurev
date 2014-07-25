"""This module provides most common functions for AccuRev.
   Authors: Anastasia Panchenko, Oleksandr Chyrkov
"""

import os
import socket
import subprocess


class ARException(Exception):
    """Exception thrown by AR in case of some AccuRev exceptions"""
    
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value
        
    def __str__(self):
        return str(self.value)

class AccuRev(object):
    """"Use this class for getting AccuRev info (host, port, user),
        connection to server, login/logout commands.
        """
    
    def __init__(self):
        self.info()

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

    def change_root(self, root):
        print "Changing directory to %s..." % root
        try:
            os.chdir(root)
        except Exception as e:
            print str(e)
    
    def info(self):
        self.params = {
                       "current_user"      : "Principal",
                       "current_host"      : "Host",
                       "current_server"    : "Server name",
                       "current_port"      : "Port",
                       "current_encoding"  : "DB Encoding",
                       "current_bin"       : "ACCUREV_BIN",
                       "current_depot"     : "Depot",
                       "current_workspace" : "Workspace/ref",
                       "current_stream"    : "Basis",
                       "current_top"       : "Top",
                      }
        
        info, error, ecode = self.run("info", "-v")
        self.error = error
        for k, v in self.params.items():
            value = [i.split(v + ":")[1].strip() for i in info.splitlines() if v in i]
            if value:
                setattr(self, k, value[0])
    
    def __getattr__(self, name):
        if name in self.params.keys():
            return self.error if self.error else "(undefined)"

    
class ARWorkspace(AccuRev):
    """
    A class for working with current workspace or for
    creating new workspace.
    """
    
    def workspace_dir_required(func):
        """
        Decorator for function which should be called only
        in workspace directory.
        """
        def wrapper(self, *args):
            if self.error:
                print "An error occured while executing the '%s' function: %s" \
                                                    % (func.__name__, self.error)
                return
            else:
                func(self, *args)
        return wrapper
    
    def create(self):
        required = ["name", "location", "stream"]
        print "Creating new workspace %s..." % self.name
        for i in required:
            if not getattr(self, i):
                print "Workspace's %s is not set." % i
                break
        else:
            self.run("mkws", "-w", self.name, "-l", self.location, "-b", self.stream)
            print "Done."

    @workspace_dir_required
    def change_name(self, name=""):
        if name:
            self.name = name
        print "Changing workspace name from {0} to {1}...".format(self.current_workspace,
                                                                  self.name)
        self.run("chws", "-w", self.current_workspace, self.name)
        print "Done."
    
    @workspace_dir_required
    def change_stream(self, stream=""):
        if stream:
            self.stream = stream
        print "Changing workspace stream from {0} to {1}...".format(self.current_stream,
                                                                    self.stream)
        self.run("chws", "-w", self.current_workspace, "-b", self.stream)
        print "Done."
    
    @workspace_dir_required
    def change_location(self, location=""):
        if location:
            self.location = location
        print "Changing workspace location from {0} to {1}...".format(self.current_top,
                                                                      self.location)
        self.run("chws", "-w", self.current_workspace, "-l", self.location)
        print "Done."
    
    @workspace_dir_required
    def change(self):
        if not self.machine_name:
            self.machine_name = socket.gethostname()
        print "Changing workspace %s..." % self.current_workspace
        self.run("chws", "-w", self.current_workspace, "-l", self.location,
                 "-b", self.stream, "-m", self.machine_name)
        print "Done."

    @workspace_dir_required
    def update(self):
        print "Update started..."
        stdout, stderr, ecode = self.run("update")
        print stdout
    
    @workspace_dir_required
    def populate(self):
        print "Populate started..."
        stdout, stderr, ecode = self.run("pop -O -R .")
        print stdout

if __name__ == '__main__':
    ar = AccuRev()
#     ar.run(bla='bla')
#     ar.logout()
    ar.change_root(r'D:\BSENV\AccuRev\dev.ws.buildmgr.TestOverlaps')
    w = ARWorkspace()
    w.populate()
#     w.name = "dev.ws.Test"
#     w.location = r"D:\\foo"
#     w.stream = "dev.buildmgr.TestProject"
#     w.create()
#     w.change_name("dev.ws.buildmgr.TestOverlaps3")
#     w.change_stream("dev.buildmgr.TestStream")
#     w.change_location(r"D:\\Test")
#     w.location = r'D:\BSENV\AccuRev\dev.ws.buildmgr.TestOverlaps'
#     w.stream = r"dev.buildmgr.TestProject"
#     w.change()
    
    
    
