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

from supybot.test import *

class JabbarTestCase(PluginTestCase):
    plugins = ('Jabbar',)

    def testJabbar(self):
        # difficult to test, let's just make sure it works
        self.assertNotError('jabbar')

    def testSeed(self):
        # just make sure it works
        self.assertNotError('seed 20')
        
        
    def testSample(self):
        self.assertError('sample 20 foo')
        self.assertResponse('sample 1 foo', 'foo')
        self.assertRegexp('sample 2 foo bar', '... and ...')
        self.assertRegexp('sample 3 foo bar baz', '..., ..., and ...')

    def testDiceRoll(self):
        self.assertActionRegexp('diceroll', 'rolls a \d')

    def testSeedActuallySeeds(self):
        # now to make sure things work repeatably
        self.assertNotError('seed 20')
        m1 = self.getMsg('random')
        self.assertNotError('seed 20')
        m2 = self.getMsg('random')
        self.failUnlessEqual(m1, m2)
        m3 = self.getMsg('random')
        self.failIfEqual(m2, m3)

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
