import os
from posixpath import split

from time import sleep

import time

from typing import Dict, List

from google_auth_oauthlib import get_user_credentials

from random import randint,choice

from instagrapi import Client

from instagrapi.types import UserShort

from instagrapi.exceptions import UserNotFound

from instagrapi.utils import json_value

from instagrapi.extractors import extract_user_gql, extract_user_short, extract_user_v1

from instagrapi.exceptions import LoginRequired

from wakepy import set_keepawake, unset_keepawake

IG_USERNAME = 'beaux_poemes_fr'
IG_PASSWORD = 'POem123!'
IG_CREDENTIAL_PATH = './ig_settings.json'
SLEEP_TIME = 400 # in seconds


class Bot:
    _cl = None

    def __init__(self,infoslogin,listargs5):
        self.heure=time.localtime()
        
        
        #CONNECTION----------------------------------
        self._cl = Client()
        if os.path.exists(IG_CREDENTIAL_PATH):
            self._cl.load_settings(IG_CREDENTIAL_PATH)
            self._cl.login(infoslogin[0], infoslogin[1])
            try:
                bot_account = self._cl.account_info()
            except LoginRequired:
                self._cl.relogin()
            self._cl.dump_settings(IG_CREDENTIAL_PATH)
            self.listabos=self.get_followers()
            self.listsuivis=self.get_following()
        else:
            self._cl.login(infoslogin[0], infoslogin[1])
            self._cl.dump_settings(IG_CREDENTIAL_PATH)

        #---------------------------------------------

        
        self.pathmediaapost=listargs5[0]
        self.listeinflusuivis=listargs5[1]
        self.htgasuivre=listargs5[2]
        self.liste_commentairesuniv=listargs5[3]
        self.liste_addcommpop=listargs5[4]


