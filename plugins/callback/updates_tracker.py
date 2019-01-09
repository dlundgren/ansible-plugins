# -*- coding: utf-8 -*-
# Ansible callback plugin for watching the list of restarted & rebooted hosts
#
# (c) 2018 David Lundgren <dlundgren@syberisle.net>
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = '''
    callback: updates_tracker
    type: notification
    short_description: Monitors Reboot & Restart events
    version_added: "2.7"
    options:
      use_updates_tracker:
        description: Whether or not use this callback
        required: False
        default: False
'''

import os
from datetime import datetime
from collections import defaultdict
import json
import time

from ansible.plugins.callback import CallbackBase

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'updatestracker'
    CALLBACK_NEEDS_WHITELIST = False

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.disabled = False
        self.rebooted = set()
        self.updated = set()

    def v2_playbook_on_play_start(self, play):
        self.disabled = not play.vars.get('use_updates_tracker', False)

    def playbook_on_notify(self, host, handler):
        if self.disabled:
            return
        if 'system rebooted' in handler.get_name():
            self.rebooted.add(host.get_name())
        if 'system updated' in handler.get_name():
            self.updated.add(host.get_name())

    def v2_playbook_on_stats(self, stats):
        if self.disabled:
            return
        # list of non-rebooted
        if not self.rebooted and not self.updated:
            self._display.display("No systems updated or rebooted")
            return

        updated_only = self.updated - self.rebooted
        if updated_only:
            self._display.display("updated: %s"  % " ".join(updated_only))

        rebooted = self.rebooted - updated_only
        if rebooted:
            self._display.display("updated / rebooted: %s" % " ".join(rebooted))
