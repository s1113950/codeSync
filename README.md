# Usage

Create `watcherConfig.txt` that contains entries like:

    [project_name]
    local_dir = /your/local/path
    remote_dir = /your/remote/path
    remote_addr = username@server
    remote_port = {port}
    
    [project_name]
    local_dir = /your/local/path
    remote_dir = /app
    remote_addr = {username@server|server}
    languages = {c++|all}
    ignore_filetypes = {.so*|.so*,.cpp...}
    file_delete = {True|False}

Language, remote_port, ignore_filetypes are optional

`ignore_filetypes` is useful if you have embedded c++ code in your project and the machine you're syncing to isn't the same type of machine as the one you're developing on.

The `all` language will sync the entired directory over. By default the language is `python`

`file_delete` will default to True, but if set to False will not delete files on remote if they don't exist on local. This is useful for building env-specific stuff that you don't want overwritten by a different env (or if you don't build on local because you can't or something).

`server` can be an alias set in your `~/.ssh/config`

Run `make`, which will install the required libraries and start the watcher. It will call `rsync` every time a change to a local_dir is made.

## TODO
* Have codeSync create the config files for you
* Extend makefile commands so that `make` isn't the only one
* Enable force-sync
* Sync both ways
