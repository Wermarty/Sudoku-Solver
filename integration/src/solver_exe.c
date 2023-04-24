#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <math.h>
#include <string.h>

#define MAX_COLUMNS 25

//int number_of_constraints(sudoku_t* psudoku, int x, int y);
int backtracking(sudoku_t* psudoku, int nbempty);
int optimised_backtracking(sudoku_t* psudoku, int nbempty);
int count_contraints(sudoku_t* psudoku, int x, int y);
void set_possibilities(sudoku_t* psudoku, int x, int y);


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

int count_contraints(sudoku_t* psudoku, int x, int y) {
  int possibilities = 0;
  int num;
  for (num = 1; num <= 9; num++) {
    possibilities = possibilities + (psudoku->cells[x][y].possibilities[num-1] == 1);
  }
  //printf("(%d, %d) = %d | ", x, y, possibilities);
  return 9 - possibilities;
}

void set_possibilities(sudoku_t* psudoku, int x, int y) {
  int i, j, num;
  for (num = 1; num <= 9; num++) {
    psudoku->cells[x][y].possibilities[num-1] = 1;
  }

  if (psudoku->cells[x][y].number != 0) {
    for (num = 1; num <= 9; num++) {
      psudoku->cells[x][y].possibilities[num-1] = 0;
    }
    return;
  }

  for (i = 0; i < 9; i++) {
    num = psudoku->cells[i][y].number;
    if (num != 0) {
      psudoku->cells[x][y].possibilities[num-1] = 0;
    }
  }

  for (j = 0; j < 9; j++) {
    num = psudoku->cells[x][j].number;
    if (num != 0) {
      psudoku->cells[x][y].possibilities[num-1] = 0;
    }
  }
  for (i = x / 3 * 3; i < x / 3 * 3 + 3; i++) {
    for (j = y / 3 * 3; j < y / 3 * 3 + 3; j++) {
      num = psudoku->cells[i][j].number;
      if (num != 0) {
        psudoku->cells[x][y].possibilities[num-1] = 0;
      }
    }
  }
}


static void max_index(int matrice[9][9], int nb_lignes, int nb_colonnes, int *xmax, int *ymax) {
  int i, j;
  *xmax = 0;
  *ymax = 0;
  int max = -1;
  for (i = 0; i < nb_lignes; i++) {
    for (j = 0; j < nb_colonnes; j++) {
      if (matrice[i][j] > max && matrice[i][j] < 9) {
        max = matrice[i][j];
        *xmax = i;
        *ymax = j;
      }
    }
  }
}


int backtracking(sudoku_t* psudoku, int nbempty) {
  int i, j, k;
  if (nbempty == 0) {
    return 1;
  }
  for (i = 0; i < 9; i++) {
    for (j = 0; j < 9; j++) {
      if (psudoku->cells[i][j].number == EMPTY) {
        for (k = 1; k <= 9; k++) {
          psudoku->cells[i][j].number = k;
          if (is_valid_sudoku(*psudoku)) {
            if (backtracking(psudoku, nbempty - 1)) {
              return 1;
            }
          }
        }
        psudoku->cells[i][j].number = 0;
        return 0;
      }
    }
  }
  return 0;
}


int optimised_backtracking(sudoku_t* psudoku, int nbempty) {
  int i, j, k, m;
  int l = 0;
  int choice[9] = {0};
  int valid_choices[9] = {0}; // tableau pour stocker les indices des possibilités valides
  int num_valid_choices = 0; // nombre de possibilités valides
  sudoku_t next_sudoku = *psudoku;

  if (nbempty == 0) {
    return 1;
  }

  // calcul des contraintes
  int tab_of_constraints[9][9];
  for (i = 0; i < 9; i++) {
    for (j = 0; j < 9; j++) {
      set_possibilities(psudoku, i, j);
      tab_of_constraints[i][j] = count_contraints(psudoku, i, j);
    }
  }

  // choix de la cellule la plus contrainte
  max_index(tab_of_constraints, 9, 9, &i, &j);
  m = tab_of_constraints[i][j];

  // stockage des possibilités valides dans le tableau choice
  for (k = 0; k < 9; k++) {
    if ((psudoku->cells[i][j].possibilities)[k] == 1) {
      choice[l] = k + 1;
      l++;
      num_valid_choices++;
    }
  }

  // stockage des indices des possibilités valides dans le tableau valid_choices
  for (k = 0; k < num_valid_choices; k++) {
    if (k < m) {
      valid_choices[k] = k;
    }
  }

  // parcours des possibilités valides
  for (k = 0; k < num_valid_choices; k++) {
    psudoku->cells[i][j].number = choice[valid_choices[k]];
    next_sudoku.cells[i][j].number = choice[valid_choices[k]];
    if (optimised_backtracking(&next_sudoku, nbempty - 1)) {
      *psudoku = next_sudoku;
      return 1;
    }
  }
  printf("solution non valable à la case (%d,%d), avec m=%d\n", i, j, m);
  psudoku->cells[i][j].number = EMPTY; // réinitialisation de la cellule
  return 0;
}


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