#SABO--------------------------------------------------------------------------------------------
    def follow_by_username(self, username) -> bool:
        """
        Follow a user
        Parameters
        ----------
        username: str
            Username for an Instagram account
        Returns
        -------
        bool
            A boolean value
        """
        userid = self._cl.user_id_from_username(username)
        return self._cl.user_follow(userid)

    def unfollow_by_username(self, username) -> bool:
        """
        Unfollow a user
        Parameters
        ----------
        username: str
            Username for an Instagram account
        Returns
        -------
        bool
            A boolean value
        """
        userid = self._cl.user_id_from_username(username)
        return self._cl.user_unfollow(userid)
    
    def get_followers(self, amount: int = 0) -> Dict[int, UserShort]:
        """
        Get bot's followers
        Parameters
        ----------
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf
        Returns
        -------
        Dict[int, UserShort]
            Dict of user_id and User object
        """
        return self._cl.user_followers(self._cl.user_id, amount=amount)
    
    def get_followers_usernames(self, amount: int = 0) -> List[str]:
        """
        Get bot's followers usernames
        Parameters
        ----------
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf
        Returns
        -------
        List[str]
            List of usernames
        """
        followers = self._cl.user_followers(self._cl.user_id, amount=amount)
        return [user.username for user in followers.values()]

    def get_following(self, amount: int = 0) -> Dict[int, UserShort]:
        """
        Get bot's followed users
        Parameters
        ----------
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf
        Returns
        -------
        Dict[int, UserShort]
            Dict of user_id and User object
        """
        return self._cl.user_following(self._cl.user_id, amount=amount)
    
    def get_following_usernames(self, amount: int = 0) -> List[str]:
        """
        Get bot's followed usernames
        Parameters
        ----------
        amount: int, optional
            Maximum number of media to return, default is 0 - Inf
        Returns
        -------
        List[str]
            List of usernames
        """
        following = self._cl.user_following(self._cl.user_id, amount=amount)
        return [user.username for user in following.values()]
    
    def tstflr(self,username):
        c=self._cl.user_info_by_username(username)
        f=c.follower_count
        g=c.following_count
        if g>f:
            return True
        else:
            return False

    def getusrflwers(self,username,amount):
        a=self._cl.user_id_from_username(username)
        list=self._cl.user_followers_gql(a,amount)
        list1=[]
        for i in list:
            list1.append(i.username)
        return list1
    
    def getusrflwersnsuivis(self,username,amount):
        amount1=amount
        compte=0
        while amount1!=compte:
            li=self.getusrflwers(username,amount)
            compte=0
            for i in range(len(li)):
                if li[i] not in self.listabos:
                    compte+=1
            amount+=amount-compte
        return li

    def getusrflwerssivpas(self,username,amount):
        amount1=amount
        compte=0
        while amount1!=compte:
            li=self.getusrflwers(username,amount)
            compte=0
            for i in range(len(li)):
                if li[i] not in self.listsuivis:
                    compte+=1
            amount+=amount-compte
        return li

    def getusrsansrap(self,username,amount):
        amount1=amount
        compte=0
        while amount1!=compte:
            li=self.getusrflwers(username,amount)
            compte=0
            for i in range(len(li)):
                if li[i] not in self.listabos and li[i] not in self.listsuivis :
                    compte+=1
            amount+=amount-compte
        return li

    def choiceabbos(self,username,amount):
        compte=0
        print("oj")
        li1=[]
        while len(li1)<amount:
            li1=[]
            li=self.getusrflwers(username,amount)
            compte=0
            #blacklist =[]
            print("ok1")
            for i in range(len(li)):
                if li[i] not in self.listabos and li[i] not in self.listsuivis:
                    print("ok3")
                    if self.tstflr(li[i]):
                        print("ok4")
                        li1.append(li[i])
                        compte+=1
            amount+=compte

        """    def sabosqqn(self):

                    
                    
        #print(li1)
        
        
        
        for i in range(len(li)):
            print("ok5")
            #self.follow_by_username(li[i])
            sleep(randint(2,30))
          """      
    
    def saboqqnabos(self,username,nb):
        list=self.getusrflwers(username,nb)
        for i in range(nb):
            self.follow_by_username(list[i])
            
            sleep(randint(2,30))

    def sabov1(self,liste,nb):
        for i in (liste):
            self.saboqqnabos(i,nb)


#PUB--------------------------------------------------------------------------------------------

    #Popular medias:---------------------------------------------------------
    def likepophtg(self,htg):
        top=self._cl.hashtag_medias_top(htg,9)
        strtop=[]
        for i in top:
            strtop.append(i.id)
        for i in strtop:
            self._cl.media_like(i)

    def commenthtgpop(self,htg,liste):
        top=self._cl.hashtag_medias_top(htg,9)
        strtop=[]
        for i in top:
            strtop.append(i.id)
        for i in strtop:
            self._cl.media_like(i)
            self._cl.media_comment(i,choice(liste))

    #Recent medias:---------------------------------------------------------
    def likehtg(self,htg,nb):
        top=self._cl.hashtag_medias_recent(htg,nb)
        strtop=[]
        for i in top:
            strtop.append(i.id)
        for i in strtop:
            self._cl.media_like(i)

    def commenthtg(self,htg,liste,nb):
        top=self._cl.hashtag_medias_top(htg,nb)
        strtop=[]
        for i in top:
            strtop.append(i.id)
        for i in strtop:
            self._cl.media_like(i)
            self._cl.media_comment(i,choice(liste))
            
    def activite(self,pop,pap):

        #pop-------------
        self.likepophtg()


#POST--------------------------------------------------------------------------------------------

    def gethtg(list):

        pass

    def selectfolder(self,rep1):
        listname = os.listdir(rep1)
        print(listname)
        name = choice(listname)
        name = os.path.join(rep1,name)
        return name

    def createpost(self,file):
        path=self.selectfolder(file)

        with open(file+'\texte.txt') as f:
            lines = f.readlines()

            c=lines.split(";")
            htg="".join(htgasuivre)
            desc=c[0]+".\n.\n.\n.\n.\n.\n.\n"+phrasedesc+".\n.\n"+htg+c[1]
            
        

        photo = path+"\media.jpg"
        return photo,lines

    def uploadmedia(self,file):
        #a modif, pr l'instant photo
        P,T = self.createpost(file)
        self.photo_upload(P, T)


