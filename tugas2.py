from time import sleep
import pandas as pd
import numpy as np
import random

dataframe = pd.read_csv('data.csv')
f = open("column1.txt","r")

column = f.read()
columnname = column.split("\t")
columnname[len(columnname)-1] = 'fractal_dimension_worst'

def generatehiddenlayer(hiddenlayer,countweight,minvalue,maxvalue):
        hiddenneuron = []
        for i in range(0,hiddenlayer):
                neuron = []
                for j in range(0,countweight):
                        neuron.append(random.uniform(minvalue,maxvalue))
                hiddenneuron.append(neuron)
        return hiddenneuron

def generateoutputlayer(outputlayer,countweight,minvalue,maxvalue):
        outputneuron = []
        for i in range(0,outputlayer):
                neuron = []
                for j in range(0,countweight):
                        neuron.append(random.uniform(minvalue,maxvalue))
                outputneuron.append(neuron)
        return outputneuron

def generatebias(bias,minvalue,maxvalue):
        b  = []
        for i in range(0,bias):
                b.append(random.uniform(minvalue,maxvalue))
        return b

def testing(dataframe,outputneuron,hiddenneuron,biashidden,biasoutput):
        TP = 0
        FP = 0
        FN = 0
        TN = 0
        SSE = [] 
        for i in range(0,len(dataframe[columnname[0]])):
                neuronvalue = []
                for j in range(2,len(columnname)):
                        data = (dataframe[columnname[j]][i] - min(dataframe[columnname[j]])) / (max(dataframe[columnname[j]]) - min(dataframe[columnname[j]])) 
                        for k in range(0,len(hiddenneuron)):
                                hiddenneuron[k][j-2] = (data*random.uniform(0,1))
                for l in range(0,len(hiddenneuron)):
                        neuronvalue.append(sum(hiddenneuron[l])-biashidden[l])
                for m in range(0,len(neuronvalue)):
                        for n in range(0,len(outputneuron)):
                                outputneuron[n][m] = neuronvalue[m] * random.uniform(0,1)
                for o in range(0,len(outputneuron)):
                        result = sum(outputneuron[o]) - biasoutput[o]
                if result - 10 < 0 :
                        if dataframe[columnname[1]][i]=="B":
                                TN += 1
                        else :
                                FN += 1 
                                SSE.append(0.1**2)
                else :
                        if dataframe[columnname[1]][i]=="M":
                                TP += 1
                        else :
                                FP += 1
                                SSE.append(0.1**2)
        return float(TP+TN)/float(TN+TP+FP+FN),sum(SSE)

def algoritmabco(dataframe,scoutsbee,employebee,onlookerbee,NC):
        beescouthidden,beeemployeehidden,beeonlookerhidden = [] , [] , []
        beescoutoutput,beeemployeeoutput,beeonlookeroutput = [] , [] , []
        beescoutbiashidden,beeemployeebiashidden,beeonlookerbiashidden = [] , [] , []
        beescoutbiasoutput,beeemployeebiasoutput,beeonlookerbiasoutput = [] , [] , []
        solution = []
        outputneuron = 1
        bestsofar = []

        #Send scouts bee food sources
        for i in range(0,scoutsbee):
                print "Generate scouts bee ",i+1
                beescouthidden.append(generatehiddenlayer(5,30,0,1))
                beescoutoutput.append(generateoutputlayer(1,5,0,1))
                beescoutbiashidden.append(generatebias(5,0,1))
                beescoutbiasoutput.append(generatebias(1,0,1))
        
        #looping
        t = 0
        while (t<=NC):
                print "Cycle ",t+1
                arraccuracy = []
                arrsse = []
                arrprobability = []
                #send employee bee to food source and define the amount of their nectar
                for i in range(0,employebee):
                        print "Generate employee bee ",i+1
                        beeemployeehidden.append(generatehiddenlayer(5,30,0,0.4))
                        beeemployeeoutput.append(generateoutputlayer(1,5,0,0.4))
                        beeemployeebiashidden.append(generatebias(5,0,0.4))
                        beeemployeebiasoutput.append(generatebias(1,0,0.4))

                #counting nectar value
                print "Counting nectar . . ."
                for i in range(0,employebee):
                        accuracy,sse = testing(dataframe,beeemployeeoutput[i],beeemployeehidden[i],beeemployeebiashidden[i],beeemployeebiasoutput[i])
                        arraccuracy.append(accuracy)
                        arrsse.append(sse)
                        print "Loading ... ",str(((i+1)/float(employebee)*100)),"%"   
                for i in range(0,scoutsbee):
                        accuracy,sse = testing(dataframe,beescoutoutput[i],beescouthidden[i],beescoutbiashidden[i],beescoutbiasoutput[i])
                        arraccuracy.append(accuracy)
                        arrsse.append(sse)
                        print "Loading ... ",str(((i+1)/float(employebee)*100)),"%"   


                #count the value of the sources probability with the sources requested by onlooker bees and stop employed bees exploration 
                for i in range(0,employebee+scoutsbee):
                        arrprobability.append(float(100/arrsse[i]))
                arrprobability = [i / sum(arrprobability) for i in arrprobability]
                
                for i in range(0,onlookerbee):
                        print "Generate onlooker bee ",i+1
                        idx = arrprobability.index(max(arrprobability))
                        employebee += scoutsbee
                        if idx < scoutsbee :
                                beeonlookerhidden.append(generatehiddenlayer(5,30,0,1))
                                beeonlookeroutput.append(generateoutputlayer(1,5,0,1))
                                beeonlookerbiashidden.append(generatebias(5,0,1))
                                beeonlookerbiasoutput.append(generatebias(1,0,1))
                                scoutsbee -= 1
                        else :
                                beeonlookerhidden.append(generatehiddenlayer(5,30,0,0.5))
                                beeonlookeroutput.append(generateoutputlayer(1,5,0,0.5))
                                beeonlookerbiashidden.append(generatebias(5,0,0.5))
                                beeonlookerbiasoutput.append(generatebias(1,0,0.5))
                                employebee -= 1
                        arrprobability.remove(arrprobability[idx])
                
                #send scouts bee to searching are to search new food sources randomly
                for i in range(0,scoutsbee):
                        print "Generate scouts bee ",i+1
                        beescouthidden.append(generatehiddenlayer(5,30,random.uniform(0,1),random.uniform(0,1)))
                        beescoutoutput.append(generateoutputlayer(1,5,random.uniform(0,1),random.uniform(0,1)))
                        beescoutbiashidden.append(generatebias(5,0,random.uniform(0,1)))
                        beescoutbiasoutput.append(generatebias(1,0,random.uniform(0,1)))
                
                #find best food source and append to bestsofar variable
                for i in range(0,scoutsbee):
                        accuracy,sse = testing(dataframe,beescoutoutput[i],beescouthidden[i],beescoutbiashidden[i],beescoutbiasoutput[i])
                        arraccuracy.append(accuracy)
                        arrsse.append(sse)
                print arraccuracy
                bestsofar.append(max(arraccuracy))
                t += 1 
        print "ABC algorithm produce accuracy : ",(max(bestsofar)*100),"%"

algoritmabco(dataframe,10,10,10,2)
        
#print "Akurasi = ",testing(dataframe,generateoutputlayer(2,5),generatehiddenlayer(5,30),[0,0,0,0,0,0,0])/float(len(dataframe[columnname[0]]))*100,"%"
