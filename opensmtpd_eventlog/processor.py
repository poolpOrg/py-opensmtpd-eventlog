#! /usr/bin/env python3
#
# Copyright (c) 2018 Gilles Chehade <gilles@poolp.org>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import time
import os.path

from opensmtpd.filters import smtp_in, proceed, reject, dataline

TIMEFRAME = 86400

class EventLog():
    def __init__(self, directory):
        self.directory = directory
        self.stream = smtp_in()
        self.stream.on_event(self.writeln, self)
        self.filep = None
        self.timeframe = None
        os.makedirs(directory, exist_ok = True)
        
    def run(self):
        self.stream.run()

    def writeln(self, ctx, event):
        kind, version, timestamp = event.split('|')[0:3]
        ctime = int(time.time())
        timeframe = ctime - (ctime % TIMEFRAME)

        if self.timeframe != timeframe:
            if self.filep:
                self.filep.close()
                self.filep = None

        if not self.filep:
            self.filep = open(os.path.join(self.directory, str(timeframe)), "a+")
            self.timeframe = timeframe
            
        self.filep.write(event + "\n")
        self.filep.flush()
