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

import time
import string
import random
import supybot.utils as utils
import supybot.world as world
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.schedule as schedule
import supybot.callbacks as callbacks

class Lazor(callbacks.Plugin):
    """Add the help for "@plugin help Lazor" here
    This should describe *how* to use this plugin."""
    threaded = True
    
    def __init__(self, irc):
        self.__parent = super(Lazor, self)
        self.__parent.__init__(irc)
        self.rng = random.Random()
        self.rng.seed()
        self.bombs = {}
        self.lastBomb = ""
        self.talktimes = {}


    def doPrivmsg(self, irc, msg):
        self.talktimes[msg.nick] = time.time()


    def doJoin(self, irc, msg):
        if self.registryValue('joinIsActivity', msg.args[0]):
            self.talktimes[msg.nick] = time.time()
    
    class LazorBlast():
        def __init__(self, irc, victim, detonateTime, channel, sender, debug):
            self.victim = victim
            self.startTime = time.time();
            self.detonateTime = detonateTime
            self.active = True
            self.channel = channel
            self.sender = sender
            self.irc = irc
            self.debug = debug
            self.thrown = False
            self.responded = False
            self.rng = random.Random()
            self.rng.seed()
            if self.debug:
                self.irc.reply('I just created a lazor in %s' % channel)
            def detonate():
                self.detonate(irc)
            schedule.addEvent(detonate, self.startTime + self.detonateTime, '%s_lazor' % self.channel)
            formattedTime = "%02d:%02d:%02d" % (detonateTime / 3600, detonateTime / 60, detonateTime % 60)
            irc.reply ("IMMA CHARGIN MAH LAZOR")
            s = 'charges his lazor'
            self.irc.queueMsg(ircmsgs.action(self.channel, s))

        def throw(self, irc, thrownObject):
                schedule.removeEvent('%s_bomb' % self.channel)
                self.detonate(irc)

		"""
        def duck(self, irc, ducker):
            if self.thrown and ircutils.nickEqual(self.victim, ducker):
                self.irc.queueMsg(ircmsgs.privmsg(self.channel, '%s ducks!  The bomb misses, and explodes harmlessly a few meters away.' % self.victim))
                self.active = False
                self.thrown = False
                schedule.removeEvent('%s_bomb' % self.channel)
		"""

        def detonate(self, irc):
            self.active = False
            #if self.showCorrectWire:
            #    self.irc.reply('Should\'ve gone for the %s wire!' % self.goodWire)

            self.irc.sendMsg(ircmsgs.privmsg(self.channel, ' .___                                     '))
            self.irc.sendMsg(ircmsgs.privmsg(self.channel, ' (,) O/```````````````````````````````````'))
            self.irc.sendMsg(ircmsgs.privmsg(self.channel, 'c   [|                              >->o  '))
            self.irc.sendMsg(ircmsgs.privmsg(self.channel, '      \___________________________________'))
            self.active = False
            self.thrown = False
            self.irc.queueMsg(ircmsgs.kick(self.channel, self.victim, 'shoop da woop') )
            
                        
            def reinvite():
                if not self.victim in irc.state.channels[self.channel].users:
                    self.irc.queueMsg(ircmsgs.invite(self.victim, self.channel))
            if not self.responded:
                schedule.addEvent(reinvite, time.time()+5)
                

    def lazor(self, irc, msg, args, channel, victim ):
        """<nick>

        For lazoring people!"""
        channel = ircutils.toLower(channel)
        
        if irc.nick in irc.state.channels[channel].ops:
            pass
        else:
            irc.reply("OPS FOOL")
            return
        #if not self.registryValue('allowLazor', msg.args[0]):
        #    irc.noReply()
        #    return
        try:
            if self.bombs[channel].active:
                irc.reply('ALREADY CHARGIN')
                return
                
        except KeyError:
            pass
        if victim == irc.nick :
            irc.reply('no')
            return
        victim = string.lower(victim)
        found = False
        for nick in list(irc.state.channels[channel].users):
            if victim == string.lower(nick):
                victim = nick
                found = True
        if not found:
            irc.reply('Error: nick not found.')
            return
        detonateTime = self.rng.randint(self.registryValue('minTime', msg.args[0]), self.registryValue('maxTime', msg.args[0]))

        if self.registryValue('debug'):
            irc.reply('I\'m about to create a bomb in %s' % channel)
        self.bombs[channel] = self.LazorBlast(irc, victim, detonateTime,  channel, msg.nick, self.registryValue('debug'))
        if self.registryValue('debug'):
            irc.reply('This message means that I got past the bomb creation line in the timebomb command')
    lazor = wrap( lazor, ['Channel', ('checkChannelCapability', 'timebombs'), 'somethingWithoutSpaces'])

    def doNick(self, irc, msg):
        oldNick = msg.nick
        newNick = msg.args[0]
        for key in self.bombs:
            if self.bombs[key].victim == oldNick:
                print("Lazor dodger found!")
                self.bombs[key].victim = newNick


Class = Lazor


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
