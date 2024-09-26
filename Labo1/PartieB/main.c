#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define GRID_SIZE 9

int loadGrid(const char *src, int grid[GRID_SIZE][GRID_SIZE]) {
    FILE *f = fopen(src, "r");
    if (f == NULL) {
        perror("Error opening file");
        return 1;
    }

    char line[GRID_SIZE + 1];
    int row = 0;
    while (fgets(line, GRID_SIZE + 1, f) != NULL) {
        if (line[0] == '\n') {
            break;
        }

        for (int col = 0; col < GRID_SIZE; col++) {
            grid[row][col] = (line[col] == '.') ? 0 : (line[col] - '0');
        }

        row++;
    }

    fclose(f);
    return 0;
}

int heuristic(int grid[GRID_SIZE][GRID_SIZE]) {
    int conflicts = 0;

    // Column conflicts
    for (int j = 0; j < GRID_SIZE; j++) {
        int counts[10] = {0};
        for (int i = 0; i < GRID_SIZE; i++) {
            counts[grid[i][j]]++;
        }
        for (int i = 1; i <= GRID_SIZE; i++) {
            conflicts += counts[i] - 1;
        }
    }

    // Square 3x3 conflicts
    for (int x = 0; x < GRID_SIZE; x += 3) {
        for (int y = 0; y < GRID_SIZE; y += 3) {
            int counts[10] = {0};
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    counts[grid[x + i][y + j]]++;
                }
            }
            for (int i = 1; i <= GRID_SIZE; i++) {
                conflicts += counts[i] - 1;
            }
        }
    }

    return -conflicts;
}

void fillInitialGrid(int grid[GRID_SIZE][GRID_SIZE], int initialGrid[GRID_SIZE][GRID_SIZE]) {
    for (int row = 0; row < GRID_SIZE; row++) {
        int availableNumbers[GRID_SIZE] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
        int numAvailable = GRID_SIZE;

        for (int col = 0; col < GRID_SIZE; col++) {
            if (initialGrid[row][col] != 0) {
                availableNumbers[initialGrid[row][col] - 1] = 0;
                numAvailable--;
            }
        }

        for (int col = 0; col < GRID_SIZE; col++) {
            if (initialGrid[row][col] == 0) {
                int index = rand() % numAvailable;
                int num = availableNumbers[index];
                grid[row][col] = num;
                availableNumbers[index] = 0;
                numAvailable--;
            }
        }
    }
}

void printGrid(int grid[GRID_SIZE][GRID_SIZE]) {
    for (int i = 0; i < GRID_SIZE; i++) {
        for (int j = 0; j < GRID_SIZE; j++) {
            printf("%d ", grid[i][j]);
        }
        printf("\n");
    }
}

int isFixed(int x, int y, int initialGrid[GRID_SIZE][GRID_SIZE]) {
    return initialGrid[y][x] != 0;
}

void swap(int grid[GRID_SIZE][GRID_SIZE], int x1, int y1, int x2, int y2) {
    int tmp = grid[y2][x2];
    grid[y2][x2] = grid[y1][x1];
    grid[y1][x1] = tmp;
}

int getNeighbor(int grid[GRID_SIZE][GRID_SIZE], int initialGrid[GRID_SIZE][GRID_SIZE]) {
    int tmp[GRID_SIZE][GRID_SIZE];
    memcpy(tmp, grid, sizeof(tmp));

    int row = rand() % GRID_SIZE;
    int bestx1 = -1, bestx2 = -1;
    int bestHeuristic = INT_MAX;

    for (int x1 = 0; x1 < GRID_SIZE; x1++) {
        for (int x2 = x1 + 1; x2 < GRID_SIZE; x2++) {
            if (isFixed(x1, row, initialGrid) || isFixed(x2, row, initialGrid)) {
                continue;
            }

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

    swap(grid, bestx1, row, bestx2, row);

    return bestHeuristic;
}

int hillClimb(int grid[GRID_SIZE][GRID_SIZE], int initialGrid[GRID_SIZE][GRID_SIZE]) {
    const int maxIter = 150;

    while (1) {
        fillInitialGrid(grid, initialGrid);
        int currentHeuristic = heuristic(grid);

        for (int i = 0; i < maxIter; i++) {
            int newHeuristic = getNeighbor(grid, initialGrid);

            if (newHeuristic == 0) {
                return 0;
            }

            if (newHeuristic < currentHeuristic) {
                currentHeuristic = newHeuristic;
            }
        }
    }

    return 1; // No solution found
}

int main() {
    int grid[GRID_SIZE][GRID_SIZE];
    int initialGrid[GRID_SIZE][GRID_SIZE];

    if (loadGrid("./input/input10.txt", initialGrid)) {
        return 1;
    }

    clock_t start = clock();
    if (hillClimb(grid, initialGrid)) {
        printf("No solution found\n");
    } else {
        printGrid(grid);
    }
    double executionTime = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("Execution time: %.3f seconds\n", executionTime);

    return 0;
}