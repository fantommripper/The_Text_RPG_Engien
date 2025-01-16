
class Alchemist():
    def __init__(self):
        self.alchemist_phrases_NULL = [
            "Ah, have we crossed paths before? No matter, you're welcome here!",
            "Hmm, your face seems familiar. Regardless, welcome to my shop!",
            "Have we met in another life, perhaps? Regardless, you're welcome here!",
            "You seem oddly familiar... Well, no matter! Welcome to my humble abode!",
            "I feel as though our paths have crossed before... In any case, welcome!",
            "Your presence feels strangely familiar... Welcome, regardless!",
            "I have a feeling we've met somewhere before... In any case, welcome!",
            "Deja vu, perhaps? No matter! Welcome to my alchemical sanctuary!",
            "There's something familiar about you... Well, welcome to my shop regardless!",
            "You have a familiar aura... Welcome, regardless of our past encounters!",
            "It's as if I've seen you in a dream... Nevertheless, welcome to my establishment!",
            "Your presence evokes a sense of familiarity... Regardless, welcome!",
            "Where have our paths crossed before, I wonder? Nonetheless, welcome!",
            "There's a strange familiarity about you... Welcome, regardless!",
            "Did our fates intertwine in another life, I wonder? In any case, welcome!"
        ]

        self.alchemist_phrases = [
            "Welcome, seeker of the arcane! How may I assist you today?",
            "Greetings, traveler! Step into the realm of alchemy. What brings you here?",
            "Ahoy, fellow adventurer! Seeking potions or perhaps a little magic?",
            "Well met, friend! What mysterious concoctions are you in search of?",
            "Hello there! Delving into the secrets of alchemy, are we?",
            "Greetings, wanderer! How can I aid you on your mystical journey?",
            "Welcome, brave soul! Care for a taste of the elixirs of old?",
            "Greetings, intrepid explorer! What alchemical wonders do you seek?",
            "Ah, a visitor! What rare ingredients or potions do you desire today?",
            "Salutations, traveler! Step closer and let's uncover the secrets of alchemy together.",
            "Welcome to my humble abode, seeker of the esoteric! What brings you to my doorstep?",
            "Greetings, fellow adventurer! Come, let us unlock the mysteries of alchemy.",
            "Well met, friend of the arcane! What alchemical marvels can I provide you with?",
            "Hello, curious soul! Seeking the elixirs of life or perhaps something more peculiar?",
            "Ah, a new face in my shop! How can I assist you on your alchemical journey today?"
        ]

        self.alchemist_phrases_no_product = [
            "Ah, it seems you're looking for something I don't have in stock. Let me check if I can order it for you! Why don't you swing by later?",
            "Oh, out of stock on that one, my friend. But fear not, I'll make a note to have it in stock next time. Could you drop by a bit later?",
            "Looks like I've run dry on that potion. But fret not, I can place an order for it and have it ready for you later. When are you thinking of stopping by?",
            "Seems like you've got a taste for the rare stuff! Unfortunately, I'm fresh out. How about I arrange to have it for you by the time you swing by later?",
            "Oh, that elixir? It's a popular one, but alas, I've exhausted my supply. Let's schedule a time for you to come back, and I'll make sure to have it ready for you!",
            "Looks like I need to restock on that particular brew. But don't despair, I'll make sure to have it available for you when you come back. What time works for you?",
            "Sorry, it seems you've caught me at a bad time. I've just run out of that potion. How about you come back later, and I'll make sure to have it freshly brewed for you?",
            "Oh, that's a hot item lately! Unfortunately, I'm all sold out. But hey, I'll make sure to restock it for you. When do you plan on stopping by again?",
            "Out of stock on that one, my friend. But I'm always up for a challenge! Let's arrange a time for you to return, and I'll make sure to have it in stock for you.",
            "Looks like you've got a discerning taste! Unfortunately, I've just run out of that particular brew. How about I place an order for it and have it ready for you when you swing by later?"
        ]

        self.alchemist_purchase_phrases = [
            "Ah, an excellent choice! This potion will serve you well on your journey.",
            "You've made a wise decision. This elixir is brewed with the finest ingredients.",
            "A fine selection indeed! May this potion aid you in your adventures.",
            "Ah, stocking up on essentials, I see. This potion will not disappoint.",
            "An astute purchase! This concoction holds great power within its vial.",
            "Excellent taste! This potion is renowned for its potency and effectiveness.",
            "Ah, you've chosen wisely. This elixir is sure to bolster your strength.",
            "A discerning eye, indeed! This potion is among my finest creations.",
            "A wise investment! This elixir is worth its weight in gold, I assure you.",
            "Ah, a discerning customer! This potion is sure to exceed your expectations."
        ]

        self.alchemist_purchase_no_gold = [
            "Oh, it seems you're a bit short on gold for that potion. No worries, my friend! Perhaps there's something else I can interest you in within your budget?",
            "Ah, looks like that potion is just a tad out of your gold range. Not to fret! Let's see if we can find something more suitable for your coin purse, shall we?",
            "Hmm, it appears your purse strings are feeling a bit tight for that elixir. Fear not! Let's explore some alternatives that won't break the bank.",
            "Sorry, friend, it seems that potion might be a bit too pricey for your current gold reserves. But hey, I'm sure we can find something equally beneficial within your budget!",
            "Oh dear, it seems that potion is a bit beyond your current gold stash. Not to worry, though! Let's see if we can't find a more affordable option together.",
            "Ah, it looks like that potion might be stretching your gold supply a bit thin. No need to despair, though! Let's find something that fits your budget a bit better.",
            "Hmm, it seems you're a bit short on gold for that particular potion. But fret not, my friend! I'm sure we can work out a deal or find an alternative that suits you better.",
            "Oh, that potion does seem to be on the pricier side, doesn't it? But fear not! Let's see if we can find something equally beneficial that's a bit more wallet-friendly.",
            "Sorry about that, it seems the cost of that potion is a bit steep for your current gold reserves. But hey, let's not lose hope! I'm sure there's something else we can find for you.",
            "Ah, it appears that potion might be a bit out of reach for your current gold pouch. But don't worry! Let's explore some other options together and find something more within your means.",
        ]

        self.alchemist_purchase_exit = [
            "Farewell, adventurer! May the potions you seek bring you fortune on your journey!",
            "Safe travels, brave soul! Remember, the mysteries of alchemy are always here for you to explore.",
            "Until we meet again, seeker of the arcane! May your path be illuminated with the light of wisdom.",
            "Take care on your travels, wanderer! Should you ever need more elixirs, you know where to find me.",
            "Goodbye for now, intrepid explorer! May the potions you've acquired serve you well in your endeavors.",
            "May the winds of fortune guide your steps, traveler! Fare thee well, until our paths cross again.",
            "Bon voyage, my friend! Should you thirst for more alchemical wonders, you'll always be welcome here.",
            "May your journey be as fruitful as your visit here, brave adventurer! Farewell, and may the potions be with you.",
            "Remember, the doors of my shop are always open to you, seeker of mysteries! Farewell, and may magic protect you.",
            "As you venture forth, know that the alchemical arts are ever at your service! Fare thee well, until next time!"
        ]

        self.alchemist_purchase_back = [
            "Oh, is there something else that interests you?",
            "Anything else I can do for you?",
            "Did anything else catch your eye?",
            "Would you like to add anything?",
            "What else do you need?",
            "Anything else you'd like to purchase?",
            "Is there anything else on your list?",
            "Any other requests?",
            "Did something else catch your interest?",
            "What else can I offer you?",
        ]

