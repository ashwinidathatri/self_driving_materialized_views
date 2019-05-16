# Self Driving Materialized Views
TODO - Add a good readme.md for this project

### Usage
To process the JOB dataset which is placed in project/data/JOB, go to folder project and run
```
python3 selma_cli.py --process_dataset True 'data/JOB' 'data/JOB/processed/job.pickle'
```

To see all the options provided by the CLI, you can use the help option
```
python3 selma_cli.py -h
```

# Standard Git workflow for Project

- MOST IMPORTANT RULE -- NEVER PUSH TO MASTER
- To start off, branch off from master and create your branch for development (the changes you want to add).
- Do all changes nicely, add changes, and commit changes on your local repo.
- Try to ensure that the commit message explains the changes being made within the commit
- Once its all good, push your branch to origin ('our remote repo')
- Create a Pull Request
- Wait for Pull Request to be reviewed by someone, discuss changes, and get everything in place.
- Merge the Pull Request
- Chill
