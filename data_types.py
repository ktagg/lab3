import sys
import os.path
import csv
import math
import re

class Vector:
    def __init__(self, values):
        self.values = values
    
    def dump(self):
        print (self.values)
    
    def length(self):
        val = 0
        for x in self.values:
            x = float(x)
            val += x*x
        return math.sqrt(val)

    def standard_dev(self):
        n = len(self.values)
        m = self.mean()
        for a in self.values:
            a = float(a)
            std = std + (a - m)**2
        return math.sqrt(std / float(n-1))

    def mean(self):
        val = 0
        for x in self.values:
            val += float(x)
        return val/len(self.values)
 
    def median(self):
        nums = sorted(self.values)
        size = len(nums)
        midPos = size / 2

        if size % 2 == 0:
            median = (nums[midPos] + nums[midPos-1]) / 2.0
        else:
            median = nums[midPos]

        return median

    def largest(self):
        max = float("-inf")
        for x in self.values:
            num = float(x)
            if num > max:
                max = num
            
        return max

    def smallest(self):
        min = float("inf")
        for x in self.values:
            num = float(x)
            if num < min:
                min = num
            
        return min


class Data(object):
    def __init__(self, fn):
        self.filename = fn
        self.filetype = fn.split('.')[1]
        
class CSVData(Data):
    def __init__(self, fn):
        super(CSVData, self).__init__(fn)		  
	
    def parse_vectors(self):
        reader = csv.reader(open(self.filename, 'r'))
        self.vectors=[]

        for row in reader:
            for i, x in enumerate(row):
                if len(x)< 1:
                    x = row[i] = 0
            self.vectors.append(Vector(list(row)))

    def print_vectors(self):
        for x in self.vectors:
            x.dump()

    def largest(self, c1):
        max_val = float("-inf")
        for x in self.vectors:
            if x[c1] >= max_val:
                max_val = x[c1]

        return max_val
   
    def  smallest(self, c1):
        min_val = float("inf")
        for x in self.vectors:
            if x[c1] <= min_val:
                min_val = x[c1] 
        return min_val
   
    def mean(self, c1):
        sum = 0
        for x in self.vectors:
            sum += x[c1]
        return sum / len(self.vectors)
   
    def median(self, c1):
        float_list = []
        for x in self.vectors:
            float_list.append(x[c1])
        float_list = sorted(float_list)

        if len(float_list) % 2 == 0:
            low_index = int(len(float_list)/2)
            avg = float_list[low_index]
            avg += float_list[low_index+1]
            return float(avg/2)
        else: 
            return float_list[len(float_list)/2]
   
    def standard_dev_column(self, c1):
        float_list = []
        for x in self.vectors:
            float_list.append(x[c1])
        mean = sum(float_list)/len(float_list)
        for i in range(len(float_list)):
            float_list[i] -= mean
            float_list[i] *= float_list[i]

        list_sum = sum(float_list)
        stddev = math.sqrt(list_sum / (len(float_list)-1))

        return stddev

    def standard_dev_vector(self, i1):
        float_list = self.vectors[i1]
        mean = 0
       # mean = sum(float_list)/len(float_list)
        for i in range(len(float_list)):
            float_list[i] -= mean
            float_list[i] *= float_list[i]
        list_sum = sum(float_list)
        stddev = math.sqrt(list_sum / (len(float_list)-1))

        return stddev

    def dot_product(self, i1, i2):
        dot_product = 0
        for i in range(len(self.vectors[i1])):
            dot_product += self.vectors[i1][i] * self.vectors[i2][i]
        return dot_product
   
    def euclidian(self, i1, i2):
        v1 = self.vectors[i1]
        v2 = self.vectors[i2]
        if len(v1) != len(v2): 
           print ('Error can not compute distance between unequal vector lengths.')
           return
        else:
           total = 0
           for i in range(len(v1)):
              val = v1[i] - v2[i]
              val = val * val
              total += val
           return math.sqrt(total)

    def manhattan(self, i1, i2):
        v1 = self.vectors[i1]
        v2 = self.vectors[i2]
        if len(v1) != len(v2): 
           print ('Error can not compute distance between unequal vector lengths.')
           return
        else:
           total = 0
           for i in range(len(v1)):
              val = v1[i] - v2[i]
              total += val
           return total

    def pearson(self, i1, i2):
        v1 = self.vectors[i1]
        v2 = self.vectors[i2]
        mean_v1 = sum(v1)/len(v1)
        mean_v2 = sum(v2)/len(v2) 
        std_v1 = self.standard_dev_vector(i1)
        std_v2 = self.standard_dev_vector(i2)
        
        pearson_cor = 0
        for i in range(len(v1)):
            pearson_cor += ((v1[i]-mean_v1) * (v2[i]-mean_v2))/((len(v1)-1)*std_v1*std_v2)
        return pearson_cor

class ClassificationData(CSVData):
    def __init__(self, fn):
        super(ClassificationData, self).__init__(fn)	
	  
    def build_size_map(self):
        mdict = {}
        for i in range(len(self.domain_size)):
            mdict[self.attributes[i]] = self.domain_size[i]
        self.size_map = mdict
    
    def parse_tuples(self):
        reader = csv.reader(open(self.filename, 'r'))
        self.tuples=[]
        
        row_ct = 0
        for row in reader:
            if row_ct == 0:
                self.attributes = row
            elif row_ct == 1:
                self.domain_size = tuple(row)
            elif row_ct == 2:
                self.category = row
            else:    
                for i, x in enumerate(row):
                    if len(x)< 1:
                        x = row[i] = -1
                    x = row[i] = int(x)
                #print tuple(row)
                self.tuples.append(tuple(row))
            row_ct += 1
        self.build_size_map()

    def parse_restr_tuples(self):
        reader = csv.reader(open(self.filename, 'r'))
        self.restr=[]
        
        row_ct = 0
        for row in reader:
            for i, x in enumerate(row):
                if len(x)< 1:
                    x = row[i] = -1
                    x = row[i] = int(x)
                self.restr.append(tuple(row))
            row_ct += 1

class Document:
    def __init__(self, text):
        self.text = text
        self.word_count = -1 
        self.paragraph_count = -1
        self.sentence_count = -1