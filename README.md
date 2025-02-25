# N-Queen Solver

## Overview
The **N-Queen Solver** is a C++ implementation of the N-Queens problem, which involves placing N queens on an N×N chessboard such that no two queens attack each other. The solution is computed using backtracking, a recursive search algorithm.

## Features
- Solves N-Queen problem for any **N ≥ 1**.
- Implements **backtracking** for efficient searching.
- Prints solutions in a structured format.
- Can handle larger values of N efficiently.

## Installation
```bash
git clone https://github.com/roycaspi/NQueen.git
cd NQueen
```

## Usage
Run the program with a specified board size:
```bash
python nqueen.py 8
```
This will solve the 8-Queens problem.

## Example Output
```
Solution 1:
. Q . . . . . .
. . . . Q . . .
. . . . . . Q .
. . . . . . . Q
. . . Q . . . .
. . . . . Q . .
Q . . . . . . .
. . Q . . . . .

Solution 2:
...
```
