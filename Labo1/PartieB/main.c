#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <getopt.h>

#define SIZE 9

void initializeRandomSeed() {
    srand(time(NULL) ^ getpid());
}

int initialGrid[SIZE][SIZE];
int shuffle = 1;

void loadGrid(const char *src, int matrix[SIZE][SIZE]) {
    FILE *f = fopen(src, "r");
    if (f == NULL) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }

    char line[SIZE + 2];
    int i = 0;
    while (fgets(line, sizeof(line), f)) {
        if (line[0] == '\n') break;
        for (int j = 0; j < SIZE; j++) {
            matrix[i][j] = (line[j] == '.') ? 0 : line[j] - '0';
        }
        i++;
    }

    fclose(f);
}

int heuristic(int grid[SIZE][SIZE]) {
    int conflicts = 0;

    for (int j = 0; j < SIZE; j++) {
        int col[SIZE] = {0};
        for (int i = 0; i < SIZE; i++) {
            col[i] = grid[i][j];
        }
        int unique_count = 0;
        for (int i = 0; i < SIZE; i++) {
            for (int k = i + 1; k < SIZE; k++) {
                if (col[i] == col[k] && col[i] != 0) {
                    unique_count++;
                }
            }
        }
        conflicts += unique_count;
    }

    for (int x = 0; x < SIZE; x += 3) {
        for (int y = 0; y < SIZE; y += 3) {
            int sub_grid[SIZE] = {0};
            int index = 0;
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    sub_grid[index++] = grid[x + i][y + j];
                }
            }
            int unique_count = 0;
            for (int i = 0; i < SIZE; i++) {
                for (int k = i + 1; k < SIZE; k++) {
                    if (sub_grid[i] == sub_grid[k] && sub_grid[i] != 0) {
                        unique_count++;
                    }
                }
            }
            conflicts += unique_count;
        }
    }

    return conflicts;
}

void fillInitialGrid(int grid[SIZE][SIZE]) {
    int tempGrid[SIZE][SIZE];
    memcpy(tempGrid, grid, sizeof(tempGrid));

    for (int row = 0; row < SIZE; row++) {
        int availableNumbers[SIZE];
        for (int i = 0; i < SIZE; i++) {
            availableNumbers[i] = i + 1;
        }

        if (shuffle) {
            for (int i = SIZE - 1; i > 0; i--) {
                int j = rand() % (i + 1);
                int temp = availableNumbers[i];
                availableNumbers[i] = availableNumbers[j];
                availableNumbers[j] = temp;
            }
        }

        for (int col = 0; col < SIZE; col++) {
            if (tempGrid[row][col] != 0) {
                for (int i = 0; i < SIZE; i++) {
                    if (availableNumbers[i] == tempGrid[row][col]) {
                        availableNumbers[i] = 0;
                        break;
                    }
                }
            }
        }

        int index = 0;
        for (int col = 0; col < SIZE; col++) {
            if (tempGrid[row][col] == 0) {
                while (availableNumbers[index] == 0) {
                    index++;
                }
                tempGrid[row][col] = availableNumbers[index];
                index++;
            }
        }
    }

    memcpy(grid, tempGrid, sizeof(tempGrid));
}

void printGrid(int grid[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf("%d ", grid[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

int isFixed(int x, int y) {
    return initialGrid[y][x] != 0;
}

void swap(int grid[SIZE][SIZE], int x1, int y1, int x2, int y2) {
    int tmp = grid[y2][x2];
    grid[y2][x2] = grid[y1][x1];
    grid[y1][x1] = tmp;
}

void getNeighbor(int grid[SIZE][SIZE], int result[SIZE][SIZE]) {
    int tmp[SIZE][SIZE];
    memcpy(tmp, grid, sizeof(tmp));

    int row = rand() % SIZE;
    int bestx1 = -1, bestx2 = -1;
    int bestHeuristic = 999;

    for (int x1 = 0; x1 < SIZE; x1++) {
        for (int x2 = x1; x2 < SIZE; x2++) {
            if (isFixed(x1, row) || isFixed(x2, row)) continue;

            swap(tmp, x1, row, x2, row);
            int newHeuristic = heuristic(tmp);
            swap(tmp, x1, row, x2, row);

            if (newHeuristic < bestHeuristic) {
                bestHeuristic = newHeuristic;
                bestx1 = x1;
                bestx2 = x2;
            }
        }
    }

    swap(tmp, bestx1, row, bestx2, row);
    memcpy(result, tmp, sizeof(tmp));
}

void HillClimb(int grid[SIZE][SIZE], int max_iter) {
    int currentGrid[SIZE][SIZE];
    int newGrid[SIZE][SIZE];
    int currentHeuristic, newHeuristic;

    while (1) {
        int i = 0;
        fillInitialGrid(grid);
        memcpy(currentGrid, grid, sizeof(currentGrid));
        currentHeuristic = heuristic(currentGrid);

        while (i < max_iter) {
            getNeighbor(currentGrid, newGrid);
            newHeuristic = heuristic(newGrid);

            if (newHeuristic == 0) {
                memcpy(grid, newGrid, sizeof(newGrid));
                return;
            }

            if (newHeuristic < currentHeuristic) {
                memcpy(currentGrid, newGrid, sizeof(newGrid));
                currentHeuristic = newHeuristic;
                //printf("Iteration: %d, Heuristic: %d\n", i, currentHeuristic);
            }

            i++;
        }
    }
}

int main(int argc, char *argv[]) {
    int opt;
    int max_iter = 250;

    initializeRandomSeed();

    loadGrid("./input/input10.txt", initialGrid);
    int result[SIZE][SIZE];
    memcpy(result, initialGrid, sizeof(result));

    clock_t start = clock();
    HillClimb(result, max_iter);
    clock_t end = clock();

    printGrid(result);
    printf("Execution time: %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);

    return 0;
}