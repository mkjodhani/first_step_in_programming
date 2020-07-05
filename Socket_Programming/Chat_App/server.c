#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc ,char *argv[])
{
    if (argc < 2)
    {
        fprintf(stderr,"port_number is not provided.Program terminated\n");
    }

    int sockfd,newsockfd,portNo,n;
    char buffer[256];

    struct sockaddr_in server_address, client_address;
    socklen_t client_length;

    sockfd=socket(AF_INET,SOCK_STREAM,0);

    if(sockfd<0)
    {
        error("Error opening Socket");
    }
    portNo=atoi(argv[1]);

    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(portNo);

    if(bind(sockfd,(struct sockaddr *)&server_address,sizeof(server_address))<0)
    {
        error("Binding Complete!");
    }

    listen(sockfd,5);
    client_length = sizeof(client_address);

    newsockfd = accept(sockfd ,(struct sockaddr *)&client_address,&client_length);

    if (newsockfd < 0)
    {
        error("Error on Accept");
    }
    while(1)
    {
        char client_buffer[256];
        n=read(newsockfd,buffer,sizeof(buffer));
        if(n<0)
        {
            error("Error on Reading");
        }
        printf("Client: %s\n",buffer);
        char server_buffer[256];
        fgets(server_buffer,256,stdin);

        n = write(newsockfd,server_buffer,strlen(server_buffer));
        if(n<0)
        {
            error("Error on Writing");
        }
        int i=strncmp(server_buffer,"Bye",3);
        if(i==0)
        break;
    }
    close(newsockfd);
    close(sockfd);
    return 0;
}
