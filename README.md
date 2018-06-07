To use, create `watcherConfig.txt` that contains entries like:

    [project_name]
    local_dir = /your/local/path
    remote_dir = /your/remote/path
    remote_addr = username@server
    remote_port = {port}
    
    [project_name]
    local_dir = /your/local/path
    remote_dir = /app
    remote_addr = server

Additionally, you can set file types to ignore by adding the attribute below:

`ignore_filetypes = .so*`

You can also comma-delimit them to add multiple:

`ignore_filetypes = .so*,.cpp`

This is useful if you have embedded c++ code in your project and the machine you're syncing to isn't the same type of machine as the one you're developing on.

where remote_port is optional, and `server` could be an alias set in your ~/.ssh/config

TODO

* Have codeSync create the config files for you
* Extend makefile commands so that `make` isn't the only one
* Enable force-sync
* Sync both ways

Run `make`, which will install the required libraries and start the watcher. It will call `rsync` every time a change to a local_dir is made.
