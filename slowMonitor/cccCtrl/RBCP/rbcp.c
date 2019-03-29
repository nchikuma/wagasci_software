#define MAX_LINE_LENGTH 1024
#define MAX_PARAM_LENGTH 20
#define RBCP_VER 0xFF
#define RBCP_CMD_WR 0x80
#define RBCP_CMD_RD 0xC0
#define DEFAULT_IP "192.168.10.16"
#define DEFAULT_PORT 4660
#define UDP_BUF_SIZE 2048

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/fcntl.h>
#include <netdb.h>
#include <unistd.h>
#include <ctype.h>
#include <getopt.h>

#include "rbcp.h"
#include "rbcp_com.c"
#include "myAtoi.c"
#include "myScanf.c"
#include "DispatchCommand.c"

int myGetArg(char* inBuf, int i, char* argBuf);
int myScanf(char* inBuf, char* argBuf1, char* argBuf2,  char* argBuf3);
int rbcp_com(char* ipAddr,
    unsigned int port,
    struct rbcp_header* sndHeader,
    char* sndData,
    char* readData,
    char dispMode
    );
int DispatchCommand(char* pszVerb,
    char* pszArg1,
    char* pszArg2,
    char* ipAddr,
    unsigned int rbcpPort,
    struct rbcp_header* sndHeader,
    char dispMode
    );

static void printUsage();

struct option options[] = {
  {"help"        , no_argument, NULL, 'h'},
  {"interactive" , no_argument, NULL, 'i'},
  {"write"       , no_argument, NULL, 'w'},
  {"read"        , no_argument, NULL, 'r'},
  {"long"        , no_argument, NULL, 'l'},
  {"addr"        , required_argument, NULL, 'a'},
  {"data"        , required_argument, NULL, 'd'},
  {0, 0, 0, 0}
};

int main(int argc, char* argv[]){

  char* sitcpIpAddr;
  unsigned int sitcpPort;

  struct rbcp_header sndHeader;

  char tempKeyBuf[MAX_LINE_LENGTH];
  char szVerb[MAX_PARAM_LENGTH];
  char szArg1[MAX_PARAM_LENGTH];
  char szArg2[MAX_PARAM_LENGTH];
  int rtnValue;

  FILE *fin;

  char comRBCP[10];
  int  addrRBCP = -1;
  int  dataRBCP = -1;
  int  long_mode = 0;
  int  inter_mode = -1;

  while(1){
    int index = 0;
    int result=getopt_long(argc,argv,"hiwrla:d:",options,&index);
    if(result==-1) break;
    switch(result){
      case 'h': printUsage();
      case 'i': inter_mode = 1; 
                break;
      case 'w': strcpy(comRBCP,"write"); inter_mode = 0; 
                break;
      case 'r': strcpy(comRBCP,"read"); inter_mode = 0; 
                break;
      case 'l': long_mode = 1; 
                break;
      case 'a': addrRBCP = atoi(optarg); 
                break;
      case 'd': dataRBCP = atoi(optarg); 
                break;
      default : printUsage();
    }
  }

  if(inter_mode==0){
    if(strcmp(comRBCP,"write")==0){ 
      if(addrRBCP==-1||dataRBCP==-1) printUsage();
    }else if(strcmp(comRBCP,"read")==0){
      if(addrRBCP==-1) printUsage();
    }else printUsage();
  }

  sitcpIpAddr = DEFAULT_IP;
  sitcpPort   = DEFAULT_PORT;

  //printf("sitcpIpAddr : %s\n",sitcpIpAddr);
  //printf("sitcpPort   : %d\n",sitcpPort);

  sndHeader.type=RBCP_VER;
  sndHeader.id=0;

  if(inter_mode==1){
    while(1){
      printf("SiTCP-RBCP$ ");
      fgets(tempKeyBuf, MAX_LINE_LENGTH, stdin);
      if((rtnValue=myScanf(tempKeyBuf,szVerb, szArg1, szArg2))<0){
        printf("ERROR: myScanf(): %i\n",rtnValue);
        return -1;
      }

      if(strcmp(szVerb, "load") == 0){
        if((fin = fopen(szArg1,"r"))==NULL){
          printf("ERROR: Cannot open %s\n",szArg1);
          break;
        }
        while(fgets(tempKeyBuf, MAX_LINE_LENGTH, fin)!=NULL){
          if((rtnValue=myScanf(tempKeyBuf,szVerb, szArg1, szArg2))<0){
            printf("ERROR: myScanf(): %i\n",rtnValue);
            return -1;
          }

          sndHeader.id++;

          if(DispatchCommand(szVerb,szArg1,szArg2,
                sitcpIpAddr,sitcpPort,&sndHeader,1)<0) 
            exit(EXIT_FAILURE);
        }

        fclose(fin);
      }
      else{

        sndHeader.id++;

        if(DispatchCommand(szVerb,szArg1,szArg2,
              sitcpIpAddr,sitcpPort,&sndHeader,1)<0)
          break;
      }
    }
  }
  else if(inter_mode==0){
    if(strcmp(comRBCP,"write")==0){
      if(!long_mode) strcpy(szVerb,"wrb");
      else           strcpy(szVerb,"wrs");
      sprintf(szArg1,"%d",addrRBCP);
      sprintf(szArg2,"%d",dataRBCP);
      if(DispatchCommand(szVerb,szArg1,szArg2,
            sitcpIpAddr,sitcpPort,&sndHeader,1)<0)
        exit(EXIT_FAILURE);
    }
    else if(strcmp(comRBCP,"read")==0){
      strcpy(szVerb,"rd");
      sprintf(szArg1,"%d",addrRBCP);
      sprintf(szArg2,"%d",1);
      if(DispatchCommand(szVerb,szArg1,szArg2,
            sitcpIpAddr,sitcpPort,&sndHeader,1)<0)
        exit(EXIT_FAILURE);
      if(long_mode){
        strcpy(szVerb,"rd");
        sprintf(szArg1,"%d",addrRBCP+1);
        sprintf(szArg2,"%d",1);
        if(DispatchCommand(szVerb,szArg1,szArg2,
              sitcpIpAddr,sitcpPort,&sndHeader,1)<0)
          exit(EXIT_FAILURE);
      }
    }
    else{
      puts("ERROR: unexpected mode.");
      exit(EXIT_FAILURE);
    }
  }
  else printUsage();

  return 0;
}



