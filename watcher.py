import configparser
import os
from subprocess import PIPE, Popen
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, *args, **kwargs):
        super(ChangeHandler, self).__init__()
        self._load_config()
        self._watch_dirs()

    def _load_config(self):
        self.conf = configparser.SafeConfigParser()
        self.conf.read(['watcherConfig.txt'])

    def _watch_dirs(self):
        self.observer = Observer()
        # dict of dir --> remote_dir mapping
        self.section_data = {}
        # TOOD: might be unnecessary to store conf in dict again
        for section in self.conf.sections():
            local_dir = self.conf.get(section, 'local_dir')
            self.section_data.setdefault(local_dir, []).append({
                'remote_dir': self.conf.get(section, 'remote_dir'),
                'remote_addr': self.conf.get(section, 'remote_addr'),
            })
            self.observer.schedule(self, local_dir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def make_subprocess_call(self, command):
        proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line)
        proc.communicate()

    def on_any_event(self, event):
        """React to any change from any of the dirs from the config"""
        remote_dir = None
        for key, data in self.section_data.items():
            # match the dir, primitive and probably could change
            if event.src_path.startswith(key):
                local_dir = key + '/'
                for item in data:
                    remote_dir = item['remote_dir']
                    remote_addr = item['remote_addr']
                    # ignore modified events related to the whole dir
                    if event.src_path == local_dir:
                        return
                    if remote_dir:
                        remote_file_path = "{}:{}".format(remote_addr, remote_dir)
                        exclude_string = "--include '.venv/src/' --exclude '.venv/*'"
                        call_str = "rsync -azvp --delete {} {} {}".format(exclude_string, local_dir, remote_file_path)
                        print('Running command: {}'.format(call_str))
                        self.make_subprocess_call(call_str)
                    else:
                        raise ValueError('Not sure where server is at :(')

def main():
        ChangeHandler()

if __name__ == '__main__':
    main()
