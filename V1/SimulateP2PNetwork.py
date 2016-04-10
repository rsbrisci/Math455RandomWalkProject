# Author:
# Ross Sbriscia, April 2016
import random
import sys
import traceback
import os
import math
import argparse
import time
import random_connected_graph

# Parses Arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='Simulates a P2P network with random dynamic connectivity in order to examines runtime \
and space complexity of search algorithms.',
                                 epilog="Examples:\n\
\n\
python SimulateP2PNetwork.py 30 randomwalk -o output\n\
This will simulate a network of 30 vertices and use the random walk algorithm, outputs in output.csv\n\
\n\
python SimulateP2PNetwork.py 500 bfs -e 20\n\
This will simulate a network of 500 verticies, using the BFS algorithm, and run a \
new experiment (assign new start and end nodes) on each graph 20 times.\n\
\n\
python SimulateP2PNetwork.py 350 randomwalk -e 30 -t 200\n\
This will simulate a network of 500 verticies, using the randomwalk algorithm, run a \
new trial (assign new start and end nodes) on each graph 30 times and re-build (assign new edges) the graph 200 times.\n\
\n\
Output: a csv in the following form (one line per experiment);\n\
num vertices, num edges, algorithm used, average length of path found, space needed per host\n\
Ex:\n\
300,543,randomwalk,102,32\n\
300,543,randomwalk,34,32\n\
300,1120,randomwalk,3,32\n\
.\n\
.\n\
.")
parser.add_argument('vertices', type=int,
                    help='Number of vertices in the simulated network (Recommend <= 1000)')
parser.add_argument('algorithm', choices=['randomwalk', 'bfs', 'lazyrandomwalk'],
                    help='Choose an algorithm to use in the simulation')
parser.add_argument('-r', type=int,
                    help='(Default 10) Number of RUNS per EXPERIMENTS (exact same start and end nodes, on network with same edges)')
parser.add_argument('-e', type=int,
                    help='(Default 50) Number of EXPERIMENTS per TRIAL (new start and end nodes, on network with same edges)')
parser.add_argument('-t', type=int,
                    help='(Default 100) Number of TRIALS (times graph will be re-built with new edges)')
parser.add_argument('-o',
                    help='Specify output filename')
args = parser.parse_args()
numberOfVertices = args.vertices
algorithm = args.algorithm
numberOfFailiures = 0
maxPathLength = 4 * (math.pow(numberOfVertices, 1))
if args.t:
    numberOfTrails = args.t
else:
    numberOfTrails = 100

if args.o:
    outfileName = "./Data/" + args.o + ".csv"
else:
    if (algorithm == "randomwalk"):
        outfileName = "../Data/RandomWalkSimulation.csv"
    if (algorithm == "bfs"):
        outfileName = "../Data/BFSSimulation.csv"
    if (algorithm == "lazyrandomwalk"):
        outfileName = "../Data/LazyRandomWalkSimulation.csv"

if args.e:
    numberOfExperiments = args.e
else:
    numberOfExperiments = 50

if args.r:
    numberOfRuns = args.r
else:
    numberOfRuns = 10

# Code Starts Here!

# Returns the maximum possible number of edges of an undirected graph with
# n verticies


def maxEdges(n):
    return (n * (n - 1)) / 2

# Runs the algorithm and collects data


def runAlgorithm(graph, startHost, endHost):
    # Algorithm sends a constant ammount of data per hop. 8 bytes of data.
    if (algorithm == "randomwalk"):
        hops = []
        currHost = random.choice(graph.neighborSet[startHost])
        starttime = time.time()
        while (len(hops) <= maxPathLength and currHost != endHost):
            currHost = random.choice(graph.neighborSet[currHost])
            hops.append(currHost)
        finishtime = time.time()
        return hops, (finishtime - starttime)
    if (algorithm == "bfs"):
     # maintain a queue of paths
        queue = []
        # push the first path into the queue
        queue.append([startHost])
        starttime = time.time()
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            # get the last node from the path
            currHost = path[-1]
            # path found
            if currHost == endHost:
                finishtime =  time.time()
                return path, (finishtime - starttime)
            # enumerate all adjacent nodes, construct a new path and push it
            # into the queue
            for adjacent in graph.neighborSet[currHost]:
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)

    if (algorithm == "lazyrandomwalk"):
        hops = []
        currHost = random.choice(graph.neighborSet[startHost])
        starttime = time.time()
        while (len(hops) <= maxPathLength and currHost != endHost):
            stay = random.random();
            if (stay > .5):
                currHost = random.choice(graph.neighborSet[currHost])
            hops.append(currHost)
        finishtime = time.time()
        return hops, (finishtime - starttime)

# Returns a connected graph with randomized edges.
# This simulates the reality of real p2p networks,
# as hosts very often come online and go offline.


def shuffleConnections():
    edges = random.randrange(numberOfVertices - 1, maxEdges(numberOfVertices))
    verts = [x for x in xrange(int(numberOfVertices))]
    network = random_connected_graph.random_walk(verts, edges)
    network.sort_edges()
    # print "Generated network containing:\n\
    #%d hosts (vertices)\n\
    #%d connections (edges)" % (len(network.nodes), len(network.edges));
    return network

# Shuffles node looking for the file, and node which has the file


def shuffleHostsOfInterest():
    startNode = random.randrange(0, numberOfVertices - 1)
    endNode = random.randrange(0, numberOfVertices - 1)
    if (startNode == endNode):
        return shuffleHostsOfInterest()
    else:
        return startNode, endNode

# setup loading bar
print "\n\nRunning Simulations..."
trialRatio = math.ceil(numberOfTrails * 2 / 100)
sys.stdout.write("[%s]" % (" " * 50))
sys.stdout.flush()
sys.stdout.write("\b" * (50 + 1))  # return to start of line, after '['

# Run the expirement
outputCSV = open(outfileName, 'w')

for currentTrial in range(numberOfTrails):
    network = shuffleConnections()
    for currentExeriment in range(numberOfExperiments):
        startHost, endHost = shuffleHostsOfInterest()
        hops = []
        runtime = []
        spacePerHost = 32  # Estimated 32 bytes of data for the base request.
        for currentRun in range(numberOfRuns):
            numhops, searchtime = runAlgorithm(network, startHost, endHost)
            runtime.append(searchtime)
            hops.append(sum(numhops))
        averageRunTime = sum(runtime) / len(runtime)
        averageHopLength = sum(hops) / len(hops)
        averageRunTime += averageHopLength*0.0001 # Adds link latency into computation, estimating 0.0001 second transmission delay/hop
        if algorithm == "bfs":
            spacePerHost += averageHopLength * 8
        includedFailiure = False
        averageRunTime += spacePerHost/1250000 # Allows for a 10Mbs (average) upload speed bottleneck on all hosts
        if maxPathLength in hops:
            includedFailiure = True
        outputCSV.write("%d,%d,%s,%d,%r,%d,%.6f\n" % (numberOfVertices, len(
            network.edges), algorithm, averageHopLength, includedFailiure, spacePerHost, averageRunTime))

    # Progress Bar
    try:                      # If number of Trials is >50
        if (currentTrial % trialRatio == 0):
            sys.stdout.write("\033[92m=>\033[0m")
            sys.stdout.flush()
            sys.stdout.write("\b")
            sys.stdout.flush()
    except ZeroDivisionError:  # If number of Trials is <50
        sys.stdout.write("\033[92m=>\033[0m")
        sys.stdout.flush()
        sys.stdout.write("\b")
        sys.stdout.flush()
sys.stdout.write(']\n')