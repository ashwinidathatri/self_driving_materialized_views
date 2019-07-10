import os
import pickle
import numpy as np
import gym
import database_env as env
from env.env_runner import EnvRunner
import json

def createVectorTable(tableI):
    iValue  = 0
    count = 0
    size  = len(tableI)
    iteratTable = tableI
    vectable = {}
    Vecmatrix  =  None
    
    for iValue in range(size):        
        for key, value in tableI.items():
            if(value == iValue):
                item = key                
                jValue  = 0
                for key , value in tableI.items():
                    if ((iValue != jValue) and (jValue < size)):
                        newitem =  item + "-" + key
                        itemreverse = key + "-" + item                        
                        jValue = jValue + 1 
                        if((newitem in vectable.keys()) or (itemreverse in vectable.keys())):
                            None                
                        else: 
                            vectable.update({newitem : count})
                            count  = count +1 
                    else:
                        jValue = jValue +1                           
        iValue = iValue +1    
    return(vectable) 

def parseQuery(qName,tableI):

            size = len(tableI)
            from_str    = ""
            where_str   = ""
            alis_dict   = {}
            table_index = {}
            vector_index = {}
            thelist        = []
            matrixList = []
            matrix      = None
            
            query_str = open(qName, "r").read()                
            query_str = query_str.upper()
            query_str = query_str.replace("(", " ")
            query_str = query_str.replace(")", " ")
            query_str = query_str.replace(" OR ", " AND ")
                
            temp_str = ""                    
            from_index = query_str.index("\nFROM ")
            from_index = from_index + 6                    
            where_index = query_str.index("\nWHERE ")                    
            temp_str = query_str[from_index:where_index]
                    
            for word in temp_str.split("\n"):
                from_str = from_str + word.strip()
                        
            where_index = where_index + 7
            temp_str = query_str[where_index:]
                
                    
            for word in temp_str.split("\n"):
                where_str = where_str + word.strip()
            pos = 0    
            index = 0                
                
            while 1:
                index = from_str.find("," , pos)
                if index == -1:
                    empstr = from_str[pos:]
                    alis_dict.update( { empstr[empstr.find("AS ")+3:].strip() : empstr[0:empstr.find(" AS ")].strip() } )                    
                    break;
                            
                else:
                    empstr = from_str[pos:index]
                    alis_dict.update( { empstr[empstr.find(" AS ")+3:].strip() : empstr[0:empstr.find(" AS ")].strip() } )
                pos = index + 1           

            print(alis_dict)
            posw = 0
            indexw = 0
            while 1:
                indexw = where_str.find("AND", posw)
                if indexw == -1:
                    temp_str = where_str[posw:].strip()
                    thelist.append(temp_str)
                    break;
      
                else:
                    temp_str = where_str[posw : indexw].strip()
                    thelist.append(temp_str)
                posw = indexw + 3
            print(thelist)
            for eachstr in thelist:
                if  eachstr.find("=") != -1:
                    s1 = eachstr[0 : eachstr.find("=")].strip()
                    s2 = eachstr[eachstr.find("=")+1 :].strip()
                    if s1.find(".") != -1 and s2.find(".") != -1:                    
                        matrix = [[0 for col in range(size)] for row in range(1)]
                        finalStr = alis_dict.get(s1[0 : s1.find(".") ]) + "-"+ alis_dict.get( s2[0 : s2.find(".")])
                        reverseStr  =  alis_dict.get( s2[0 : s2.find(".")]) + "-" + alis_dict.get(s1[0 : s1.find(".") ])
                        print(finalStr)
                        print(reverseStr)
                        col_num = tableI.get(finalStr)
                        print(col_num)
                        if(col_num == None):
                            col_num = tableI.get(reverseStr)
                            print(col_num)
                            if(col_num != None):
                                matrix[0][col_num] = 1                        
                                matrix = np.asarray(matrix)
                                print(matrix)
                                print(np.shape(matrix))
                                matrixList.append(matrix)
            print(matrixList)
            return matrixList

