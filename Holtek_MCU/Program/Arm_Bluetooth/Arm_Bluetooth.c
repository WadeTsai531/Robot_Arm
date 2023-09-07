#include "HT66F2390.h"

#define Mode 'T' // Switch UART Mode ( 'T' / 'R' )
#define FH 8000000
#define BR 9600

#define SEG_Port _pg
#define SEG_PortC _pgc
#define COM_Port _pf
#define COM_PortC _pfc
#define LED_Port _ph
#define LED_PortC _phc

const unsigned short tag[] = {
	0x3f, 0x06, 0x5b, 0x4f, 0x66,  // 0, 1, 2, 3, 4
	0x6d, 0x7d, 0x27, 0x7f, 0x6f}; // 5, 6, 7, 8, 9
const unsigned short scan[] = {
	0x01, 0x02, 0x04, 0x08};

void Pin_Setup();
void UART_Setup();
void Read_Data();
void Send_Data(unsigned short T_Data);
void Segment(unsigned short Value);
void Delay(unsigned short Var);

unsigned char R_Data[];
unsigned short kn = 0;

void main()
{
    _wdtc = 0b10101011;
    Pin_Setup();
    UART_Setup();

    if(Mode == 'T')
    {
        Send_Data('O');
        Send_Data('K');
    }
    else if(Mode == 'R')
    {
        Segment(R_Data[0]);
    }
    Delay(10);
}

DEFINE_ISR(Uart_R, 0x3c)
{
    Read_Data();
    _ur0f = 0;
}

void Pin_Setup()
{
    SEG_PortC = 0x00;
    COM_PortC &= ~0x0f;
}

void UART_Setup()
{
    _pas1 = 0b11110000;	// PA6 => Rx PA7 => Tx
	_u0cr1 = 0b10000000;
	_u0cr2 = 0b11000100;
	_brg0 = FH/((unsigned long)64*BR) - 1;
	_ur0e = 1;
	_ur0f = 0;
	_mf5e = 1;
	_emi = 1;
}

void Send_Data(unsigned short T_Data)
{
    _txr_rxr0 = T_Data; // Write in to UART Transmitter shift Register
	while(_tidle0 == 0);
	_ur0f = 0;
}

void Read_Data()
{
	while(_ridle0 == 0);
	R_Data[kn] = _txr_rxr0;
	if(R_Data[kn] == '/' || kn > 9)	kn = 0;
	else kn++;
}

void Segment(unsigned short Value)
{
    COM_Port |= scan[0];
    SEG_Port = tag[Value/1000%10];
	delay(30);
	COM_Port &= ~scan[0];
	
	COM_Port |= scan[1];
	SEG_Port = tag[Value/100%10];
	delay(30);
	COM_Port &= ~scan[1];
	
	COM_Port |= scan[2];
	SEG_Port = tag[Value/10%10];
	delay(30);
	COM_Port &= ~scan[2];
	
	COM_Port |= scan[3];
	SEG_Port = tag[Value%10];
	delay(30);
	COM_Port &= ~scan[3]; 
}

void Delay(unsigned short Var)
{
    unsigned short i, j;
    for(i=0;i<Var;i++)
        for(j=0;j<25;j++)
            GCC_NOP();
}
