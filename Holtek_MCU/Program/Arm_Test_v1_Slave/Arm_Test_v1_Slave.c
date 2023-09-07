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

void delay(unsigned short var);


void main()
{

}

void uart_setup()
{
	_pas1 = 0b11110000;	// PA6 => Rx PA7 => Tx
	_u0cr1 = 0b10000000;
	_u0cr2 = 0b11000000;
	_brg0 = fH/((unsigned long)64*BR) - 1;
	_ur0e = 1;
	_ur0f = 0;
	_mf5e = 1;
	_emi = 1;
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
