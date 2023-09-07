#include "HT66F2390.h"

// -------------UART setup-------------------//
#define fH 8000000
#define BR 9600

void uart_setup();
void read_data();
void send_data(unsigned short t_data);

// -------------Servo setup------------------//
void stm_setup();
void servo_setup();

// -------------Bend Sensor-----------------//
void ADC_setup();

void delay(unsigned short var);

void main()
{
    _wdtc = 0b10101011;
	stm_setup();
    servo_setup();

    while(1)
    {

    }
}

DEFINE_ISR(ISR_ADC, 0x1c)
{
	cv = (_sadoh << 7) | _sadol;
}

void ADC_setup()
{
	_pcs0 = 0b00001111;
	_sadc0 = 0b01110000;
	_sadc1 = 0b00000110;
	_sadc2 = 0b00000000;
	_ade = 1; _emi = 1;
}

void servo_setup()
{
    _st0on = 1; _st1on = 1; _st2on = 1;
	_pt0on = 1; _pt1on = 1;
	_stm0al = 100; _stm0ah = 0;
	_stm1al = 100; _stm1ah = 0;
	_stm2al = 100; _stm2ah = 0;
	_ptm0al = 100; _ptm0ah = 0;
	_ptm1al = 100; _ptm1ah = 0;
}

void stm_setup()
{
	_stm0c0 = 0b00110000;	//
	_stm0c1 = 0b10101000;
	_stm0rp = 0x0a; // => 10*256
	_stm0al = 188; _stm0ah = 0;
	
	_stm1c0 = 0b00110000;	//
	_stm1c1 = 0b10101000;
	_stm1rp = 0x0a; // => 10*256
	_stm1al = 188; _stm1ah = 0;
	
	_stm2c0 = 0b00110000;	//
	_stm2c1 = 0b10101000;
	_stm2rp = 0x0a; // => 10*256
	_stm2al = 188; _stm2ah = 0;
	
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

void uart_setup()
{
	_pas1 = 0b11110000;	// PA6 => Rx PA7 => Tx
	_u0cr1 = 0b10000000;
	_u0cr2 = 0b11000010;
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

void send_data(unsigned short t_data)
{
	_txr_rxr0 = t_data;
	
	while(_tidle0 == 0);
	_ur0f = 0;
}

void delay(unsigned short var)
{
	unsigned short i, j;
	for(i=0;i<var;i++)
		for(j=0;j<25;j++)
			GCC_NOP();
}
