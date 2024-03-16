
##Animal Simulation

import pygame,sys,random,math
from pygame.locals import*

pygame.init()

infoObject=pygame.display.Info()
screen=pygame.display.set_mode((1600,900))
pygame.display.set_caption("Animal Simulation")
clock=pygame.time.Clock()


font1 = pygame.font.Font('gomarice_game_continue_02.ttf', 32)##font5

dead=pygame.image.load("dead.png").convert_alpha()
rabbit=pygame.image.load("rabbit.png").convert_alpha()
fox=pygame.image.load("fox.png").convert_alpha()
water=pygame.image.load("water.jpg").convert()
tallGrass=pygame.image.load("tallGrass.png").convert_alpha()

#####Speed
speed=1
generation=0


class Grass():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.fullness=1
        
    def draw(self):
        r=100+39*(1-self.fullness)
        g=255-186*(1-self.fullness)
        b=100-81*(1-self.fullness)
        green=(r,g,b)
        pygame.draw.rect(screen,green,(self.x,self.y,100,100),0)
        if self.fullness<1:
            self.fullness+=0.0002*speed
        if self.fullness>=1:
            screen.blit(tallGrass,(self.x,self.y))

grassList=[]
for i in range(14):
    for j in range(7):
        grassList.append(Grass(100+i*100,100+j*100))

