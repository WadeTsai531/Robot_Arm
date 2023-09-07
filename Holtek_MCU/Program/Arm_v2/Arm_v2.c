#include "HT66F2390.h"

#define fH 8000000
#define BR 9600

#define LED_Port _pb
#define LED_PortC _pbc

#define SEG_Port _pg
#define SEG_PortC _pgc

#define COM_Port _pf
#define COM_PortC _pfc

const unsigned short tag[] = {
	0x3f, 0x06, 0x5b, 0x4f, 0x66,  	// 0, 1, 2, 3, 4
	0x6d, 0x7d, 0x27, 0x7f, 0x6f};	// 5, 6, 7, 8, 9
const unsigned short chn[] = {
	0x77, 0x7c, 0x39, 0x5e, 0x79}; 	// A, b, C, d, E
const unsigned short scan[] = {
	0x01, 0x02, 0x04, 0x08};

char value[10];
unsigned short kn = 0;

void uart_setup();
void read_data();
void stm_setup();
void segment(unsigned short chnal,unsigned short value);
void delay(unsigned short var);
void arm_initial();

void main()
{
	_wdtc = 0b10101011;
	uart_setup();
	stm_setup();
	arm_initial();
	
	COM_PortC &= 0xf0;
	SEG_PortC = 0x00;
	LED_PortC = 0x00;
	
	unsigned short tf_last, tf;
	tf = tf_last = 0;
	while(1)
	{
		tf = (value[1]-0x30)*100+(value[2]-0x30)*10+(value[3]-0x30);
		if(tf != tf_last)
		{
			tf_last = tf;
		}
		segment(value[0],tf);
		if(value[0] == 'A')
		{
			LED_Port &= ~0x02;
			_stm0al = tf+100; _stm0ah = 0;
		}
		else if(value[0] == 'B')
		{
			_stm1al = tf+100; 
			_stm1ah = 0;
		}
		else if(value[0] == 'C')
		{
			_stm2al = tf+100; 
			_stm2ah = 0;
		}
		else
			LED_Port |= 0x02;
	}
}

DEFINE_ISR(UART0,0x3c)
{	
	LED_Port &= ~0x01;
	read_data();
	_ur0f = 0;
	LED_Port |= 0x01;
}

void uart_setup()
{
	_pas1 = 0b11110000;	// PA6 => Rx PA7 => Tx
	_u0cr1 = 0b10000000;
	_u0cr2 = 0b11000100;
	_brg0 = fH/((unsigned long)64*BR) - 1;
	_ur0e = 1;
	_ur0f = 0;
	_mf5e = 1;
	_emi = 1;
}

void read_data()
{
	while(_ridle0 == 0);
	value[kn] = _txr_rxr0;
	if(value[kn] == '/' || kn > 9)	kn = 0;
	else kn++;
}

void arm_initial()
{
	_st0on = 1; _st1on = 1; _st2on = 1;
	_pt0on = 1; _pt1on = 1;
	_stm0al = 100; 
	_stm1al = 100; 
	_stm2al = 100; 
	_ptm0al = 100;
	_ptm1al = 100;
}
void stm_setup()
{
	_stm0c0 = 0b00110000;	//
	_stm0c1 = 0b10101000;
	_stm0rp = 0x0a; // => 10*256
	_stm0al = 100; _stm0ah = 0;
	
	_stm1c0 = 0b00110000;	//
	_stm1c1 = 0b10101000;
	_stm1rp = 0x0a; // => 10*256
	_stm1al = 100; _stm1ah = 0;
	
	_stm2c0 = 0b00110000;	//
	_stm2c1 = 0b10101000;
	_stm2rp = 0x0a; // => 10*256
	_stm2al = 100; _stm2ah = 0;
	
	_ptm0c0 = 0b00110000;
	_ptm0c1 = 0b10101000;
	_ptm0rpl = 0xff; _ptm0rph = 0x03;
	_ptm0al = 100; _ptm0ah = 0;
	
	_ptm1c0 = 0b00110000;
	_ptm1c1 = 0b10101000;
	_ptm1rpl = 0xff; _ptm1rph = 0x03;
	_ptm1al = 100; _ptm1ah = 0;
	
	_pcs1 = 0b00100010; // PC6 => STP0, PC4 => PTP1
	_pds0 = 0b00000010; // PD1 => STP1
	_pfs1 = 0b10000000; // PF7 => STP2
	_pcs0 = 0b00100000; // PC2 => PTP0
}

void segment(unsigned short chnal, unsigned short value)
{
	COM_Port |= scan[0];
	SEG_Port = chn[chnal-65];
	delay(20);
	COM_Port &= ~scan[0];
	
	COM_Port |= scan[1];
	SEG_Port = tag[value/100%10];
	delay(20);
	COM_Port &= ~scan[1];
	
	COM_Port |= scan[2];
	SEG_Port = tag[value/10%10];
	delay(20);
	COM_Port &= ~scan[2];
	
	COM_Port |= scan[3];
	SEG_Port = tag[value%10];
	delay(20);
	COM_Port &= ~scan[3];
}
	
void delay(unsigned short var)
{
	unsigned short i, j;
	for(i=0;i<var;i++)
		for(j=0;j<25;j++)
			GCC_NOP();
}