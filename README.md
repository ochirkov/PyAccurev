PyAccurev
=========

Python wrapper around Accurev VCS CLI commands

Getting Started
---------------


**ARPython Classes**
* ARException
* AccuRev
* ARWorkspace
 
**AccuRev Class**

Login/logout commands:


    from AR import AccuRev

    ar = AccuRev()
    ar.login('username', 'password')
    ...
    ar.logout()

This class also provides with all data that could be reached by "accurev info" command:
- current_user
- current_server
- current_port
- current_encoding
- current_bin
- current_depot
- current_workspace
- current_stream
- current_location

Here is an example of info usage:


    from AR import AccuRev
    
    ar = AccuRev()
    print ar.current_server # some-accurev-server.com
    print ar.current_user # (not logged in)
    ar.login('username', 'password')
    print ar.current_user # username


If current path is not associated with workspace or user is not logged in, all values connected to will be marked as "(undefined)". For changing root there is a method change_root():


    from AR import AccuRev
    
    ar = AccuRev()
    ar.login('username', 'password')
    print ar.current_depot # (undefined)
    ar.change_root('path/to/workspace')
    print ar.current_depot # Depot

**ARWorkspace Class**

Provides methods which are related to the workspace's actions:
- create
- change_name
- change_stream
- change_location
- change_machinename
- change
- remove
- update
- populate

There are two possibilities for using methods of this class.

**Navigate to folder associated with workspace:**


    from AR import AccuRev, ARWorkspace
    
    ar = AccuRev()
    ar.login('username', 'password')
    ar.change_root('path/to/workspace')
    w = ARWorkspace()
    w.change_name("new_workspace_name")

**Pass workspace name directly to class instance:**


    from AR import AccuRev, ARWorkspace
    
    ar = AccuRev()
    ar.login('username', 'password')
    w = ARWorkspace("workspace_name")
    w.change_name("new_workspace_name")
    

Changing of workspace could be made in two ways: by assigning new values and calling a function and by direct passing of parameter to the function e.g.:


    from AR import AccuRev, ARWorkspace
    
    ...
    w.name = "new_workspace_name"
    w.change_name()

or


    from AR import AccuRev, ARWorkspace
    
    ...
    w.change_name("new_workspace_name")


Function "change" should be used for changing of both stream and location of workspace and could be used for changing of machine name also:

    
    from AR import AccuRev, ARWorkspace
    
    ...
    w.stream = "dev.NewStream"
    w.location = "/path/to/new/location"
    w.machinename = "new_hostname" # not required
    w.change()

Functions "update" and "populate" work only in workspace's directory:


    from AR import AccuRev, ARWorkspace
    
    ar = AccuRev()
    ...
    ar.change_root('path/to/workspace')
    w = ARWorkspace()
    w.update()
