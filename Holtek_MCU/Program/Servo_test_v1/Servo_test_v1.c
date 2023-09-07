#include "HT66F2390.h"

#define Servo_deg_0 256 // fsys=16MHz 128, fsys=8MHz 64
void timer_setup();
void servo_setup();

void delay(unsigned short var);

void main()
{
	_wdtc = 0b10101011;
	
	_scc = 0b00000001;
	_hircc = 0b00001011;
	
	// Servo Setup
	servo_setup();
	
	while(1)
	{
		_stm0al = (Servo_deg_0)%256; _stm0ah = (Servo_deg_0)/256;
		delay(30000);
		
		unsigned short i;
		for(i=1;i<181;i++)
		{
			_stm0rp = i / 18 + 20;
			_stm0al = (i + Servo_deg_0)%256; _stm0ah = (i + Servo_deg_0)/256;
			delay(100);
		}
		
		for(i=180;i>1;i--)
		{
			_stm0rp = i / 18 + 20;
			_stm0al = (i + Servo_deg_0)%256; _stm0ah = (i + Servo_deg_0)/256;
			delay(100);
		}
	}
}

void timer_setup()
{
	_stm0c0 = 0b00110000; // Pause Contorl: Run, Clock: fh/64
	_stm0c1 = 0b10101000; // Mode: PWM, Output Control: Active High
	_stm0rp = 0x14; // 20*256 =>> f=48hz
	
	_stm1c0 = 0b00110000;
	_stm1c1 = 0b10101000;
	_stm1rp = 0x14;
	
	_stm2c0 = 0b00110000;
	_stm2c1 = 0b10101000;
	_stm2rp = 0x14;
	
	_ptm0c0 = 0b00110000;
	_ptm0c1 = 0b10101000;
	_ptm0rpl = 0; _ptm0rph = 0x14;
	
	_ptm1c0 = 0b00110000;
	_ptm1c1 = 0b10101000;
	_ptm1rpl = 0; _ptm1rph = 0x14;
	
	_ptm2c0 = 0b00110000;
	_ptm2c1 = 0b10101000;
	_ptm2rpl = 0; _ptm2rph = 0x14;
}

void servo_setup()
{
	timer_setup();
	_pcs1 = 0b00100010; // PC6 => STM0, PC4 => PTM1
	_pds0 = 0b00010010; // PD0 => STM1, PD2 => PTM2
	_pfs1 = 0b10000000; // PF7 => STM2
	_pcs0 = 0b00100000; // PC2 => PTM0
	
	_st0on = 1; _stm0al = Servo_deg_0%256; _stm0ah = Servo_deg_0/256;
	_st1on = 1; _stm1al = Servo_deg_0%256; _stm1ah = Servo_deg_0/256;
	_st2on = 1; _stm2al = Servo_deg_0%256; _stm2ah = Servo_deg_0/256;
	_pt0on = 1; _ptm0al = Servo_deg_0%256; _ptm0ah = Servo_deg_0/256;
	_pt1on = 1; _ptm1al = Servo_deg_0%256; _ptm1ah = Servo_deg_0/256;
	_pt2on = 1; _ptm2al = (Servo_deg_0 + 10)%256; _ptm2ah = (Servo_deg_0 + 10)/256;
}

void delay(unsigned short var)
{
	unsigned short i, j;
	for(i=0;i<var;i++)
		for(j=0;j<25;j++)
			GCC_NOP();
}
