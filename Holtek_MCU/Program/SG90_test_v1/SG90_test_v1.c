#include "HT66F2390.h"

#define LED_Port _pd
#define LED_PortC _pdc

#define SEG_Port _pg
#define SEG_PortC _pgc

#define COM_Port _pf
#define COM_PortC _pfc

const unsigned short tag[] = {
	0x3f, 0x06, 0x5b, 0x4f, 0x66,  	// 0, 1, 2, 3, 4
	0x6d, 0x7d, 0x27, 0x7f, 0x6f};	// 5, 6, 7, 8, 9

const unsigned short scan[] = {
	0x01, 0x02, 0x04, 0x08};

void time_setup();
void servo_setup();
void segment(unsigned short value);

void delay(unsigned short var);
void main()
{
	_wdtc = 0b10101011;
	servo_setup();
	COM_PortC &= 0xf0;
	SEG_PortC = 0x00;
	LED_PortC = 0x00;
	
	_st0on = 1; _st1on = 0; _st2on = 0;
	_pt0on = 0; _pt1on = 0;
	_stm0al = 100; _stm0ah = 0;
	_stm1al = 100; _stm1ah = 0;
	_stm2al = 100; _stm2ah = 0;
	_ptm0al = 100; _ptm0ah = 0;
	_ptm1al = 100; _ptm1ah = 0;

	while(1)
	
	{
		unsigned short k;
		for(k=100;k<200;k++)
		{
			_stm0al = k; _stm0ah = 0;
			segment(k);
			//segment(k+1000);
		}
		delay(5000);
		
		for(k=200;k>100;k--)
		{
			_stm0al = k; _stm0ah = 0;
			segment(k);
			//segment(k+1000);
		}
		delay(5000);
		
		/*for(k=100;k<230;k++)
		{
			_stm1al = k; _stm1ah = 0;
			delay(100);
			//segment(k+2000);
		}
		
		for(k=100;k<230;k++)
		{
			_stm2al = k; _stm2ah = 0;
			delay(100);
			//segment(k+3000);
		}

		for(k=100;k<230;k++)
		{
			_ptm0al = k; _ptm0ah = 0;
			delay(100);
			//segment(k+4000);
		}
		
		for(k=100;k<230;k++)
		{
			_ptm1al = k; _ptm1ah = 0;
			delay(100);
			//segment(k+5000);
		}
		
		
		for(k=230;k>100;k--)
		{
			_stm0al = k; _stm0ah = 0;
			_stm1al = k; _stm1ah = 0;
			_stm2al = k; _stm2ah = 0;
			_ptm0al = k; _ptm0ah = 0;
			_ptm1al = k; _ptm1ah = 0;
			delay(100);
		}
		
		for(k=230;k>100;k--)
		{
			_stm0al = k; _stm0ah = 0;
			//_stm1al = k; _stm1ah = 0;
			//_stm2al = k; _stm2ah = 0;
			//_ptm0al = k; _ptm0ah = 0;
			_ptm1al = k; _ptm1ah = 0;
			segment(k);
		}
		
		for(k=230;k>100;k--)
		{
			//_stm0al = k; _stm0ah = 0;
			_stm1al = k; _stm1ah = 0;
			//_stm2al = k; _stm2ah = 0;
			_ptm0al = k; _ptm0ah = 0;
			//_ptm1al = k; _ptm1ah = 0;
			segment(k);
		}*/
	}
}

void servo_setup()
{
	time_setup();	
	_pcs1 = 0b00100010; // PC6 => STP0, PC4 => PTP1
	_pds0 = 0b00010010; // PD0 => STP1, PD2 => PTP2
	_pfs1 = 0b10000000; // PF7 => STP2
	_pcs0 = 0b00100000; // PC2 => PTP0
	_st0on = 1; _stm0al = 200; _stm0ah = 0;
	_st1on = 1; _stm1al = 200; _stm1ah = 0;
	_st2on = 1; _stm2al = 160; _stm2ah = 0;
	_pt0on = 0; _ptm0al = 200; _ptm0ah = 0;
	_pt1on = 0; _ptm1al = 200; _ptm1ah = 0;
	_pt2on = 0; _ptm2al = 200; _ptm2ah = 0;
}

void time_setup()
{
	_stm0c0 = 0b00110000;	//
	_stm0c1 = 0b10101000;
	_stm0rp = 0x14; // => 10*256
	_stm0al = 376%256; _stm0ah = 376/256;
	
	_stm1c0 = 0b00110000;	//
	_stm1c1 = 0b10101000;
	_stm1rp = 0x14; // => 10*256
	_stm1al = 376%256; _stm1ah = 376/256;
	
	_stm2c0 = 0b00110000;	//
	_stm2c1 = 0b10101000;
	_stm2rp = 0x14; // => 10*256
	_stm2al = 376/256; _stm2ah = 376/256;
	
	_ptm0c0 = 0b00110000;
	_ptm0c1 = 0b10101000;
	_ptm0rpl = 0xfe; _ptm0rph = 0x07;
	_ptm0al = 200; _ptm0ah = 0;
	
	_ptm1c0 = 0b00110000;
	_ptm1c1 = 0b10101000;
	_ptm0rpl = 0xfe; _ptm0rph = 0x07;
	_ptm1al = 200; _ptm1ah = 0;
	
	_ptm2c0 = 0b00110000;
	_ptm2c1 = 0b10101000;
	_ptm0rpl = 0xfe; _ptm0rph = 0x07;
	_ptm2al = 160; _ptm2ah = 0;
}


void segment(unsigned short value)
{
	COM_Port |= scan[0];
	SEG_Port = tag[value/1000%10];
	delay(50);
	COM_Port &= ~scan[0];
	
	COM_Port |= scan[1];
	SEG_Port = tag[value/100%10];
	delay(50);
	COM_Port &= ~scan[1];
	
	COM_Port |= scan[2];
	SEG_Port = tag[value/10%10];
	delay(50);
	COM_Port &= ~scan[2];
	
	COM_Port |= scan[3];
	SEG_Port = tag[value%10];
	delay(50);
	COM_Port &= ~scan[3];
}
	
void delay(unsigned short var)
{
	unsigned short i, j;
	for(i=0;i<var;i++)
		for(j=0;j<25;j++)
			GCC_NOP();
}