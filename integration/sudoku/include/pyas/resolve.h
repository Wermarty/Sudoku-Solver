#include "pyas/sudoku.h"

#ifndef RESOLVE_H
#define RESOLVE_H

#define MAX_COLUMNS 25

//int number_of_constraints(sudoku_t* psudoku, int x, int y);
int backtracking(sudoku_t* psudoku, int nbempty);
int optimised_backtracking(sudoku_t* psudoku, int nbempty);
int count_contraints(sudoku_t* psudoku, int x, int y);
void set_possibilities(sudoku_t* psudoku, int x, int y);

#endif