class Blacksmith():
    def __init__(self):

        self.blacksmith_purchase_back = [
            "Don’t waste my time, kid.",
            "Hurry up, I’ve got work to do.",
            "What else do you need?",
            "Got more business? Speak up.",
            "Stop dawdling, let's get to the point.",
            "Quit talking, what else?",
            "Don’t waste my time, boy.",
            "Quit dragging it out, what else?",
            "I’ve got little time, make it quick.",
            "Make it quick, what else do you need?",
        ]

        self.blacksmith_phrases = [
            "Well, look what the cat dragged in. What do you need?",
            "Huh, new face in town. What's it gonna be?",
            "Ain't seen you 'round these parts before. What can I do for ya?",
            "What's your poison, stranger? Spit it out!",
            "You lost, or you lookin' to buy somethin'?",
            "You got a reason to be standin' in my forge, or you just wastin' my time?",
            "You want somethin' sharp, or somethin' blunt?",
            "Don't know what you're after, but make it quick. I got work to do.",
            "Got any idea what you're lookin' for, or you just browsin'?",
            "Well, spit it out, ain't got all day to chat.",
            "You want steel? I got steel. What else you want?",
            "You got the coin, I got the goods. Simple as that.",
            "Ain't got time for small talk, what do you need?",
            "Make it quick, I ain't got all day to stand around jabberin'.",
            "If you ain't buyin', you better be leavin'."
        ]

        self.wicked_blacksmith_phrases = [
            "Hey, I'm tryin' to work here! What do you want now?",
            "Can't you see I'm busy? Quit botherin' me!",
            "Get outta my face! Can't you see I'm workin'?",
            "What's your problem? Can't you see I'm tryin' to make a livin' here?",
            "Great, just what I needed, more interruptions. What do you want?",
            "You're really startin' to get on my nerves. What do you need this time?",
            "Ain't you got better things to do than botherin' me while I'm workin'?",
            "I swear, if you ain't got a good reason for botherin' me, I'm gonna lose it.",
            "You're lucky I got patience, 'cause you're testin' it right now.",
            "What do you want now? Can't you see I'm tryin' to get some work done?",
            "You better have a good reason for botherin' me, 'cause I ain't in the mood.",
            "I don't know who you think you are, but you're startin' to get on my nerves.",
            "I oughta toss you outta here if you don't start mindin' your own business.",
            "You're really pushin' it, you know that? What do you want now?",
            "You got a death wish or somethin'? Leave me alone and let me work!"
        ]

        self.blacksmith_phrases_NULL = [
            "Oh, it's you again. I thought I told you to stay outta here. Get lost!",
            "What're you doing back here? I already told you to scram. Beat it!",
            "You again? I ain't runnin' no charity. Get out before I throw you out!",
            "I knew you'd show your face again. You ain't welcome here. Now get out!",
            "Well, well, well... Look who decided to come back for more. Get outta here!",
            "You got some nerve showin' up here after what happened last time. Get out!",
            "You got a lotta guts comin' back here after what you pulled. Leave, now!",
            "Don't think I forgot about you. Get out before I call the guards!",
            "You again? I thought I made myself clear. Get out before I lose my temper!",
            "What's it gonna take to get rid of you? Get outta here before I lose it!",
            "I don't wanna see your face in here ever again. Now get out and stay out!",
            "You think I'm playin' around? Get out before I make you regret it!",
            "I don't have time for your games. Get out of my forge, now!",
            "You've worn out your welcome. Get out before I decide to make you leave!",
            "You're not welcome here. Get out before I have to forcibly remove you!"
        ]

        self.blacksmith_purchase_no_gold = [
            "No gold, no goods. Come back when your pockets jingle, lad.",
            "Got naught but air in them pockets, eh? Ain't charity hour here.,"
            "You think I'm running a charity? Get outta here 'til you got something to show.",
            "Back again? Still empty-handed, I see. Come back when you've got coin to spare.",
            "Not even a single coin to rub together? Can't help you then, can I?",
            "Empty purse, empty hands. No transactions without compensation.",
            "Money makes the world go 'round, mate. Come back when you're part of the rotation.",
            "Sorry, lad, but I ain't in the business of giving things away for free.",
            "If wishes were gold, you'd be the richest man alive. But they ain't, so scram.",
            "Until you bring something other than excuses, we ain't got no business."
        ]

        self.blacksmith_purchase_exit = [
            "Leaving so soon? Don't let the door hit you on the way out.",
            "Off with ya then, but remember where the good stuff is.",
            "Don't let the sun set on your back while you're still in my shop.",
            "And there he goes, like a shadow in the night. Come back when you're serious.",
            "Headed out empty-handed? Don't expect a hero's welcome when you return.",
            "If you're leaving, be quick about it. I've got work to do.",
            "Don't make promises you can't keep, especially when you're heading out the door.",
            "Think twice before you wander off. Might not be so lucky next time.",
            "If you're not buying, you're wasting my time. Off you go then.",
            "And off he trots, like a lost pup. Hope he finds what he's looking for.",
        ]

        self.blacksmith_phrases_no_product = [
            "You think I'm some sort of wizard? Can't whip up the same thing in a blink of an eye, you know.",
            "What, you want me to clap my hands and make it appear? Get real, it takes time and effort.",
            "Not everyone's blessed with your level of impatience. Quality takes time, mate.",
            "You're a piece of work, ain't ya? Can't replicate craftsmanship like mine on a whim.",
            "Do I look like a miracle worker to you? Go find someone else to pester.",
            "Oh, I'm sorry, I didn't realize I was dealing with a professional armchair blacksmith.",
            "Didn't your parents teach you patience? Can't rush perfection, even for you.",
            "You must think you're special, huh? Well, newsflash, you ain't. Wait your turn like everyone else.",
            "I've got half a mind to charge you double for being such a pain in the rear.",
            "You're as persistent as a flea on a dog's back, you know that? Back off and let me work."
        ]

        self.blacksmith_purchase_phrases = [
            "A fine choice, my friend. It'll serve you well.",
            "You've got yourself a sturdy piece there. Treat it right.",
            "Excellent taste, if I may say so. May it bring you fortune.",
            "A wise investment, indeed. Few can appreciate quality craftsmanship like you do.",
            "You won't regret that, mark my words. A weapon of true quality.",
            "Good choice, adventurer. With that in hand, you'll be ready for whatever comes your way.",
            "Ah, that's a fine piece you've chosen. May it keep you safe.",
            "A discerning eye you have, my friend. That's one of my best works, if I do say so myself.",
            "You've made a wise decision. It will become an extension of your arm.",
            "I'll admit, you've got a knack for picking the best. That purchase will serve you well."
        ]

