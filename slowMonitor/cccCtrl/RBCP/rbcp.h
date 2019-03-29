/*************************************************
 *                                                *
 * SiTCP Remote Bus Control Protocol              *
 * Header file                                    *
 *                                                *
 * 2017/01/24 Naruhiro Chikuma                    *
 *                                                *
 *************************************************/

struct rbcp_header{
  unsigned char type;
  unsigned char command;
  unsigned char id;
  unsigned char length;
  unsigned int address;
};


