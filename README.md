# Wordle-solver

the actual calculator is called wordle_solver_v2.py
if you'd like to change the algorithm and test the results use wordle_bot27.py

this project is a rough draft, but has been optimized to the point the average laptop can run it. There is a file called resultmap.txt required that is larger than github allows to upload. if you run wordle_solver_v2.py, the create_files() function will detect its absence, and begin writing it. this will take a while as it has to caculate what result you get for every possible guess on every possible answer. once this file is written, the program can read from resultmap.txt rather then making all the calculations each time. this project was written on windows, not certain of mac compatability.
