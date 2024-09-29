#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <getopt.h>
#include <pthread.h>

#define SIZE 9
#define NUM_THREADS 8
#define MAX_ITER 200

typedef struct {
    int grid[SIZE][SIZE];
    int thread_id;
} ThreadData;

int initialGrid[SIZE][SIZE];
int shuffle = 1;

int solutionThreadId = 0;
int solution_found = 0;


void initializeRandomSeed() {
    srand(time(NULL) ^ getpid());
}

int loadGrid(const char *src, int matrix[SIZE][SIZE]) {
    FILE *f = fopen(src, "r+");
    if (!f) {
        return 1;
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
    return 0;
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

int countFixed(int rowIndex) {
    int count = 0;
    for (int i = 0; i < SIZE; i++) {
        if (isFixed(i, rowIndex)) {
            count++;
        }
    }
    return count;
}

void getNeighbor(int grid[SIZE][SIZE], int result[SIZE][SIZE]) {
    int row, x1, x2;;
    
    do {
        row = rand() % SIZE;
        x1 = rand() % SIZE;
        x2 = rand() % SIZE;
    } while (isFixed(x1, row) || isFixed(x2, row) || x1==x2);
    
    memcpy(result, grid, sizeof(int)*SIZE*SIZE);
    swap(result, x1, row, x2, row);
}

int HillClimb(int grid[SIZE][SIZE]) {
    int currentGrid[SIZE][SIZE];
    int newGrid[SIZE][SIZE];
    int currentHeuristic, newHeuristic;

    while (!solution_found) {

        int i = 0;
        fillInitialGrid(grid);
        memcpy(currentGrid, grid, sizeof(currentGrid));
        currentHeuristic = heuristic(currentGrid);

        while (i < MAX_ITER) {
            getNeighbor(currentGrid, newGrid);
            newHeuristic = heuristic(newGrid);

            if (newHeuristic == 0) {
                memcpy(grid, newGrid, sizeof(newGrid));
                solution_found = 1;
                return 1;
            }

            if (newHeuristic < currentHeuristic) {
                i=0;
                memcpy(currentGrid, newGrid, sizeof(newGrid));
                currentHeuristic = newHeuristic;
            }else{
                i++;
            }
        }
    }

    return 0;
}

void* thread(void* arg) {
    ThreadData* data = (ThreadData*)arg;

    if(HillClimb(data->grid)){
        solutionThreadId = data->thread_id;
    }

    return NULL;
}

int main(int argc, char *argv[]) {
    pthread_t threads[NUM_THREADS];
    ThreadData threadData[NUM_THREADS];

    if(argc == 1){
        printf("Usage: %s [file]\n", argv[0]);
        return 1;
    }

    initializeRandomSeed();
    
    printf("Loading grid from file '%s' ...\n", argv[1]);

    if(loadGrid(argv[1], initialGrid)){
        printf("File does not exists.\n");
        return 1;
    };
    int result[SIZE][SIZE];


    time_t first_time;
    time(&first_time);

    printf("Running Hill Climbing algorithm on %d threads...\n", NUM_THREADS);

    //Multithreading managment
    for (int i = 0; i < NUM_THREADS; i++) {
        memcpy(threadData[i].grid, initialGrid, sizeof(initialGrid));
        threadData[i].thread_id = i;

        pthread_create(&threads[i], NULL, thread, &threadData[i]);
    }
    for (int i = 0; i < NUM_THREADS; i++) pthread_join(threads[i], NULL);
    

    memcpy(result, threadData[solutionThreadId].grid, sizeof(result));


    time_t new_time;
    time(&new_time);


    //Print results
    printf("Found a solution :\n");
    printGrid(result);
    printf("Execution time: %d seconds.\n", (int)(new_time - first_time));

    return 0;
}