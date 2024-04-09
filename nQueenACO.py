import numpy as np
import os
from ChessBoard import *
import matplotlib.pyplot as plt
from tqdm import tqdm
import timeit


class Colony:

    def __init__(self, cb: ChessBoard, n_ants: int, budget: int, rho: float = 0.999,
                 pdFunc=lambda threats: 1 / threats, seed=None):
        self.board = cb
        self.ants = [Ant(self.board, self, seed) for __ in range(n_ants)]
        self.max_evals = budget
        self.rho = rho
        self.best_tour = [-1 for __ in range(cb.n)]
        self.best_fit = cb.n ** 2
        self.pheromones = np.ones(
            (self.board.n, self.board.n, self.board.n)) / self.board.n  # each square on the board, has n edges
        self.startPoint = np.ones(self.board.n)  # separate array for start point pheromones (first column)
        self.pd_func = pdFunc

    def solve(self, sync: bool = False, storm: bool = False, storm_n=4, storm_rho=0.5):
        fit_history, tour_history = [], []
        pbar = tqdm(total=self.max_evals, position=0, leave=True)
        while self.max_evals > 0 and self.best_fit != 0:
            """ evaporate pheromones """
            if storm:
                self.storm(storm_n, storm_rho)
            self.pheromones *= self.rho
            self.startPoint *= self.rho

            """ evaluate each tour, and find current best """
            for ant in self.ants:
                ant.run_tour()
                self.max_evals -= 1
                if ant.fitness < self.best_fit:
                    self.best_fit = ant.fitness
                    self.best_tour = ant.tour
                    if self.best_fit == 0:
                        print(f"\n{'=' * 60}\nSuccesses!\n")
                        self.board.print(self.best_tour)
                        fit_history.append(self.best_fit)
                        tour_history.append(self.best_tour)
                        return fit_history, tour_history, True
                if sync:
                    ant.depositPheromones()
                    ant.restart()
                fit_history.append(self.best_fit)
                tour_history.append(self.best_tour)
                pbar.update()
            if not sync:
                for ant in self.ants:
                    ant.depositPheromones()
                    ant.restart()
        return fit_history, tour_history, False

    def storm(self, n_times=4, rho=0.5):
        """
        Violently evaporates the pheromone matrix n_times while solving the problem, using rho as the evaporation rate
        of the storm.
        """
        if self.max_evals % (self.max_evals // n_times) == 0:
            self.pheromones *= rho
            self.startPoint *= rho


class Ant:
    def __init__(self, board: ChessBoard, colony: Colony, seed=None):
        self.p = board
        self.c = colony
        self.local_state = np.random.RandomState(seed)
        x, y = self.local_state.randint(self.p.n), 0  # an ants tour starts in a random square in row 0
        self.currSquare = x, y
        self.tour = [x]
        self.fitness = board.n ** 2       # default value, larger then any tour possible

    def step(self):
        """ the ant chooses the next queen to apply on the board using roulette """
        x, y = self.currSquare
        no_tabu = [self.c.pheromones[x][y][i] if i not in self.tour else 0 for i in range(self.p.n)]
        pr = np.cumsum(no_tabu)
        ps = pr[-1]  # pr[-1] is the sum of pheromones
        if ps == 0:  # should never happen
            raise ZeroDivisionError
        r = self.local_state.uniform(0, 1)
        x = 0
        while pr[x] / ps < r:  # roulette choice of next row
            x += 1
        y += 1
        self.tour.append(x)
        self.currSquare = x, y

    def run_tour(self):
        for __ in range(self.p.n - 1):
            self.step()
        threats = self.p.threats(self.tour)
        if threats == 0:
            self.fitness = 0
        else:
            self.fitness = self.p.threats(self.tour)
        return self.tour

    def depositPheromones(self):
        self.c.startPoint[self.tour[0]] += self.c.pd_func(self.fitness)
        for col in range(len(self.tour) - 1):
            row = self.tour[col]
            self.c.pheromones[row][col][self.tour[col + 1]] += self.c.pd_func(self.fitness)

    def restart(self):
        pr = np.cumsum(self.c.startPoint)
        ps = pr[-1]  # pr[-1] is the sum of pheromones of first column
        if ps == 0:  # should never happen
            raise ZeroDivisionError
        r = self.local_state.uniform(0, 1)
        x = 0
        while pr[x] / ps < r:  # roulette choice of next row
            x += 1
        self.tour = [x]
        self.currSquare = x, 0


if __name__ == '__main__':
    start = timeit.default_timer()
    logfile_name = "run_log"
    logger_name = "logger "
    """ this run's parameters """
    loops = 4
    n = 32
    antsNum = 200
    budget = 10**5
    rho = 0.9
    sync = False
    storm = False
    storm_n = 4
    storm_rho = 0.5

    def phro_deposit_func(threats):
        """ (1 / threats)**3 """
        return (1 / threats)**2

    seed = None
    board = ChessBoard(n)

    """ main logging file - documents global stats """
    if not os.path.isfile(f'{logger_name}{n}X{n}.txt'):
        with open('logger_example.txt', 'r') as firstfile, open(f'{logger_name}{n}X{n}.txt', 'w') as secondfile:
            # read content from first file
            for line in firstfile:
                # append content to second file
                secondfile.write(line)
    with open(f'{logger_name}{n}X{n}.txt') as reader:
        lines = reader.readlines()
    runs = int(lines[0].split()[-1])
    num_successes = int(lines[1].split()[-1])
    targetFunc_calls = int(lines[2].split()[-1])
    average_us_threats = float(lines[3].split()[-1])
    for i in range(4, 8):
        lines[i] = lines[i][:-1]

    for __ in range(loops):
        """ init colony """
        colony = Colony(board, antsNum, budget, rho, phro_deposit_func, seed)
        """ logger parameters """
        runs += 1
        run_log = open(os.getcwd() + "\\log\\" + f'{logfile_name}{n}X{n}_{runs}.txt', "w")
        """ run colony """
        fitHis, tourHis, success = colony.solve(sync, storm, storm_n, storm_rho)

        """ plot fit history - headline and summary for each run """
        plt.plot(np.array(fitHis))
        plt.title(f"Run {runs}")
        plt.savefig(os.getcwd() + "\\log\\" + f'{logfile_name}{n}X{n}_{runs}.png')
        plt.show()

        targetFunc_calls += budget - colony.max_evals
        """ log """
        t = f"{'='*60}\nRun {runs}:\n"\
            f"Best tour found:\n{colony.best_tour}\n"\
            f"{board.print(colony.best_tour, run_log)}"\
            f"Number of threats: {colony.board.threats(colony.best_tour)}\n\n{'=' * 60}\n" \
            f"Run Parameters:\n"\
            f"n = {n}\nMain loops = {loops}\nNumber of ants = {antsNum}\nBudget = {budget}\n"\
            f"evals = {budget - colony.max_evals}\nrho = {rho}\nseed = {seed}\n" \
            f"Pheromones deposit function = {colony.pd_func.__doc__}\n"\
            f"sync = {sync}\nstorm = {storm} with params n={storm_n} rho={storm_rho}"
        run_log.write(t)
        print('\n'+t)
        if success:
            num_successes += 1
            if len(lines[4]) > 0:
                lines[4] += f' '
                lines[6] += f' '
            lines[4] += f'{runs}'
            lines[6] += f'{budget - colony.max_evals}'
        else:
            average_us_threats = ((runs-num_successes-1)*average_us_threats + colony.board.threats(colony.best_tour)) \
                                 / runs - num_successes
    """ end loop """
    # log to main logger
    log_params = [runs, num_successes, targetFunc_calls, average_us_threats]
    for i in range(len(log_params)):
        lines[i] = ' '.join((lines[i].split())[:-1] + [str(log_params[i])])

    lt = '\n'.join(lines)
    with open(f'{logger_name}{n}X{n}.txt', 'w') as writer:
        writer.write(lt+'\n')
    end = timeit.default_timer()
    print(f"\n{'='*60}\nTotal time elapsed: {(end-start) // 60} minutes and {(end-start) % 60} seconds\n{lt}")
