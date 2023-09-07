#include "HT66F2390.h"

#define Sen _pc3
#define SenC _pcc3
#define SenU _pcpu3
#define LED _pc4
#define LEDC _pcc4
#define ENA _pd5
#define ENAC _pdc5
#define PUL _pd3
#define PULC _pdc3
#define DIR _pd4
#define DIRC _pdc4

void motor_callb();
void motor_deg(unsigned short deg, unsigned short time);

void stm_delay(unsigned short tm);
void stm_setup();
void delay(unsigned short var);
void main()
{
	_wdtc = 0b10101011;
	
	DIRC = 0;
	ENAC = 0;
	LEDC = 0;
	PULC = 0;
	SenC = 1;
	SenU = 1;
	
	ENA = 0;
	while(1)
	{
		DIR = 1;
		LED = 0;
		motor_deg(500, 200);
		//motor_deg(180, 600);
		
		LED = 1;
		DIR = 0;
		delay(10000);
		motor_deg(500, 200);
		
		/*DIR = 0;
		LED = 0;
		motor(360, 200);
		motor(360, 500);*/
		//motor_callb();
		
		delay(10000);
		
	}	
}

void motor_callb()
{
	DIR = 0;
	LED = 0;
	while(Sen)
	{
		PUL = 0;
		stm_delay(200);
		PUL = 1;
		stm_delay(200);
	}
}

void motor_deg(unsigned short deg, unsigned short time)
{
	unsigned short i, j;
	for(j=0;j<deg;j++)
	{
		for(i=0;i<9;i++)
		{
			PUL = 0;
			stm_delay(time);
			PUL = 1;
			stm_delay(time);
		}
	}
}

void stm_setup()
{
	_stm0c0 = 0b00000000;
	_stm0c1 = 0b11000001;
	_emi = 1;
	_mf0e = 1;
	_stm0ae = 1;
	_stm0af = 0;
}

void stm_delay(unsigned short tm)
{
	_stm0al = tm%256;
	_stm0ah = tm/256;
	_st0on = 1;
	while(!_stm0af);
	_st0on = 0;
	_stm0af = 0;
}

void delay(unsigned short var)
{
	unsigned short i, j;
	for(i=0;i<var;i++)
		for(j=0;j<25;j++)
			GCC_NOP();
}