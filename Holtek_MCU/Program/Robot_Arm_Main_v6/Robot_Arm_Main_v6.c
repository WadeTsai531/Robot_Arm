#include "HT66F2390.h"

// UART
#define FH 16000000
#define BR 38400

unsigned char R_Data[10];
unsigned char Data[10];
unsigned short kn = 0;

void UART_Setup();
void Read_Data();

// Servo 
#define Servo_deg_0 256 // fsys=16MHz 128, fsys=8MHz 64
void timer_setup();
void servo_setup();

// Step Motor
#define PUL _pd3
#define PULC _pdc3
#define PULU _pdpu3

#define DIR _pd4
#define DIRC _pdc4
#define DIRU _pdpu4

#define ENA _pd5
#define ENAC _pdc5
#define ENAU _pdpu5

#define Sen _pd6
#define SenC _pdc6
#define SenU _pdpu6

#define LED _pg0
#define LEDC _pgc0

void ptm_setup();
void ptm_delay(unsigned int tm);

void motor_deg(unsigned short deg, unsigned int time);
void motor_callb();

void delay(unsigned short var);

void main()
{
	_wdtc = 0b10101011;
	
	_scc = 0b00000001;
	_hircc = 0b00001011;
	
	// UART Setup
	UART_Setup();
	
	// Servo Setup
	servo_setup();
	
	// Step Motor Setup
	ptm_setup();

	DIRC = 0;
	ENAC = 0;
	PULC = 0;
	SenC = 1;
	SenU = 1;
	
	// Step Motor Reset
	motor_callb();
	DIR = 1;
	motor_deg(360, 800);
	delay(5000);
	ENA = 1;
	
	// Other Setup
	LEDC = 0;
	LED = 1;
	
	unsigned short A_deg, B_deg, C_deg, D_deg, E_deg, F_deg;
	A_deg = B_deg = C_deg = D_deg = E_deg = F_deg = 0;
	unsigned short clear = 0;
	unsigned short run = 0;
	
	while(1)
	{
		// --------------------- Servo Motor --------------------------
		if(R_Data[0] == 'A') // Thumb
		{
			A_deg = (R_Data[1] - 48)*100 + (R_Data[2] - 48)*10 + (R_Data[3] - 48);
			_stm0rp = A_deg / 18 + 20;
			_stm0al = (A_deg + Servo_deg_0)%256; _stm0ah = (A_deg + Servo_deg_0)/256;
			delay(1);
		}
		if(R_Data[0] == 'B') // Index Finger
		{
			B_deg = (R_Data[1] - 48)*100 + (R_Data[2] - 48)*10 + (R_Data[3] - 48);
			_stm1rp = B_deg / 18 + 20;
			_stm1al = (B_deg + Servo_deg_0)%256; _stm1ah = (B_deg + Servo_deg_0)/256;
			delay(1);
		}
		if(R_Data[0] == 'C') // Middle Figger
		{
			C_deg = (R_Data[1] - 48)*100 + (R_Data[2] - 48)*10 + (R_Data[3] - 48);
			_stm2rp = C_deg / 18 + 20;
			_stm2al = (C_deg + Servo_deg_0)%256; _stm2ah = (C_deg + Servo_deg_0)/256;
			delay(1);
		}
		if(R_Data[0] == 'D') // Ring Figger
		{
			D_deg = (R_Data[1] - 48)*100 + (R_Data[2] - 48)*10 + (R_Data[3] - 48);
			_ptm0rpl = 0; _ptm0rph = D_deg / 18 + 20;
			_ptm0al = (D_deg + Servo_deg_0)%256; _ptm0ah = (D_deg + Servo_deg_0)/256;
			delay(1);
		}
		if(R_Data[0] == 'E') // Pinky
		{
			E_deg = (R_Data[1] - 48)*100 + (R_Data[2] - 48)*10 + (R_Data[3] - 48);
			_ptm1rpl = 0; _ptm1rph = E_deg / 18 + 20;
			_ptm1al = (E_deg + Servo_deg_0)%256; _ptm1ah = (E_deg + Servo_deg_0)/256;
			delay(1);
		}
		
		if(R_Data[0] == 'F') // Arm
		{
			F_deg = (R_Data[1] - 48)*100 + (R_Data[2] - 48)*10 + (R_Data[3] - 48);
			_ptm2rpl = 0; _ptm2rph = F_deg / 20 + 25;
			_ptm2al = (F_deg + Servo_deg_0)%256; _ptm2ah = (F_deg + Servo_deg_0)/256;
			delay(1);
		}
		
		// ---------------------- Step Motor --------------------------
		if(R_Data[0] == 'L')
		{
			LED = 0;
			ENA = 0;
			DIR = 1;
			delay(1);
		}
		if(R_Data[0] == 'S')
		{
			LED = 1;
			ENA = 1;
			delay(1);
		}
		if(R_Data[0] == 'R')
		{
			ENA = 0;
			DIR = 0;
			delay(1);
		}
		
		// All Motor Reset
		if(R_Data[0] == 'K')
		{
			_stm0al = Servo_deg_0%256; _stm0ah = Servo_deg_0/256;
			_stm1al = Servo_deg_0%256; _stm1ah = Servo_deg_0/256;
			_stm2al = Servo_deg_0%256; _stm2ah = Servo_deg_0/256;
			_ptm0al = Servo_deg_0%256; _ptm0ah = Servo_deg_0/256;
			_ptm1al = Servo_deg_0%256; _ptm1ah = Servo_deg_0/256;
			_ptm2al = (Servo_deg_0 + 10)%256; _ptm2ah = (Servo_deg_0 + 10)/256;
			
			motor_callb();
			DIR = 1;
			motor_deg(360, 800);
			delay(5000);
			ENA = 1;
		}
		
		for(run=0;run<9;run++)
		{
			PUL = 0;
			ptm_delay(1300);
			PUL = 1;
			ptm_delay(1300);
		}
	}
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
	_u0cr2 = 0b01100100;
	_brg0 = FH/((unsigned long)16*BR) - 1;
	_ur0e = 1;
	_ur0f = 0;
	_mf5e = 1;
	_emi = 1;
}

void Read_Data()
{
	while(_ridle0 == 0);
	R_Data[kn] = _txr_rxr0;
	if(R_Data[kn] == '/' || kn > 9) kn = 0;
	else kn++;
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
	_ptm2rpl = 0; _ptm2rph = 0x1e;
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

void ptm_setup()
{
	_ptm3c0 = 0b00000000;
	_ptm3c1 = 0b11000001;
	_ptm3ae = 1;
	_ptm3af = 0;
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

void motor_callb()
{
	ENA = 0;
	DIR = 0;
	while(Sen)
	{
		PUL = 0;
		ptm_delay(800);
		PUL = 1;
		ptm_delay(800);
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