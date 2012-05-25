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
import random
import urllib

class Jabbar(callbacks.Plugin):
    """Add the help for "@plugin help Jabbar" here
    This should describe *how* to use this plugin."""

    def myReadFile(self, path):
        """reads a file to a list"""
        f = open(path,'r')
        result = f.readlines()
        f.close
        return result
        
    def myWriteFile(self, path, data):
        """writes a list to a file"""
        f = open(path,'w')
        result = f.writelines( data )
        f.close
        
        
    def __init__(self, irc):
        self.__parent = super(Jabbar, self)
        self.__parent.__init__(irc)
        self.rng = random.Random()   # create our rng
        self.rng.seed()   # automatically seeds with current time
        self.fartOptions = self.myReadFile("./plugins/Jabbar/data/farts.txt")
        self.lunchOptions = self.myReadFile("./plugins/Jabbar/data/lunch.txt")
        self.faceItems = self.myReadFile("./plugins/Jabbar/data/faces.txt")
        self.pasteSites = ["http://paste2.org","http://pastebin.org/","http://ideone.com","http://rgrd.pastebin.org/","http://www.fpaste.org/"]
        #self.faceItems = ["palms","desks","pianos","trees","plants","books","bombs","derps","bonks","skins"]
	self.butttext = "butt"

    def randomnick(self, irc, msg, args, channel, nicks):
        """takes no arguments
        a random person in the channel
        """
        channel = ircutils.toLower(channel)
        if len(nicks) == 0:
            nicks = list(irc.state.channels[channel].users)

        victim = self.rng.choice(nicks)
        irc.reply(victim)
        try:
            irc.noReply()
        except AttributeError:
            pass
    randomnick = wrap(randomnick, ['Channel', any('NickInChannel')])

    def bling(self, irc, msg, args, channel, nicks):
        """takes no arguments
        a random person in the channel
        """
        channel = ircutils.toLower(channel)
        if len(nicks) == 0:
            nicks = list(irc.state.channels[channel].users)

        unoppeds = []
        
        for n in nicks:
            if not n.ops:
                unoppeds.append(n)
        
        #victim = self.rng.choice(nicks)
        irc.reply(unoppeds)
        try:
            irc.noReply()
        except AttributeError:
            pass
    bling = wrap(bling, ['op', ('haveOp', 'op someone'), any('nickInChannel')])

    def buttset(self,irc, msg, args, text ):
        """specifies the output of butt."""
        if  len(text) > 2 :
            self.butttext = text                
    buttset = wrap (buttset,[additional('text')] )

    def butt(self, irc, msg, args, text):
        """[<text to be butted>]
        someone is apparently really into butts
        """
        l = len(text)
        if l>4:
            p = random.randrange(0, l-4)
            irc.reply(text[0:p]+self.butttext+text[p+4:l])
        else:
            irc.reply(self.butttext);
    butt = wrap(butt, [additional('text')])
    
    def butt2(self, irc, msg, args, text):
        """[<text to be butted>]"""
        li = text.split(" ")
        if ( len(li)-1 > 0 ):
            #which = self.rng.randint(0,len(li)-1)
            li[self.rng.randint(0,len(li)-1)] = self.butttext
            text = " ".join(li)
        else:
            text = self.butttext
        irc.reply(text)
    butt2 = wrap(butt2, [additional('text')])

    def paste(self, irc, msg, text):
        """provides a paste site to use.  Also falls into passive aggressive irc manners education."""
        irc.reply( self.rng.choice( self.pasteSites) )
    paste = wrap(paste)

    def face(self, irc, msg, args, text):
        """<text> optional."""
        print(text)
        reply = "face"
        if text == None : 
            reply += (self.rng.choice( self.faceItems))[:-1]
        else:
            reply += text.strip()
            self.faceItems.append( text+"\n" )
            print( self.faceItems )
            self.myWriteFile( "./plugins/Jabbar/data/faces.txt", self.faceItems )
            print("checking for plural")
        if reply[-1] != 's' : 
            print(reply)
            print "quote pluralizing unquote"
            reply += "s"
        print("done. replying")
        irc.reply(reply, action=True, prefixNick=False)
    face = wrap(face, [additional('text')])

    def myRandom(self, irc, msg, args):
        """takes no arguments
        
        Returns random #
        """
        irc.reply(str(self.rng.random()))
    myRandom = wrap(myRandom)
    
    def idle(self, irc, msg, args, text ):
        """Scrape nethack idlerpg page for user stats
        """
        f = urllib.urlOpen("http://pallas.crash-override.net/nethackidle/players.php")
        page = f.read()
        f.close
        
    def lunch(self, irc, msg, args, text):
        """<text> optional."""
        print(text)
        reply = ""
        if text == None : 
            reply += (self.rng.choice( self.lunchOptions))[:-1]
            irc.reply(reply, action=True, prefixNick=False)
        else:
            reply += text.strip()
            self.faceItems.append( text+"\n" )
            print( self.faceItems )
            self.myWriteFile( "./plugins/Jabbar/data/lunch.txt", self.lunchOptions )
    lunch = wrap(lunch, [additional('text')])

    def addfart(self, irc, msg, args, text):
        """Adds a new random entry to the "fart" list."""
        print(text)
        reply = ""
        if text == None :
            reply += "What FART do you wish to ADD?"
            irc.reply(reply, action=True, prefixNick=False)
        else:
            reply += text.strip()
            self.fartOptions.append( text+"\n" )
            print( self.fartOptions )
            self.myWriteFile( "./plugins/Jabbar/data/farts.txt", self.fartOptions )
    addfart = wrap(addfart, [additional('text')])

    def fart(self, irc, msg, args, text):
        """[<text to be farted upon>]"""
        if text == None :
            reply += "Nothing here to FART on."
            irc.reply(reply, action=True, prefixNick=False)
        else:
            li = text.split(" ")
            thefart = (self.rng.choice( self.fartOptions))[:-1]
            if ( len(li)-1 > 0 ):
                #which = self.rng.randint(0,len(li)-1)
                li[self.rng.randint(0,len(li)-1)] = thefart
                text = " ".join(li)
            else:
                text = thefart
            irc.reply(text)
    fart = wrap(fart, [additional('text')])

    
    def seed(self, irc, msg, args, seed):
        """<seed>
        
        seed must be floating point
        """
        self.rng.seed(seed)
        irc.replySuccess()
    seed = wrap(seed, ['float'])
    
    def diceroll(self, irc, msg, args, n):
        """[<number of sides>]
        
        rolls dice with n sides
        """
        s = 'rolls a %s' % self.rng.randrange(1,n)
        irc.reply(s, action=True)
    diceroll = wrap(diceroll, [additional(('int', 'number of sides'), 6)])
    
    def decide(self, irc, msg, args, text):
        """[<text>]

       Decide between n items separated by commas.
        """
        s = "".join(text)
        l = s.split(',')
        result = random.choice(l)
        result = result.strip()
        irc.reply(result)
    decide = wrap(decide, [additional('text')])


    def bender(self, irc, msg, args):
        response = random.choice(self.benderquotes)
        response = response[0:-1]
        irc.reply( response )
    bender = wrap(bender)
    
    def adams(self, irc, msg, args):
        quotes =["He attacked everything in life with a mix of extraordinary genius and naive incompetence, and it was often difficult to tell which was which.","He hoped and prayed that there wasn't an afterlife. Then he realized there was a contradiction involved here and merely hoped that there wasn't an afterlife.","Humans are not proud of their ancestors, and rarely invite them round to dinner.","I love deadlines. I like the whooshing sound they make as they fly by.","I may not have gone where I intended to go, but I think I have ended up where I needed to be.","In the beginning the Universe was created. This has made a lot of people very angry and has been widely regarded as a bad move.","In those days spirits were brave, the stakes were high, men were real men, women were real women and small furry creatures from Alpha Centauri were real small furry creatures from Alpha Centauri.","It is a mistake to think you can solve any major problems just with potatoes.","It is no coincidence that in no known language does the phrase 'As pretty as an Airport' appear.","Life... is like a grapefruit. It's orange and squishy, and has a few pips in it, and some folks have half a one for breakfast.","The ships hung in the sky in much the same way that bricks don't.","There is a theory which states that if ever anybody discovers exactly what the Universe is for and why it is here, it will instantly disappear and be replaced by something even more bizarre and inexplicable. There is another theory which states that this has already happened.","Time is an illusion. Lunchtime doubly so.","You live and learn. At any rate, you live.","Human beings, who are almost unique in having the ability to learn from the experience of others, are also remarkable for their apparent disinclination to do so.","The last time anybody made a list of the top hundred character attributes of New Yorkers, common sense snuck in at number 79.","He felt that his whole life was some kind of dream and he sometimes wondered whose it was and whether they were enjoying it.","Nothing travels faster than the speed of light with the possible exception of bad news, which obeys its own special laws.","Ah, this is obviously some strange usage of the word 'safe' that I wasn't previously aware of.","The major difference between a thing that might go wrong and a thing that cannot possibly go wrong is that when a thing that cannot possibly go wrong goes wrong it usually turns out to be impossible to get at or repair.","Anyone who is capable of getting themselves made President should on no account be allowed to do the job.","Space is big. You just won't believe how vastly, hugely, mind- bogglingly big it is. I mean, you may think it's a long way down the road to the chemist's, but that's just peanuts to space.","Even he, to whom most things that most people would think were pretty smart were pretty dumb, thought it was pretty smart."]
        irc.reply(random.choice(quotes))
    adams = wrap(adams)

    def dune(self, irc, msg, args):
        quotes=["Too much knowledge never makes for simple decisions.","The pitfall of Bene Gesserit training, she reminded herself, lay in the powers granted: such powers predisposed one to vanity and pride. But power deluded those who used it. One tended to believe power could overcome any barrier . . . including ones own ignorance.","When a creature has developed into one thing, he will choose death rather than change into his opposite.","The flesh surrenders itself, he thought. Eternity takes back its own. Our bodies stirred these waters briefly, danced with a certain intoxication before the love of life and self, dealt with a few strange ideas, then submitted to the instruments of Time. What can we say of this? I occurred. I am not . . . yet, I occurred.","I think what a joy it is to be alive, and I wonder if Ill ever leap inward to the root of this flesh and know myself as once I was. The root is there. Whether any act of mine can find it, that remains tangled in the future. But all things a man can do are mine. Any act of mine may do it.","Wild Fremen said it well: Four things cannot be hidden -- love, smoke, a pillar of fire and a man striding across the open bled.","Laws to suppress tend to strengthen what they would prohibit","To use raw power is to make yourself infinitely vulnerable to greater power","How often it is that the angry man rages denial of what his inner self is telling him.","I am I because I am here.","Deep in the human unconscious is a pervasive need for a logical universe that makes sense. But the real universe is always one step beyond logic.","The man without emotions is the one to fear.","One bargains with equals or near equals!","The concept of progress acts as a protective mechanism to shield us from the terrors of the future.","Survival is the ability to swim in strange water.","A world is supported by four things:  the learning of the wise; the justice of the great;  the prayers of the righteous,  the valor of the brave.  But all of these are as nothing without a ruler who knows the art of ruling. ","Any road followed precisely to its end leads precisely nowhere.","Climb the mountain just a little bit to test that its a mountain.","From the top of the mountain, you cannot see the mountain.","the proximity of a desirable thing tempts one to overindulgence.","Growth is limited by that necessity which is present in the least amount.","Humans live best when each has his own place, when each knows where he belongs in the scheme of things. ","Destroy the place and you destroy the person.","If you rely only on your eyes, your other senses weaken.","The way the mind will lean under stress is strongly influenced by training.","The Fremen were supreme in that quality the ancients called spannungsbogen--which is the self-imposed delay between desire for a thing and the act of reaching out to grasp that thing.","Spannungsbogen!. Waff rolled the ancient word on his tongue: The span of the bow! How far back you draw the bow before releasing your arrow. This arrow would strike deep!","It could be only the adab, the demanding memory that comes upon you of itself. She gave herself up to it, allowing the words to flow from her.","When your opponent fears you, thens the moment when you give the fear its own rein, give it the time to work on him. Let it become terror. The terrified man fights himself. Eventually, he attacks in desperation. That is the most dangerous moment, but the terrified man can be trusted usually to make a fatal mistake. You are being trained here to detect these mistakes and use them.","But Paul had been warned by Chani: Jamis fights with either hand. And the depth of his training had taken in that trick en passant. Keep the mind on the knife and not on the hand that holds it,  Gurney Halleck had told him time and again. The knife is more dangerous than the hand and the knife can be in either hand.","The purpose of argument is to change the nature of truth.","Most deadly errors arise from obsolete assumptions, Ghanima said. Thats what my mother kept quoting.","Leave absolute knowledge of the future to those moments of deja vu which any human may experience.","To know the future absolutely is to be trapped into that future absolutely. It collapses time. Present becomes future. I require more freedom than that.","A large populace held in check by a small but powerful force is quite a common situation in our universe. And we know the major conditions wherein this large populace may turn upon its keepers:,When they find a leader. This is the most volatile threat to the powerful; they must retain control of leaders.,When the populace recognizes its chains. Keep the populace blind and unquestioning.,When the populace perceives a hope of escape from bondage. They must never even believe that escape is possible!,To suspect your own mortality is to know the beginning of terror; to learn irrefutably that you are mortal is to know the end of terror.","All proofs inevitably lead to propositions which have no proof! All things are known because we want to believe in them.","This is the fallacy of power: ultimately it is effective only in an absolute, a limited universe. But the basic lesson of our relativistic universe is that things change. Any power must always meet a greater power. Paul MuadDib taught this lesson to the Sardaukar on the Plains of Arrakeen. His descendants have yet to learn the lesson for themselves.  -The Preacher at Arrakeen","When I am weaker than you, I ask you for freedom because that is according to your principles; when I am stronger than you, I take away your freedom because that is according to my principles.","You understand? One uses power by grasping it lightly. To grasp too strongly is to be taken over by power, and thus to become its victim.","He told you that completion equals death! The Preacher shouted. Absolute prediction is completion . . . is death!","In the Bene Gesserit Way, he opened his mind to Jacurutu, seeking to know nothing about it. Knowing was a barrier which prevented learning.","The trouble with peace is that it tends to punish mistakes instead of rewarding brilliance.","The surest way to keep a secret is to make people believe they already know the answer,","I assure you that the ability to view our futures can become a bore. Even to be thought of as a god, as I certainly was, can become ultimately boring. It has occurred to me more than once that holy boredom is good and sufficient reason for the invention of free will.","Enemies strengthen you.  Allies weaken.","This wise man observed that wealth is a tool of freedom. But the pursuit of wealth is the way to slavery.","They(Good adminstrators) never lie about what theyve done if their verbal orders cause problems, and they surround themselves with people able to act wisely on the basis of verbal orders. Often, the most important piece of information is that something has gone wrong. Bad administrators hide their mistakes until its too late to make corrections.","One of the hardest things for a tyrant to find, he said, is people who actually make decisions.","Overwhelming force destroys people who pose too great a threat.","Never attempt to reason with people who know they are right!","Prophets hold a key to the lock in a language. The mechanical image remains only an image to them. This is not a mechanical universe. The linear progression of events is imposed by the observer. Cause and effect? Thats not it at all. The prophet utters fateful words. You glimpse a thing destined to occur. But the prophetic instant releases something of infinite portent and power. The universe undergoes a ghostly shift. Thus, the wise prophet conceals actuality behind shimmering labels. The uninitiated then believe the prophetic language is ambiguous. The listener distrusts the prophetic messenger. Instinct tells you how the utterance blunts the power of such words. The best prophets lead you up to the curtain and let you peer through for yourself.","Monarchies have some good features beyond their star qualities. They can reduce the size and parasitic nature of the management bureaucracy. They can make speedy decisions when necessary.","Agreement bought with threats is no agreement, she said.","Do you know what guerrillas often say? They claim that their rebellions are invulnerable to economic warfare because they have no economy, that they are parasitic on those they would overthrow. The fools merely fail to assess the coin in which they must inevitably pay. The pattern is inexorable in its degenerative failures. You see it repeated in the systems of slavery, of welfare states, of caste-ridden religions, of socializing bureaucracies-in any system which creates and maintains dependencies. Too long a parasite and you cannot exist without a host.","Most believe that a satisfactory future requires a return to an idealized past, a past which never in fact existed.","Love leads to misery. Love is a very ancient force, which served its purpose in its day but no longer is essential for the survival of the species. Remember that womans mistake, the pain.","In the Bene Gesserit schools where first names tended to slip away, roll call was by last name. Friends and acquaintances picked up the habit of using the roll-call name. They learned early that sharing secret or private names was an ancient device for ensnaring a person in affections.","Mobility is the key to military success, Teg said. If youre tied down in forts, even whole-planet forts, you are ultimately vulnerable.","Quis custodiet ipsos custodiet? Who shall guard the guardians? Who shall see that the guardians commit no offenses?","Has not religion claimed a patent on creation for all of these millennia?","Hydraulic despotism: central control of an essential energy such as water, electricity, fuel, medicines, melange . . . Obey the central controlling power or the energy is shut off and you die!","Some people never observe anything. Life just happens to them. They get by on little more than a kind of dumb persistence, and they resist with anger and resentment anything that might lift them out of that false serenity.","I hear the doubt in your voice, Miles. Did he predict or did he create? Prescience can be deadly. The people who demand that the oracle predict for them really want to know next years price on whalefur or something equally mundane. None of them wants an instant-by-instant prediction of his personal life.","The mind of the believer stagnates. It fails to grow outward into an unlimited, infinite universe.","Quite naturally, holders of power wish to suppress wild research. Unrestricted questing after knowledge has a long history of producing unwanted competition. The powerful want a safe line of investigations, which will develop only those products and ideas that can be controlled and, most important, that will allow the larger part of the benefits to be captured by inside investors. Unfortunately, a random universe full of relative variables does not insure such a safe line of investigations.","Bureaucracy destroys initiative. There is little that bureaucrats hate more than innovation, especially innovation that produces better results than the old routines. Improvements always make those at the top of the heap look inept. Who enjoys appearing inept?","Memory never recaptures reality. Memory reconstructs. All reconstructions change the original, becoming external frames of reference that inevitably fall short.","You could drag humankind almost anywhere by manipulating the enormous energies of procreation. You could goad humans into actions they would never have believed possible. One of his teachers had said it directly: This energy must have an outlet. Bottle it up and it becomes monstrously dangerous. Redirect it and it will sweep over anything in its path. This is an ultimate secret of all religions.","There were many paradise planets in the Old Empire, probably many more among the people of the Scattering. Humans always seemed capable of trying that foolish experiment. People in such places mostly lazed along. A quick-smart analysis said this was because of the easy climates on such planets. He knew this for stupidity. It was because sexual energy was easily released in such places. Let the Missionaries of the Divided God or some denominational construct enter one of these paradises and you got outrageous violence.","For a few moments longer, Teg watched the drinks being distributed by the skilled waiting staff: dark local beers and some expensive imports. Scattered along the bar and on the softly illuminated tables were bowls containing crisp-fried local vegetables, heavily salted. Such an obvious move to heighten thirst apparently offended no one. It was merely expected in this trade. The beers would be heavily salted, too, of course. They always were. Brewers knew how to kick off the thirst response.","Sometimes, the supremely rich did become depraved. That came from believing that money (power) could buy anything and everything. And why shouldnt they believe this? They saw it happening every day. It was easy to believe in absolutes.","Enclosed, she said. How tempting it is to raise high walls and keep out change. Rot here in our own self-satisfied comfort.","Enclosures of any kind are a fertile breeding ground for hatred of outsiders, she said. That produces a bitter harvest.","We tend to become like the worst in those we oppose.","Incomplete suppression of trade in any commodity always increases the profits of the tradesmen, especially the profits of the senior distributors. His voice was warningly hesitant. That is the fallacy of thinking you can control unwanted narcotics by stopping them at your borders.","Confine yourself to observing and you always miss the point of your own life. The object can be stated this way: Live the best life you can. Life is a game whose rules you learn if you leap into it and play it to the hilt. Otherwise, you are caught off balance, continually surprised by the shifting play. Non-players often whine and complain that luck always passes them by. They refuse to see that they can create some of their own luck.","All governments suffer a recurring problem: Power attracts pathological personalities. It is not that power corrupts but that it is magnetic to the corruptible. Such people have a tendency to become drunk on violence, a condition to which they are quickly addicted.","Power attracts the corruptible. Suspect all who seek it. She knew the chances were great that such people were susceptible to corruption or already lost.","We should grant power over our affairs only to those who are reluctant to hold it and then only under conditions that increase the reluctance.","Education is no substitute for intelligence. That elusive quality is defined only in part by puzzle-solving ability. It is in the creation of new puzzles reflecting what your senses report that you round out the definition.","Many things we do naturally become difficult only when we try to make them intellectual subjects. It is possible to know so much about a subject that you become totally ignorant.","Silence is often the best thing to say, some Bene Gesserit humorist had scrawled on a washroom mirror. Odrade found that good advice then and later.","Educational bureaucracies dull a childs questing sensitivity. Odrade explaining. The young must be damped down. Never let them know how good they can be. That brings change. Spend lots of committee time talking about how to deal with exceptional students. Dont spend any time dealing with how the conventional teacher feels threatened by emerging talents and squelches them because of a deep-seated desire to feel superior and safe in a safe environment. ","The Senior Watchdog had her own watchwords: Show me a completely smooth operation and Ill show you someone whos covering mistakes. Real boats rock.","Democracy is susceptible to being led astray by having scapegoats paraded in front of the electorate. Get the rich, the greedy, the criminals, the stupid leader and so on ad nauseam.","Never bring such people bad news. No wonder their minions behaved with frenzy. A powerful person in fright might kill the bearer of bad tidings. Bring no bad tidings. Better to die in battle.","The true warrior often understands his enemy better than he understands his friends. A dangerous pitfall if you let understanding lead to sympathy as it will naturally do when left unguided.","Sympathy for the enemy -- a weakness of police and armies alike. Most perilous are the unconscious sympathies directing you to preserve your enemy intact because the enemy is your justification for existence.","- Within limits you will learn and appreciate. For now, I warn you the Bene Gesserit work under a system of organized distrust.","Success, that was the danger. It had cost them an empire. If you waved your success around like a banner someone always wanted to cut you down. Envy!","The difference between sentiment and sentimentality is easy to see. When you avoid killing somebodys pet on the glazeway, thats sentiment. If you swerve to avoid the pet and that causes you to kill pedestrians, that is sentimentality.","Since every individual is accountable ultimately to the self, formation of that self demands the utmost care and attention.","Spend energies on those who make you strong. Energy spent on weaklings drags you to doom.","War is behavior with roots in the single cell of the primeval seas. Eat whatever you touch or it will eat you.","Juries are not popular with legalists. Juries oppose the law. They can ignore judges.","To create change you find leverage points and move them. Beware blind alleys. Offers of high positions are a common distraction paraded before marchers. Leverage points are not all in high office. They are often at economic or communications centers and unless you know this, high office is useless.","If your weapons cost only a small fraction of the energy your enemy spent, you had a potent lever that could prevail against seemingly overwhelming odds. Prolong the conflict and you wasted enemy substance. Your foe toppled because control of production and workers was lost.","When you think to take determination of your fate into your own hands, that is the moment you can be crushed. Be cautious. Allow for surprises. When we create, there are always other forces at work.","Litany against fear","Fear is the mind-killer. Fear is the little death that brings total obliteration. I will face my fear. I will permit it to pass over me and through me. And when it has gone past me I will turn to see fears path. Where the fear has gone there will be nothing. Only I will remain.","I must not fear. Fear is the mind-killer. Fear is the little-death that brings total obliteration. I will face my fear. I will permit it to pass over me and through me. And when it has gone past I will turn the inner eye to see its path. Where the fear has gone there will be nothing. Only I will remain.  She did this silently and took a deep, calming breath."]
        irc.reply(random.choice(quotes))
    dune = wrap(dune)

