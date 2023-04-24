#include "pyas/sudoku.h"
#include "pyas/resolve.h"

/*
static int not_in(int num, int tab[9]) {
int i;
//printf("num=%d is in ?\n", num);
for (i = 0; i < 9; i++) {
//printf("tab[i]=%d\n,", tab[i]);
if (num == tab[i]) {
return 0;
}
}
return 1;
}
*/


/*
int count_contraints(sudoku_t* psudoku, int row, int col) {
int i, j, count = 0;

// Count constraints in same row
for (j = 0; j < 9; j++) {
if (j != col && psudoku->cells[row][j].number == EMPTY) {
if (is_possible(psudoku, row, j, psudoku->cells[row][col].number)) {
count++;
}
}
}

// Count constraints in same column
for (i = 0; i < 9; i++) {
if (i != row && psudoku->cells[i][col].number == EMPTY) {
if (is_possible(psudoku, i, col, psudoku->cells[row][col].number)) {
count++;
}
}
}

// Count constraints in same 3x3 square
int box_min_row, box_max_row, box_min_col, box_max_col;
get_box_range(row, col, &box_min_row, &box_max_row, &box_min_col, &box_max_col);
for (i = box_min_row; i <= box_max_row; i++) {
for (j = box_min_col; j <= box_max_col; j++) {
if (i != row || j != col) {
if (psudoku->cells[i][j].number == EMPTY && is_possible(psudoku, i, j, psudoku->cells[row][col].number)) {
count++;
}
}
}
}

return count;
}
*/



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



/*
int number_of_constraints(sudoku_t* psudoku, int x, int y) {
int already_counted[9] = {0};
if (psudoku->cells[x][y].number != 0) {
return 9;
}
int c = 0;
int i, j;
int num;
int new;
//printf("----Case (%d, %d)\n", x, y);
for (i = 0; i < 9; i++) {
num = psudoku->cells[i][y].number;
new = not_in(num, already_counted);
c = c + (num != 0 && new); //lines constraints
if (num != 0 && new) {
if (already_counted[num-1] == 0) {
already_counted[num-1] = 1;
psudoku->cells[x][y].possibilities[num-1] = 0;
//printf("(%d, %d) => +%d\n", x, y, num);
}
}
}
for (j = 0; j < 9; j++) {
num = psudoku->cells[x][j].number;
new = not_in(num, already_counted);
c = c + (num != 0 && new); //columns constraints
if (num != 0 && new) {
if (already_counted[num-1] == 0) {
already_counted[num-1] = 1;
psudoku->cells[x][y].possibilities[num-1] = 0;
//printf("(%d, %d) => +%d\n", x, y, num);
}
}
}
for (i = 0; i < 3; i++) {
for (j = 0; j < 3; j++) {
num = psudoku->cells[x % 3 + i][y % 3 + j].number;
new = not_in(num, already_counted);
c = c + (num != 0 && new); //box constraints
if (num != 0 && new) {
if (already_counted[num-1] == 0) {
already_counted[num-1] = 1;
psudoku->cells[x][y].possibilities[num-1] = 0;
//printf("(%d, %d) => +%d\n", x, y, num);
}
}
}
}
return c;
}
*/

//Renvoie le nombre de contraintes associées à la case x, y, et met les possibilités de choix dans
//psudoku->cells[x][y].possibilities[num-1] = 0;
/*
int number_of_constraints(sudoku_t* psudoku, int x, int y) {
int* already_counted = calloc(9, sizeof(int));
if (psudoku->cells[x][y].number != 0) {
return 9;
}
int constraints = 0;
int num;
int is_new;
int i, j;
for (i = 0; i < 9; i++) {
num = psudoku->cells[i][y].number;
is_new = not_in(num, already_counted);
if (num != 0 && is_new) {
already_counted[num-1] = 1;
psudoku->cells[x][y].possibilities[num-1] = 0;
constraints++; //Column constraints
//printf("(%d, %d) => +%d\n", x, y, num);
}
}
//printf("Case (%d,%d) = %d contraintes\n", x, y, constraints);
free(already_counted);
return constraints;
}
*/