#UPDATE------------------------------------------------------------------------------------------

    def action(self,horaire,action,*args):
        if self.heure.tm_hour==horaire:
            b,*end =args
            time.sleep(randint(1,10))
            action(b,*end)

    def update(self):
        
        self.heure=time.localtime()
        
        
        #8h__PREMIER_POST------------------------------------------------------------------------

        self.action(8,self.uploadmedia,self.pathmediaapost)
        
        #9h__100_PERSONNES-----------------------------------------------------------------------

        self.action(9,self.sabov1,self.listeinflusuivis,10)

        #12h__20comhtg+70likes-------------------------------------------------------------------

        self.action(12,self.commenthtgpop,choice(self.htgasuivre),choice(self.liste_commentairesuniv + choice(self.liste_addcommpop)))
        self.action(12,self.commenthtg,choice(self.htgasuivre),choice(self.liste_commentairesuniv),11)
        self.action(12,self.likehtg,choice(self.htgasuivre),70)

        #13h__100_PERSONNES-----------------------------------------------------------------------

        self.action(13,self.sabov1,self.listeinflusuivis,10)

        #18h__DEUXIEME_POST----------------------------------------------------------------------

        #pr l'instant flemme

        #19h__9comhtgp+50likes+10comnorm---------------------------------------------------------

        self.action(19,self.commenthtgpop,choice(self.htgasuivre),choice(self.liste_commentairesuniv + choice(self.liste_addcommpop)))
        self.action(19,self.commenthtg,choice(self.htgasuivre),choice(self.liste_commentairesuniv),11)
        self.action(19,self.likehtg,choice(self.htgasuivre),70)

        #20h__100_PERSONNES----------------------------------------------------------------------

        self.action(20,self.sabov1,self.listeinflusuivis,10)

        #self.action(18,print,self.heure.tm_hour)




#BOT1-------------------------------------------------------------------------------------------- 
       

here = os.path.dirname(os.path.abspath(__file__))

pathmediaapost= os.path.join(here,"MEDIAAPOST")

listeinflusuivis=[
"liliana_jasnyjewelry",
"haremsjewel",
"lelaleagems",
"mahgold_gallery",
"giagrams",
"jewelryathenaeum",
"eastwestgemco",
"galerie.lydia.rupp",
"ronaldabram",
"lightworker_jewellery",
"atelier.nanako",
"badis_jewelers",
]

htgasuivre=[
    "#gemstonejewelry"
    "#gemstoneearrings"
    "#jewelry"
    "#diamond"
    "#gold"
    "#emerald"
    "#rings"
    "#necklace"
    "#necklaceoftheday"
    "#necklacelovers"
    "#ring"
    "#jewelrydesigner"
    "#jewellery"
    "#jewelryaddict"
]

liste_commentairesuniv=[


]

liste_addcommpop=[

]

phrasedesc="Yo! Check our account to see our creations !!"


BOT1=[
    pathmediaapost,
    listeinflusuivis,
    htgasuivre,
    liste_commentairesuniv,
    liste_addcommpop
    ]

IG_USERNAME = 'beaux_poemes_fr'
IG_PASSWORD = 'POem123!'
IG_CREDENTIAL_PATH = './ig_settings.json'
SLEEP_TIME = 400 # in seconds

#MAIN---------------------------------------------------------------------------------------------



set_keepawake(keep_screen_awake=False)


if __name__ == '__main__':
    bot = Bot()

    while True:
        """
        Infnit loop
        """
        bot.update()
        time.sleep(SLEEP_TIME)


# do stuff that takes long time
unset_keepawake()
        


        
        
        





