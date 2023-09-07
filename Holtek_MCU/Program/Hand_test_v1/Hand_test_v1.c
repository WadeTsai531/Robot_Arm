#include "HT66F2390.h"

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

#define FH 16000000
#define BR 38400

#define LED _pc0
#define LEDC _pcc0

unsigned char R_Data[10];
unsigned char Data[10];
unsigned short kn = 0;

void UART_Setup();
void Read_Data();

void time_setup();
void servo_setup();

void delay(unsigned short var);

void main()
{
	_wdtc = 0b10101011;
	_scc = 0b00000001;
	_hircc = 0b00001011;
	
	LEDC = 0;
	LED = 1;
	SEG_PortC = 0x00;
	COM_PortC &= ~0x0f;
	
	UART_Setup();
	servo_setup();
	
	unsigned short A_deg, B_deg, C_deg, D_deg, E_deg, F_deg;
	A_deg = B_deg = C_deg = D_deg = E_deg = F_deg = 0;
	unsigned short clear;
	
	while(1)
	{
		if(R_Data[0] == 'A')
		{
			A_deg = (R_Data[1] - 48)*100 + (R_Data[2] - 48)*10 + (R_Data[3] - 48);
			_stm0al = ((130 - A_deg)*2+170)%256; _stm0ah = ((130 - A_deg)*2+170)/256;
			delay(10);
		}
		if(R_Data[0] == 'B')
		{
			B_deg = (R_Data[1] - 48)*100 + (R_Data[2] - 48)*10 + (R_Data[3] - 48);
			_stm1al = ((130 - B_deg)*2+170)%256; _stm1ah = ((130 - B_deg)*2+170)/256;
			delay(10);
		}
		if(R_Data[0] == 'C')
		{
			C_deg = (R_Data[1] - 48)*100 + (R_Data[2] - 48)*10 + (R_Data[3] - 48);
			_stm2al = ((130 - C_deg)*2+150)%256; _stm2ah = ((130 - C_deg)*2+150)/256;
			delay(10);
		}
		if(R_Data[0] == 'D')
		{
			D_deg = (R_Data[1] - 48)*100 + (R_Data[2] - 48)*10 + (R_Data[3] - 48);
			_ptm0al = ((130 - D_deg)*2+150)%256; _ptm0ah = ((130 - D_deg)*2+150)/256;
			delay(10);
		}
		if(R_Data[0] == 'E')
		{
			E_deg = (R_Data[1] - 48)*100 + (R_Data[2] - 48)*10 + (R_Data[3] - 48);
			_ptm1al = ((130 - E_deg)*2+150)%256; _ptm1ah = ((130 - E_deg)*2+150)/256;
			delay(10);
		}
		if(R_Data[0] == 'F')
		{
			F_deg = (R_Data[1] - 48)*100 + (R_Data[2] - 48)*10 + (R_Data[3] - 48);
			_ptm2al = F_deg + 50; _ptm2ah = 0;
			delay(10);
		}
		Segment(R_Data[0]);
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
	LED = 0;
    Read_Data();
    _ur0f = 0;
    LED = 1;
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
	if(R_Data[kn] == '/' || kn > 9) // kn = 0;
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
	_st0on = 1; _stm0al = 190; _stm0ah = 0;
	_st1on = 1; _stm1al = 190; _stm1ah = 0;
	_st2on = 1; _stm2al = 170; _stm2ah = 0;
	_pt0on = 1; _ptm0al = 190; _ptm0ah = 0;
	_pt1on = 1; _ptm1al = 190; _ptm1ah = 0;
	_pt2on = 0; _ptm2al = 200; _ptm2ah = 0;
}

void time_setup()
{
	_stm0c0 = 0b00110000;	//
	_stm0c1 = 0b10101000;
	_stm0rp = 0x19; // => 19*256
	_stm0al = 400%256; _stm0ah = 1;
	
	_stm1c0 = 0b00110000;	//
	_stm1c1 = 0b10101000;
	_stm1rp = 0x19; // => 10*256
	_stm1al = 400%256; _stm1ah = 1;
	
	_stm2c0 = 0b00110000;	//
	_stm2c1 = 0b10101000;
	_stm2rp = 0x19; // => 10*256
	_stm2al = 400%256; _stm2ah = 1;
	
	_ptm0c0 = 0b00110000;
	_ptm0c1 = 0b10101000;
	_ptm0rpl = 0xfe; _ptm0rph = 0x07;
	_ptm0al = 400%256; _ptm0ah = 1;
	
	_ptm1c0 = 0b00110000;
	_ptm1c1 = 0b10101000;
	_ptm1rpl = 0xfe; _ptm1rph = 0x07;
	_ptm1al = 400%256; _ptm1ah = 1;
	
	_ptm2c0 = 0b00110000;
	_ptm2c1 = 0b10101000;
	_ptm2rpl = 0xfe; _ptm2rph = 0x07;
	_ptm2al = 160; _ptm2ah = 0;
}

void delay(unsigned short var)
{
	unsigned short i, j;
	for(i=0;i<var;i++)
		for(j=0;j<25;j++)
			GCC_NOP();
}