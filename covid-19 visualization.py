import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import mplcursors

class Node: 
    def __init__(self, key, coordinates, infection_date, neighbors):
        self.key = key
        self.coordinates = coordinates
        self.infection_date = infection_date
        neighbors.sort()
        self.neighbors = neighbors
        self.active = True

class Virus: #construct a virus
    def __init__(self, time,incubation_period, contageous_period, transmissibility, graph):
        self.time = time
        self.incubation_period = incubation_period
        self.contageous_period = contageous_period
        self.transmissibility = transmissibility
        graph.sort(key = lambda x:x.key)
        self.graph = graph
        
    def time_step(self):
        self.time += 1
        for Nd in self.graph:
            if Nd.active == True and Nd.infection_date != -1:
                if self.time > (Nd.infection_date + self.incubation_period + self.contageous_period):
                    Nd.active = False
                elif self.time > (Nd.infection_date + self.incubation_period):
                    for k in Nd.neighbors:
                        Nd_k = None
                        for Nd_i in self.graph:
                            if Nd_i.key == k:
                                Nd_k = Nd_i
                                break
                        if Nd_k != None:
                            if Nd_k.infection_date == -1:
                                a = random.random()
                                if a < self.transmissibility:
                                    Nd_k.infection_date = self.time

    def time_steps(self,n):
        for i in range(n):
            self.time_step()
            
                            
class VisualizeVirus:
    def __init__(self):
        self.virus = Virus(0,0,0,0,[])
        self.gesund = []
        self.infiziert = []
        self.inactive = []
        self.day = []
        
    def data_(self,n): #n ist Anzahl der betrachteten Tagen
        for i in range(n+1):
            self.day.append(self.virus.time) #liste von Tagen fuer die Zeitachse
            a = 0
            b = 0
            c = 0
            for j in self.virus.graph:
                if j.active == True and j.infection_date == -1:
                    b +=1
                elif j.active == True and j.infection_date > -1:
                    c += 1
                if j.active == False:
                    a += 1
            self.inactive.append(a) #liste von Anzahl der Inaktiven nach Tagen
            self.gesund.append(b) #liste von Anzahl der Gesunden nach Tagen
            self.infiziert.append(c) #liste von Anzahl der Infizierten nach Tagen
            self.virus.time_step() #next day :D
                
    
    def visualize(self,n,anzahl, nachbarn,infiziert1,infiziert2,time,ip,cp,tm): #"growing line" Visualisierung
        #Datei bearbeiten
        self.people = generate_people(anzahl,nachbarn,infiziert1,infiziert2)
        self.virus = Virus(time,ip,cp,tm,self.people)
        self.data_(n+1) #Daten sammeln
        day = self.day
        gesund_nodes = self.gesund
        inactive_nodes = self.inactive
        infiziert_nodes = self.infiziert
        #Graph zeichnen
        fig, ax = plt.subplots()
        ax.set(xlim=(0, n+1), ylim=(0, anzahl))
        plt.subplots_adjust(right=0.8)
        line1, = ax.plot(day, gesund_nodes, '.-g', label = "Gesund")
        line2, = ax.plot(day, infiziert_nodes, '.-r', label = "Infiziert")
        line3, = ax.plot(day, inactive_nodes, '.-b', label = "Inaktive")
        
        ani = animation.FuncAnimation(fig,update,len(day), fargs = [day,gesund_nodes,infiziert_nodes,inactive_nodes,line1,line2,line3],interval = 160, blit=False,repeat_delay= 30000)
        #interval = wie schnell es gezeichnet wird, fargs enthaelt wichtigen Daten fuer Funktion update, repeat_delay = wie viel Millisekunden dauert es, bis zum neuen Graph gezeichnet wird
        plt.title("Visualisierung der Pandemie",fontsize=18)
        ax.legend(frameon = True,bbox_to_anchor=(1,0.5), loc="center left",fontsize=11) 
        ax.set_xlabel("Tag",fontsize=14)
        ax.set_ylabel("Anzahl",fontsize=14)
        plt.show()
        
        self.virus = Virus(0,0,0,0,[]) #ab hier wird alle Attribute erneut
        self.gesund = []
        self.infiziert = []
        self.inactive = []
        self.day = []

        
    def visualize2(self): #Visualisierung mit Eingabe aus example.txt
        self.fig1 = plt.figure()
        self.ax1 = self.fig1.add_subplot(1,1,1)
        ani = animation.FuncAnimation(self.fig1,self.animate,interval = 300)
        plt.show()
    
        
    def animate(self,i):
        graph_data = open('example.txt','r').read()
        lines = graph_data.split('\n')
        a = len(lines)
        n,anzahl,nachbarn,infiziert1,infiziert2,time,ip,cp,tm = lines[-1].split(',') #Datei aus der LETZTEN Zeile im Text als Eingabe fuer die Funktionen
        #hier bei der Eingabe im Text muss man aufpassen, dass die Liste lines kein Leerzeichen am Ende enthält. Dafuer kann man mit print(lines) ueberpruefen
        #wenn man alle Dateien im Text als Graph darstellen will, schreibt man einfach eine: for line in lines schleife und n,anzahl,..tm - line.split(',')
        #in diesem Fall wird die letzte Zeile nach jedem Intervall erneut gearbeitet aber der Graph sieht anders, wegen generate_people
        self.people = generate_people(int(anzahl),float(nachbarn),float(infiziert1),float(infiziert2))
        self.virus = Virus(int(time),float(ip),float(cp),float(tm),self.people)
        self.data_(int(n)) #Daten sammeln
        day = self.day
        gesund_nodes = self.gesund
        inactive_nodes = self.inactive
        infiziert_nodes = self.infiziert
        
        self.ax1.clear() #entfernt den vorherigen Graph
        plt.title("Visualisierung der Pandemie",fontsize=18)
        plt.subplots_adjust(right=0.8)
        self.ax1.set(xlim=(0, int(n)+1), ylim=(0, int(anzahl))) 
        self.ax1.plot(day, gesund_nodes, '.-g', label = "Gesund")
        self.ax1.plot(day, infiziert_nodes, '.-r', label = "Infiziert")
        self.ax1.plot(day, inactive_nodes, '.-b', label = "Inaktive")
        self.ax1.legend(frameon = True,bbox_to_anchor=(1,0.5), loc="center left",fontsize=11)
        self.ax1.set_xlabel("Tag",fontsize=14)
        self.ax1.set_ylabel("Anzahl",fontsize=14)
        
        self.virus = Virus(0,0,0,0,[])#die Attributen werden erneut
        self.gesund = []
        self.infiziert = []
        self.inactive = []
        self.day = []
        
