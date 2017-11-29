To use, create `watcherConfig.txt` that contains entries like:

    [project_name]
    local_dir = /your/local/path
    remote_dir = /your/remote/path
    remote_addr = username@server
    remote_port = {port}

where remote_port is optional

TODO

* Have codeSync create the config files for you
* Extend makefile commands so that `make` isn't the only one
* Enable force-sync
* Sync both ways

Run `make`, which will install the required libraries and start the watcher. It will call `rsync` every time a change to a local_dir is made.
