"""This module provides most common functions for AccuRev.
   Author: Anastasia Panchenko
"""

import os
import sys
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
    
    # Not in directory message
    NID_MESSAGE = "You are not in a directory associated with a workspace"
    
    def __init__(self):
        self.info()

    def run(self, command, verbose=False):
        """Runs raw AccuRev commands."""
        
        out = sys.stdout if verbose else subprocess.PIPE
        cmd = subprocess.Popen("accurev %s" % command,
                               stdout=out,
                               stderr=subprocess.PIPE)
        stdout, stderr = cmd.communicate()
        retcode = cmd.returncode
        
        if retcode:
            raise ARException(stderr)
        
        return stdout, stderr, retcode
    
    def login(self, username, passwd):
        self.run("login %s %s" % (username, passwd))
    
    def logout(self):
        self.run("logout")

    def change_root(self, root):
        """Use this function for moving to the workspace directory
           """
        
        print "Changing directory to %s..." % root
        try:
            os.chdir(root)
        except Exception as e:
            print str(e)
        else:
            print "Done."

    
    def info(self):
        """ Sets main environment parameters as properties.
            """
        
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
                       "current_location"  : "Top",
                      }
        
        info, error = self.run("info -v")[:2]
        
        if self.NID_MESSAGE in error:
            self.nid_error = error
        
        for k, v in self.params.items():
            value = [i.split(v + ":")[1].strip() for i in info.splitlines() if v in i]
            if value:
                setattr(self, k, value[0])
    
    def __getattr__(self, name):
        if name in self.params.keys():
            return self.error if self.error else "(undefined)"
    
    
class ARWorkspace(AccuRev):
    """A class for working with current workspace or for
       creating new workspace.
       """

    def workspace_dir_required(func):
        """
        Decorator for functions which should be called only
        in workspace directory.
        """
        def wrapper(self, *args):
            if self.nid_error:
                print "Cann't execute the '%s' function" % func.__name__
                raise ARException(self.nid_error)
            else:
                func(self, *args)
        return wrapper

    def create(self):
        """ Use it for creating of new workspace.
            Name, location and stream options are required.
            """
        
        required = ["name", "location", "stream"]
        print "Creating new workspace %s..." % self.name
        for i in required:
            if not getattr(self, i):
                raise ARException("Workspace's %s is not set." % i)
        else:
            self.run("mkws -w %s -l %s -b %s" % (self.name, self.location, self.stream))
            print "Done."
            sys.exit(0)

    @workspace_dir_required
    def change_name(self, name=""):
        if name:
            self.name = name
        print "Changing workspace name from {0} to {1}...".format(self.current_workspace,
                                                                  self.name)
        self.run("chws -w %s %s" % (self.current_workspace, self.name))
        print "Done."
        sys.exit(0)
    
    @workspace_dir_required
    def change_stream(self, stream=""):
        if stream:
            self.stream = stream
        print "Changing workspace stream from {0} to {1}...".format(self.current_stream,
                                                                    self.stream)
        self.run("chws -w %s -b %s" % (self.current_workspace, self.stream))
        print "Done."
        sys.exit(0)
    
    @workspace_dir_required
    def change_location(self, location=""):
        if location:
            self.location = location
        print "Changing workspace location from {0} to {1}...".format(self.current_location,
                                                                      self.location)
        self.run("chws -w %s -l %s" % (self.current_workspace, self.location))
        print "Done."
        sys.exit(0)
    
    @workspace_dir_required
    def change(self):
        """Changes all parameters of workspace: location, stream, machine name.
           """ 
        
        if not self.machine_name:
            self.machine_name = socket.gethostname()
        print "Changing workspace %s..." % self.current_workspace
        self.run("chws -w %s -l %s -b %s -m %s" % (self.current_workspace, self.location,
                                                   self.stream, self.machine_name))
        print "Done."
        sys.exit(0)
    
    @workspace_dir_required
    def remove(self):
        print "Removing workspace %s..." % self.current_workspace
        self.run("rmws %s" % self.current_workspace)
        print "Done"
        sys.exit(0)
    
    @workspace_dir_required
    def update(self):
        print "Starting update of workspace..."
        self.run("update", verbose=True)
        sys.exit(0)
    
    @workspace_dir_required
    def populate(self):
        print "Starting populate of workspace..."
        self.run("pop -O -R .", verbose=True)
        print "Done."
        sys.exit(0)

if __name__ == '__main__':
    ar = AccuRev()
#     ar.run(bla='bla')
#     ar.logout()
    ar.login('bla', 'foo')
    ar.change_root(r"D:\BSENV\AccuRev\dev.ws.buildmgr.TestOverlaps")
    w = ARWorkspace()
#     w.remove()
#     print w.current_location
#     w.update()
#     w.populate()
#     w.name = "dev.ws.Test3"
#     w.location = r"D:\\foo3"
#     w.stream = "dev.buildmgr.TestProject"
#     w.create()
#     w.change_name("dev.ws.buildmgr.TestOverlaps4")
#     w.change_stream("dev.buildmgr.TestStream")
#     w.change_location(r"D:\Test")
#     w.location = r'D:\BSENV\AccuRev\dev.ws.buildmgr.TestOverlaps'
#     w.stream = r"dev.buildmgr.TestProject"
#     w.change()
    
    
    
