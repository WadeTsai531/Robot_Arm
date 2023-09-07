#include "HT66F2390.h"

#define LED _pc0
#define LEDC _pcc0
#define PUL _pd3
#define PULC _pdc3
#define DIR _pd4
#define DIRC _pdc4
#define ENA _pd5
#define ENAC _pdc5
#define Sen _pd6
#define SenC _pdc6
#define SenU _pdpu6

#define SEG_Port _pg
#define SEG_PortC _pgc
#define COM_Port _pf
#define COM_PortC _pfc

const unsigned short tag[] = {
	0x3f, 0x06, 0x5b, 0x4f, 0x66,  // 0, 1, 2, 3, 4
	0x6d, 0x7d, 0x27, 0x7f, 0x6f}; // 5, 6, 7, 8, 9
const unsigned short scan[] = {
	0x01, 0x02, 0x04, 0x08};
void Segment(unsigned short Value);

// Uart define
#define FH 8000000
#define BR 9600

unsigned char R_Data[10];
unsigned char Data[10];
unsigned short kn = 0;

void UART_Setup();
void Read_Data();

// Servo setup
void time_setup();
void servo_setup();

// Motor Setup
void ptm_setup();
void ptm_delay(unsigned int tm);

void motor_deg(unsigned short deg, unsigned int time);
void motor_callb();

void delay(unsigned short var);

void main()
{
	_wdtc = 0b10101011;
	
	DIRC = 0;
	ENAC = 0;
	PULC = 0;
	SenC = 1;
	SenU = 1;
	
	LEDC = 0;
	
	UART_Setup();
	servo_setup();
	
	SEG_PortC = 0x00;
	COM_PortC &= ~0x0f;
	
	motor_callb();
	DIR = 1;
	motor_deg(360, 500);
	delay(5000);
	ENA = 1;
	
	unsigned short A_deg, B_deg, C_deg, D_deg, E_deg, F_deg = 0;
	unsigned short clear;
	unsigned short show;
	unsigned short run;
	unsigned int sp;
	sp = 1600;
	
	while(1)
	{	
		if(Data[0] == 'A')
		{
			A_deg = (Data[1] - 48)*100 + (Data[2] - 48)*10 + (Data[3] - 48);
			_stm0al = 130 - A_deg + 100; _stm0ah = 0;
			Segment(A_deg);
			for(clear=0;clear<10;clear++)
				Data[clear] = ' ';
		}
		else if(Data[0] == 'B')
		{
			B_deg = (Data[1] - 48)*100 + (Data[2] - 48)*10 + (Data[3] - 48);
			_stm1al = 130 - B_deg+100; _stm1ah = 0;
			Segment(B_deg);
			for(clear=0;clear<10;clear++)
				Data[clear] = ' ';
		}
		else if(Data[0] == 'C')
		{
			C_deg = (Data[1] - 48)*100 + (Data[2] - 48)*10 + (Data[3] - 48);
			_stm2al = 130 - C_deg + 80; _stm2ah = 0;
			Segment(C_deg);
			for(clear=0;clear<10;clear++)
				Data[clear] = ' ';
		}
		else if(Data[0] == 'D')
		{
			D_deg = (Data[1] - 48)*100 + (Data[2] - 48)*10 + (Data[3] - 48);
			_ptm0al = 130 - D_deg+100; _ptm0ah = 0;
			Segment(D_deg);
			for(clear=0;clear<10;clear++)
				Data[clear] = ' ';
		}
		else if(Data[0] == 'E')
		{
			E_deg = (Data[1] - 48)*100 + (Data[2] - 48)*10 + (Data[3] - 48);
			_ptm1al = 130 -E_deg+100; _ptm1ah = 0;
			Segment(E_deg);
			for(clear=0;clear<10;clear++)
				Data[clear] = ' ';
		}
		else if(Data[0] == 'F')
		{
			F_deg = (Data[1] - 48)*100 + (Data[2] - 48)*10 + (Data[3] - 48);
			_ptm2al = F_deg+100; _ptm2ah = 0;
			Segment(F_deg);
			for(clear=0;clear<10;clear++)
				Data[clear] = ' ';
		}
		
		if(Data[0] == 'R')
		{
			LED = 0;
			ENA = 0;
			DIR = 1;
			for(clear=0;clear<10;clear++)
				Data[clear] = ' ';
		}
		else if(Data[0] == 'S')
		{
			LED = 1;
			ENA = 1;
			for(clear=0;clear<10;clear++)
				Data[clear] = ' ';
		}
		else if(R_Data[0] == 'L')
		{
			ENA = 0;
			DIR = 0;
			for(clear=0;clear<10;clear++)
				Data[clear] = ' ';
		}
		
		if(Data[0] == 'V')
		{
			sp = (Data[1] - 48)*1000 + (Data[2] - 48)*100 + (Data[3] - 48)*10 + (Data[4] - 48);
			for(clear=0;clear<10;clear++)
				Data[clear] = ' ';
		}
		if(Data[0] == 'H')
		{
			delay(3000);
			motor_callb();
			DIR = 1;
			motor_deg(360, 500);
			ENA = 1;
			for(clear=0;clear<10;clear++)
				Data[clear] = ' ';
		}
		
		for(run=0;run<9;run++)
		{
			PUL = 0;
			ptm_delay(800);
			PUL = 1;
			ptm_delay(800);
		}
	}
}

