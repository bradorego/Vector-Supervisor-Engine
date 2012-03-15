#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <time.h>
#include <string.h>

char *DIRECTIONS[] = {"N", "NE", "E", "SE", "S", "SW", "W", "NW"};
char *MAGNITUDES[] = {"0", "1", "2", "3"};

void error(char *msg) {
	fprintf(stderr, "%s\n", msg);
	exit(0);
}

void writeline(int sock, char* line) {
	char *out = (char*)malloc(sizeof(line) + 2);
	sprintf(out, "%s\r\n", line);
	printf("]] %s",out);
	int n = write(sock, out, strlen(out));
	if (n < 0)
		error("Error writing to socket");
}

void send_direction(sock) {
	int r = rand() % 8;
	char line[15];
	sprintf(line, "DIRECTION: %s", DIRECTIONS[r]);
	writeline(sock, line);
}

void send_magnitude(sock) {
	int r = rand() % 4;
	char line[15];
	sprintf(line, "MAGNITUDE: %s", MAGNITUDES[r]);
	writeline(sock, line);
}

void readline(int sock, char* buff, char* line) {
	bzero(line, 512);
	char *p = strchr(buff, '\r');
	char *t;
	int n;
	int len = strlen(buff);
	while (p == NULL && len < 511) {
		t = buff + strlen(buff);
		n = read(sock, t, buff+511-t);
		if (n < 0) error("Error reading from socket");
		//printf("    buff: \"%s\"", buff);
		len = strlen(buff);
		p = strchr(buff, '\r');	
	}
	strncpy(line, buff, p-buff);
	char b[512];
	bzero(b, 512);
	strcpy(b, p+2);
	bzero(buff, 512);
	strcpy(buff, b);
	printf(">> %s\n", line);
}

int main(int argc, char* argv[]) {
	if (argc < 4) {
		printf("Usage: %s <host> <port> <player name>\n", argv[0]);
		return 1;
	}
	
	int port = atoi(argv[2]);

	// declare socket variables
	int sock, n;
	struct sockaddr_in serv_addr;
	struct hostent *server;

	char buffer[512];

	// initialize socket variables
	sock = socket(AF_INET, SOCK_STREAM, 0);
	if (sock < 0)
		error("Error opening socket");
	server = gethostbyname(argv[1]);
	if (server == NULL)
		error("Error: no such host");
	bzero((char *) &serv_addr, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
	serv_addr.sin_port = htons(port);
	
	if (connect(sock, &serv_addr, sizeof(serv_addr)) < 0)
		error("Error connecting");

	// zero the buffer
	bzero(buffer, 512);
	char line[512];
	bzero(buffer, 512);
	while (strcmp("IDENTIFY?", line) != 0)
		readline(sock, buffer, line);
	writeline(sock, argv[3]);
	
	while (1) {
		readline(sock, buffer, line);
		
		if (strcmp(line, "DIRECTION?") == 0) {
			send_direction(sock);
		} else if (strcmp(line, "MAGNITUDE?") == 0) {
			send_magnitude(sock);
		} else if (strcmp(line, "TOURNAMENT OVER") == 0) {
			break;
		}
	}

	close(sock);
	return 0;
}
