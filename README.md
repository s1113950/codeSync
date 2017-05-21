To use, create `watcherConfig.txt` that contains entries like:

    [project_name]
    local_dir = /your/local/path
    remote_dir = /your/remote/path
    remote_addr = username@server


TODO

* Have codeSync create the config files for you
* Extend makefile commands so that `make` isn't the only one

Run `make`, which will install the required libraries and start the watcher. It will call `rsync` every time a change to a local_dir is made.