/*
int optimised_backtracking(sudoku_t* psudoku, int nbempty) {
  //printf(">declaration variables\n");
  int i, j, k, m;
  int l = 0;
  //printf(">alloc choice\n");
  int choice[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
  //printf(">alloc tab_of_constraints\n");
  if (nbempty == 0) {
    return 1;
  }

  int** tab_of_constraints = malloc(9 * sizeof(int*));
  for (i = 0; i < 9; i++) {
    tab_of_constraints[i] = malloc(9 * sizeof(int));
  } //allocation dynamique du tableau des contraintes !


  //printf(">affectation tab_of_constraints\n");
  for (i = 0; i < 9; i++) {
    for (j = 0; j < 9; j++) {
      //printf(">>>set_possibilities[%d][%d]\n", i, j);
      set_possibilities(psudoku, i, j);
      tab_of_constraints[i][j] = count_contraints(psudoku, i, j); //stockage des possibilités dans chaque cellule et creation du tableau de contraintes
      //printf("2");
    }
  }

  //printf(">selection max_index\n");
  max_index(tab_of_constraints, 9, 9, &i, &j); //choix des meilleurs indices i et j
  m = tab_of_constraints[i][j];
  //tab_of_constraints[i][j] = 9;
  //printf(">alloc stockage possibilites dans choice\n");
  for (k = 0; k < 9; k++) {
    if ((psudoku->cells[i][j].possibilities)[k] == 1) {
      choice[l] = k + 1; //stockage des possibilités
      l = l + 1;
    }
  }
  for (k = 0; k <= m-1; k++) {
    psudoku->cells[i][j].number = choice[k];
    //print_sudoku(*psudoku);
    if (optimised_backtracking(psudoku, nbempty - 1)) {
      for (i = 0; i < 9; i++) {
        free(tab_of_constraints[i]);
      }
      free(tab_of_constraints);
      return 1;
    }
    else {
      psudoku->cells[i][j].number = EMPTY;
    }
  }
  for (i = 0; i < 9; i++) {
    free(tab_of_constraints[i]);
  }
  free(tab_of_constraints);
  return 0;
}*/



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




/*
int optimised_backtracking(sudoku_t* psudoku, int nbempty) {
int i, j, k, m;
int l = 0;
int choice[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
int** tab_of_constraints = malloc(9 * sizeof(int*)); // changed sizeof(char*) to sizeof(int*)
for (i = 0; i < 9; i++) {
tab_of_constraints[i] = malloc(9 * sizeof(int)); // changed sizeof(char) to sizeof(int)
}
if (nbempty == 0) {
for (i = 0; i < 9; i++) {
free(tab_of_constraints[i]);
}
free(tab_of_constraints);
return 1;
}
for (i = 0; i < 9; i++) {
for (j = 0; j < 9; j++) {
set_possibilities(psudoku, i, j);
tab_of_constraints[i][j] = count_constraints(psudoku, i, j); // changed count_contraints to count_constraints
}
}

max_index(tab_of_constraints, 9, 9, &i, &j);
m = tab_of_constraints[i][j];
tab_of_constraints[i][j] = 9;
for (k = 0; k < 9; k++) {
if ((psudoku->cells[i][j].possibilities)[k] == 1) {
choice[l] = k + 1;
l = l + 1;
}
}
if (m == 9) {
for (i = 0; i < 9; i++) {
free(tab_of_constraints[i]);
}
free(tab_of_constraints);
return 1;
}
for (k = 0; k <= m-1; k++) {
psudoku->cells[i][j].number = choice[k];
if (is_valid_sudoku(*psudoku)) {
if (optimised_backtracking(psudoku, nbempty - 1)) {
for (i = 0; i < 9; i++) {
free(tab_of_constraints[i]);
}
free(tab_of_constraints);
return 1;
}
psudoku->cells[i][j].number = EMPTY;
}
}
for (i = 0; i < 9; i++) {
free(tab_of_constraints[i]);
}
free(tab_of_constraints);
return 0;
}
*/
