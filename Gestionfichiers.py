import os
import random
import string

here = os.path.dirname(os.path.abspath(__file__))

pathmedia= os.path.join(here,"MEDIAAPOST")

def rename():
    inpathmedianame=os.listdir(pathmedia)

    for i in inpathmedianame:
        for k in os.listdir(os.path.join(pathmedia,i)):
            if k.endswith(".jpg"):
                os.rename(os.path.join(pathmedia,i,k),os.path.join(pathmedia,i,"media.jpg"))
            if k.endswith(".png"):
                os.rename(os.path.join(pathmedia,i,k),os.path.join(pathmedia,i,"media.png"))
            if k.endswith(".txt"):
                os.rename(os.path.join(pathmedia,i,k),os.path.join(pathmedia,i,"texte.txt"))

def creatdossier():
    inpathmedianame=os.listdir(pathmedia)
    for i in inpathmedianame:
        if i.endswith(".jpg"):
            new_abs_path = os.path.join(pathmedia, ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)))
            if not os.path.exists(new_abs_path):
                os.mkdir(new_abs_path)
                os.rename(os.path.join(pathmedia,i),os.path.join(new_abs_path,"media.jpg"))
                with open(os.path.join(new_abs_path,'texte.txt'), 'w') as fp:
                    pass




