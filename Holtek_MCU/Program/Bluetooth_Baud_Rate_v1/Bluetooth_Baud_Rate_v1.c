#include "HT66F2390.h"

#define FH 8000000
#define BR 9600
unsigned char R_Data[10];
unsigned char Data[10];
unsigned short kn = 0;

void UART_Setup();
void Read_Data();
void Send_Data(unsigned short T_Data);

#define SEG_Port _pg
#define SEG_PortC _pgc
#define COM_Port _pf
#define COM_PortC _pfc

const unsigned short tag[] = {
	0x3f, 0x06, 0x5b, 0x4f, 0x66,  // 0, 1, 2, 3, 4
	0x6d, 0x7d, 0x27, 0x7f, 0x6f}; // 5, 6, 7, 8, 9
const unsigned short scan[] = {
	0x01, 0x02, 0x04, 0x08};
void Segment(unsigned short Value);

#define LED _pc0
#define LEDC _pcc0

#define LED2 _pc1
#define LED2C _pcc1

void delay(unsigned short var);

void main()
{
	_wdtc = 0b10101011;
	_scc = 0b00000001;
	_hircc = 0b00000011;
	
	UART_Setup();
	
	unsigned short clear;
	for(clear=0;clear<10;clear++)
		R_Data[clear] = ' ';
	
	LEDC = 0;
	LED2C = 0;
	SEG_PortC = 0x00;
	COM_PortC &= ~0x0f;
	
	unsigned short A_value = 0;
	
	while(1)
	{
		if(R_Data[0] == 'A')
		{
			LED = 0;
			delay(10);
		}
		else if(R_Data[0] == 'C')
		{
			LED = 1;
			delay(10);
		}
	}
}

DEFINE_ISR(Uart_R, 0x3c)
{
	LED2 = 0;
    Read_Data();
    _ur0f = 0;
    LED2 = 1;
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

void Read_Data()
{
	while(_ridle0 == 0);
	R_Data[kn] = _txr_rxr0;
	if(R_Data[kn] == '/' || kn > 9) //kn = 0;
	{
		kn = 0;
		unsigned short cl;
		for(cl=0;cl<10;cl++)
			Data[cl] = R_Data[cl];
	}
	else kn++;
}

void Send_Data(unsigned short T_Data)
{
    _txr_rxr0 = T_Data; // Write in to UART Transmitter shift Register
	while(_tidle0 == 0);
	_ur0f = 0;
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

void delay(unsigned short var)
{
	unsigned short i, j;
	for(i=0;i<var;i++)
		for(j=0;j<25;j++)
			GCC_NOP();
}