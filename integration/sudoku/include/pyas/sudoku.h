#ifndef SUDOKU_H
#define SUDOKU_H

#ifndef EMPTY
#define EMPTY 0
#endif

typedef struct {
  unsigned int number;  // stores the number between 1 and 9 (or 0 if not filled)
  unsigned int isFilled; // stores 0 if the number has to be filled by the user, 1 if it was given originally
  unsigned int possibilities[9];
} sudoku_cell_t;

typedef struct {
  sudoku_cell_t cells[9][9]; //tableau de taille n², n² représentant la grille, 0 si le chiffre n'est pas rempli
} sudoku_t;

sudoku_t create_sudoku(void);
int number_of_empty_cells(sudoku_t sudoku);
int is_valid_sudoku(sudoku_t sudoku);
int is_final_sudoku(sudoku_t sudoku);
void print_sudoku(sudoku_t sudoku);
sudoku_t generate_random_sudoku(void);
int resolve(sudoku_t* psudoku, int method);
sudoku_t read_sudoku(char* source);
int write_sudoku(sudoku_t sudoku, char* filename);
#endif
