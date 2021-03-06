# Math455RandomWalkProject
NOT YET FEATURE COMPLETE

The purpose of this project is to examine the performance consequences of using random-walk based algorithms in p2p filesharing networks.

## Requirements
1. Python https://www.python.org/downloads/
2. R-Base https://cran.cnr.berkeley.edu/
3. python Library FNSS (pip install fnss)

## Usage
#### First, to generate data, run the following python script on your desired algorithms!
```
cd Python\ Solution\ v1.0
python SimulateP2PNetwork.py -h
usage: SimulateP2PNetwork.py [-h] [-r R] [-e E] [-t T] [-o O]
                             vertices {randomwalk,bfs,lazyrandomwalk}

Simulates a P2P network with random dynamic connectivity in order to examines runtime and space complexity of search algorithms.

positional arguments:
  vertices              Number of vertices in the simulated network (Recommend
                        <= 1000)
  {randomwalk,bfs,lazyrandomwalk}
                        Choose an algorithm to use in the simulation

optional arguments:
  -h, --help            show this help message and exit
  -r R                  (Default 10) Number of RUNS per EXPERIMENTS (exact
                        same start and end nodes, on network with same edges)
  -e E                  (Default 50) Number of EXPERIMENTS per TRIAL (new
                        start and end nodes, on network with same edges)
  -t T                  (Default 100) Number of TRIALS (times graph will be
                        re-built with new edges)
  -o O                  Specify output filename

Examples:

python SimulateP2PNetwork.py 30 randomwalk -o output
This will simulate a network of 30 vertices and use the random walk algorithm, outputs in output.csv

python SimulateP2PNetwork.py 500 bfs -e 20
This will simulate a network of 500 verticies, using the BFS algorithm, and run a new experiment (assign new start and end nodes) on each graph 20 times.

python SimulateP2PNetwork.py 350 randomwalk -e 30 -t 200
This will simulate a network of 500 verticies, using the randomwalk algorithm, run a new trial (assign new start and end nodes) on each graph 30 times and re-build (assign new edges) the graph 200 times.

Output: a csv in the following form (one line per experiment);
num vertices, num edges, algorithm used, average length of path found, if file NEVER found, average data per hop (bytes), runningtime (seconds)
Ex:
250,10898,randomwalk,32373,False,32,3.237650
250,10898,randomwalk,25520,False,32,2.553203
250,10898,randomwalk,28501,False,32,2.851121
.
.
.
```
#### Next, to visualize (graph) the data, run the following R command:
#### Outputs a PDF "Rplots.pdf" in the same directory
```
cd R
Rscript visualizeData.R ../Data/[name of CSV file]
or
Rscript compareData.R ../Data/[name of 1st CSV file] ../Data/[name of 2nd CSV file]
```
###### Credit Github User: bwbaugh, original creator of "random_connected_graph.py", which I modified for this project!
###### Credit for FNSS Library: L. Saino, C. Cocora, G. Pavlou, A Toolchain for Simplifying Network Simulation Setup, in Proceedings of the 6th International ICST Conference on Simulation Tools and Techniques (SIMUTOOLS '13), Cannes, France, March 2013