class Animal():
    def __init__(self,x,y,animaltype):
        self.x=x
        self.y=y
        self.sex=random.choice(["male","female"])
        self.food=30
        self.water=30
        self.health=10
        self.maxHealth=10
        if animaltype=="fox":
            self.food=100
            self.health=20
            self.maxHealth=20
        self.speed=2
        self.type=animaltype
        self.loss=1
        self.mate=60
        self.mateIncrease=0.8
        self.age=1
        

    def evolve(self):
        
        ##Random evolution things
        evolve=random.randint(0,5)
        
        if evolve==0:
            self.maxHealth+=0.5
            self.loss+=0.05
        elif evolve==1:
            self.speed+=0.2
            self.loss+=0.05
        elif evolve==2:
            self.mateIncrease+=0.01
            self.loss+=0.05
        elif evolve==3:
            self.maxHealth-=0.5
            self.loss-=0.05
        elif evolve==4:
            self.speed-=0.2
            self.loss-=0.05
        elif evolve==5:
            self.mateIncrease-=0.01
            self.loss-=0.05
            
    def draw(self):
        if self.type=="rabbit":
            screen.blit(rabbit,(self.x,self.y))
        elif self.type=="fox":
            screen.blit(fox,(self.x,self.y))

    def subtract(self):
        self.food-=0.1*speed*self.loss
        self.water-=0.1*speed*self.loss
        if self.type=="rabbit":
            self.mate+=0.5*speed*self.mateIncrease
        else:
            self.mate+=0.2*speed*self.mateIncrease
        self.age+=0.1*speed

        if self.health<self.maxHealth:
            self.health+=0.01*speed
        
        if self.water<0 or self.food<0:
            self.health-=0.1*speed
        if self.health<0:
            return True
        return False


    
    def move(self):
        global animalList,deadList
        closest=None
        if self.type=="rabbit":
            closest=None
            for i in animalList:
                distance=math.sqrt(abs((i.x+25)-(self.x+25))**2+abs((i.y+25)-(self.y+25))**2)
                if i.type=="fox" and distance<50 and i.food<100:
                    closest=i
        if closest!=None:
            if closest.x<self.x and self.x<1400:
                self.x+=self.speed*speed
            elif closest.x>self.x and self.x>100:
                self.x-=self.speed*speed
                
            if closest.y<self.y and self.y<750:
                self.y+=self.speed*speed
            elif closest.y>self.y and self.y>100:
                self.y-=self.speed*speed
                
            
        elif self.water<50:
            minimum=10000
            if abs(self.x+25-100)<minimum:
                direction="left"
                minimum=abs(self.x+25-100)
            if abs(1450-self.x+25)<minimum:
                direction="right"
                minimum=abs(1450-self.x+25)
            if abs(self.y+25-100)<minimum:
                direction="up"
                minimum=abs(self.y+25-100)
            if abs(800-(self.y+25))<minimum:
                direction="down"
                minimum=abs(800-(self.y+25))
            if minimum<20:
                self.water+=50
            else:
                if direction=="left":
                    self.x-=self.speed*speed
                elif direction=="right":
                    self.x+=self.speed*speed
                elif direction=="up":
                    self.y-=self.speed*speed
                elif direction=="down":
                    self.y+=self.speed*speed
                    
        elif self.food<50 and self.type=="rabbit":
            closest=10000
            number=0
            closeNum=0
            for i in grassList:
                distance=math.sqrt(abs((i.x+50)-(self.x+25))**2+abs((i.y+50)-(self.y+25))**2)
                if distance<closest and i.fullness>0.2:
                    closest=distance
                    closeNum=number

                number+=1
            #print(closest)
            if grassList[closeNum].fullness>0.2:
                if closest<25:
                    self.food+=30
                    grassList[closeNum].fullness-=0.2
                else:
                    if grassList[closeNum].x+50<self.x+25:
                        self.x-=self.speed*speed
                    elif grassList[closeNum].x+50>self.x+25:
                        self.x+=self.speed*speed
                    if grassList[closeNum].y+50<self.y+25:
                        self.y-=self.speed*speed
                    elif grassList[closeNum].y+50>self.y+25:
                        self.y+=self.speed*speed
        elif self.food<100 and self.type=="fox":
            closest=10000
            number=0
            closeNum=0
            for i in animalList:
                distance=math.sqrt(abs((i.x+25)-(self.x+25))**2+abs((i.y+25)-(self.y+25))**2)
                if distance<closest and i.type=="rabbit":
                    closest=distance
                    closeNum=number
                number+=1

            if closest!=10000:     
                if closest<25:
                    self.food+=400
                    animalList.pop(closeNum)
                    new=[self.x,self.y]
                    deadList.append(new)
                else:
                    if animalList[closeNum].x+25<self.x+25:
                        self.x-=self.speed*speed
                    elif animalList[closeNum].x+25>self.x+25:
                        self.x+=self.speed*speed
                    if animalList[closeNum].y+25<self.y+25:
                        self.y-=self.speed*speed
                    elif animalList[closeNum].y+25>self.y+25:
                        self.y+=self.speed*speed






                
        elif self.mate>80:
            if self.sex=="male":
                closest=10000
                number=0
                closeNum=0
                for i in animalList:
                    distance=math.sqrt(abs((i.x+25)-(self.x+25))**2+abs((i.y+25)-(self.y+25))**2)
                    if distance<closest and i.x!=self.x and i.sex=="female" and i.type==self.type and i.mate>20:
                        closest=distance
                        closeNum=number
                    number+=1
                if closest!=10000:
                    if closest<25 and self.mate>100 and animalList[closeNum].mate>100:
                        animalList.append(Animal(random.randint(round(self.x),round(self.x)),random.randint(round(self.y),round(self.y)),self.type))
                        animalList[-1].speed=(self.speed+animalList[closeNum].speed)/2
                        animalList[-1].maxHealth=(self.maxHealth+animalList[closeNum].maxHealth)/2
                        animalList[-1].mateIncrease=(self.mateIncrease+animalList[closeNum].mateIncrease)/2
                        animalList[-1].loss=(self.loss+animalList[closeNum].loss)/2
                        animalList[-1].evolve()

                        
                        self.mate=0
                        animalList[closeNum].mate=0
                        self.food-=30

                    else:
                        if animalList[closeNum].x+25<self.x+25:
                            self.x-=self.speed*speed
                        elif animalList[closeNum].x+25>self.x+25:
                            self.x+=self.speed*speed
                        if animalList[closeNum].y+25<self.y+25:
                            self.y-=self.speed*speed
                        elif animalList[closeNum].y+25>self.y+25:
                            self.y+=self.speed*speed
        elif self.type=="fox":
            closest=10000
            number=0
            closeNum=0
            for i in animalList:
                distance=math.sqrt(abs((i.x+25)-(self.x+25))**2+abs((i.y+25)-(self.y+25))**2)
                if distance<closest and i.type=="rabbit":
                    closest=distance
                    closeNum=number
                number+=1

            if closest!=10000:     
                    if animalList[closeNum].x+25<self.x+25:
                        self.x-=self.speed*speed
                    elif animalList[closeNum].x+25>self.x+25:
                        self.x+=self.speed*speed
                    if animalList[closeNum].y+25<self.y+25:
                        self.y-=self.speed*speed
                    elif animalList[closeNum].y+25>self.y+25:
                        self.y+=self.speed*speed
            
            
        
