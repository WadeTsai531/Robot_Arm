#include "HT66F2390.h"

#define FH 8000000
#define BR 9600

#define LED _pd1
#define LEDC _pdc1
#define PUL _pd3
#define PULC _pdc3
#define DIR _pd4
#define DIRC _pdc4
#define ENA _pd5
#define ENAC _pdc5
#define Sen _pd6
#define SenC _pdc6
#define SenU _pdpu6

#define SEG_Port _pg
#define SEG_PortC _pgc
#define COM_Port _pf
#define COM_PortC _pfc

const unsigned short tag[] = {
	0x3f, 0x06, 0x5b, 0x4f, 0x66,  // 0, 1, 2, 3, 4
	0x6d, 0x7d, 0x27, 0x7f, 0x6f}; // 5, 6, 7, 8, 9
const unsigned short scan[] = {
	0x01, 0x02, 0x04, 0x08};

unsigned char R_Data[10];
unsigned char Data[10];
unsigned short kn = 0;

void UART_Setup();
void Read_Data();

void motor_callb();
void motor_deg(unsigned short deg, unsigned int time);

void ptm_delay(unsigned int tm);
void ptm_setup();
void Segment(unsigned short Value);
void delay(unsigned short var);
void main()
{
	_wdtc = 0b10101011;
	UART_Setup();
	
	// SEG_PortC = 0x00;
    // COM_PortC &= ~0x0f;
    
	DIRC = 0;
	ENAC = 0;
	LEDC = 0;
	PULC = 0;
	SenC = 1;
	SenU = 1;
	
	motor_callb();
	DIR = 1;
	motor_deg(360, 500);
	LED = 0;
	delay(5000);
	LED = 1;
	unsigned int sp;
	sp = 1600;
	ENA = 1;
	unsigned short clear;
	while(1)
	{
		if(Data[0] == 'V')
		{
			sp = (Data[1] - 48)*1000 + (Data[2] - 48)*100 + (Data[3] - 48)*10 + (Data[4] - 48);
			Segment(0100);
			for(clear=0;clear<10;clear++)
			{
				Data[clear] = ' ';
			}
		}
		if(Data[0] == 'S')
		{
			LED = 1;
			ENA = 1;
			Segment(0200);
			for(clear=0;clear<10;clear++)
			{
				Data[clear] = ' ';
			}
		}
		if(Data[0] == 'R')
		{
			LED = 0;
			ENA = 0;
			DIR = 1;
			Segment(0300);
			for(clear=0;clear<10;clear++)
			{
				Data[clear] = ' ';
			}
		}
		if(R_Data[0] == 'L')
		{
			ENA = 0;
			DIR = 0;
			Segment(0400);
			for(clear=0;clear<10;clear++)
			{
				R_Data[clear] = ' ';
			}
		}
		if(Data[0] == 'H')
		{
			delay(3000);
			motor_callb();
			DIR = 1;
			motor_deg(360, 500);
			ENA = 1;
			for(clear=0;clear<10;clear++)
			{
				Data[clear] = ' ';
			}
		}
		unsigned short i;
		for(i=0;i<9;i++)
		{
			PUL = 0;
			ptm_delay(sp);
			PUL = 1;
			ptm_delay(sp);
		}	
	}	
}

DEFINE_ISR(Uart_R, 0x3c)
{
    Read_Data();
    _ur0f = 0;
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
	if(R_Data[kn] == '/' || kn > 9)
	{
		kn = 0;
		unsigned short cl;
		for(cl=0;cl<10;cl++)
			Data[cl] = R_Data[cl];
	}	
	else kn++;
}

void motor_callb()
{
	ENA = 0;
	DIR = 0;
	while(Sen)
	{
		PUL = 0;
		ptm_delay(500);
		PUL = 1;
		ptm_delay(500);
	}
}

void motor_deg(unsigned short deg, unsigned int time)
{
	unsigned short i, j;
	for(j=0;j<deg;j++)
	{
		for(i=0;i<9;i++)
		{
			PUL = 0;
			ptm_delay(time);
			PUL = 1;
			ptm_delay(time);
		}
	}
}

void ptm_setup()
{
	_ptm3c0 = 0b00000000;
	_ptm3c1 = 0b11000001;
	_emi = 1;
	_mf4e = 1;
	_ptm3ae = 1;
	_ptm3af = 0;
}

void ptm_delay(unsigned int tm)
{
	_ptm3al = tm%256;
	_ptm3ah = tm/256;
	_pt3on = 1;
	while(!_ptm3af);
	_pt3on = 0;
	_ptm3af = 0;
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

void fn()
{
	unsigned short times;
		unsigned short speed;
		if(times >= 1300)
		{
			times = 0;
			delay(5000);
			motor_callb();
			delay(10000);
			DIR = 1;
		}
		else if(times >= 300)
		{
			speed = 200;
		}
		else
		{
			speed = (300 - times) * 1 + 150;
		}
		
		motor_deg(1, speed);
		
		times++;
}