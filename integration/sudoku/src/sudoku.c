#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <math.h>
#include <string.h>
#include "pyas/resolve.h"
#include "pyas/sudoku.h"


sudoku_t create_sudoku(void) {
  sudoku_t sudoku;
  int i, j;
  for (i = 0; i < 9; i++) {
    for (j = 0; j < 9; j++) {
      sudoku.cells[i][j].number = EMPTY;
      sudoku.cells[i][j].isFilled = 0;
      int initial_possibilities[9] = {1, 1, 1, 1, 1, 1, 1, 1, 1};
      memcpy(sudoku.cells[i][j].possibilities, initial_possibilities, sizeof(initial_possibilities));
    }
  }
  return sudoku;
}

static int is_valid(int arr[]) {
  int i;
  int count[10] = {0}; //Liste d'appel des chiffres entre 0 et 9
  for (i = 0; i < 9; i++) {
    if (arr[i] < 0 || arr[i] > 9) { //tous les chiffres doivent etre entre 0 et 9...
      return 0; //invalid sudoku
    }
    count[arr[i]]++; //Incrément de présence
  }
  for (i = 1; i <= 9; i++) {
    if (count[i] > 1) {
      return 0; //invalid sudoku
    }
  }
  return 1; //valid sudoku
}


int is_valid_sudoku(sudoku_t sudoku) {
  int i, j, k, l;
  int row[9], col[9], box[9];
  for (i = 0; i < 9; i++) {
    for (j = 0; j < 9; j++) {
      row[j] = sudoku.cells[i][j].number;
    }
    if (!is_valid(row)) {
      return 0;
    }
  }
  for (i = 0; i < 9; i++) {
    for (j = 0; j < 9; j++) {
      col[j] = sudoku.cells[j][i].number;
    }
    if (!is_valid(col)) {
      return 0;
    }
  }
  for (i = 0; i < 9; i += 3) {
    for (j = 0; j < 9; j += 3) {
      for (k = 0; k < 3; k++) {
        for (l = 0; l < 3; l++) {
          box[k * 3 + l] = sudoku.cells[i + k][j + l].number;
        }
      }
      if (!is_valid(box)) {
        return 0;
      }
    }
  }
  return 1;
}

int is_final_sudoku(sudoku_t sudoku) {
  return (is_valid_sudoku(sudoku) && (number_of_empty_cells(sudoku) == 0));
}

sudoku_t generate_random_sudoku() {
  sudoku_t sudoku;
  unsigned int seed = time(NULL);
  int i, j;
  for (i = 0; i < 9; i++) {
    for (j = 0; j < 9; j++) {
      sudoku.cells[i][j].number = rand_r(&seed) % 9 + 1;
      sudoku.cells[i][j].isFilled = 0;
    }
  }
  return sudoku;
}

int number_of_empty_cells(sudoku_t sudoku) {
  int c = 0;
  int i, j;
  for (i = 0; i < 9; i++) {
    for (j = 0; j < 9; j++) {
      c = c + (sudoku.cells[i][j].number == EMPTY);
    }
  }
  return c;
}

int resolve(sudoku_t* psudoku, int method) {
  clock_t start, end;
  double cpu_time_used;
  switch (method) {
    case 1:
    start = clock();
    if (backtracking(psudoku, number_of_empty_cells(*psudoku))){
      end = clock();
      cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
      printf("Backtracking resolution succeeded in %f seconds.\n", cpu_time_used);
      return 1;
    }
    else {
      end = clock();
      cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
      printf("Backtracking resolution failed in %f seconds.\n", cpu_time_used);
      return 0;
    }
    break;
    case 2:
    start = clock();
    if (optimised_backtracking(psudoku, number_of_empty_cells(*psudoku))) {
      end = clock();
      cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
      printf("Optimised backtracking resolution succeeded in %f seconds.\n", cpu_time_used);
      return 1;
    }
    else {
      end = clock();
      cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
      printf("Optimised backtracking resolution failed in %f seconds.\n", cpu_time_used);
      return 0;
    }
    break;
    default:
    printf("Please specify which method you want to use :\n");
    printf("- 1 : backtracking\n");
    printf("- 2 : optimised backtracking\n");
    return 0;
  }
}


void print_sudoku(sudoku_t sudoku) {
  int i, j;
  printf("\n");
  for (i = 0; i < 9; i++) {
    if (i % 3 == 0) {
      printf("+-------+-------+-------+\n");
    }
    for (j = 0; j < 9; j++) {
      if (j % 3 == 0) {
        printf("| ");
      }
      printf("%d", sudoku.cells[i][j].number);
      if (sudoku.cells[i][j].isFilled == 1) {
        printf(".");
      } else {
        printf(" ");
      }
    }
    printf("|\n");
  }
  printf("+-------+-------+-------+\n\n");
}


sudoku_t read_sudoku(char* source) {
  FILE* sudoku_file;
  sudoku_file = fopen(source, "r");
  if (sudoku_file == NULL) {
    printf("Error opening file");
    exit(EXIT_FAILURE);
  }

  int size = 0;
  char c;
  while ((c = fgetc(sudoku_file)) != '\n') {
    size++;
  }
  rewind(sudoku_file);
  sudoku_t sudoku = create_sudoku();
  int i, j;

  for (i = 0; i < size; i++) {
    for (j = 0; j < size; j++) {
      char numcell;
      numcell = (int)fgetc(sudoku_file) - 48;
      sudoku.cells[i][j].number = numcell;
      if (numcell != EMPTY) {
        sudoku.cells[i][j].isFilled = 1;
      }
    }
    fscanf(sudoku_file, "\n");
  }
  fclose(sudoku_file);
  if (!(is_valid_sudoku(sudoku))) {
    printf("LE SUDOKU LU N'EST PAS VALIDE ! \n");
    exit(0);
  }
  return sudoku;
}


int write_sudoku(sudoku_t sudoku, char* filename) {
  FILE* sudoku_file;
  sudoku_file = fopen(filename, "w");
  if (sudoku_file == NULL) {
    printf("Error creating file");
    exit(EXIT_FAILURE);
  }
  int size = 9; //pour l'instant, que des sudoku de taille 9
  char eol = '\n';
  int i, j;
  for (i = 0; i < size; i++) {
    for (j = 0; j < size; j++) {
      char numcell = 48 + sudoku.cells[i][j].number;
      if (!(sudoku.cells[i][j].isFilled)) {
        fwrite(&numcell, sizeof(numcell), 1, sudoku_file);
      }
      else {
        numcell = '0';
        fwrite(&numcell, sizeof(numcell), 1, sudoku_file);
      }
    }
    fwrite(&eol, sizeof(char), 1, sudoku_file);
  }
  fclose(sudoku_file);
  return 1;
}
