#include "HT66F2390.h"

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
	
void ADC_setup();
void segment(unsigned short value);
void delay(unsigned short var);

unsigned short cv ;

void main()
{
	_wdtc = 0b10101011;
	
	ADC_setup();
	SEG_PortC = 0x00;
	COM_PortC = 0x00;
	
	unsigned short t = 0;
	unsigned short chanl = 0;
	short a, b;
	a = b = 0;
	while(1)
	{	
		if(t == 15)
		{
			chanl = 0;
			_sadc0 = 0b01110000;
			_start = 1;
			_start = 0;
			a = cv;
			t=0;
		}
		else if(t == 30)
		{
			chanl = 1;
			_sadc0 = 0b01110001;
			_start = 1;
			_start = 0;
			t = 0;
			b = cv;
		}
		t++;
		
		if(chanl == 0)
		{
			LED_Port |= 0x02;
			LED_Port &= ~0x01;
		}
		else
		{
			LED_Port |= 0x01;
			LED_Port &= ~0x02;
		}
		
		segment(cv);
	}
}

DEFINE_ISR(ISR_ADC, 0x1c)
{
	cv = (_sadoh << 8) | _sadol;
}

void ADC_setup()
{
	_pcs0 = 0b00001111;
	_sadc0 = 0b01110000;
	_sadc1 = 0b00000110;
	_sadc2 = 0b00000000;
	_ade = 1; _emi = 1;
}

void segment(unsigned short value)
{
	COM_Port |= scan[0];
	SEG_Port = tag[value/1000%10];
	delay(30);
	COM_Port &= ~scan[0];
	
	COM_Port |= scan[1];
	SEG_Port = tag[value/100%10];
	delay(30);
	COM_Port &= ~scan[1];
	
	COM_Port |= scan[2];
	SEG_Port = tag[value/10%10];
	delay(30);
	COM_Port &= ~scan[2];
	
	COM_Port |= scan[3];
	SEG_Port = tag[value%10];
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