animalList=[Animal(random.randint(200,400),random.randint(500,700),"rabbit"),Animal(random.randint(200,400),random.randint(500,700),"rabbit"),
            Animal(random.randint(1000,1300),random.randint(200,400),"fox"),Animal(random.randint(1000,1300),random.randint(200,400),"fox")]
animalList[0].sex="male"
animalList[1].sex="female"
animalList[2].sex="male"
animalList[3].sex="female"
"""
for i in range(1):
    animalList.append(Animal(random.randint(200,1300),random.randint(200,700),"rabbit"))
"""



def island():
    pygame.draw.rect(screen,(139,69,19),(100,100,1400,700),0)
    for i in grassList:
        i.draw()

def animals():
    global animalList,deadList
    for i in animalList:
        i.move()
        i.draw()
        dead=i.subtract()
        if dead==True:
            animalList.remove(i)
            new=[i.x,i.y]
            deadList.append(new)
        elif i.age>200 and i.type=="rabbit":
            animalList.remove(i)
            new=[i.x,i.y]
            deadList.append(new)
        elif i.age>400 and i.type=="fox":
            animalList.remove(i)
            new=[i.x,i.y]
            deadList.append(new)
          
deadList=[]
def drawDead():
    global deadList
    if len(deadList)>50:
        deadList.pop(0)
    for i in deadList:
        screen.blit(dead,(i[0],i[1]))


timer=0
graphList=[]
speedT=0
maxHealthT=0
mateIncreaseT=0
speedF=0
maxHealthF=0
mateIncreaseF=0

lossT=0
lossF=0



def graph():
    global graphList,timer,speedT,maxHealthT,mateIncreaseT,speedF,maxHealthF,mateIncreaseF,lossF,lossT
    
    rabbitCount,foxCount=0,0

    speedT=0
    maxHealthT=0
    mateIncreaseT=0
    speedF=0
    maxHealthF=0
    mateIncreaseF=0
    lossT=0
    lossF=0
   
    if (timer%10):
        for i in animalList:
            if i.type=="rabbit":
                rabbitCount+=1
                speedT+=i.speed
                maxHealthT+=i.maxHealth
                mateIncreaseT+=i.mateIncrease
                lossT+=i.loss
            else:
                foxCount+=1
                speedF+=i.speed
                maxHealthF+=i.maxHealth
                mateIncreaseF+=i.mateIncrease
                lossF+=i.loss
                
        new=[timer+200,rabbitCount,(255,255,255)]
        new2=[timer+200,foxCount,(255,0,0)]
        graphList.append(new)
        graphList.append(new2)

        
    popText=font1.render("Rabbits: "+str(rabbitCount),True,(255,255,255))
    screen.blit(popText,(10,20))
    popText=font1.render("Foxes: "+str(foxCount),True,(255,0,0))
    screen.blit(popText,(10,50))
    popText=font1.render("Speed: x"+str(speed),True,(255,255,255))
    screen.blit(popText,(10,860))


    ##Evolved rabbit stats
    if rabbitCount!=0:
        popText=font1.render("Speed: "+str(round(speedT/rabbitCount,2)),True,(0,0,0))
        screen.blit(popText,(1300,800))
        popText=font1.render("Health: "+str(round(maxHealthT/rabbitCount,2)),True,(255,255,0))
        screen.blit(popText,(1300,830))
        popText=font1.render("Mate Increase: "+str(round(mateIncreaseT/rabbitCount,2)),True,(255,255,0))
        screen.blit(popText,(1300,860))
    if foxCount!=0:
        popText=font1.render("Speed: "+str(round(speedF/foxCount,2)),True,(0,0,0))
        screen.blit(popText,(1000,800))
        popText=font1.render("Health: "+str(round(maxHealthF/foxCount,2)),True,(255,255,0))
        screen.blit(popText,(1000,830))
        popText=font1.render("Mate Increase: "+str(round(mateIncreaseF/foxCount,2)),True,(255,255,0))
        screen.blit(popText,(1000,860))

        

        
    biggest=0
    for i in graphList:
        if i[1]>biggest:
            biggest=i[1]

    pygame.draw.rect(screen,(0,0,0),(200,0,1200,98),0)
    for i in graphList:
        pygame.draw.rect(screen,i[2],(i[0],98-i[1]*(100/biggest),2,2),0)
        
    popText=font1.render("Generation: "+str(generation),True,(255,0,0))
    screen.blit(popText,(1220,10))
    
    timer+=0.1


