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
    for m in range(1, 4):
        num_of_threads = 2 ** m

        for n in range(2, 7):
            total_num_of_points = 10 ** n

            chunk = total_num_of_points // num_of_threads
            start = chunk + total_num_of_points % num_of_threads

            threads = []

            start_time = time.time()

            t = MonteThread(args=(0, start))
            t.start()
            threads.append(t)

            for i in range(1, num_of_threads):
                start_index = start + chunk * (i - 1)
                end_index = start_index + chunk
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

            pi_estimate = 4 * count / total_num_of_points
            print("number of points:  ", total_num_of_points)
            print("number of threads: ", num_of_threads)
            print("pi estimate:       ", pi_estimate)
            print("dela:              ", math.pi - pi_estimate)
            print("time:              ", net_time)
            print()


main()
