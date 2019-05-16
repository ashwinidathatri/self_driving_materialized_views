import sys
import re
import numpy as np
class Parser:
    _query       = ""
    _from_str    = ""
    _where_str   = ""
    _alis_dict   = {}
    _table_index = {}
    _list        = []
    _matrix		 = None
    _outputfilename    = None
	
	
    def __init__(self, str, filename):
        
        self._query 		 = str
        self._outputfilename = filename
		
    def changeQuery(self):
        self._query = self._query.upper()
        self._query = self._query.replace("(", " ")
        self._query = self._query.replace(")", " ")
        self._query = self._query.replace(" OR ", " AND ")
		
    def display(self):
        print (self._query)
		
    def prepareVector(self):
        temp_str = ""
		
        from_index = self._query.index("\nFROM ")
        from_index = from_index + 6
		
        where_index = self._query.index("\nWHERE ")
        
        temp_str = self._query[from_index:where_index]	
		
        for word in temp_str.split("\n"):
            self._from_str = self._from_str + word.strip()
			
        where_index = where_index + 7
        temp_str = self._query[where_index:]
        
        for word in temp_str.split("\n"):
            self._where_str = self._where_str + word.strip()
			
			
    def prepareFrom(self):

        pos = 0
        index = 0
        idx = -1
        while 1:
            index = self._from_str.find("," , pos)
            if index == -1:
                temp_str = self._from_str[pos:]
                self._alis_dict.update( { temp_str[temp_str.find("AS ")+3:].strip() : temp_str[0:temp_str.find(" AS ")].strip() } )
                if temp_str[0 : temp_str.find(" AS ")].strip() in self._table_index.keys():
                    None
                else:
                    idx = idx + 1
                    self._table_index.update( { temp_str[0 : temp_str.find(" AS ")].strip() : idx } )
                break;
				
            else:
                temp_str = self._from_str[pos:index]
                self._alis_dict.update( { temp_str[temp_str.find(" AS ")+3:].strip() : temp_str[0:temp_str.find(" AS ")].strip() } )
                if temp_str[0 : temp_str.find(" AS ")].strip() in self._table_index.keys():
                    None
                else:
                    idx = idx + 1
                    self._table_index.update( { temp_str[0 : temp_str.find(" AS ")].strip() : idx } )
            pos = index + 1
			
        for key , value in self._table_index.items():
            print ("table name is " ,key, " its index is ", value, "\n")
        size = len(self._table_index)
        self._matrix = [[0 for col in range(size)] for row in range(size)]

        print ("=============================================================================================================\n")
 			
    def populateMatrix(self, str):

        if 	str.find("=") != -1:
            s1 = str[0 : str.find("=")].strip()
            s2 = str[str.find("=")+1 :].strip()
            if s1.find(".") != -1 and s2.find(".") != -1:
                #print ("s1 is ", s1, " s2 is ", s2, "\n")
                row_num = self._table_index.get( self._alis_dict.get( s1[0 : s1.find(".")] ) )
                col_num = self._table_index.get( self._alis_dict.get( s2[0 : s2.find(".")] ) )
				
                #print ("row num is ", row_num, " col num is ", col_num, "\n")
                self._matrix[row_num][col_num] = 1
                print (self._alis_dict.get( s1[0 : s1.find(".")] ), "  join ", self._alis_dict.get( s2[0 : s2.find(".")] ) , " = " , self._matrix[row_num][col_num])
			
    def prepareWhere(self):
	
        pos = 0
        index = 0
        while 1:
            index = self._where_str.find("AND", pos)
            if index == -1:
                temp_str = self._where_str[pos:].strip()
                self._list.append(temp_str)
                break;
  
            else:
                temp_str = self._where_str[pos : index].strip()
                self._list.append(temp_str)
            pos = index + 3
        #print ("the where clauses are ", self._list, "\n")
        for i in self._list:
            self.populateMatrix(i)

        self._matrix = np.asarray(self._matrix)
        np.savetxt(self._outputfilename, self._matrix, "%d")
			
        print "\nThe Final Matrix is \n", self._matrix
                
if __name__ == '__main__':
  
    query = ""
    input_filename = input('Enter file name , Give the absolute Path : ')
    output_dir     = input('Enter Output Path: ')
    temp 		   = input_filename[input_filename.rfind("/")+1:]
    output_filename = output_dir + re.split("\.", temp)[0] + ".out"
    f = open(input_filename, "r")
    for x in f:
        query = query + x  

    obj = Parser(query, output_filename)
    obj.changeQuery()
    #obj.display()
    obj.prepareVector()
    obj.prepareFrom()
    obj.prepareWhere()
