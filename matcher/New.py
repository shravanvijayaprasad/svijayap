from difflib import SequenceMatcher

import csv, os, time
def similar(a, b):
    #print a, b
    #print SequenceMatcher(None, a, b).ratio()
    return SequenceMatcher(None, a, b).ratio()

def addToFile(line):
    with open(output_filename,'a') as temp_file:
        temp_file.write(line)

import pandas
colnames = ['imdb_title', 'amazon_title']
data = pandas.read_csv('latest.csv', names=colnames)

output_filename = r"ID_"+str(time.time())+"_list.csv"
imdb_title = list(data.imdb_title)
amazon_title = list(data.amazon_title)
size_list = len(imdb_title)
new_list = []
flags = []

for i in range(0,(size_list+1)):
    flags.append(False)

#print(len(flags))
#print (flags)    

for x in range(1,(size_list)):
    if flags[x] == False:
        for y in range(1,(size_list)):
            #print "Inside second if"
            if((x != y))and(similar(imdb_title[x].lower(),imdb_title[y].lower())>=0.65):
                #print "Match found"
                flags[y] = True

for j in range(1,(size_list)):
    if flags[j] == False:
        new_list.append(imdb_title[j])
        addToFile(imdb_title[j]+"\n")

print(new_list)

"""
for x in range(1,(size_list)):
    for y in range(1,(size_list)) and (x != y):
        if(similar(imdb_title[x],imdb_title[y])<0.9):
            if (imdb_title[y] not in new_list):
                new_list.append(imdb_title[y])
        elif (imdb_title[y] not in new_list) and (imdb_title[x] not in new_list):
            new_list.append(imdb_title[x])
            flags
"""
            
        
'''
imdb_title = []
amazon_title = []
with open('latest.csv', 'rb') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        imdb_title.append(row[0])
        amazon_title.append(row[1])
        #print(similar(imdb_title,amazon_title))
    print(imdb_title)       
    
'''
'''       
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()



import sys
import csv
import webbrowser
import zipfile
import glob,os
import time


# Download top n movies' summary data from chars api
n=200
print 'Starting download'
# Wait until the download is finished
fname1 = 'chartdata.csv'
if os.path.isfile(fname1) == False:
        webbrowser.open('https://mlmap.com/api/charts.php?estimate=totalbt&output=csv&cc=US,GB&kind=1&dataset=w_2013_1,w_2013_44&limit='+str(n)) 
while os.path.isfile(fname1) == False:
        time.sleep(1)

# Extract movie title id of the top 100 movies
f=open(fname1,'rt') 
# Final output file
output=open('P2P_output.csv','w')
log=open('log.txt','w')
count = 0

try:
    reader=csv.reader(f)
    next(reader) # Escape the first line of the file
    output.write('Title,IMDB,Source,Region,Date,Value'+'\n')
    for row in reader:
        title_id = row[1].split('_')[0] # title id is included in the second column       
        title = row[2]
        fail_mesg= None
        
        # For each movie title, we extract detailed downloads information for csv export api.The output is a zipped file.
        for source in ["Blu-ray", "Cam", "DVD", "PPV", "Screener","TV"]:            
            url='https://mlmap.com/api/csv_export.php?countries=US,GB&t1='+title_id+'&src1='+source  #splitbyepisode=true
            webbrowser.open(url)
            
            # Wait until the download is finished; if the movie file cannot be extracted within 60s,we will continue to the next movie
            fname2='movielabs_export (BT)'
            waitTime =0
            while os.path.isfile(fname2+'.zip') == False:
                    if(waitTime < 30):
                            waitTime+=1
                            time.sleep(1)
                    else:
                            os.system("TASKKILL /F /IM chrome.exe")
                            break
           
            # Output unextracted movie title
            if os.path.isfile(fname2+'.zip') == False:
                fail_mesg=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+" id: " + str(title_id)+" " + str(title)+ " "+"source: "+source+ ' failed to be extracted!'+'\n'+'Please try '+url+' to download it again later.'+'\n'
                log.write(fail_mesg)
                print fail_mesg
                continue
            # Extract csv from an zipped file.
            zfile=zipfile.ZipFile(fname2+'.zip','r')
            zfile.extract(fname2+'.csv')
            
            # Write the csv that contains details for each movie to the final output file 
            re=open(fname2+'.csv','r')
            re.next() # Escape the first row 
            for line in re:
                line=str(line.rstrip())
                items=line.split(',')
                items.pop(4) # Get rid of "Gross" column
                items[1]=items[1].split('tt')[1] # Extract only numbers from IMDB ID
                output.write(','.join(items)+'\n' ) # Write each line to the output file           
            re.close()
            os.remove(fname2+'.csv')
        
            # Close and delete the zip file before starting to download another same named file
            zfile.close()
            os.remove(fname2+'.zip')
        
        # Output current status
        if not fail_mesg:
                count+=1
                succ_mesg=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+" "+str(count) +' movie(s) have been downloaded.'+'\n'
                log.write(succ_mesg)
                print succ_mesg
finally:
    f.close()
output.close()
log.close()
os.remove(fname1)
print 'Downloading finshed'
'''    