class World():
    def __init__(self):
        self.sorry_Im_lazy = [
            "Oops! Looks like I forgot to finish this. My bad!",
            "Uh-oh, you’ve found my secret unfinished corner. Sorry about that!",
            "Looks like I got a little too lazy here. Forgive me!",
            "Oh, you weren’t supposed to see this yet. Pretend you didn’t!",
            "Oops! I guess I forgot to polish this part. My bad!",
            "This is awkward... I meant to finish this. Honest!",
            "Caught me slacking! This part’s not done yet.",
            "Well, this is embarrassing... Let’s just say I was saving this for later.",
            "Whoops, my procrastination showed up here. Sorry!",
            "You found the unfinished zone! Please excuse my laziness.",
            "Uh, this wasn’t supposed to be visible yet. My mistake!",
            "Oops! This area is still under construction. Apologies!",
            "Looks like I missed a spot... or a whole area. Sorry!",
            "Yikes, you found my work-in-progress. I’ll get back to it soon!",
            "Oh no, you weren’t supposed to find this yet! I’ll get it done, promise!",
            "Oops! Looks like I need to get back to work here.",
            "Well, this is awkward... I forgot to finish this. My bad!",
            "You caught me! This part isn’t ready yet. Apologies!",
            "Oops! This section is still on my to-do list.",
            "Oh, you found my lazy zone. I’ll get back to it... eventually.",
            "Oops, this part slipped through the cracks. My bad!",
            "Looks like I took a break here... and forgot to come back.",
            "Oops, I guess this area missed the memo. Sorry about that!",
            "Uh, yeah... about this... I’ll get back to it soon!",
            "Oops! I promise I’ll finish this part. Eventually.",
            "You weren’t supposed to find this! I’ll fix it, I swear!",
            "Whoops, this one’s still in the oven. My apologies!",
            "Caught me napping on the job! This part isn’t done yet.",
            "Uh-oh, looks like I hit the snooze button on this one. Sorry!",
            "Oops! This area is still on the drawing board. Apologies!",
            "Yikes, you found my unfinished masterpiece. I’ll get back to it!",
            "Whoops, this part’s still a work in progress. Sorry!",
            "Oh, you found the beta zone! I’ll finish it up soon.",
            "Oops! This area is still in the ‘coming soon’ category.",
            "Looks like this section is still waiting for its big debut. My bad!",
            "Oh no, you found my secret lazy spot. Sorry!",
            "Oops! Looks like this area’s still in development. My bad!",
            "Whoops, I guess I forgot to finish this part. My apologies!",
            "Oops, this part is still in the works. I’ll get back to it soon!",
            "Uh-oh, looks like I got distracted here. Sorry about that!",
        ]

alchemist = Alchemist()
dlacksmith = Blacksmith()
world = World()