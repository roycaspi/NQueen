N-Queen Solver

Overview

This repository provides an implementation of the N-Queen problem, a classic combinatorial problem that involves placing N queens on an N×N chessboard so that no two queens threaten each other. This means that no two queens can be in the same row, column, or diagonal.

Features

Supports solving the N-Queen problem for any N ≥ 1.

Uses backtracking to efficiently find all possible solutions.

Provides a simple and clean implementation in Python.

Installation

Clone this repository using:

git clone https://github.com/roycaspi/NQueen.git
cd NQueen

Ensure you have Python installed (Python 3.x recommended).

Usage

Run the script to solve the N-Queen problem for a given N:

python nqueen.py <N>

Example:

python nqueen.py 8

This will solve the 8-Queen problem and print the possible solutions.

Algorithm

The implementation uses the backtracking algorithm:

Place a queen in a row and try different column positions.

If a valid position is found, recursively move to the next row.

If all queens are placed successfully, save the solution.

If no valid position is found, backtrack and try a different column.

Example Output

For N = 4, a sample output could be:

Solution 1:
. Q . .
. . . Q
Q . . .
. . Q .

Solution 2:
. . Q .
Q . . .
. . . Q
. Q . .

Complexity Analysis

The time complexity of the backtracking approach is approximately O(N!), though pruning techniques significantly reduce the search space.

Contributions

Contributions are welcome! If you'd like to improve the implementation, submit a pull request or open an issue.

License

This project is licensed under the MIT License.

Contact

For any inquiries or discussions, feel free to reach out via the GitHub Issues section.
