EXEC = hill_climbing_main

CC = gcc

CFLAGS = -Wall -Wextra -O2

all: $(EXEC)

$(EXEC): hill_climbing_main.c
	$(CC) $(CFLAGS) hill_climbing_main.c -o $(EXEC)

clean:
	rm -f $(EXEC)
	
.PHONY: clean
