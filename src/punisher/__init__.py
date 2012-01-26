# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from argparse import ArgumentParser
from getpass import getuser
from threading import Event, Thread
import datetime
import os
import pickle
import random
import sys
import time

from foxxy.daemon import Daemon
from pyutmp import UtmpFile

from punisher.punishments import PUNISHMENTS

# Ensure the config directory exists.
_CONFIG_DIR = os.path.expanduser('~/.punisher')
if not os.path.isdir(_CONFIG_DIR):
    os.mkdir(_CONFIG_DIR, 0700)

class Punisher(object):
    def __init__(self, punishments=None, safe_mode=True):
        self._punishments = \
                punishments if punishments is not None else PUNISHMENTS
        self.safe_mode = safe_mode
        self._dont_punish = Event()

    def _punish(self):
        punishment = random.choice(self._punishments)
        if self.safe_mode:
            print('[SAFE MODE] %s' % punishment, file=sys.stderr)
            return
        punishment.punish()
        self._cleanup()

    def _cleanup(self):
        os.remove(os.path.expanduser('~/.ssh/rc'))

    def _wait(self, punish_in):
        if not self._dont_punish.wait(punish_in):
            self._punish()

    def configure(self, names=None):
        config_path = os.path.join(_CONFIG_DIR, 'config')
        if os.path.isfile(config_path):
            with open(config_path) as config_file:
                config = pickle.load(config_file)
        else:
            config = {}
        punishments = set()
        for punishment_class in self._punishments:
            if names is not None and punishment_class.__name__ not in names:
                continue
            punishment = punishment_class(self)
            if punishment.requires_configuration:
                fullname = '%s.%s' % (punishment_class.__module__,
                    punishment_class.__name__)
                punishment.configure(config.setdefault(fullname, {}))
            if punishment.enabled:
                punishments.add(punishment)
        self._punishments = tuple(punishments)
        if not self._punishments:
            raise PunisherError('no punishments')
        print('Punishments loaded: %s' % ' '.join(map(str, self._punishments)))
        with open(config_path, 'w') as config_file:
            pickle.dump(config, config_file)

    def start(self, punish_in):
        with open(os.path.expanduser('~/.ssh/rc'), 'w') as ssh_rc:
            ssh_rc.write(os.path.expandvars('killall -u $USER sshd\n'))
        self._timer = Thread(target=self._wait, args=(punish_in,))
        self._timer.start()

    def stop(self):
        self._dont_punish.set()
        self._cleanup()

    def wait(self):
        while self._timer.is_alive():
            self._timer.join(1)


class PunisherDaemon(Daemon):
    def __init__(self, *args, **kwargs):
        pid_path = os.path.join(_CONFIG_DIR, 'pid')
        super(PunisherDaemon, self).__init__(pid_path, *args, **kwargs)

    def run(self, punisher, *args, **kwargs):
        os.nice(20)
        self._punisher = punisher
        self._punisher.start(*args, **kwargs)
        self._punisher.wait()

    def on_stop(self):
        self._punisher.stop()


def is_remote_user():
    tty = os.ttyname(sys.stdin.fileno())
    for utmp in UtmpFile():
        if utmp.ut_user_process and utmp.ut_line == tty:
            return bool(utmp.ut_addr)
    raise ValueError('could not find tty')

def compute_time(time_str):
    offset = time_str.startswith('+')
    if offset:
        time_str = time_str[1:]
    time = datetime.datetime.strptime(time_str, '%H:%M:%S').time()
    if offset:
        return datetime.timedelta(hours=time.hour, minutes=time.minute,
                                  seconds=time.second).total_seconds()
    else:
        today = datetime.datetime.today()
        now = today.time()
        if time <= now:
            date = (today + datetime.timedelta(days=1)).date()
        else:
            date = today
        time = datetime.datetime.combine(date, time)
        return (time - today).total_seconds()

def build_argument_parser():
    argument_parser = ArgumentParser()
    subparser = argument_parser.add_subparsers(dest='command')
    subparser.add_parser('status')
    start = subparser.add_parser('start')
    start.add_argument('-a', '--arm', action='store_false', default=True,
                       dest='safe_mode')
    start.add_argument('-p', '--punishments')
    start.add_argument('time')
    stop = subparser.add_parser('stop')
    return argument_parser

def main(argv=None):
    if argv is None:
        argv = sys.argv
    argument_parser = build_argument_parser()
    args = argument_parser.parse_args(args=argv[1:])

    punisher_daemon = PunisherDaemon()

    command = args.command
    if command == 'status':
        print('The punisher %s running' 
                % ('IS' if punisher_daemon.is_running() else 'IS NOT'))
    elif command == 'start':
        punisher = Punisher(safe_mode=args.safe_mode)
        if args.punishments:
            punishments = args.punishments.split(':')
        else:
            punishments = None
        punisher.configure(names=punishments)
        punisher_daemon.start(punisher, compute_time(args.time))
    elif command == 'stop':
        if is_remote_user():
            print('Get up out of bed and turn me off in person.')
        else:
            punisher_daemon.stop()

    return 0

if __name__ == '__main__':
    exit(main())

