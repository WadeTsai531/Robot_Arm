#include "HT66F2390.h"

// UART
#define FH 16000000
#define BR 38400

unsigned char R_Data[10];
unsigned char Data[10];
unsigned short kn = 0;

void UART_Setup();
void Read_Data();


void ptm_setup();
void ptm_delay(unsigned int tm);

#define output _pg0
#define outputC _pgc0

#define LED _pg2
#define LEDC _pgc2

void main()
{
	_wdtc = 0b10101011;
	
	_scc = 0b00000001;
	_hircc = 0b00001011;
	
	UART_Setup();
	
	ptm_setup();
	
	outputC = 0;
	LEDC = 0;
	
	output = 0;
	LED = 0;
	_emi = 1;
	
	while(1)
	{
		ptm_delay(500);
		
		ptm_delay(500);
	}
}

DEFINE_ISR(Uart_R, 0x3c)
{
	LED = 0;
    Read_Data();
    _ur0f = 0;
    LED = 1;
}

DEFINE_ISR(timer, 0x38)
{
	output = ~output;
}

void UART_Setup()
{
    _pas1 = 0b11110000;	// PA6 => Rx PA7 => Tx
	_u0cr1 = 0b10000000;
	_u0cr2 = 0b01100100;
	_brg0 = FH/((unsigned long)16*BR) - 1;
	_ur0e = 1;
	_ur0f = 0;
	_mf5e = 1;
}

void Read_Data()
{
	while(_ridle0 == 0);
	R_Data[kn] = _txr_rxr0;
	if(R_Data[kn] == '/' || kn > 9) kn = 0;
	else kn++;
}

void ptm_setup()
{
	_ptm3c0 = 0b00000000;
	_ptm3c1 = 0b11000001;
	_ptm3ae = 1;
	_ptm3af = 0;
	_mf4e = 1;
}

void ptm_delay(unsigned int tm)
{
	_ptm3al = tm%256;
	_ptm3ah = tm/256;
	//_ptm3af = 0;
	_pt3on = 1;
	while(!_ptm3af);
	_pt3on = 0;
	_ptm3af = 0;
}