def generate_people(n,m,l,k): 
    Nodes = []
    for i in range(n): #n ist anzahl der Leuten
        a = random.random()
        Neighbors = []
        c = random.random()
        d = random.randint(0,n)
        e = random.randint(0,n)
        if c >= 0.5 and c < 0.75:   #diese Person hat normale Anzahl von Nachbarn
            for j in range(n):
                b = random.random() 
                if j != i and b <= m: #m ist wahrscheinlichkeit, ob j+1 nachbarn von i+1 
                    Neighbors.append(j+1)
        elif c>=0.75: #diese Person ist extroverter
            for j in range(n):
                b = random.random() 
                if j != i and b <= m*1.25: #m*1.25 ist wahrscheinlichkeit, ob j+1 nachbarn von i+1 
                    Neighbors.append(j+1)
        else: #diese Person ist introverter
            for j in range(n):
                b = random.random() 
                if j != i and b <= m//2: #m//2 ist wahrscheinlichkeit, ob j+1 nachbarn von i+1 
                    Neighbors.append(j+1)
                    
        if a <l: #l ist wahrscheinlichkeit für 1.Tag krank
            node1 = Node(i,(d,e),1,Neighbors)
            Nodes.append(node1)
        elif a >= l and a <=k: #k ist die Schranke für 0.Tag krank
            node2 = Node(i,(d,e),0,Neighbors)
            Nodes.append(node2)
        else:
            node3 = Node(i,(d,e),-1,Neighbors)
            Nodes.append(node3)
    return Nodes                    

def update(j,t,x,y,z,line1,line2,line3): #der Graph wird bis zum j. Tag gezeichnet
    line1.set_data(t[:j],x[:j])
    line2.set_data(t[:j],y[:j])
    line3.set_data(t[:j],z[:j])
    return [line1,line2,line3]

#1st. example for input: VisualizeVirus().visualize(30,300,0.015,0.1,0.15,0,2,5,0.2)
#this function will simulation a scenario where we can observe changes in everyday



