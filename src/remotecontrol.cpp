//***************************************************************************************
//  MSP430 Blink the LED Demo - Software Toggle P1.0
//
//  Description; Toggle P1.0 by xor'ing P1.0 inside of a software loop.
//  ACLK = n/a, MCLK = SMCLK = default DCO
//
//                MSP430x5xx
//             -----------------
//         /|\|              XIN|-
//          | |                 |
//          --|RST          XOUT|-
//            |                 |
//            |             P1.0|-->LED
//
//  J. Stevenson
//  Texas Instruments, Inc
//  July 2011
//  Built with Code Composer Studio v5
//***************************************************************************************

#include <msp430.h>
//#include "uart.h"
#define LED_OUTPUT_BIT BIT0
bool flag;

void TimerAConfigure()
{
	TACCR0 = 1;
	TACCTL0 = CCIE;
	TACTL = TASSEL1 + MC0 + TAIE;
}

void TimerConfigure()
{
    WDTCTL = WDTPW + WDTHOLD;
    BCSCTL1 |= BIT0 + BIT1 + BIT2 + BIT3;
    DCOCTL = BIT5;
    BCSCTL2 = SELS;
    BCSCTL3  = XCAP_3;

    while((LFXT1OF & BCSCTL3) != 0)
    {
    }
}

void IoPinConfigure()
{
    P1DIR |= LED_OUTPUT_BIT + BIT6; // Set P1.0 and P1.6 to output direction
    P1REN |= BIT3;
    //P1OUT |= BIT3;
}

// Two ISRs to double the sample rate
#pragma vector = TIMER0_A1_VECTOR
__interrupt void TimerA0ISR()
{
	// Read TAIV to clear the flag
	TAIV = TAIV;
	flag = false;
}

#pragma vector = TIMER0_A0_VECTOR
__interrupt void TimerA1ISR()
{
	// Read TAIV to clear the flag
	TAIV = TAIV;
	flag = false;
}
inline void delay(int i)
{
	for (volatile int j = 0; j < i; j++)
	{
	}
}

inline void wait(int bit)
{
	flag = true;

	while(flag)
	{
		delay(7);
		P1OUT^=bit;
	}
}

void printSeq(int *numberList, int length)
{
	_disable_interrupt();
	TimerConfigure();
	TimerAConfigure();
	IoPinConfigure();
	_enable_interrupt();
	for (int i = 0; i < length; i++)
	{
		P1OUT = (P1OUT&(~LED_OUTPUT_BIT))|((i+1)&1);
		for (int j = 0; j < numberList[i]; j++)
		{
			P1OUT ^= BIT6;
			wait((i+1)&1);
		}
	}
}

void dimUp()
{
	int numberList[] = {682, 220, 82, 220, 82, 370, 79, 220, 82, 220, 79, 367};
	const int length = 12;
	printSeq(numberList, length);
}

void dimDown()
{
	int numberList[] = {682, 223, 79, 220, 82, 370, 79, 295, 82, 69, 82, 439};
	const int length = 12;
	printSeq(numberList, length);
}

void turnOn()
{
	int numberList[] = {682, 220, 82, 220, 79, 295, 82, 144, 82, 69, 229, 514};
	const int length = 12;
	printSeq(numberList, length);
}

void turnOff()
{
	int numberList[] = {682, 220, 82, 220, 79, 72, 305, 69, 82, 220, 79, 147, 79, 364};
	const int length = 14;
	printSeq(numberList, length);
}

void remember()
{
	int numberList[] = {682, 220, 82, 220, 79, 298, 79, 144, 82, 69, 157, 69, 229, 288};
	const int length = 14;
	printSeq(numberList, length);
}


int main(void)
{
	WDTCTL = WDTPW + WDTHOLD;             // Stop watchdog timer

	int buttonCount = 0;
	for (;;)
	{
		bool buttonpressed = !((P1IN&BIT3)>0);
		if (buttonpressed)
		{
			buttonCount++;
			for (int i = 0; i<10; i++)
			{
				switch (buttonCount%5)
				{
					case 0:
						turnOn();
						break;
					case 1:
						turnOff();
						break;
					case 2:
						remember();
						break;
					case 3:
						dimUp();
						break;
					case 4:
						dimDown();
						break;
					default:
						turnOff();
				}
			}
		}
	}
}