def eno(self, irc, msg, args):
        """quotes at random from Brian Eno's Oblique Strategies deck"""
        quotes=["Remove specifics and convert to ambiguities","Don't be frightened of cliches","What is the reality of the situation?","Are there sections?  Consider transitions","Turn it upside down","Think of the radio","Allow an easement (an easement is the abandonment of a stricture)","Simple subtraction","Be dirty","Go slowly all the way round the outside","A line has two sides","Make an exhaustive list of everything you might do & do the last thing on the list","Into the impossible","Towards the insignificant","Ask people to work against their better judgement","Take away the elements in order of apparent non-importance","Infinitesimal gradations","Change instrument roles","Accretion","Disconnect from desire","Emphasize repetitions","Faced with a choice, do both","Children-speaking -singing","Lost in useless territory","A very small object Its center","Dont be afraid of things because they're easy to do","Dont be frightened to display your talents","Breathe more deeply","Honor thy error as a hidden intention","What are the sections sections of?  Imagine a caterpillar moving","Only one element of each kind","Is there something missing","Use 'unqualified' people","How would you have done it?","Emphasize differences","Do nothing for as long as possible","Bridges - build - burn","Always give yourself credit for having more than personality","You don't have to be ashamed of using your own ideas","Tidy up","Do the words need changing?","Ask your body","Tape your mouth","Water","Simply a matter of work","Make a sudden, destructive unpredictable action; incorporate","Consult other sources-promising-unpromising","Use an unacceptable color","Humanize something free of error","Use filters","Fill every beat with something","Discard an axiom","Not building a wall but making a brick","What wouldn't you do?","Lowest common denominator","Decorate, decorate","Balance the consistency principle with the inconsistency principle","Get your neck massaged","Listen to the quiet voice","Do the washing up","Is it finished?","Put in earplugs","Reevaluation (a warm feeling)","Give the name away","Intentions-nobility of  -humility of-credibility of","Abandon normal instruments","Use fewer notes","Repetition is a form of change","Give way to your worst impulse","Reverse","Trust in the you of now","Imagine the piece as a set of disconnected events","What would your closest friend do?","Distorting time","Make a blank valuable by putting it in an exquisite frame","Feed the recording back out of the medium","Convert a melodic element into a rhythmic element","The most important thing is the thing most easily forgotten","Ghost echoes","You can only make one dot at a time","Just carry on","(Organic) machinery","The inconsistency principle","Don't break the silence","Idiot glee (?)","Discover the recipes you are using and abandon them","Cascades","Courage!","Spectrum analysis","What mistakes did you make last time?","Consider different fading systems","Mute and continue","Be extravagant","It is quite possible (after all)","What are you really thinking about just now?","Don't stress on thing more than another [sic]","State the problem in words as clearly as possible","Abandon desire","Abandon normal instructions","Accept advice","Adding on","Always the first steps","Be less critical","Bridges -build -burn","Change ambiguities to specifics","Change nothing and continue consistently","Change specifics to ambiguities","Consider transitions","Cut a vital connection","Destroy nothing; Destroy the most important thing","Disciplined self-indulgence","Discover your formulas and abandon them","Display your talent","Distort time","Don't avoid what is easy","Don't stress one thing more than another","Do something boring","Do something sudden, destructive and unpredictable","Do the last thing first","Emphasize the flaws","Faced with a choice, do both (from Dieter Rot)","Find a safe part and use it as an anchor","Give the game away","Go outside. Shut the door.","Go to an extreme, come part way back","How would someone else do it?","In total darkness, or in a very large room, very quietly","Is something missing?","Is the style right?","It is simply a matter or work","Look at the order in which you do things","Magnify the most difficult details","Make it more sensual","Make what's perfect more human","Move towards the unimportant","Not building a wall; making a brick","Once the search has begun, something will be found","Only a part, not the whole","Openly resist change","Pae White's non-blank graphic metacard","Question the heroic","Remember quiet evenings","Remove a restriction","Retrace your steps","Simple Subtraction","Slow preparation, fast execution","State the problem as clearly as possible","Take a break","Take away the important parts","The most easily forgotten thing is the most important","Think -inside the work -outside the work","Try faking it (from Stewart Brand)","Use an old idea","Use cliches","Use something nearby as a model","Use `unqualified' people","Use your own ideas","Voice your suspicions","What context would look right?","What is the simplest solution?","What to increase? What to reduce? What to maintain?","What were you really thinking about just now?","When is it for?","Where is the edge?","Which parts can be grouped?","Work at a different speed","Would anyone want it?","Your mistake was a hidden intention","Assemble some of the elements in a group and treat the group","You are an engineer","Remove ambiguities and convert to specifics","Go outside.  Shut the door.","Do we need holes?","Cluster analysis","Always first steps","Define an area as 'safe' and use it as an anchor","Is the information correct?","Overtly resist change","Question the heroic approach","Twist the spine","Look closely at the most embarrassing details & amplify them","Mechanicalize something idiosyncratic","Remember those quiet evenings","Short circuit (example: a man eating peas with the idea that they will improve his virility shovels them straight into his lap)","Left channel, right channel, center channel","Destroy-nothing-the most important thing","Change nothing and continue with immaculate consistency","The tape is now the music"]
        irc.reply(random.choice(quotes))
    eno = wrap(eno)

Class = Jabbar


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
