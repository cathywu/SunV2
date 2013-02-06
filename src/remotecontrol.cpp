//***************************************************************************************
//  MSP430 Lutron IR Dimmer Remote Control
//
//  Description: Operate the dimmer from your computer.
//
//  Usage:
//  - Flash the firmware
//  - Make sure the IR LED is within a few feet and pointed at the IR reciever
//    of the dimmer
//  - $ screen /dev/ttyACM0 9600
//  - Use keys ASDW to control the dimmer
//
//  @author jasondu, cathywu
//***************************************************************************************

#include <msp430.h>
#include <stdint.h>

#include "include/uart.h"
#define LED_OUTPUT_BIT BIT0
bool flag;

/*
 * Reset master timer attributes to default values
 */
void timer_deconfigure()
{
    DCOCTL = 0x60;
    BCSCTL1 = 0x87;
    BCSCTL2 = 0x00;
    BCSCTL3 = 0x04;
}

/*
 * Configure master clock attributes
 */
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

/*
 * Configure Timer1 for dimming
 */
void TimerAConfigure()
{
	TA1CCR0 = 1;
	TA1CCTL0 = CCIE;
	TA1CTL = TASSEL1 + MC0 + TAIE;
}

/*
 * Disable Timer1
 */
void TimerADisable()
{
	TA1CCTL0 &= ~CCIE;
	TA1CTL &= ~TAIE;
}

/*
 * Configure I/O for dimming
 */
void IoPinConfigure()
{
    P1DIR |= LED_OUTPUT_BIT + BIT6; // Set P1.0 and P1.6 to output direction
    P1REN |= BIT3;
    //P1OUT |= BIT3;
}

/*
 * Deconfigure I/O for dimming
 */
void IoPinDeconfigure()
{
    P1DIR &= ~(LED_OUTPUT_BIT + BIT6); // Clear P1.0 and P1.6
    P1REN &= ~BIT3;
}

// Two ISRs to double the sample rate
#pragma vector = TIMER1_A1_VECTOR
__interrupt void TimerA0ISR()
{
	// Read TA1IV to clear the flag
	TA1IV = TA1IV;
	flag = false;
}

#pragma vector = TIMER1_A0_VECTOR
__interrupt void TimerA1ISR()
{
	// Read TA1IV to clear the flag
	TA1IV = TA1IV;
	flag = false;
}

/*
 * Software delay
 */
inline void delay(int i)
{
	for (volatile int j = 0; j < i; j++)
	{
	}
}

/*
 * Software wait
 */
inline void wait(int bit)
{
	flag = true;

	while(flag)
	{
		delay(7);
		P1OUT^=bit;
	}
}

/*
 * Configure environment for dimming, send a dimming instruction, then undo
 * configuration.
 */
void printSeq(int *numberList, int length)
{
	timer_deconfigure();
	TimerConfigure();
	TimerAConfigure();
	IoPinConfigure();
	_enable_interrupts();
	for (int i = 0; i < length; i++)
	{
		P1OUT = (P1OUT&(~LED_OUTPUT_BIT))|((i+1)&1);
		for (int j = 0; j < numberList[i]; j++)
		{
			P1OUT ^= BIT6;
			wait((i+1)&1);
		}
	}
	_disable_interrupts();
	timer_deconfigure();
	TimerADisable();
	IoPinDeconfigure();
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
	WDTCTL = WDTPW + WDTHOLD; // Stop watchdog timer
	uart_timer_configure();
	uart_init();
    _enable_interrupts();

    uart_puts("\n\r***************\n\r");
    uart_puts("MSP430 SunV2\n\r");
    uart_puts("***************\n\r\n\r");

    uint8_t c;

    // Timeshare between UART and dimming
    while(1) {
        if(uart_getc(&c)) {
            if(c == '\r') {
                 uart_putc('\n');
                 uart_putc('\r');
            } else {
                uart_putc('[');
                uart_putc(c);
                uart_putc(']');
            
                // Clear UART configuration
                _disable_interrupts();
                timer_deconfigure();
                uart_disable();
                uart_timerA_disable();
                switch (c)
                {
                    case 'w':
                        turnOn();
                        break;
                    case 's':
                        turnOff();
                        break;
                    case 'r':
                        remember();
                        break;
                    case 'd':
                        dimUp();
                        break;
                    case 'a':
                        dimDown();
                        break;
                }
                // UART configuration
                art_init();
                timer_deconfigure();
                uart_timer_configure();
                uart_timerA_enable();
                _enable_interrupts();
            }
        }
    }
}
