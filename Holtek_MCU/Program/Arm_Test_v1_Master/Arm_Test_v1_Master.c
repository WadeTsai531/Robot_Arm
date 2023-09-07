/*
	Description:
		Use bluetooth to send data of bend sensor to slave

	Pin Define:
		PC0 => AN0
		PA6 => RX, PA7 => TX
*/
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

// -------------Bend Sensor setup-----------------//
void ADC_setup();

void delay(unsigned short var);

// ------------ Variable set-------------------//
unsigned short cv; // for ADC Data


void main()
{
	_wdtc = 0b10101011;
	uart_setup();
	ADC_setup();
	
	// --------variavle---------- //
	unsigned short t=0; 
	unsigned short a=0;
	unsigned short degA = 0;
	// -------------------------- //
	
	while(1)
	{
		if(t == 10)
		{
			_sadc0 = 0b01110000;
			_start = 1;
			_start = 0;
			a = cv;
			degA = (float)((a-1600))*2.6;
			send_data('A');
			send_data(degA);
			send_data('/');
			t=0;
		}
		t++;
		delay(100);
	}
}

DEFINE_ISR(ISR_ADC, 0x1c)
{
	cv = (_sadoh << 8) | _sadol;
}

void ADC_setup()
{
	_pcs0 = 0b00000011;	// PC0 => AN0
	_sadc0 = 0b01110000;
	_sadc1 = 0b00000110;
	_sadc2 = 0b00000000;
	_ade = 1; _emi = 1;
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
