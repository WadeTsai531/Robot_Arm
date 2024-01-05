#include "HT66F2390.h"

// Servo 
#define Servo_deg_0 256 // fsys=16MHz 128, fsys=8MHz 64
void timer_setup();
void servo_setup();

void delay(unsigned short var);

void main()
{
	_wdtc = 0b10101011;
	
	_scc = 0b00000001;
	_hircc = 0b00001011;
	
	servo_setup();
	
	while(1)
	{
		unsigned short i;
		for(i=0;i<270;i+=10)
		{
			_stm0al = (i + Servo_deg_0)%256; _stm0ah = (i + Servo_deg_0)/256;
			delay(2500);
		}
		
		for(i=270;i>1;i-=10)
		{
			_stm0al = (i + Servo_deg_0)%256; _stm0ah = (i + Servo_deg_0)/256;
			delay(2500);
		}
	}
}

void timer_setup()
{
	_stm0c0 = 0b00110000; // Pause Contorl: Run, Clock: fh/64
	_stm0c1 = 0b10101000; // Mode: PWM, Output Control: Active High
	_stm0rp = 0x05; // 20*256 =>> f=48hz
}

void servo_setup()
{
	timer_setup();
	_pcs1 = 0b00100010; // PC6 => STM0, PC4 => PTM1
	
	_st0on = 1; _stm0al = Servo_deg_0%256; _stm0ah = Servo_deg_0/256;
}

void delay(unsigned short var)
{
	unsigned short i, j;
	for(i=0;i<var;i++)
		for(j=0;j<25;j++)
			GCC_NOP();
}
