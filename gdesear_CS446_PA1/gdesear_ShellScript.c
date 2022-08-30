// Misha Desear
// CS 446 PA 1
// Shell replica in C

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>
#include <stdbool.h>

#define MAX_VALUE 1024

void promptUser(bool isBatch);
void printHelp(char *tokens[], int numTokens);
void printError();
int parseInput(char *input, char *splitWords[]);
char *redirectCommand(char *special, char *line, bool *isRedirect, char *tokens[], char *outputTokens[]);
char *executeCommand(char *cmd, bool *isRedirect, char* tokens[], char* outputTokens[], bool *isExits);
bool exitProgram(char *tokens[], int numTokens);
void launchProcesses(char *tokens[], int numTokens, bool isDirect);
void changeDirectories(char *tokens[], int numTokens);

int main(int argc, char const *argv[]) 
{
	setlinebuf(stdout);
	bool isBatch = NULL, isRedirect = false, isExits = false;
	FILE *input = NULL, *output = NULL, *redirect = NULL;
	char line[MAX_VALUE] = "", *tokens[MAX_VALUE], *outputTokens[MAX_VALUE], *temp, *outputFile;
	int numTokens = 0, i = 0;
	
	if (argc > 2) {
		printError();
		return 1;
	} else if (argc == 2) {
		if ((input = fopen(argv[1], "r")) == NULL) {
			printError(); 
			return 1;
		}	
		isBatch = true; 
	} else {
		isBatch = false;
		input = stdin; 
	} 
	
	promptUser(isBatch);
	fgets(line, MAX_VALUE, input); 
	do {
		if(isBatch) {
			printf("%s\n", line);
		}
		temp = strdup(line);
		parseInput(temp, tokens);
		outputFile = executeCommand(line, &isRedirect, tokens, outputTokens, &isExits);
		if (isRedirect) {
			output = fopen(outputFile, "w");
			redirect = fopen(outputTokens[0], "r");
			while(fgets(temp, MAX_VALUE, redirect)) {
				fprintf(output, "%s", temp);
			}
			fclose(output);
			fclose(redirect);
			isRedirect = false;
		}
		
		if (!isExits) {
			promptUser(isBatch);
			if (fgets(line, MAX_VALUE, input) == NULL) {
				isExits = true;
			}	
		}
	} while (!isExits);

	printf("Exiting...\n");
	kill(getpid(), SIGTERM);
	
	return 0;
}

void promptUser(bool isBatch)
{
	char* userPtr = getenv("USER"); 
	char hostname[MAX_VALUE];
	hostname[MAX_VALUE - 1] = '\0';
	char cwd[MAX_VALUE];
	cwd[MAX_VALUE - 1] = '\0';
	
	gethostname(hostname, sizeof(hostname));
	getcwd(cwd, sizeof(cwd));
	
	if (isBatch == 0) {
		printf("%s@%s:%s$ ", userPtr, hostname, cwd);
	}
}

void printHelp(char *tokens[], int numTokens) 
{
	if (strcmp(tokens[0], "help") == 0) {
		if (numTokens > 1) {
			printError();
			return;
		}
		printf("These commands are defined internally.\nhelp -prints this screen so you can see available shell commands\ncd - changes directories to specified path; if not given, defaults to home\nexit -closes the shell.\n[input] > [output] -pipes input file into output file\n\n"); 
	}
}

void printError()
{
	fprintf(stderr, "Shell Program Error Encountered\n");
}

int parseInput(char *input, char *splitWords[])
{
	int wordInd = 0;
	splitWords[0] = strtok(input, " \n\r");
	while(splitWords[wordInd] != NULL) {
		splitWords[++wordInd] = strtok(NULL, " \n\r");
	}
	
	return wordInd;
}

char *redirectCommand(char *special, char *line, bool *isRedirect, char *tokens[], char *outputTokens[])
{
	int counter = 0;
	char *bracketCheck = strchr(line, '>');
	while (bracketCheck != NULL) {
		counter++;
		bracketCheck = strchr(bracketCheck + 1, '>'); 
	}

	if (counter > 1) {
		printError();
		return "";
	}
	
	outputTokens[0] = strtok(line, " >\n");
	outputTokens[1] = strtok(NULL, " >\n");

	*isRedirect = true;
	return outputTokens[1];
}

char *executeCommand(char *cmd, bool *isRedirect, char* tokens[], char* outputTokens[], bool *isExits)
{
	char *copy = strdup(cmd), *output = "", *redirect = NULL;
	int numTokens;
	
	strcat(copy, "\n");
	redirect = strchr(copy, '>');
	
	if (redirect != NULL) {
		output = redirectCommand(copy, copy, isRedirect, tokens, outputTokens);
		return output;
	}
	
	numTokens = parseInput(copy, tokens);
	if (numTokens == 0) {
		return output;
	}
	
	*isExits = exitProgram(tokens, numTokens);
	if (*isExits) {
		return output;
	}
	
	changeDirectories(tokens, numTokens);
	printHelp(tokens, numTokens);
	launchProcesses(tokens, numTokens, isRedirect);
	return output;
}


bool exitProgram(char *tokens[], int numTokens)
{
	if (strcmp(tokens[0], "exit") != 0) {
		return false;
	} else if (numTokens > 1) {
		printError();
		return false;
	}
	return true;
}

void launchProcesses(char *tokens[], int numTokens, bool isDirect)
{
	pid_t pid;
	int status;
	
	if (strcmp(tokens[0], "help") != 0 && strcmp(tokens[0], "exit") != 0 && strcmp(tokens[0], "cd") != 0) {
		int status;
		pid = fork();
		if (pid == 0) {
			if (execvp(tokens[0], tokens) == -1) {
				printError();
				kill(getpid(), SIGTERM); 
			}
		}
		wait(&status);
	}
}

void changeDirectories(char *tokens[], int numTokens)
{
	if (strcmp(tokens[0], "cd") == 0) {
		if (numTokens > 2 || numTokens == 1) {
			printError();
			return;
		}
		if (chdir(tokens[1]) == -1) {
			printError();
		}
	}	 
}

