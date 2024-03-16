
##Animal Simulation test setup


import random,math
#####Speed
speed=1



class Grass():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.fullness=startFullness
        




class Animal():
    def __init__(self,x,y,animaltype):
        self.x=x
        self.y=y
        self.sex=random.choice(["male","female"])
        self.food=rabbitFood
        self.water=rabbitWater
        self.health=rabbitHealth
        self.maxHealth=rabbitHealth
        if animaltype=="fox":
            self.food=foxFood
            self.maxHealth=foxHealth
            self.health=foxHealth
        self.speed=speed2
        self.type=animaltype
        self.loss=1
        self.mate=60
        self.mateIncrease=1
        self.age=1
        

    def evolve(self):
        
        ##Random evolution things
        evolve=random.randint(0,5)
        
        if evolve==0:
            self.maxHealth+=1
            self.loss+=0.05
        elif evolve==1:
            self.speed+=0.5
            self.loss+=0.05
        elif evolve==2:
            self.mateIncrease+=0.02
            self.loss+=0.05
        elif evolve==3:
            self.maxHealth-=1
            self.loss-=0.05
        elif evolve==4:
            self.speed-=0.5
            self.loss-=0.05
        elif evolve==5:
            self.mateIncrease-=0.05
            self.loss-=0.05
            

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
        global animalList
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
            
            




def animals():
    global animalList,deadList,foxCount,rabbitCount
    foxCount=0
    rabbitCount=0
    for i in animalList:
        i.move()
        dead=i.subtract()

        if i.type=="fox":
            foxCount+=1
        if i.type=="rabbit":
            rabbitCount+=1


        
        if dead==True:
            animalList.remove(i)

        elif i.age>rabbitAge and i.type=="rabbit":
            animalList.remove(i)

        elif i.age>foxAge and i.type=="fox":
            animalList.remove(i)


          





timer=0
graphList=[]
allDead=False
foxCount=0
rabbitCount=0

while timer<20000:
    
    allDead=False
    timer=0
    startFullness=random.uniform(0.3,1)
    rabbitFood=random.randint(20,100)
    
    rabbitWater=30
    foxFood=100

    rabbitHealth=10
    foxHealth=50
    speed2=2

    rabbitAge=200
    foxAge=400
    
    grassList=[]
    for i in range(14):
        for j in range(7):
            grassList.append(Grass(100+i*100,100+j*100))    

    
    animalList=[Animal(300,600,"rabbit"),Animal(300,600,"rabbit"),
                Animal(1200,300,"fox"),Animal(1200,300,"fox")]
    animalList[0].sex="male"
    animalList[1].sex="female"
    animalList[2].sex="male"
    animalList[3].sex="female"
    
    while allDead==False:

        animals()
        if len(animalList)==0 or foxCount==0 or len(animalList)>300 or rabbitCount==0:
            allDead=True
            print(startFullness,rabbitFood)
            print(timer)
        timer+=1

        
print(timer)

print(startFullness,rabbitFood,rabbitWater,foxFood,rabbitHealth,foxHealth,speed2,rabbitAge,foxAge)


    






















    
