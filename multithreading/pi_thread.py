import math
import time
import random
import threading


class MonteThread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)
        self.count = 0
        self.starti = args[0]
        self.endi = args[1]

    def run(self):
        for i in range(self.starti, self.endi):
            if math.sqrt(random.uniform(0, 1) ** 2 + random.uniform(0, 1) ** 2) <= 1:
                self.count += 1

    def get_count(self):
        return self.count


def main():

    print()

    thread_min, thread_max = map(int, input("Enter minimum and maximum number of threads :\n"
                                   "(where n is a power of 2 i.e. 2^n): ").split())
    points_min, points_max = map(int, input("\nEnter minimum and maximum number of points n: \n"
                                   "(where n is a power of 10 i.e. 10^n): ").split())

    print()

    # For each number of threads (between 2**thread_min and 2**thread_max) the Monte Carlo method is
    # used to estimate pi (and delta) for each power of 10 between 10**points_min and 10**points_max.

    for m in range(thread_min, thread_max + 1):
        num_of_threads = 2 ** m

        for n in range(points_min, points_max + 1):
            total_num_of_points = 10 ** n

            block = total_num_of_points // num_of_threads                   # block: number of points passed to sheep nodes 
            first_block = block + total_num_of_points % num_of_threads      # first_block: number of points passed to shepherd node
                                                                            # (accounts for any remainder not passed to sheep nodes)
            threads = []

            start_time = time.time()

            t = MonteThread(args=(0, first_block))
            t.start()
            threads.append(t)

            for i in range(1, num_of_threads):
                start_index = first_block + block * (i - 1)
                end_index = start_index + block
                t = MonteThread(args=(start_index, end_index))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            count = 0
            for t in threads:
                count += t.get_count()

            end_time = time.time()
            net_time = end_time - start_time

            pi_estimate = 4 * count / total_num_of_points                   # pi_estimate = points within circle / total points
            print("number of points:  ", total_num_of_points)
            print("number of threads: ", num_of_threads)
            print("pi estimate:       ", pi_estimate)
            print("dela:              ", math.pi - pi_estimate)
            print("time:              ", net_time)
            print()

        print("--------------------------------------------\n")


main()
