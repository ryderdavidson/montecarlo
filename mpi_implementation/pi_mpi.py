from mpi4py import MPI
import math
import random

world = MPI.COMM_WORLD
numprocs = world.size                               # SBATCH variable: nodes (defined in SBATCH file)
myid = world.rank
procname = MPI.Get_processor_name()

START_RANGE = 2                                     # Lower range (10 ** START_RANGE) number of points 
END_RANGE = 7                                       # Upper range (10 ** END_RANGE) number of points 

def main():
    for i in range(START_RANGE, END_RANGE):
        random.seed()
        list_size = 10 ** i
        points = []
        for j in range(list_size):
            points.append([random.uniform(0, 1), random.uniform(0, 1)])

        block = list_size // numprocs               # block: number of points passed to sheep nodes 
        first_block = block + list_size%numprocs    # first_block: number of points passed to shepherd node
                                                    # (accounts for any remainder not passed to sheep nodes)
        start_index = first_block + (myid-1)*block
        end_index = start_index + block

        if myid == 0:
            startwtime = MPI.Wtime()

        part_point_counter = 0

        if myid == 0:
            for k in range(0, first_block):
                if ((points[k][0] ** 2) + (points[k][1] ** 2)) <= 1:
                    part_point_counter += 1
        else:
            for k in range(start_index, end_index):
                if ((points[k][0] ** 2) + (points[k][1] ** 2)) <= 1:
                    part_point_counter += 1

        sum = world.reduce(part_point_counter, op=MPI.SUM, root=0)  # Sum of all points within unit circle

        if myid == 0:
            endwtime = MPI.Wtime()
            runtime = endwtime - startwtime
            pi_estimate = 4*sum / list_size         # pi_estimate = points within circle / total points
            delta = abs(pi_estimate - math.pi)
            print("List Size:", list_size, "| Number of Nodes:", numprocs)
            print("{:30} {:>10d}"
                  .format("Total Number of Points:", sum))
            print("{:30} {:>10.6f}"
                  .format("Pi Estimate:", pi_estimate))
            print("{:30} {:>10.6f}"
                  .format("Delta Value:", delta))
            print("{:30} {:>10.6f} \n"
                  .format("Runtime (sec):", runtime))

    print("--------------------------------------------\n")

        world.barrier()