def checkGone():
    global grassList,animalList,timer,graphList,generation
    fox=0
    rabbit=0
    for i in animalList:
        if i.type=="fox":
            fox+=1
        else:
            rabbit+=1
    if fox<=1 or rabbit<=1:
        for g in grassList:
            g.fullness=1
        animalList=[Animal(random.randint(200,400),random.randint(500,700),"rabbit"),Animal(random.randint(200,400),random.randint(500,700),"rabbit"),
                    Animal(random.randint(1000,1300),random.randint(200,400),"fox"),Animal(random.randint(1000,1300),random.randint(200,400),"fox")]
        animalList[0].sex="male"
        animalList[1].sex="female"
        animalList[2].sex="male"
        animalList[3].sex="female"

        for i in range(2):
            if rabbit<=1:
                animalList[i].speed=(speedT)
                animalList[i].maxHealth=(maxHealthT)
                animalList[i].mateIncrease=(mateIncreaseT)
                animalList[i].loss=(lossT)
                animalList[i].evolve()
            else:
                animalList[i].speed=(speedT/rabbit)
                animalList[i].maxHealth=(maxHealthT/rabbit)
                animalList[i].mateIncrease=(mateIncreaseT/rabbit)
                animalList[i].loss=(lossT/rabbit)
                animalList[i].evolve()
        for i in range(2):
            if fox<=1:
                animalList[2+i].speed=(speedF)
                animalList[2+i].maxHealth=(maxHealthF)
                animalList[2+i].mateIncrease=(mateIncreaseF)
                animalList[2+i].loss=(lossF)
                animalList[2+i].evolve()  

            else:
                animalList[2+i].speed=(speedF/fox)
                animalList[2+i].maxHealth=(maxHealthF/fox)
                animalList[2+i].mateIncrease=(mateIncreaseF/fox)
                animalList[2+i].loss=(lossF/fox)
                animalList[2+i].evolve()
        timer=0
        graphList=[]
        generation+=1
        

while True:
    screen.fill((100,150,255))
    screen.blit(water,(0,0))
    pygame.draw.rect(screen,(255,222,173),(80,80,1440,740),0)
    island()
    drawDead()
    animals()
    graph()
    checkGone()
    




    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==KEYDOWN:
            if event.key==K_r:
                for i in grassList:
                    i.fullness=1
            elif event.key==K_1:
                speed=1
            elif event.key==K_2:
                speed=2
            elif event.key==K_3:
                speed=3
            elif event.key==K_4:
                speed=4
            elif event.key==K_5:
                speed=5

            elif event.key==K_t:
                animalList=animalList[:int(len(animalList)/2)]
    pygame.display.update()
    clock.tick(60)


















    
