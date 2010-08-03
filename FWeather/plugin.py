###
# Copyright (c) 2010, futurestack
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import thefuckingweather
import random
#from optparse import OptionParser
import re

class FWeather(callbacks.Plugin):
    """Add the help for "@plugin help Blank" here
    This should describe *how* to use this plugin."""
    pass

    
    def weather(self, irc, msg, args, text):
        """[<text>]

       Decide between n items separated by commas.
        """
        found = text.find("-c")
        result = False
        if( found > -1 ):
            #irc.reply("celsius detected.")
            text = text.replace("-c","")
            #irc.reply(text)
            result = True
        w = thefuckingweather.get_weather(text, result)
        w_tuple = (      w["current"]["temperature"],
                         'degrees',
                         "\n".join(w["current"]["weather"]),
                         w["current"]["remark"])
        result = """%d %s?! %s (%s)""" % w_tuple
        result = result.replace('\n','. ')
        irc.reply(result)
    weather = wrap(weather, [additional('text')])


Class = FWeather


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