def allTablesIndex(dataPath):

        from_str    = ""
        where_str   = ""
        alis_dict   = {}
        table_index = {}
        vector_index = {}
        thelist        = []
        matrix      = None
        outputfilename    = None
        idx = -1
        files_to_ignore = ['processed', 'README.md', 'fkindexes.sql', 'schema.sql', 'selmaparser.py']
        files = [f for f in os.listdir(dataPath) if f not in files_to_ignore]
        for file in files:
            filename = file[file.rfind("/")+1:]
            query_str = os.path.join(dataPath,filename)
            query_str = open(query_str, "r").read()
            query_str = query_str.upper()
            query_str = query_str.replace("(", " ")
            query_str = query_str.replace(")", " ")
            query_str = query_str.replace(" OR ", " AND ")
            temp_str = ""
                    
            from_index = query_str.index("\nFROM ")
            from_index = from_index + 6
                    
            where_index = query_str.index("\nWHERE ")
                    
            temp_str = query_str[from_index:where_index]
                    
            for word in temp_str.split("\n"):
                from_str = from_str + word.strip()
                        
            where_index = where_index + 7
            temp_str = query_str[where_index:]
                
                    
            for word in temp_str.split("\n"):
                where_str = where_str + word.strip()


            pos = 0    
            index = 0
            while 1:
                index = from_str.find("," , pos)
                if index == -1:
                    temp_str = from_str[pos:]
                    alis_dict.update( { temp_str[temp_str.find("AS ")+3:].strip() : temp_str[0:temp_str.find(" AS ")].strip() } )
                    if temp_str[0 : temp_str.find(" AS ")].strip() in table_index.keys():
                        None
                    else:
                        idx = idx + 1
                        table_index.update( { temp_str[0 : temp_str.find(" AS ")].strip() : idx } )
                    break;
                            
                else:
                    temp_str = from_str[pos:index]
                    alis_dict.update( { temp_str[temp_str.find(" AS ")+3:].strip() : temp_str[0:temp_str.find(" AS ")].strip() } )                    
                    if temp_str[0 : temp_str.find(" AS ")].strip() in table_index.keys():
                        None
                    else:
                        idx = idx + 1
                        table_index.update( { temp_str[0 : temp_str.find(" AS ")].strip() : idx } )
                pos = index + 1
                    
        # Hack!!
        table_index['AKA_TITLE'] = 20
        vectorTable  = createVectorTable(table_index)
        return(vectorTable)

def process_job_dataset(job_dataset_path):
    files_to_ignore = ['processed', 'README.md', 'fkindexes.sql', 'schema.sql', 'selmaparser.py']
    files = [f for f in os.listdir(job_dataset_path) if f not in files_to_ignore]
    parsed_dataset = []
    vectorTableindex = allTablesIndex(job_dataset_path)
    with open('data/JOB/processed/table_index_mapping.json', 'w') as json_file:
        json.dump(vectorTableindex, json_file)
    # -----------------------------------------------------------------------------
    # In the JOB dataset, each SQL file is a query. So we save the parsed features
    # for each query and store it along with its filename for further use
    # And since we have all our SQL files neatly laid out ..
    # -----------------------------------------------------------------------------
    for file in files:
        filename = file[file.rfind("/")+1:]
        print('------------------------------------------------')
        filename  = os.path.join(job_dataset_path, filename)
        print(filename)
        query_features = parseQuery(filename,vectorTableindex)
        parsed_dataset.append(
           {
                filename : query_features
            }
        )
        print('------------------------------------------------')
    output_path = os.path.join(job_dataset_path, 'processed')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # Store the stuff we parsed to pickle, because why not?
    with open(os.path.join(output_path, 'job_processed.pickle'), 'wb') as f:
        pickle.dump(parsed_dataset, f)    

        

def load_parsed_dataset(dataset_path):
    print(dataset_path)
    with open(dataset_path, 'rb') as pickle_file:
        content = pickle.load(pickle_file)
    return content

process_job_dataset('data/JOB/')
d = load_parsed_dataset('data/JOB/processed/job_processed.pickle')
print(d)