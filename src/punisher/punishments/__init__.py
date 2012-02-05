from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from types import TypeType

class Punishment(object):
    enabled = False
    requires_configuration = False

    def __init__(self, punisher):
        self._punisher = punisher

    def __str__(self):
        return self.__class__.__name__

    def configure(self, settings):
        raise NotImplementedError

    def punish(self):
        raise NotImplementedError('punishment not implemented')


# ==============================================================================
# = Installed punishments                                                      =
# ==============================================================================
from punisher.punishments.olive import DeleteHomeDirPunishment
from punisher.punishments.olive import HurtfulTwitterPost
from punisher.punishments.olive import OffensiveEmail
from punisher.punishments.olive import TestPunishment
# ==============================================================================

def _build_punishment_set():
    punishements = set()
    for obj in globals().itervalues():
        if obj is not Punishment and isinstance(obj, TypeType) \
                and issubclass(obj, Punishment):
            punishements.add(obj)
    return punishements
PUNISHMENTS = _build_punishment_set()

