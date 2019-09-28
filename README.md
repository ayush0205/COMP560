# COMP560
Project:     HW1 - KenKen Solver
Authors:     Ayush Jha, Rupesh Gudipudi, Varun Srivastava
Date:        09/27/19

Description: This program uses three algorithms (simple backtracking search,
             our own optimized backtracking search, and a local search) to
             solve a KenKen puzzle. A KenKen puzzle is a constrained NxN grid
             partitioned into groups of blocks, where each group must have numbers
             that satisfy an mathematical operational constraint. In addition,
             there can be no repetitions in number across a row or down a column
             - they must be unique numbers between 1=>N.

Input:       Refer to the main file when accessing the algorithms.
             The program takes in a standard user input, with the first line being
             N (positive integer), or the dimensions of the dimensions of the KenKen
             grid (i.e. 6).The following N lines of the input should be a sequence
             of N characters per line to simulate a grid of alphabetical characters
             (first N letters), where each individual character on the grid represents
             one block to be operationally constrained (i.e ABBCDD). The following
             N lines should contain the alphabetical character followed by a
             colon (:), followed by the target number for the mathematical expression,
             followed by the operational character (i.e A:11+). This all should be
             entered as a newline-separated single input. Attempting to run this
             program while not meeting all of the above specifications will result
             in an error.

Output:      The program will output a space-separated  NxN grid of the correct
             solution to the KenKen puzzle. This grid will then be followed by
             three numbers, separated by newlines. The first number is the number
             of nodes traversed by the simple backtracking search algorithm.
             The second number is the number of nodes traversed by the optimized
             backtracking search algorithm. Finally, the third number is the number
             of total swaps completed by the local search algorithm.
