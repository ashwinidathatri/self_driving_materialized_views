# Self Driving Materialized Views

# Brief Introduction

Usage of intermediate results of queries can reduce the computational cost and improve DB performance. The problem of Materialized View Selection is addressed here. There can be static or dynamic approaches to the this problem. 
Here we consider a dynamic approach, based on deep reinforcement learning. We implement a prototype using the Apache Hive, SQL-on-Hadoop database and we experiment using the Join Order Benchmark. Hive improves the computational cost and query performance by rewriting the queries in accordance with selected materialized views. With the usage of Deep Reinforcement Learning we develop a system called Selma DQM, wherein the incremental value of materializing certain views is evaluated. This is based on selection and eviction policies. This system aims to be an improvement to the heuristic approach and works on an evolving workload. The system is trained using existing queries.


### Usage
To process the JOB dataset which is placed in *project/data/JOB*, go to folder *project* and run
```
python3 selma_cli.py --process_dataset True 'data/JOB' 'data/JOB/processed/job.pickle'
```

To see all the options provided by the CLI, you can use the help option
```
python3 selma_cli.py -h
```
