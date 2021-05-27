from mpi4py import MPI
import math
import random

world = MPI.COMM_WORLD
numprocs = world.size
myid = world.rank
procname = MPI.Get_processor_name()

# test comment
for i in range(2, 7):
    random.seed(i)
    list_size = 10 ** i
    points = []
    for j in range(list_size):
        points.append([random.uniform(0, 1), random.uniform(0, 1)])

    chunk_width = list_size // numprocs
    chunk_start = chunk_width + list_size%numprocs

    start_index = chunk_start + (myid-1)*chunk_width
    end_index = start_index + chunk_width

    if myid == 0:
        startwtime = MPI.Wtime()

    part_point_counter = 0

    if myid == 0:
        for k in range(0, chunk_start):
            if ((points[k][0] ** 2) + (points[k][1] ** 2)) <= 1:
                part_point_counter += 1
    else:
        for k in range(start_index, end_index):
            if ((points[k][0] ** 2) + (points[k][1] ** 2)) <= 1:
                part_point_counter += 1

    sum = world.reduce(part_point_counter, op=MPI.SUM, root=0)

    if myid == 0:
        endwtime = MPI.Wtime()
        runtime = endwtime - startwtime
        pi_estimate = 4*sum / list_size
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

    world.barrier()
