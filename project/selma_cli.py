import argparse
import selma
import os

def main(args):
    print('Hello!')
    print(selma.load_parsed_dataset('/home/rithomas/Desktop/workspace/Self-Driving-Materialized-Views/project/data/JOB/processed/job_processed.pickle'))
    if False:
        if args.dataset_path:
            print('Processing JOB dataset ..')            
            outputFile = os.path.join(args.dataset_path, 'processed', 'job_processed.pickle')
            if not os.path.isfile(outputFile):
                filepath = args.dataset_path
                selma.process_job_dataset(filepath)
            
            print(outputFile)
            print(selma.load_parsed_dataset(outputFile))
            print('Processed JOB dataset. The output has been saved into a pickle file in data/JOB/processed/job_processed.pickle!')
        else:
            raise argparse.ArgumentTypeError('Please specify a dataset path buddy!')
    elif args.load_dataset:
        if args.dataset_path:
            selma.load_parsed_dataset(args.dataset_path)
        else:
            raise argparse.ArgumentTypeError('Please specify a dataset path buddy!')
    print('Ciao!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    #-------------------------------------------------------------------------------------
    # Data preprocessing arguments
    #-------------------------------------------------------------------------------------
    parser.add_argument(
        "--process_dataset",
        help = '''Set this flag incase you want to process a dataset with queries. Specify
            the relative or absolute as an argument''',
        default = False,
    )

    # Raises ArgumentError if not passed when --process_dataset flag is set 
    parser.add_argument(
        "dataset_path",
        help = '''Relative or absolute path to the raw JOB or TPCH dataset''',
    )

    parser.add_argument(
        "output_path",
        help = '''Relative or absolute path to where you want the processed dataset
            to be stored''',
    )

    args = parser.parse_args()
    print(args)
    main(args)