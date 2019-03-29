int OnHelp();

int DispatchCommand(char* pszVerb,
    char* pszArg1,
    char* pszArg2,
    char* ipAddr,
    unsigned int rbcpPort,
    struct rbcp_header* sndHeader,
    char dispMode
    ){
  char recvData[UDP_BUF_SIZE];

  unsigned int tempInt;

  if(strcmp(pszVerb, "wrb") == 0){
    tempInt = myAtoi(pszArg2);    
    pszArg2[0]= (char)(0xFF & tempInt);

    sndHeader->command= RBCP_CMD_WR;
    sndHeader->length=1;
    sndHeader->address=htonl(myAtoi(pszArg1));

    return rbcp_com(ipAddr, rbcpPort, sndHeader, pszArg2,recvData,dispMode);
  }
  else if(strcmp(pszVerb, "wrs") == 0){
    tempInt = myAtoi(pszArg2);    
    pszArg2[1]= (char)(0xFF & tempInt);
    pszArg2[0]= (char)((0xFF00 & tempInt)>>8);

    sndHeader->command= RBCP_CMD_WR;
    sndHeader->length=2;
    sndHeader->address=htonl(myAtoi(pszArg1));

    return rbcp_com(ipAddr, rbcpPort, sndHeader, pszArg2,recvData,dispMode);
  }
  else if(strcmp(pszVerb, "wrw") == 0){
    tempInt = myAtoi(pszArg2);

    pszArg2[3]= (char)(0xFF & tempInt);
    pszArg2[2]= (char)((0xFF00 & tempInt)>>8);
    pszArg2[1]= (char)((0xFF0000 & tempInt)>>16);
    pszArg2[0]= (char)((0xFF000000 & tempInt)>>24);

    sndHeader->command= RBCP_CMD_WR;
    sndHeader->length=4;
    sndHeader->address=htonl(myAtoi(pszArg1));

    return rbcp_com(ipAddr, rbcpPort, sndHeader, pszArg2,recvData,dispMode);
  }
  else if(strcmp(pszVerb, "rd") == 0){
    sndHeader->command= RBCP_CMD_RD;
    sndHeader->length=myAtoi(pszArg2);
    sndHeader->address=htonl(myAtoi(pszArg1));

    return rbcp_com(ipAddr, rbcpPort, sndHeader, pszArg2,recvData,dispMode);
  }
  else if(strcmp(pszVerb, "help") == 0){
    return OnHelp();
  }
  else if(strcmp(pszVerb, "quit") == 0){
    return -1;
  }
  puts("No such command!\n");
  return 0;

};

int OnHelp()
{
  puts("\nCommand list:");
  puts("   wrb [address] [byte_data] : Write byte");
  puts("   wrs [address] [short_data]: Write short(16bit)");
  puts("   wrw [address] [word_data] : Write word(32bit)");
  puts("   rd [address] [length]     : Read data");
  puts("   load [file name]          : Execute a script");
  puts("   quit                      : quit from this program\n");

  return 0;
}
