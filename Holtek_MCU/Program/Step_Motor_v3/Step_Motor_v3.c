#include "HT66F2390.h"

#define PUL _pd3
#define PULC _pdc3

#define DIR _pd4
#define DIRC _pdc4

#define ENA _pd5
#define ENAC _pdc5

#define Sen _pd6
#define SenC _pdc6
#define SenU _pdpu6

void ptm_setup();
void ptm_delay(unsigned int tm);

void motor_deg(unsigned short deg, unsigned int time);
void motor_callb();

void delay(unsigned short var);

void main()
{
	_wdtc = 0b10101011;
	
	_scc = 0b00000001;
	_hircc = 0b00001011;
	
	ptm_setup();
	
	// Step Motor Setup
	DIRC = 0;
	ENAC = 0;
	PULC = 0;
	SenC = 1;
	SenU = 1;
	
	while(1)
	{
		DIR = 1;
		unsigned short i;
		for(i=0;i<400;i++)
		{
			PUL = 0;
			ptm_delay(2000);
			PUL = 1;
			ptm_delay(2000);
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

void motor_callb()
{
	ENA = 0;
	DIR = 0;
	while(Sen)
	{
		PUL = 0;
		ptm_delay(800);
		PUL = 1;
		ptm_delay(800);
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

void delay(unsigned short var)
{
	unsigned short i, j;
	for(i=0;i<var;i++)
		for(j=0;j<25;j++)
			GCC_NOP();
}
