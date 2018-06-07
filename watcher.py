from __future__ import print_function

import configparser
import os
from subprocess import PIPE, Popen
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ObjectList(list):
    """a way to store vars on a list"""
    pass


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, *args, **kwargs):
        super(ChangeHandler, self).__init__()
        self._load_config()
        self._watch_dirs()

    def _load_config(self):
        """loads self.conf from watcherConfig.txt"""
        self.conf = configparser.SafeConfigParser()
        self.conf.read(['watcherConfig.txt'])

    def _watch_dirs(self):
        """sets up the watchdog observer and schedules sections to watch"""
        self.observer = Observer()
        self._schedule_sections()
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def _schedule_sections(self):
        """creates section data dir for later reference
           and schedules each conf section with the observer
        """
        # dict of dir --> remote_dir mapping
        self.section_data = {}
        # TOOD: might be unnecessary to store conf in dict again
        for section in self.conf.sections():
            local_dir = self.conf.get(section, 'local_dir')
            # TODO: I thought a 3rd optional arg was allowed?
            # TODO: there's gotta be a better way to load default args
            try:
                remote_port = self.conf.get(section, 'remote_port')
            except configparser.NoOptionError:
                remote_port = None
            try:
                ignore_filetypes = self.conf.get(section, 'ignore_filetypes')
            except configparser.NoOptionError:
                ignore_filetypes = ''
            self.section_data.setdefault(local_dir, ObjectList()).append({
                'remote_dir': self.conf.get(section, 'remote_dir'),
                'remote_addr': self.conf.get(section, 'remote_addr'),
                'remote_port': remote_port,
                'ignore_filetypes': ignore_filetypes.split(',')
            })
            self.observer.schedule(self, local_dir, recursive=True)
            # last_updated time will be used to prevent oversyncing
            self.section_data[local_dir].last_updated = 0

    def _should_sync_dir(self, event, key, local_dir):
        """returns True if dir syncing should happen
           also updates the last modified time of the folder in the process"""
        # some files get removed before sync (ie git locks)
        file_updated_time = os.stat(
            event.src_path if os.path.exists(event.src_path)
            else local_dir).st_mtime
        if file_updated_time > self.section_data[key].last_updated:
            self.section_data[key].last_updated = file_updated_time
            return True
        else:
            return False

    def _sync_dir(self, data, local_dir):
        """Creates the sync command and runs a subprocess call to sync"""
        for item in data:
            remote_dir = item['remote_dir']
            remote_addr = item['remote_addr']
            remote_port = item['remote_port']
            ignore_filetypes = item['ignore_filetypes']
            if remote_dir:
                if remote_port:
                    remote_file_path = "rsync://{}:{}{}".format(
                        remote_addr, remote_port, remote_dir)
                else:
                    remote_file_path = "{}:{}".format(remote_addr, remote_dir)
                include_and_exclude_args = self._get_include_and_exclude_args(
                    ignore_filetypes)
                call_str = "rsync -azvp --delete -e ssh {} {} {}".format(
                    include_and_exclude_args, local_dir, remote_file_path)
                print('Running command: {}'.format(call_str))
                self._make_subprocess_call(call_str)
            else:
                raise ValueError('Not sure where server is at :(')

    def _get_include_and_exclude_args(self, ignore_filetypes):
        """creates the string of files to exclude
           by default includes code in .venv/src and excludes the rest
           of the venv and pyc files
        """
        args = "--include '.venv/src/' " + \
            "--exclude '.venv/*' --exclude '*.pyc' "
        for filetype in ignore_filetypes:
            args += '--exclude ' + filetype + ' '
        return args

    def _make_subprocess_call(self, command):
        """Runs the subprocess call to sync code"""
        proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line, end="")
        proc.communicate()

    def on_any_event(self, event):
        """React to any change from any of the dirs from the config"""
        remote_dir = None
        for key, data in self.section_data.items():
            # match the dir, primitive and probably could change
            if event.src_path.startswith(key):
                local_dir = key + '/'
                if self._should_sync_dir(event, key, local_dir):
                    self._sync_dir(data, local_dir)


def main():
    ChangeHandler()


if __name__ == '__main__':
    main()