static void printUsage(){
  puts("-------------------------------------------------------------------");
  puts("Usage : ");
  puts("\tInteractive mode : ./rbcp -i");
  puts("\tWrite mode : ./rbcp -w  -a <32-bit address> -d <8-bit data>");
  puts("\t             ./rbcp -wl -a <32-bit address> -d <16-bit data>");
  puts("\tRead  mode : ./rbcp -r  -a <32-bit address>");
  puts("\t             ./rbcp -rl -a <32-bit address>");
  puts("-------------------------------------------------------------------");
  puts("\t-h[--help]       : Display this help.");
  puts("\t-i[--interactive]: Run in interactive mode.");
  puts("\t-w[--write]      : Run in write mode.");
  puts("\t-r[--read]       : Run in read mode.");
  puts("\t-l[--long]       : Write/Read 16-bit data.");
  puts("\t-a[--addr]       : Register address.");
  puts("\t-d[--data]       : Data sent to the register.");
  puts("-------------------------------------------------------------------");
  puts("\tC_SPILLMODE_W_ADDR := X'00000001' (1) ");
  puts("\t\t mode: 0 -> External spill, 1 -> Internal spill");
  puts("\t\t       2 -> Beam trigger  , 3 -> Beam trigger + Internal spill");
  puts("\tC_SPILLMODE_R_ADDR := X'00000010' (16) ");
  puts("\t\t Read spill mode.");
  puts("\tC_SPILLGEN_W_ADDR  := X'00000100' (256) ");
  puts("\t\t sub_addr: 0 -> Period of internal spill (bit 15 to 8).");
  puts("\t\t           1 -> Period of internal spill (bit 7 to 0).");
  puts("\t\t           2 -> Active time of internal spill (bit 15 to 8).");
  puts("\t\t           3 -> Active time of internal spill (bit 7 to 0).");
  puts("\t\t time : 5us x input number.");
  puts("\tC_BUNCHGEN_W_ADDR  := X'00000100' (272) ");
  puts("\t\t sub_addr: 0 -> Period of internal spill (bit 15 to 8).");
  puts("\t\t           1 -> Period of internal spill (bit 7 to 0).");
  puts("\t\t           2 -> Active time of internal spill (bit 7 to 0).");
  puts("\t\t           3 -> Delay after spill leading edge (bit 15 to 8).");
  puts("\t\t           4 -> Delay after spill leading edge (bit 7 to 0).");
  puts("\t\t           5 -> Number of bunches (bit 7 to 0).");
  puts("\t\t time : 8ns x input number.");
  puts("\tC_SPILLGEN_R_ADDR  := X'00001000' (4096) ");
  puts("\t\t Read internal spill info.");
  puts("\t\t sub_addr: 0 to 3");
  puts("\tC_SPILLGEN_R_ADDR  := X'00001000' (4112) ");
  puts("\t\t Read internal bunch info.");
  puts("\t\t sub_addr: 0 to 5");
  puts("\tC_RBCP_TEST_R_ADDR := X'00FF000F' (4294901775) ");
  puts("\t\t Control 4 LEDs (pin 6-9)");
  puts("\tC_RBCP_TEST_W_ADDR := X'00FF00FF' (4294902015) ");
  puts("\t\t Read status of RBCP test.");
  puts("\t\t\t*max addr is 0x0FFFFFFF");
  puts("-------------------------------------------------------------------");

  exit(0);
}
