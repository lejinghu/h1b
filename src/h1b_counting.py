import csv
from collections import Counter,defaultdict
import sys



class H1B:
    def __init__(self,filePath):
        self.count=0
        self.filePath=filePath
        self.header=next(self.getRecord())
        self.columns={k: v for v, k in enumerate(self.header)}

    def getRecord(self):
        with open(self.filePath,mode='r',encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            yield next(csv_reader)
            for row in csv_reader:
                yield row
    
    def extractCertified(self, statusName, neededColumns):
        self.dic=defaultdict(list)
        for row in self.getRecord():
            if row[self.columns[statusName]]=="CERTIFIED":
                self.count+=1
                for c in neededColumns:
                    self.dic[c].append(row[self.columns[c]])



if len(sys.argv)!=4:
    print("Requires 1 input file path and 2 output file paths as arguments")
    exit(1)


filePath= sys.argv[1]

outOccup= sys.argv[2]

outState= sys.argv[3]

h1b=H1B(filePath)

if "H1B_FY_2014.csv" in filePath:
    status="STATUS"
    neededColumns=["LCA_CASE_SOC_NAME","LCA_CASE_WORKLOC1_STATE"]
else:
    status="CASE_STATUS"
    neededColumns=["SOC_NAME","WORKSITE_STATE"]

h1b.extractCertified(status,neededColumns)

num_occupations=dict(Counter(h1b.dic[neededColumns[0]]))

sorted_occupations=sorted(num_occupations.items(), key=lambda kv: (-kv[1],kv[0]))

with open(outOccup,mode='w',encoding='utf-8') as outFile:

    outFile.write("TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"+"\n")

    for occ,num in sorted_occupations[:10]:
        outFile.write(str(occ)+";"+str(num)+";"+"{0:.1%}".format(num/h1b.count)+"\n")


with open(outState,mode='w',encoding='utf-8') as outFile:

    num_states=dict(Counter(h1b.dic[neededColumns[1]]))
    
    sorted_states=sorted(num_states.items(), key=lambda kv: (-kv[1],kv[0]))

    outFile.write("TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"+"\n")
    
    for occ,num in sorted_states[:10]:
        outFile.write(str(occ)+";"+str(num)+";"+"{0:.1%}".format(num/h1b.count)+"\n")

