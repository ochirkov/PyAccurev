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
    # Undefined value
    UNDEFINED = "(undefined)"
    
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
            else:
                setattr(self, k, self.UNDEFINED)
    
    
class ARWorkspace(AccuRev):
    """A class for working with current workspace or for
       creating new workspace.
       """
    
    def __init__(self, workspace=""):
        super(self.__class__, self).__init__()
        if self.current_workspace == self.UNDEFINED and not workspace:
            raise ARException("Can't get workspace name. " + \
                              "Please set it while creating ARWorkspace object")
        else:
            self.current_workspace = workspace
            
    def workspace_dir_required(func):
        """
        Decorator for functions which should be called only
        in workspace directory.
        """
        def wrapper(self, *args):
            if self.nid_error:
                print "Cann't execute '%s' function" % func.__name__
                raise ARException(self.nid_error)
            else:
                func(self, *args)
        return wrapper
    
    def workspace_name_required(func):
        """Use it for functions which requires workspace's name (change, remove, etc.).
           """
        def wrapper(self, *args):
            if not self.current_workspace:
                print "Cann't execute '%s' function" % func.__name__
                raise ARException("Name of working workspace isn't set.")
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

    @workspace_name_required
    def change_name(self, name=""):
        return self.__change_parameter("name", name)
    
    @workspace_name_required
    def change_stream(self, stream=""):
        return self.__change_parameter("stream", stream)
    
    @workspace_name_required
    def change_location(self, location=""):
        return self.__change_parameter("location", location)

    @workspace_name_required
    def change_machinename(self, machinename=""):
        return self.__change_parameter("machinename", machinename)
    
    @workspace_name_required
    def __change_parameter(self, parameter, value=""):
        """This function is called when workspace's name, backed stream, location 
           or machine name should be changed.
           """
        
        params = {
                   "name"        : (self.current_workspace, ""),
                   "location"    : (self.current_location, "-l"),
                   "stream"      : (self.current_stream, "-b"),
                   "machinename" : (socket.gethostname(), "-m")
                   }
        
        if value:
            setattr(self, parameter,value)
        print "Changing workspace's %s to %s..." % \
                                (parameter, getattr(self, parameter))
        self.run("chws -w %s %s %s" % \
                 (self.current_workspace, params[parameter][1], getattr(self, parameter)), verbose=True)
        print "Done."
        sys.exit(0)
    
    
    @workspace_name_required
    def change(self):
        """Changes all parameters of workspace: location, stream, machine name.
           """ 
        
        if not getattr(self, "machinename", None):
            self.machinename = socket.gethostname()
        print "Changing workspace %s..." % self.current_workspace
        self.run("chws -w %s -l %s -b %s -m %s" % (self.current_workspace, self.location,
                                                   self.stream, self.machinename))
        print "Done."
        sys.exit(0)
    
    @workspace_name_required
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
    pass