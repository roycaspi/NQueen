import sys


class ChessBoard:
    def __init__(self, n: int):
        """

        :param n: the dimension of the problem
        """
        self.n = n

    def print(self, tour, out=sys.stdout):
        for i in range(self.n):
            col = tour.index(i)
            print(str('|_' * col + '|X' + '|_' * (self.n - col - 1) + '|'), file=out)
        return ''

    def threats(self, tour):
        threats = 0
        for orgCol in range(len(tour)):  # checking only diagonals
            row = tour[orgCol]
            # curCol = orgCol - 1
            # i = 1
            # while curCol >= 0:  # check upper left diagonal
            #     if tour[curCol] == row - i:
            #         threats += 1
            #         break
            #     curCol -= 1
            #     i += 1
            # i = 1
            # curCol = orgCol - 1
            # while curCol >= 0: # check lower left diagonal
            #     if tour[curCol] == row + i:
            #         threats += 1
            #         break
            #     curCol -= 1
            #     i += 1
            curCol = orgCol + 1
            i = 1
            while curCol < self.n:  # check upper right diagonal
                if tour[curCol] == row - i or tour[curCol] == row + i:
                    threats += 1
                    # break
                curCol += 1
                i += 1
            # i = 1
            # curCol = orgCol + 1
            # while curCol < self.n:  # check lower right diagonal
            #     if tour[curCol] == row + i:
            #         threats += 1
            #         # break
            #     curCol += 1
            #     i += 1
        return threats

    # TODO - if needed - try a different calculation of the threats

    # def fitnessFunc(self, tour):
    #     threats = self.threats(tour)
    #     if threats == 0:
    #         # return 2
    #         return 0
    #     else:
    #         # return 1 / threats
    #         return threats
