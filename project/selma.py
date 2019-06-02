import os
import pickle
import selmaparser as sp
import numpy as np

def process_job_dataset(job_dataset_path):
    files_to_ignore = ['README.md', 'fkindexes.sql', 'schema.sql']
    files = [f for f in os.listdir(job_dataset_path) if f not in files_to_ignore]
    parsed_dataset = []
    vectorTableindex = sp.allTablesIndex(job_dataset_path)
    # -----------------------------------------------------------------------------
    # In the JOB dataset, each SQL file is a query. So we save the parsed features
    # for each query and store it along with its filename for further use
    # And since we have all our SQL files neatly laid out ..
    # -----------------------------------------------------------------------------
    for file in files:
        filename = file[file.rfind("/")+1:]
        filename  = os.path.join(job_dataset_path, filename)
        #print(filename)
        query_features = sp.parseQuery(filename,vectorTableindex)
        parsed_dataset.append(
           {
                filename : query_features
            }
        )
        #print(parsed_dataset)
    output_path = os.path.join(job_dataset_path, 'processed')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
 
    # Store the stuff we parsed to pickle, because why not?
    with open(os.path.join(output_path, 'job_processed.pickle'), 'w') as f:
        pickle.dump(parsed_dataset, f)    

        

def load_parsed_dataset(dataset_path):
    with open(dataset_path, 'rb') as pickle_file:
        content = pickle.load(pickle_file)
    return content