void Segment(unsigned short Value)
{
    COM_Port |= scan[0];
    SEG_Port = tag[Value/1000%10];
	delay(30);
	COM_Port &= ~scan[0];
	
	COM_Port |= scan[1];
	SEG_Port = tag[Value/100%10];
	delay(30);
	COM_Port &= ~scan[1];
	
	COM_Port |= scan[2];
	SEG_Port = tag[Value/10%10];
	delay(30);
	COM_Port &= ~scan[2];
	
	COM_Port |= scan[3];
	SEG_Port = tag[Value%10];
	delay(30);
	COM_Port &= ~scan[3]; 
}

DEFINE_ISR(Uart_R, 0x3c)
{
    Read_Data();
    _ur0f = 0;
}

void UART_Setup()
{
    _pas1 = 0b11110000;	// PA6 => Rx PA7 => Tx
	_u0cr1 = 0b10000000;
	_u0cr2 = 0b01000100;
	_brg0 = FH/((unsigned long)64*BR) - 1;
	_ur0e = 1;
	_ur0f = 0;
	_mf5e = 1;
	_emi = 1;
}

void Read_Data()
{
	while(_ridle0 == 0);
	R_Data[kn] = _txr_rxr0;
	if(R_Data[kn] == '/' || kn > 9)
	{
		kn = 0;
		unsigned short cl;
		for(cl=0;cl<10;cl++)
			Data[cl] = R_Data[cl];
	}	
	else kn++;
}

void servo_setup()
{
	time_setup();	
	_pcs1 = 0b00100010; // PC6 => STP0, PC4 => PTP1
	_pds0 = 0b00010010; // PD0 => STP1, PD2 => PTP2
	_pfs1 = 0b10000000; // PF7 => STP2
	_pcs0 = 0b00100000; // PC2 => PTP0
	_st0on = 1; _stm0al = 100; _stm0ah = 0;
	_st1on = 1; _stm1al = 100; _stm1ah = 0;
	_st2on = 1; _stm2al = 80; _stm2ah = 0;
	_pt0on = 1; _ptm0al = 100; _ptm0ah = 0;
	_pt1on = 1; _ptm1al = 100; _ptm1ah = 0;
	_pt2on = 1; _ptm2al = 100; _ptm2ah = 0;
}

void time_setup()
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
	
	_ptm2c0 = 0b00110000;
	_ptm2c1 = 0b10101000;
	_ptm2rpl = 0xff; _ptm2rph = 0x03;
	_ptm2al = 80; _ptm2ah = 0;
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
		ptm_delay(500);
		PUL = 1;
		ptm_delay(500);
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