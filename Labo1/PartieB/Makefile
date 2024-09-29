EXEC = main_version

CC = gcc

CFLAGS = -Wall -Wextra -O2

all: $(EXEC)

$(EXEC): main_version.c
	$(CC) $(CFLAGS) main_version.c -o $(EXEC)

clean:
	rm -f $(EXEC)
	
.PHONY: clean
