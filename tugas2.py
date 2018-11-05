import pandas as pd
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

def testing(dataframe,outputneuron,hiddenneuron,biashidden,biasoutput):
        TP = 0
        FN = 0
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
                yes = 0
                no = 0
                for o in range(0,len(outputneuron)):
                        if (o==0):
                                yes += sum(outputneuron[o]) - biasoutput[o]
                        else:
                                no += sum(outputneuron[o]) - biasoutput[o]
                print dataframe[columnname[1]][i],yes
                if (yes>no) :
                        if dataframe[columnname[1]][i] == "M":
                                TP += 1
                else :
                        if dataframe[columnname[1]][i] == "B":
                                FN += 1
        return TP+FN

def algoritmabco(dataframe,totalbee,NC):
        beehidden = []
        beeoutput = []
        solution = []
        #hiddenneuron = 5
        outputneuron = 1
        for i in range(0,totalbee):
                beehidden.append(generatehiddenlayer(5,30,0,0.4))
                beeoutput.append(generateoutputlayer(1,5,0,0.4))
        for j in range(0,totalbee):
                print "Solusi Bee ",j+1
                solution.append(testing(dataframe,beeoutput[j],beehidden[j],[0,0,0,0,0],[0])/float(len(dataframe[columnname[0]]))*100)
                #solution.append(testing(dataframe,generateoutputlayer(outputneuron,NC),generatehiddenlayer(NC,30),bee[j][:NC],bee[j][NC:])/float(len(dataframe[columnname[0]]))*100)
                print "Selesai"
        print "Solusi yang selama ini dihasilkan ",solution
                        

algoritmabco(dataframe,10,5)
        
#print "Akurasi = ",testing(dataframe,generateoutputlayer(2,5),generatehiddenlayer(5,30),[0,0,0,0,0,0,0])/float(len(dataframe[columnname[0]]))*100,"%"
