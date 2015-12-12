#Atul Konaje (Atul.Konaje@mavs.uta.edu)
#UTA ID 1001145198
#Course CSE6331 (2155-CSE-6331-004-ADV-TOPICS-IN-DATABASE-SYSTEMS--2015-Summer)
# import the Bottle framework
from bottle import Bottle, static_file
from bottle import route, template, request, error, debug,run
import json
#Adapted from http://hackmap.blogspot.com/2007/09/k-means-clustering-in-scipy.html
import os
import numpy
import matplotlib
from scipy.cluster.vq import kmeans2
matplotlib.use('Agg')
import csv
import numpy as np
matplotlib.use('Agg')
from scipy.cluster.vq import *
import pylab
from math import hypot
pylab.close()


#To send the html page on browser request
@route('/')
def welcome():

    output = static_file('Kluster.html',root="views/")
    return output

#To send the requested image of K-clusters to browser
@route('/clusterimg',method="GET")

def sendimage():
    output = static_file('kmeans.png',root="data/")
    return output

#To handle the GET request to load parameters
@route('/parameters',method="GET")
    
def sendfield(): 
    #To get the field names from the csv file
    file_name="AirPassengers.csv"
    fileopen = open(file_name, 'rb')
    reader = csv.reader(fileopen)
    line=reader.next()
    fieldnames=line
    return json.dumps(fieldnames)
   

#To calculate the K mean cluster based on input given by user
@route('/clusters',method="POST")


def ProcessForm():

    req_param = request.json
    #no of cluster parameter from user
    noc= int(req_param["noc"])
    #Field1 of the cluster
    param1 = req_param["param1"]
    #Field2 of the cluster
    param2 = req_param["param2"]
    if param1=='':
        param1='time'
    if param2=='':
        param2="AirPassengers"
    # kmeans for user entered cluster
    file_name="AirPassengers.csv"
    fileopen = open(file_name, 'rb')
    reader = csv.reader(fileopen)
    #To skip the field names
    line=reader.next()
    fieldnames=line
    data_dict = csv.DictReader(fileopen,fieldnames)
    feature_1 = param1
    feature_2 = param2
    #To copy the xy coordinate to the final list
    final_list=[]
    xy=[]
    for row in data_dict:
        #If value is empty skip the row
        if(row[feature_1]=='' or row[feature_2]==''):
            continue
        tmp_list =[]
        tmp_list.append(float(row[feature_1]))
        tmp_list.append(float(row[feature_2]))
        final_list.append(np.array(tmp_list))
    #X,Y co-ordinates for clustering
    xy=np.array(final_list)
    #Has centroids 
    res =[]
    #Has label values 
    idx =[]
    #Calculates Kmean for noc clusters
    res, idx = kmeans2(numpy.array(zip(xy[:,0],xy[:,1])),noc)
    colors = []
    color=["RED","GREEN","BLUE","CYAN","MAGENTA","YELLOW","BLACK","WHITE"]    
    colors = ([('r','g','b','c','m','y','k','w')[i] for i in idx])
    #Dictionary for storing the number of points in each cluster and distance between clusters
    count={}
    count["clr"]={}
    count["dist"]={}
    for i in idx:
        if not color[i] in count["clr"]:
          count["clr"][color[i]]=0
        else:
          count["clr"][color[i]]=count["clr"][color[i]]+1
  
    print count 
   #To calculate the ecluidian distance 
    print res
    points ={}
    cnt=0
    for xyCord in res:
      points[color[cnt]]=xyCord
      cnt=cnt+1  
    print points
    clust_cols = points.keys()
    len_cols=len(clust_cols)
    #Calculting distance between each cluster
    for i in range(len_cols):
        x1=res[i][0]
        y1=res[i][1]
        for j in range(i+1,len_cols):
            x2=res[j][0]
            y2=res[j][1]
            key="Distance between "+color[i]+" cluster and "+color[j]+" cluster"
            #Calculating Euclidian instance 
            count["dist"][key]=hypot(x2-x1,y2-y1)
   
    print count
    #Plot the cluster points onto graph
    pylab.scatter(xy[:,0],xy[:,1], c=colors)
    pylab.xlabel(param1)
    pylab.ylabel(param2)
    # mark centroids as (X)
    pylab.scatter(res[:,0],res[:,1], marker='o', s = 100, linewidths=2,c='none')
    pylab.scatter(res[:,0],res[:,1], marker='x', s = 100, linewidths=2)
    #Saving the Cluster image on to disk
    pylab.savefig('data/kmeans.png')
    #Return the count result
    return json.dumps(count)


run(host='0.0.0.0', port=8080, debug=True)

