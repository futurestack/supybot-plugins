###
# Copyright (c) 2010, quantumlemur
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

import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Lazor', True)


Lazor = conf.registerPlugin('Lazor')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Lazor, 'someConfigVariableName',
#     registry.Boolean(False, """Help for someConfigVariableName."""))

conf.registerChannelValue(Lazor, 'exclusions',
        registry.SpaceSeparatedListOfStrings([], 
        """A list of nicks who should be excluded from being 
            randombombed"""))

conf.registerChannelValue(Lazor, 'allowBombs', 
        registry.Boolean(True, """Determines whether timebombs are allowed 
            in the channel."""))

conf.registerChannelValue(Lazor, 'minTime',
        registry.PositiveInteger(45, """Determines the minimum time of a 
            timebomb timer, in seconds."""))

conf.registerChannelValue(Lazor, 'maxTime',
        registry.PositiveInteger(600, """Determines the maximum time of a 
            timebomb timer, in seconds."""))

conf.registerGlobalValue(Lazor, 'debug',
        registry.Boolean(False, """Determines whether debugging info will be
            shown."""))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
