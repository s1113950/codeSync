To use, create `watcherConfig.txt` that contains entries like:

    [folder_name]
    local_dir = /your/local/path
    remote_dir = /your/remote/path
    remote_addr = username@server


The creation of this (and migration to .watcherConfigrc) will come later in the future.

Run `make`, which will install the required libraries and start the watcher. It will call `rsync` every time a change to a local_dir is made. In the future, there'll be optimizations to sync only once every time anything in a folder changes as opposed to on every file change.
