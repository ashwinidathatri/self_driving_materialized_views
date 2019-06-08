import os
import argparse
import numpy as np


'''class Parser:
    _query       = ""
    _from_str    = ""
    _where_str   = ""
    _alis_dict   = {}
    _table_index = {}
    thelist        = []
    _matrix      = None
    _outputfilename    = None'''

    

def main(args):
    print('Hello!')    
    tableIndex = {}
    queryDic = {}
    matrixTable =  None    
    
    tableIndex = allTablesIndex(args.dataset_path)
    #print(tableIndex)
    matrixVector  = parseQuery(args.queryName, tableIndex)
    #print(matrixVector)

    

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
                
                #print(query_str)
            temp_str = ""                    
            from_index = query_str.index("\nFROM ")
            from_index = from_index + 6                    
            where_index = query_str.index("\nWHERE ")                    
            temp_str = query_str[from_index:where_index]
                #print(temp_str)  
                    
            for word in temp_str.split("\n"):
                from_str = from_str + word.strip()
                        
            where_index = where_index + 7
            temp_str = query_str[where_index:]
                
                    
            for word in temp_str.split("\n"):
                where_str = where_str + word.strip()
            #print(from_str)
            #print(where_str)
            pos = 0    
            index = 0                
                
            while 1:
                    #print(from_str)
                index = from_str.find("," , pos)
                if index == -1:
                    empstr = from_str[pos:]
                    alis_dict.update( { empstr[empstr.find("AS ")+3:].strip() : empstr[0:empstr.find(" AS ")].strip() } )                    
                    break;
                            
                else:
                    empstr = from_str[pos:index]
                    alis_dict.update( { empstr[empstr.find(" AS ")+3:].strip() : empstr[0:empstr.find(" AS ")].strip() } )
                pos = index + 1           


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
                
            for eachstr in thelist:
                if  eachstr.find("=") != -1:
                    s1 = eachstr[0 : eachstr.find("=")].strip()
                    s2 = eachstr[eachstr.find("=")+1 :].strip()
                    if s1.find(".") != -1 and s2.find(".") != -1:                    
                        matrix = [[0 for col in range(size)] for row in range(1)]
                        finalStr = alis_dict.get(s1[0 : s1.find(".") ]) + "-"+ alis_dict.get( s2[0 : s2.find(".")])
                        reverseStr  =  alis_dict.get( s2[0 : s2.find(".")]) + "-" + alis_dict.get(s1[0 : s1.find(".") ])
                        col_num = tableI.get(finalStr)
                        if(col_num == None):
                            col_num = tableI.get(reverseStr)
                            if(col_num != None):
                                #print(col_num)
                                matrix[0][col_num] = 1                        
                                matrix = np.asarray(matrix)
                                matrixList.append(matrix)
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
        files_to_ignore = ['README.md', 'fkindexes.sql', 'schema.sql']
        files = [f for f in os.listdir(dataPath) if f not in files_to_ignore]
        for file in files:
            filename = file[file.rfind("/")+1:]
            query_str = os.path.join(dataPath,filename)
        
        
        #parsed_dataset = []
    
            #print(filename)
            query_str = open(query_str, "r").read()
                #print(query_str)
            query_str = query_str.upper()
            query_str = query_str.replace("(", " ")
            query_str = query_str.replace(")", " ")
            query_str = query_str.replace(" OR ", " AND ")
                
                #print(query_str)
            temp_str = ""
                    
            from_index = query_str.index("\nFROM ")
            from_index = from_index + 6
                    
            where_index = query_str.index("\nWHERE ")
                    
            temp_str = query_str[from_index:where_index]
                #print(temp_str)  
                    
            for word in temp_str.split("\n"):
                from_str = from_str + word.strip()
                        
            where_index = where_index + 7
            temp_str = query_str[where_index:]
                
                    
            for word in temp_str.split("\n"):
                where_str = where_str + word.strip()


            pos = 0    
            index = 0
            while 1:
                    #print(from_str)
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
                    
        vectorTable  = createVectorTable(table_index)
        return(vectorTable)
                    
            

            

if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        
        #-------------------------------------------------------------------------------------
        # Data preprocessing arguments
        #-------------------------------------------------------------------------------------
        '''parser.add_argument(
            "sqlFilename",
            help = '''#To directly send the sql file as an input''',
            
        #)'''
        parser.add_argument(
        "dataset_path",
        help = '''Relative or absolute path to the raw JOB or TPCH dataset''',
        )

        parser.add_argument(
        "queryName",
        help = '''Relative or absolute path to the raw JOB or TPCH dataset''',
        )        
    
        args = parser.parse_args()
        print(args)
        main(args)



