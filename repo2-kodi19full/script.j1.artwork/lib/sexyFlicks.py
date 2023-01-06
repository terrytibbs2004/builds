"""

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import os, re, sys, string, json, random, base64

try:
    # Python 3
    from urllib.request import urlopen, Request
except ImportError:
    # Python 2
    from urllib2 import urlopen, Request

try:
    # Python 3
    from html.parser import HTMLParser
except ImportError:
    # Python 2
    from HTMLParser import HTMLParser

convert_special_characters = HTMLParser()
dlg = xbmcgui.Dialog()

from resources.lib.modules.common import *

art = 'special://home/addons/script.j1.artwork/lib/resources/art/'
genreImage = 'special://home/addons/script.j1.artwork/lib/resources/images/genres/'

channellist=[
        ("[B]Rana, Queen of the Amazon (1994)[/B]", "Rfm_-wW-qR0", 801, "Action", "In the 1940s, Rana, queen of the Amazons, has to face up to the invasion of her natural paradise by the evil explorer, Ilsa. Eventually both go through unspeakable horror, and gore.", fanart),
        ("[B]If You Dont Stop It Youll Go Blind (1975)[/B]", "dUcDGjdJPPo", 801, "Comedy", "A collection of jokes makes this an hilarious spoof.", fanart),
        ("[B]The Sweet Pussycats (1969)[/B]", "B3RRwbBzkpk", 801, "Classic, Comedy", "(German) An Earl and a Colonel both claim ownership of the same castle by dividing it up with a red line. They bet each other that the first man to bed a local virgin of his choice gets to keep the castle.", fanart),
        ("[B]Doctor Jekyll Likes Them Hot (1979)[/B]", "-EBNp0no1VY", 801, "Comedy", "A lusty young woman decides to use her sexual powers to tame the evil and murderous Dr. Jekyll. ", fanart),
        ("[B]My Darling Slave (1973)[/B]", "QLPJ7c9kVmk", 801, "Comedy, Romance", "Demetrio Cultrera, is a young, rich car dealership Sicilian bachelor who becomes engaged to the beautiful Rosalba Giordano, daughter of a local business owner Giordano Tuna Company.", fanart),
        ("[B]Cavegirl (1985)[/B]", "UOA9Wz66xiQ", 801, "Comedy, Fantasy", "Thanks to a strange crystal, a shy student finds himself in the Stone Age, where he falls in love with a beautiful cave woman and helps her clan stave off a tribe of cannibals.", fanart),
        ("[B]Magique Emanuele (1993)[/B]", "H5KaNrvyJ7o", 801, "Fantasy, Drama, Romance", "Young Emmanuelle and her friend Coco visit a friend whose sculptor husband is infatuated with one of his plaster creations. Emmanuelle uses her magic to get him interested again", fanart),
        ("[B]The Beach Girls (1982)[/B]", "PetO4P7qJ1g", 801, "Comedy", "School is out, and three girls head to the beach for vacation. Two of the girls are world-wise party-goers who attempt to loosen up their naive, virginal friend", fanart),
        ("[B]Red Light Distict Amsterdam[/B]", "PpRFHIQ4DYE", 801, "Docs", "National Geographics documentary or Amsterdams Red Light District", fanart),
        ("[B]Cheerleader Camp (1988)[/B]", "xjguFaueHOs", 801, "Sports, Comedy, Horror, Thriller", "A group of cheerleaders become the targets of an unknown killer at a remote summer camp.", fanart),
        ("[B]Invasion of the Bee Girls (1973)[/B]", "n5zv516PD4c", 801, "Scifi, Horror", "A powerful cosmic force is turning Earth women into queen bees who kill men by wearing them out sexually.", fanart),
        ("[B]The Fear Of Speed (2002)[/B]", "yyJEblBO9Pc", 801, "Comedy, Action", "A low budget spoof of The Fast and the Furious - fast cars, cute girls, drugs, guns and a girl with fear of speed (Tachophobia).", fanart),
        ("[B]Mischief (1985)[/B]", "atP61pHpUwU", 801, "Comedy, Romance", "1956. Obsessed with the hottest girl in class, a gawky high school student takes a crash course in teenage coolness from his motorcycle rebel neighbour, under the watchful eye of the eternal symbol of teenage rebellion: James Dean.", fanart),
        ("[B]Vixen (1968)[/B]", "VDXmb0wKUNw", 801, "Drama", "Vixen lives in a Canadian mountain resort with her naive pilot husband. While he is away flying in tourists, she gets it on with practically everybody", fanart),
        ("[B]Supervixens (1975)[/B]", "-GibOWf1Usc", 801, "Comedy", "Clint Ramsey has to leave his job working at Martin Bormanns gas station and flee after his wife is murdered by psycho cop Harry Sledge, who tries to pin the murder on Clint. Crossing America, Clint gets sexually harassed on all sides by various voluptuous nymphomaniacs", fanart),
        ("[B]The Naked Venus (1959)[/B]", "gvVLwKdl7nQ", 801, "Classic, Drama", "A young American painter and his French wife move with their small daughter to the US when the husbands father dies. His mother takes an instant dislike to the wife, and when she finds out that her daughter-in-law is a nudist who once posed naked for an artist", fanart),
        ("[B]Dr. Sex (1964)[/B]", "P4s73NLDBPo", 801, "Classic, Comedy, Scifi", "Three sex researchers discuss their strangest cases.", fanart),
        ("[B]Sex Galaxy (2008)[/B]", "JDz2bIROFB4", 801, "Comedy, Scifi", "One hundred years in the future... Due to overpopulation and the effects of global warming, sex has been declared illegal on Earth. ", fanart),
        ("[B]Down and Dirty Duck (1974)[/B]", "0g979zRcHkg", 801, "Comedy, Fantasy", "Willard, a mild mannered insurance adjuster, teams up with a foul-mouthed fowl who takes Willard on a surreal quest to become less uptight - and possibly get laid in the process.", fanart),
        ("[B]Hey Good Lookin (1982)[/B]", "dxjxTywzF8k", 801, "Comedy, Drama", "An outrageous, affectionate look at coming of age in the Eisenhower era in Brooklyn", fanart),
        ("[B]Tarzoon Shame of the Jungle (1975)[/B]", "A609EzrAR8w", 801, "Comedy, Action", "Shame, the ape man of the jungle, is aghast when his woman, June, is kidnapped by a gang of giant penises. They take her to their queen, Bazunga, a bald woman with fourteen breasts.", fanart),
        ("[B]The Big Bang (1987)[/B]", "Wzbalg279KA", 801, "Comedy, Action", "Sex farce about Fred, an inept post WWIII superhero garbageman, who must prevent WW4 by disarming the continents of Virginia, where mutated feminists live, and USSSR, where mutated buttless men live. Beautiful Liberty is his only ally.", fanart),
        ("[B]Heavy Traffic (1973)[/B]", "q6vGEjR6tGQ", 801, "Comedy, Drama", "An underground cartoonist contends with life in the inner city, where various unsavory characters serve as inspiration for his artwork.", fanart),
        ("[B]Girl From Starship Venus (1975)[/B]", "PylC09R0A0A", 801, "Comedy, Horror, Scifi", "A young Venusian girl lands on Earth to explore the planet. She lands in Soho in London, UK where she has ample opportunities to research sex on Earth.", fanart),
        ("[B]The Playbirds (1978)[/B]", "K3-_kNDWfPw", 801, "Drama, Crime", "Two detectives are drawn into the world of porn, while investigating murders of centrefolds...", fanart),
        ("[B]Planet of Baybes (2013)[/B]", "ChKXUh-JFZw", 801, "Comedy, Scifi, Music", "Sci fi, musical spoof shot in Yorkshire, England on a shoe string budget.", fanart),
        ("[B]The Invisible Maniac (1990)[/B]", "Ds7QfRFlnjA", 801, "Comedy, Horror, Scifi", "A scientist announces his theories of invisibility, and his colleagues laugh, to which he responds by killing 4 of them. He escapes from the loony bin and gets a job teaching summer school physics. The students decide to tease him just as he perfects his invisible juice, and he goes on a spree of vengeance", fanart),
        ("[B]Dr. Minx 1:2 (1975)[/B]", "0DfAKK6nAos", 801, "Comedy, Drama, Crime", "A female physician finds no fun in brief affairs. Her luck finally seems to change with her latest lover, but when she learns that he is more interested in her money than her, murder ensues.", fanart),
        ("[B]Dr. Minx 2:2 (1975)[/B]", "Q38tdidCSK4", 801, "Comedy, Drama, Crime", "A female physician finds no fun in brief affairs. Her luck finally seems to change with her latest lover, but when she learns that he is more interested in her money than her, murder ensues.", fanart),
        ("[B]Attack of the 50 Foot Cheerleader (2012)[/B]", "kgNJfiJs_i0", 801, "Sports, Comedy, Sport", "Cassie Stratford consumes an experimental drug that grants her beauty and enough athletic ability to make the cheer squad. The drug has an unforeseen side effect - Cassie starts to grow and grow and grow.", fanart),
        ("[B]Lap Dance (2014)[/B]", "P6eeEGOCUeE", 801, "Drama", "An aspiring actress makes a pact with her fiance to take a job as an exotic dancer to care for her cancer stricken father", fanart),
        ("[B]Lady Frankenstein (1971)[/B]", "XpDdQERwto0", 801, "Horror", "Baron Frankenstein (Joseph Cotten) is hard at work trying to reanimate human tissue when his daughter, Tania (Rosalba Neri), comes home from university with a medical degree and announces that it has always been her intention to carry on her fathers work.", fanart),
        ("[B]Basic Training (1985)[/B]", "P6Zv2-Sb_9s", 801, "Comedy", "Melinda comes to Washington DC to visit her friend Debbie, and to find a job in government, where she hopes to do her part to make it better.", fanart),
        ("[B]Deep End (1970)[/B]", "8GloyJ9IGao", 801, "Comedy, Drama, Romance", "15-year-old dropout Mike takes a job at Newford Baths, where inappropriate sexual behaviour abounds, and becomes obsessed with his coworker Susan.", fanart),
        ("[B]I Am A Groupie (1970)[/B]", "6UHl0CIZdQA", 801, "Drama, Music", "18+ Beautiful blonde madly fell in love with a rock star.", fanart),
        ("[B]Unkissed Bride (1966)[/B]", "EwV1yVELoPk", 801, "Classic, Comedy", "A young couples honeymoon is disrupted by the grooms childhood obsession with Mother Goose. Unable to consummate the marriage, they head off to the psychiatrist, where the fun really begins (LSD as a treatment!?!).", fanart),
        ("[B]Spaced Out (1979)[/B]", "bibSkigeCu8", 801, "Comedy, Scifi", "Low-budget aliens (three nice-looking women and a gay computer voice-over) crash-land in England and abduct four earthlings.", fanart),
        ("[B]Whos Your Daddy (2004)[/B]", "bZ8qPP4hvqw", 801, "Comedy", "Chris Hughes, an awkward high school student struggling to be popular, suddenly finds himself the unwitting heir and appointed mogul of a vast, multimillion-dollar adult entertainment media empire left to him by the biological parents he never knew.", fanart),
        ("[B]Taking It Off (1985)[/B]", "FTlQhZ62wYQ", 801, "Comedy", "A stripper named Betty Bigones wants to be an actress, but is informed by her agent that her large breasts are keeping her from getting parts.", fanart),
        ("[B]Hot Moves (1984)[/B]", "t4lTYI6AQKQ", 801, "Comedy", "Four Venice Beach boys make a pact to lose their virginity before beginning their senior year of high school.", fanart),
        ("[B]Spanking the Monkey (1994)[/B]", "YxohvBpzQfY", 801, "Comedy, Drama", "Susan is a troubled woman, and along with Raymonds own emotional strains, it leads them to intimate physical contact, which Raymond finds uneasy. He soon meets a high school girl, Toni, but his ability to handle starting a relationship with her is difficult", fanart),
        ("[B]Private Obsession (1995)[/B]", "pjCIPxP1FoI", 801, "Drama, Thriller", "Emanuelle, a world famous fashion model, is held captive by Richard Tate, a crazed fan. Richard wants her for himself but Emanuelle uses her assets to try and escape.", fanart),
        ("[B]Crazy Little Thing (2002)[/B]", "lY0RjYRd1VM", 801, "Comedy, Romance", "A waiter/writer living with his dad and a neat freak who has just landed a job as a reporter in New York, meet by colliding on the Brooklyn Bridge, and romance ensues.", fanart),
        ("[B]Hollywood Hot Tubs (1984)[/B]", "5jJzVmWnl24", 801, "Comedy", "A young man gets a job repairing hot tubs for the rich and famous in Tinseltown, thanks to his parents. As he moves from one bubbly tub to the next, sexual situations change accordingly.", fanart),
        ("[B]Recruits (1986)[/B]", "zJ6isUDUdM8", 801, "Comedy", "A Canadian sex comedy in the tradition of Police Academy", fanart),
        ("[B]Pink Motel (1982)[/B]", "Nv-6eBv5UeA", 801, "Comedy", "A couple who own and run a cheap motel have to put up with an assortment of weirdos and perverts who rent rooms there on a Friday night.", fanart),
        ("[B]Disco Beaver From Outer Space (1979)[/B]", "eeVyOuDYrks", 801, "Comedy, Horror, Fantasy", "National Lampoons mockery of everything that is wrong with cable TV.", fanart),
        ("[B]Blood Sisters (1987)[/B]", "0tVCHNQZY88", 801, "Horror, Thriller", "Seven girls must spend the night in an old house, which once was a brothel, as part of an initiation.", fanart),
        ("[B]Emanuelle And The White Slave Trade (1978)[/B]", "5X55RnXBsjo", 801, "Romance, Action, Drama", "Emanuelle is in Kenya to arrange an interview with the Italian American gangster George Lagnetti", fanart),
        ("[B]All Ladies Do It (1992)[/B]", "1zj5cwulPEE", 801, "Comedy, Drama", "Italian - A happily married 24-year-old woman who experiences an inexplicable, rather restless craving to finally live her life intensely, retells her extra-marital escapades to her husband intending to spice up their marriage.", fanart),
        ("[B]Play Motel (Italiano) (1979)[/B]", "2PvrKgUlSJQ", 801, "Crime, Drama, Comedy", "A reporter and his girlfriend investigate deaths surrounding a hotel where several prominent people go to have sex", fanart),
        ("[B]A Woman For All Men (1975)[/B]", "e73AlfP0Lw0", 801, "Drama, Crime", "Irascible and domineering millionaire Walter McCoy marries the beautiful, but shady and duplicitous Karen Petrie. Walters son Steve automatically becomes smitten with Karen while both Walters daughter Cynthia suspect that something is up. This provokes a tangled web of deception, infidelity, and even murder.", fanart),
        ("[B]Cougar Hunting (2011)[/B]", "oJO15FYAdi0", 801, "Comedy", "Tells the tale of three buddies in their 20s whose love-lives are in shambles. They go to Aspen to pursue the booming trend of dating cougars: hot older women who prey on hot young guys.", fanart),
        ("[B]Die Watching (1993)[/B]", "EJXXyIvf94c", 801, "Romance, Thriller", "A serial killer who makes his living as an adult video maker/editor, becomes involved with an artist neighbour. He tries to keep his secret from her, but the police are slowly closing in on him.", fanart),
        ("[B]Love & Sex (2000)[/B]", "DRN_geRk-Cs", 801, "Comedy, Drama, Romance", "Kate is fired from a womens magazine for writing about BJs, based on own experience as requested. She gets a last chance - 2500 happy, perky words on finding/keeping that perfect man. She tells about her relationships.", fanart),
        ("[B]Emanuelle and the Last Cannibals (1977)[/B]", "oLnMlhmiwyk", 801, "Horror, Action", "A female journalist decides to traverse the Amazon Jungle after going undercover in a mental asylum and witnessing a disturbing behavior from a rescued white woman, who she believes was raised by a cannibalistic tribe long thought extinct.", fanart),
        ("[B]Wicket City (1987)[/B]", "LXEt0aVKHxY", 801, "Anime, Horror, Fantasy", "Two agents - a lady-killer human and a voluptuous demon - attempt to protect a signatory to a peace ceremony between the human world and the Black World from radicalized demons. ", fanart),
        ("[B]Lady Death (2004)[/B]", "iZjG9GeyeRE", 801, "Anime, Action, Fantasy", "Based on a comic book series. A woman burned at the stake in 15th century Sweden actually is Lucifers daughter - and plots revenge against him.", fanart),
        ("[B]Vampire Wars (1990)[/B]", "dh7W6euTIsw", 801, "Anime, Action, Crime", "First, a brutal terrorist attack on a NASA base takes place deep in the Arizona desert. Then ten days later, the corpse of a CIA man is found floating in the Seine in Paris.", fanart),
        ("[B]Russ Meyer Movie: MONDO TOPLESS (1966)[/B]", "2FrgpmdC4kg", 801, "Docs", "18+ Completely topless. Completely uninhibited. The craze that began in San Francisco", fanart),
        ("[B]All American Bikini Car Wash (2015)[/B]", "XB2z2zL7jdM", 801, "Comedy", "An enterprising college student agrees to run his professors Las Vegas car wash to avoid flunking out of school. But its Vegas gone wild when he decides to staff it with gorgeous bikini-clad girls. ", fanart),
        ("[B]Castaway (1986)[/B]", "Hp5cwfoHtlA", 801, "Drama,Action", "Middle-aged Gerald Kingsland advertises in a London paper for a female companion to spend a year with him on a desert island.", fanart),
        ("[B]Cinderella 2000 (1977)[/B]", "0-aeJjuUqQI", 801, "Music, Scifi", "In the year 2047, sex is forbidden and Big Brother uses robots to keep on eye on everyone. One young girl tries to outwit the government so she can be with the man she loves.", fanart),
        ("[B]Twisted Seduction (2010)[/B]", "O0zmAH4UbFA", 801, "Comedy, Romance, Thriller", "Genius British guy kidnaps a woman and is convinced that by following certain psychological steps and well planned charm, her brain will have no choice but to trigger feelings of love towards him.", fanart),
        ("[B]Slave Girls From Beyond Infinity (1986)[/B]", "138MfsLJQAw", 801, "Comedy, Action", "Lovely and resourceful Daria and Tisa escape a space gulag only to crash land on a nearby world where a guy in tight pants named Zed is playing The Most Dangerous Game.", fanart),
        ("[B]Joysticks (1983)[/B]", "GiFL3WhgV0c", 801, "Comedy", "When a top local businessman and his two bumbling nephews try to shut down the towns only video arcade, arcade employees and patrons fight back.", fanart),
        ("[B]The Vampire Lovers (1970)[/B]", "VlYQ4BCT_Ys", 801, "Horror", "Seductive vampire Carmilla Karnstein and her family target the beautiful and the rich in a remote area of late eighteenth-century Gemany.", fanart),
        ("[B]Lured Innocents (2000)[/B]", "dh1thVrs5N0", 801, "Drama, Thriller", "Elsie Townsend is a country towns-girl who wants to leave far away and get rich. She becomes the spoiled mistress of married local businessman Rick Chambers", fanart),
        ("[B]The Hitchhikers (1972)[/B]", "m45crVMbtCw", 801, "Action, Drama", "Maggie learns she is pregnant so she runs away from home. Before long she gets involved with some other girls on their own who have found a way of supporting themselves. She joins them in hitchhiking around wearing sexy outfits and robbing the men who pick them up on the road.", fanart),
        ("[B]Sorority Babes in the Slimeball Bowl-O-Rama (1988)[/B]", "UttvFSjxf24", 801, "Sports, Comedy, Horror", "As part of a sorority ritual, pledges and their male companions steal a trophy from a bowling alley; unbeknownst to them, it contains a devilish imp who makes their lives a living Hell.", fanart),
        ("[B]Dinosaur Island (1994)[/B]", "lkyKOGaJsfU", 801, "Action, Fantasy, Comedy", "An army captain is flying three misfit deserters home for a court martial when the plane has engine trouble and they must land on an uncharted island. There they find a primitive society of cave women who routinely sacrifice virgins", fanart),
        ("[B]Bikini Squad (1993)[/B]", "mUCD3l-iP1k", 801, "Comedy", "A woman director is hired to finish the season of Bikini Squad, a popular TV series about California beach lifeguards. A more than obvious lack of talent and basic intelligence among the crew make her contemplate leaving the set.", fanart),
        ("[B]Manhandlers (1974)[/B]", "3ea4Xkqb8Ho", 801, "Crime, Action, Drama", "A gorgeous girl named Katie inherits her deceased uncles business and decides that she too can be a businesswoman and hire two hot girlfriends. Katie does not like the brothel part so she gets rid of that and is soon giving legit massages.", fanart),
        ("[B]The Roommates (1973)[/B]", "xvEaJRA79VM", 801, "Crime, Drama, Thriller", "Heather, Beth, Carla, Brea, and Paula are five lovely ladies who decide to spend their summer vacation at Lake Arrowhead. While there the women hit the party circuit and get involved with various men. However, things go awry when the gals find themselves the targets of a mysterious murderer.", fanart),
        ("[B]The Body Shop (1972)[/B]", "zsYjUZIFDPU", 801, "Horror, Scifi", "Emminent plastic surgeon and mad scientist Don Brandon loses his wife Anitra - pinup model and social butterfly - in a tragic accident. He and his faithful humpbacked and drooling assistant Igor - oops, I mean Greg - busy themselves experimenting with re-animation experiments.", fanart),
        ("[B]Amazon Warrior (1998)[/B]", "gjEblPgw5QI", 801, "Action, Scifi", "A  post-apocalyptic world, a camp of Amazon women is raided by a gang of murderous bandits, who kill everyone in the camp except one small girl. She grows up to be a mercenary, and one day she takes a job escorting the two daughters of a powerful warlord across a river. ", fanart),
        ("[B]She (1984)[/B]", "YoxcpyXriEM", 801, "Action, Fantasy", "In a post-apocalyptic world, She aids two brothers quest to rescue their kidnapped sister. Along the way, they battle weird creatures before standing against the odds to defeat the evil Norks.", fanart),
        ("[B]Caged Heat (1974)[/B]", "nTedhTrzeNk", 801, "Action, Drama, Comedy", "In a womens prison, a group of inmates band together to combat the repressive and abusive policies of the warden.", fanart),
        ("[B]Barbarian Queen II (1990)[/B]", "OHSnaoJqv1w", 801, "Action, Fantasy", "In a final and epic battle in the thrilling sequel to the now classic Barbarian Queen, Althalia, leads a revolt of peasants and female warriors against the wicked ruler, Arkaris, to regain her throne.", fanart),
        ("[B]Barbarian Queen (1985)[/B]", "xI0Lf0gejnQ", 801, "Action, Fantasy", "The sword-wielding warrior, Amethea, embarks on a life-or-death mission to liberate her sister from the clutches of an evil monarch. However, only torture and death await her.", fanart),
        ("[B]So Sweet, So Dead (1972)[/B]", "0MAG8AgcV-8", 801, "Crime, Drama, Mystery", "A serial killer is on the loose. His victims are unfaithful wives and he always leaves compromising photographs at the crime scene.", fanart),
        ("[B]Swap Meet (1979)[/B]", "49AuoWyoW6Y", 801, "Comedy", "A brainless teen comedy, pepped up with a few moderate erotic scenes.", fanart),
        ("[B]A Taste For Women (1964)[/B]", "uwf_fIWvCCo", 801, "Classic, Comedy, Crime", "A secret sect of cannibals owns a vegetarian restaurant, which they use as a cover so they can find a beautiful young woman to serve as the main course at their full-moon sacrifice.", fanart),
        ("[B]The Man From O.R.G.Y. (1970)[/B]", "_nIzIz91XoA", 801, "Comedy, Crime", "A rich man suddenly dies and leaves his vast fortune to a Madam who played a number of female stars for him. She dies too, and leaves her inheritance to her top three girls, all living in different parts of the world - and the map to the fortune location can be uncovered only when their three bottoms are placed together.", fanart),
        ("[B]Nude on the Moon (1961)[/B]", "czxgLpcFovg", 801, "CLassic, Fantasy, Scifi", "A rich rocket scientist organizes an expedition to the moon, which they discover is inhabited by nude women.", fanart),
        ("[B]Six Pack Annie (1975)[/B]", "-maWwgpNyOA", 801, "Action, Comedy, Romance", "Busty, blonde and beautiful, Six-Pack Annie seeks to help her Aunt Tess raise $5,000 for the family diner...by trying to find a rich daddy.", fanart),
        ("[B]Love on the Side (2004)[/B]", "0wgI4PocHEI", 801, "Comedy, Romance", "A small-town waitress vies with a sassy city slicker for the attention of the towns most eligible bachelor.", fanart),
        ("[B]The Swinging Barmaids (1975)[/B]", "AOF4ikg_2DY", 801, "Crime, Drama", "A deranged serial killer infiltrates a popular club and slowly starts killing cocktail waitresses.", fanart),
        ("[B]Just a Little Harmless Sex (1998)[/B]", "pG9kdDzctY8", 801, "Comedy, Romance", "A strictly monogamous man stops to help a stranded female with a broken down car. In gratitude she offers oral sex, when he reluctantly accepts. However, just as they get involved, the cops show up", fanart),
        ("[B]Gimme a F (1984)[/B]", "6EfS8fFi9BY", 801, "Comedy, Sports", "Can a squad of misfit cheerleaders with an over-age trainer possibly win the big cheerleading competition? Looked down upon by the other teams, it will be an difficult.", fanart),
]

#=====================================

class sexyListing:

    @staticmethod
    def Genres(type):
		
        #errorMsg="%s" % (type)
        #xbmcgui.Dialog().ok("type", errorMsg)

        for name, url, zmode, genre, desc, fanart in sorted(channellist, reverse=False):

            addIt=False
            if type is "All":
                icon=genreImage+"All.png"
                addIt=True

            elif "Action" in genre and type is "Action":
                icon=genreImage+"Action.png"
                addIt=True

            elif "Anime" in genre and type is "Anime":
                icon=genreImage+"Anime.png"
                addIt=True

            elif "Classic" in genre and type is "Classic":
                icon=genreImage+"Classic.png"
                addIt=True

            elif "Comedy" in genre and type is "Comedy":
                icon=genreImage+"Comedy.png"
                addIt=True

            elif "Crime" in genre and type is "Crime":
                icon=genreImage+"Crime.png"
                addIt=True

            elif "Docs" in genre and type is "Docs":
                icon=genreImage+"Documentary.png"
                addIt=True

            elif "Drama" in genre and type is "Drama":
                icon=genreImage+"Drama.png"
                addIt=True

            elif "Romance" in genre and type is "Romance":
                icon=genreImage+"Romance.png"
                addIt=True

            elif "Fantasy" in genre and type is "Fantasy":
                icon=genreImage+"Fantasy.png"
                addIt=True

            elif "Horror" in genre and type is "Horror":
                icon=genreImage+"Horror.png"
                addIt=True

            elif "Music" in genre and type is "Music":
                icon=genreImage+"Music.png"
                addIt=True

            elif "Mystery" in genre and type is "Mystery":
                icon=genreImage+"Mystery.png"
                addIt=True

            elif "Scifi" in genre and type is "Scifi":
                icon=genreImage+"Scifi.png"
                addIt=True

            elif "Sports" in genre and type is "Sports":
                icon=genreImage+"Sports.png"
                addIt=True
				
            elif "Thriller" in genre and type is "Thriller":
                icon=genreImage+"Thriller.png"
                addIt=True

            elif "Western" in genre and type is "Western":
                icon=genreImage+"Western.png"
                addIt=True

            elif "Zombie" in genre and type is "Zombie":
                icon=genreImage+"Zombie.png"
                addIt=True
		
            if addIt==True:
                name = name +" | " +desc
				
                #MyAddLink(name, url, zmode, icon, fanart, desc)				
                addLink(name,url,zmode,icon,fanart)
                #if desc:
                    #add_link_info(desc, "", fanart)

				
#=====================================

