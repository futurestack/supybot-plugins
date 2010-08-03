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

class Timebomb(callbacks.Plugin):
    """Add the help for "@plugin help Timebomb" here
    This should describe *how* to use this plugin."""
    threaded = True
    
    def __init__(self, irc):
        self.__parent = super(Timebomb, self)
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
    
    class Bomb():
        def __init__(self, irc, victim, wires, detonateTime, goodWire, channel, sender, showArt, showCorrectWire, debug):
            self.victim = victim
            self.startTime = time.time();
            self.detonateTime = detonateTime
            self.wires = wires
            self.goodWire = goodWire
            self.active = True
            self.channel = channel
            self.sender = sender
            self.irc = irc
            self.showArt = showArt
            self.showCorrectWire = showCorrectWire
            self.debug = debug
            self.thrown = False
            self.responded = False
            self.rng = random.Random()
            self.rng.seed()
            if self.debug:
                self.irc.reply('I just created a bomb in %s' % channel)
            def detonate():
                self.detonate(irc)
            schedule.addEvent(detonate, self.startTime + self.detonateTime, '%s_bomb' % self.channel)
            formattedTime = "%02d:%02d:%02d" % (detonateTime / 3600, detonateTime / 60, detonateTime % 60)
            s = 'stuffs a bomb down %s\'s pants.  The display reads [%s].  The wires are: %s.' % (self.victim, formattedTime, utils.str.commaAndify(wires))
            self.irc.queueMsg(ircmsgs.action(self.channel, s))
            if self.victim == irc.nick:
                time.sleep(1)
                cutWire = self.rng.choice(self.wires)
                self.irc.queueMsg(ircmsgs.privmsg(self.channel, '@cutwire %s' % cutWire))
                time.sleep(1)
                self.cutwire(self.irc, cutWire)

        def cutwire(self, irc, cutWire):
            self.cutWire = cutWire
            self.responded = True
            if self.goodWire.lower() == self.cutWire.lower():
                self.irc.queueMsg(ircmsgs.privmsg(self.channel, '%s has cut the %s wire!  This has defused the bomb!' % (self.victim, self.cutWire)))
                self.irc.queueMsg(ircmsgs.privmsg(self.channel, 'He then quickly rearms the bomb and throws it back at %s with just seconds on the clock!' % self.sender))
                self.victim = self.sender
                self.thrown = True
                schedule.rescheduleEvent('%s_bomb' % self.channel, time.time() + 5)
                if self.victim == irc.nick:
                    time.sleep(1)
                    self.irc.queueMsg(ircmsgs.privmsg(self.channel, '@duck'))
                    time.sleep(1)
                    self.duck(self.irc, irc.nick)
            else:
                schedule.removeEvent('%s_bomb' % self.channel)
                self.detonate(irc)

        def duck(self, irc, ducker):
            if self.thrown and ircutils.nickEqual(self.victim, ducker):
                self.irc.queueMsg(ircmsgs.privmsg(self.channel, '%s ducks!  The bomb misses, and explodes harmlessly a few meters away.' % self.victim))
                self.active = False
                self.thrown = False
                schedule.removeEvent('%s_bomb' % self.channel)

        def detonate(self, irc):
            fairnessInvert = False
            if not self.responded:

                if self.sender in irc.state.channels[self.channel].ops and not self.victim in irc.state.channels[self.channel].ops:
                    print(" Sender has ops and victim does not! Throwing for a fairness detonation inversion!" )
                    randNum = self.rng.randint(0,4)
                    if randNum == 0 :
                        irc.reply("The bomb goes klunk.")
                        fairnessInvert = True
                        self.irc.queueMsg(ircmsgs.op(self.channel, self.victim) )
                    else:
                        print "Throw failed."
                    
            self.active = False
            #if self.showCorrectWire:
            #    self.irc.reply('Should\'ve gone for the %s wire!' % self.goodWire)
            if self.showArt:
                self.irc.sendMsg(ircmsgs.privmsg(self.channel, '  (}                  ,^.      .                    .'))
                self.irc.sendMsg(ircmsgs.privmsg(self.channel, ' / \\\\/\.  `      `._-\'   \'`-~.            .'))
                self.irc.sendMsg(ircmsgs.privmsg(self.channel, ' \, \`            )    __   (        .'))
                self.irc.sendMsg(ircmsgs.privmsg(self.channel, ' .  /       .   -<    //\\\\   `_-  .'))
                self.irc.sendMsg(ircmsgs.privmsg(self.channel, '    `           . )  //  \\\\  (   \'     P A N T S P L O D E'))
            detonateMsg = "BOOM!"
            if self.thrown:
                detonateMsg = "KA" + detonateMsg
            else:
                if self.showCorrectWire :
                    detonateMsg += " (it was %s)" % self.goodWire
            self.active = False
            self.thrown = False
            
            if fairnessInvert:
                #self.irc.queueMsg(irc.reply("The bomb goes klunk.") )
                print "Fairness invert activated!"
                newVictim = self.sender
                self.sender = self.victim
                self.victim = newVictim
                #irc.reply("The bomb goes beep!"))
                #time.sleep(10)
            else:
                self.irc.queueMsg(ircmsgs.kick(self.channel, self.victim, detonateMsg) )
                        
            def reinvite():
                if not self.victim in irc.state.channels[self.channel].users:
                    self.irc.queueMsg(ircmsgs.invite(self.victim, self.channel))
            if not self.responded:
                schedule.addEvent(reinvite, time.time()+5)
                
    
    def duck(self, irc, msg, args, channel):
        """takes no arguments

        DUCK!"""
        channel = ircutils.toLower(channel)
        try:
            if not self.bombs[channel].active:
                return
        except KeyError:
            return
        self.bombs[channel].duck(irc, msg.nick)
        irc.noReply()
    duck = wrap(duck, ['Channel'])

   
    def randombomb(self, irc, msg, args, channel, nicks):
        """takes no arguments

        Bombs a random person in the channel
        """
        channel = ircutils.toLower(channel)
        if not self.registryValue('allowBombs', msg.args[0]):
            irc.noReply()
            return
        try:
            if self.bombs[channel].active:
                irc.reply('There\'s already an active bomb, in %s\'s pants!' % self.bombs[channel].victim)
                return
        except KeyError:
            pass
        if self.registryValue('bombActiveUsers', msg.args[0]):
            if len(nicks) == 0:
                nicks = list(irc.state.channels[channel].users)
                items = self.talktimes.iteritems()
                nicks = []
                for i in range(0, len(self.talktimes)):
                    try:
                        item = items.next()
                        if time.time() - item[1] < self.registryValue('idleTime', msg.args[0])*60 and item[0] in irc.state.channels[channel].users:
                            nicks.append(item[0])
                    except StopIteration:
                        irc.reply('hey quantumlemur, something funny happened... I got a StopIteration exception')
                if len(nicks) == 1 and nicks[0] == msg.nick:
                    nicks = []
            if len(nicks) == 0:
                irc.reply('Well, no one\'s talked in the past hour, so I guess I\'ll just choose someone from the whole channel')
                nicks = list(irc.state.channels[channel].users)
            elif len(nicks) == 2:
                irc.reply('Well, it\'s just been you two talking recently, so I\'m going to go ahead and just bomb someone at random from the whole channel')
                nicks = list(irc.state.channels[channel].users)
        elif len(nicks) == 0:
            nicks = list(irc.state.channels[channel].users)
        if irc.nick in nicks and not self.registryValue('allowSelfBombs', msg.args[0]):
            nicks.remove(irc.nick)
        #####
        #irc.reply('These people are eligible: %s' % utils.str.commaAndify(nicks))
        victim = self.rng.choice(nicks)
        while victim == self.lastBomb or victim in self.registryValue('exclusions', msg.args[0]):
            victim = self.rng.choice(nicks)
        self.lastBomb = victim
        detonateTime = self.rng.randint(self.registryValue('minRandombombTime', msg.args[0]), self.registryValue('maxRandombombTime', msg.args[0]))
        wireCount = self.rng.randint(self.registryValue('minWires', msg.args[0]), self.registryValue('maxWires', msg.args[0]))
        if wireCount > 6:
            colors = self.registryValue('shortcolors')
        else:
            colors = self.registryValue('colors')
        wires = self.rng.sample(colors, wireCount)
        goodWire = self.rng.choice(wires)
        self.bombs[channel] = self.Bomb(irc, victim, wires, detonateTime, goodWire, channel, msg.nick, self.registryValue('showArt', msg.args[0]), self.registryValue('showCorrectWire', msg.args[0]), self.registryValue('debug'))
        try:
            irc.noReply()
        except AttributeError:
            pass
    randombomb = wrap(randombomb, ['Channel', any('NickInChannel')])

 
    def timebomb(self, irc, msg, args, channel, victim ):
        """<nick>

        For bombing people!"""
        channel = ircutils.toLower(channel)
        
        if irc.nick in irc.state.channels[channel].ops:
            pass
        else:
            irc.reply("I can't timebomb properly without ops now, can I?")
            return
        if not self.registryValue('allowBombs', msg.args[0]):
            irc.noReply()
            return
        try:
            if self.bombs[channel].active:
                irc.reply('There\'s already an active bomb, in %s\'s pants!' % self.bombs[channel].victim)
                return
        except KeyError:
            pass
        if victim == irc.nick and not self.registryValue('allowSelfBombs', msg.args[0]):
            irc.reply('You really expect me to bomb myself?  Stuffing explosives into my own pants isn\'t exactly my idea of fun.')
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
        wireCount = self.rng.randint(self.registryValue('minWires', msg.args[0]), self.registryValue('maxWires', msg.args[0]))
        if wireCount > 6:
            colors = self.registryValue('shortcolors')
        else:
            colors = self.registryValue('colors')
        wires = self.rng.sample(colors, wireCount)
        goodWire = self.rng.choice(wires)
        if self.registryValue('debug'):
            irc.reply('I\'m about to create a bomb in %s' % channel)
        self.bombs[channel] = self.Bomb(irc, victim, wires, detonateTime, goodWire, channel, msg.nick, self.registryValue('showArt', msg.args[0]), self.registryValue('showCorrectWire', msg.args[0]), self.registryValue('debug'))
        if self.registryValue('debug'):
            irc.reply('This message means that I got past the bomb creation line in the timebomb command')
    timebomb = wrap(timebomb, ['Channel', ('checkChannelCapability', 'timebombs'), 'somethingWithoutSpaces'])

    def timeleft(self, irc, msg, args ):
        channel = msg.args[0]
        if not self.registryValue('allowBombs', msg.args[0]):
            irc.noReply()
            return
        try:
            if self.bombs[channel].active:
                detonateTime = self.bombs[channel].detonateTime
                startTime = self.bombs[channel].startTime
                mCurrentTime = time.time();
                timeLeft =  (startTime + detonateTime ) - mCurrentTime;
                #irc.reply(" detonate: %02d start: %02d, current: %02d, left: %02d" % ( detonateTime, startTime, mCurrentTime, timeLeft ) )
                formattedTime = "%02d:%02d:%02d" % (timeLeft / 3600, timeLeft / 60, timeLeft % 60)
                ss  = 'The display reads [%s].' % (formattedTime,)
                irc.reply(ss)                
                return
            else:
                irc.reply("No active time bomb at the moment.")
        except KeyError:
            pass
    timeleft = wrap(timeleft)
    
    def wires(self, irc, msg, args ):
        channel = msg.args[0]
        if not self.registryValue('allowBombs', msg.args[0]):
            irc.noReply()
            return
        try:
            if self.bombs[channel].active:
                s = 'The wires are: %s.' % ( utils.str.commaAndify( self.bombs[channel].wires))
                irc.reply(s)
                return
            else:
                irc.reply("No active time bomb at the moment.")
        except KeyError:
            pass
    wires = wrap(wires)
    

    def goodwire(self, irc, msg, args ):
        channel = msg.args[0]
        if not self.registryValue('allowBombs', msg.args[0]):
            irc.noReply()
            return
        try:
            if not ircutils.nickEqual(self.bombs[channel].victim, msg.nick):
                irc.reply("You can't see the wires from there.")
                return
            else:
                self.responded = True
                
            if self.bombs[channel].active:
                randNum = self.rng.randint(0,6)
                if randNum == 0 :
                    s = "uhhhhh uhhhh I think it's the %s wire!" % ( self.bombs[channel].goodWire)
                else:
                    s = "they're all %s wires!" % self.rng.choice(self.bombs[channel].wires)
                irc.reply( s.upper())
                return
            else:
                irc.reply("No active time bomb at the moment.")
        except KeyError:
            pass
    goodwire = wrap(goodwire)

    def doNick(self, irc, msg):
        oldNick = msg.nick
        newNick = msg.args[0]
        for key in self.bombs:
            if self.bombs[key].victim == oldNick:
                print("Bomb dodger found!")
                self.bombs[key].victim = newNick

    def cutwire(self, irc, msg, args, channel, cutWire):
        """<colored wire>

        Will cut the given wire if you've been timebombed."""
        channel = ircutils.toLower(channel)
        try:
            if not self.bombs[channel].active:
                return
            if not ircutils.nickEqual(self.bombs[channel].victim, msg.nick):
                irc.reply('You can\'t cut the wire on someone else\'s bomb!')
                return
            else:
                self.responded = True

            spellCheck = False
            for item in self.bombs[channel].wires :
                if item.lower() == cutWire.lower():
                    spellCheck = True
            if spellCheck == False :
                irc.reply("That doesn't appear to be one of the options.")
                return
                
            self.bombs[channel].cutwire(irc, cutWire)
        except KeyError:
            pass
        irc.noReply()
    cutwire = wrap(cutwire, ['Channel', 'something'])

    """
    def detonate(self, irc, msg, args, channel):
        "/""Takes no arguments

        Detonates the active bomb.""/"
        channel = ircutils.toLower(channel)
        try:
            if self.bombs[channel].active:
                schedule.rescheduleEvent('%s_bomb' % channel, time.time())
        except KeyError:
            if self.registryValue('debug'):
                irc.reply('I tried to detonate a bomb in "%s"' % channel)
                irc.reply('List of bombs: %s' % self.bombs.keys())
        irc.noReply()
    detonate = wrap(detonate, [('checkChannelCapability', 'op')])
    """

Class = Timebomb


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
