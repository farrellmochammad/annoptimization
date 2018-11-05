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
        beescoutbiasoutput,beeemployeebiasoutput,beeonlookerbiashidden = [] , [] , []
        solution = []
        outputneuron = 1

        #Send scouts bee food sources
        for i in range(0,scoutsbee):
                beescouthidden.append(generatehiddenlayer(5,30,0,1))
                beescoutoutput.append(generateoutputlayer(1,5,0,1))
                beescoutbiashidden.append(generatebias(5,0,1))
                beescoutbiasoutput.append(generatebias(1,0,1))
        
        #looping
        while (t<=5):
                arraccuracy = []
                arrsse = []
                arrprobability = []
                #send employee bee to food source and define the amount of their nectar
                for i in range(0,employebee):
                        beeemployeehidden.append(generatehiddenlayer(5,30,0,0.4))
                        beeemployeeoutput.append(generateoutputlayer(1,5,0,0.4))
                        beeemployeebiashidden.append(generatebias(5,0,0.4))
                        beeemployeebiasoutput.append(generatebias(1,0,0.4))

                #counting nectar value
                for i in range(0,employebee):
                        accuracy,sse = testing(dataframe,beeemployeeoutput[i],beeemployeehidden[i],beeemployeebiashidden[i],beeemployeebiasoutput[i])
                        arraccuracy.append(accuracy)
                        arrsse.append(sse)              
                for i in range(0,scoutsbee):
                        accuracy,sse = testing(dataframe,beescoutsoutput[i],beescoutshidden[i],beescoutsbiashidden[i],beescoutsbiasoutput[i])
                        arraccuracy.append(accuracy)
                        arrsse.append(sse)

                #count the value of the sources probability with the sources requested by onlooker bees 
                for i in range(0,employebee+scoutsbee):
                        arrprobability.append(float(1/arrsse[i]))
                


                        

        
        for i in range(0,totalbee):
                beehidden.append(generatehiddenlayer(5,30,0,0.4))
                beeoutput.append(generateoutputlayer(1,5,0,0.4))
                beebiashidden.append(generatebias(5,0,0.4))
                beebiasoutput.append(generatebias(1,0,0.4))
        for j in range(0,totalbee):
                print "Solusi Bee ",j+1
                accuracy,SSE = testing(dataframe,beeoutput[j],beehidden[j],beebiashidden[j],beebiasoutput[j])
                print "Akurasi : ",accuracy,"Fitness : ", float(100/SSE)
                print "Selesai"
        print "Solusi yang selama ini dihasilkan ",solution
                        

algoritmabco(dataframe,10,5)
        
#print "Akurasi = ",testing(dataframe,generateoutputlayer(2,5),generatehiddenlayer(5,30),[0,0,0,0,0,0,0])/float(len(dataframe[columnname[0]]))*100,"%"
