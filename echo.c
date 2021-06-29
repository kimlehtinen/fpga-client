/******************************************************************************
*
* Copyright (C) 2009 - 2014 Xilinx, Inc.  All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* Use of the Software is limited solely to applications:
* (a) running on a Xilinx device, or
* (b) that interact with a Xilinx device through a bus or interconnect.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
* XILINX  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
* WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
* OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
*
* Except as contained in this notice, the name of the Xilinx shall not be used
* in advertising or otherwise to promote the sale, use or other dealings in
* this Software without prior written authorization from Xilinx.
*
******************************************************************************/

// Original author: Konsta Mäenpänen
// Edited by: Kim Lehtinen

#include <stdio.h>
#include <string.h>

#include "lwip/err.h"
#include "lwip/tcp.h"
#if defined (__arm__) || defined (__aarch64__)
#include "xil_printf.h"
#endif

// DDR
#include "platform.h"
#include "xil_printf.h"
#include "xil_types.h"
#include "xil_cache.h"
#include "xil_io.h"
#include "xparameters.h"

#ifndef DDR_BASE_ADDR
#warning CHECK FOR THE VALID DDR ADDRESS IN XPARAMETERS.H, \
         DEFAULT SET TO 0x01000000
#define MEM_BASE_ADDR		0x01000000
#else
#define MEM_BASE_ADDR		(DDR_BASE_ADDR + 0x1000000)
#endif

#define TX_BUFFER_BASE		(MEM_BASE_ADDR + 0x00100000)
#define RX_BUFFER_BASE		(MEM_BASE_ADDR + 0x00300000)

#define DMA_BASE			XPAR_AXI_DMA_0_BASEADDR
#define MM2S_DMACR			0x00 // mm2s control
#define MM2S_SA				0x18 // mm2s source address
#define MM2S_SA_MSB			0x1C // ...and msb
#define MM2S_LENGTH			0x28 // mm2s transfer length
#define S2MM_DMACR			0x30 // s2mm control
#define S2MM_DMASR			0x34 // s2mm status
#define S2MM_DA				0x48 // s2mm destination address
#define S2MM_DA_MSB			0x4C // ...and msb
#define S2MM_LENGTH			0x58 // s2mm buffer length
#define PAK_LEN				4

#define BYTES_PER_PIXEL     4
#define PIXELS     			120000
// ./DDR

UINTPTR addr;
u32 * image_in;
u32 * image_out;
int img_idx = 0;

// u32 * img_ptr;

// Function declaration to avoid warning
int networking_start_server();

int transfer_data() {
	return 0;
}

void print_app_header()
{
#if (LWIP_IPV6==0)
	xil_printf("\n\r\n\r-----lwIP TCP echo server ------\n\r");
#else
	xil_printf("\n\r\n\r-----lwIPv6 TCP echo server ------\n\r");
#endif
	xil_printf("TCP packets sent to port 6001 will be echoed back\n\r");
}

err_t recv_callback(void *arg, struct tcp_pcb *tpcb,
                               struct pbuf *p, err_t err)
{
	/* do not read the packet if we are not in ESTABLISHED state */
	if (!p) {
		tcp_close(tpcb);
		tcp_recv(tpcb, NULL);
		return ERR_OK;
	}

	/* indicate that the packet has been received */
	tcp_recved(tpcb, p->len);

	/* echo back the payload */
	/* in this case, we assume that the payload is < TCP_SND_BUF */
	if ((tcp_sndbuf(tpcb) > p->len)) {
		xil_printf("REC\r\n");

		u8 * data = p->payload;

		// Get number of pixels
		u16 pixels_amount = p->len / BYTES_PER_PIXEL;
		if (pixels_amount % BYTES_PER_PIXEL != 0) {
			xil_printf("Warning: %d bytes received which is not divisible by %d!\r\n", p->len, BYTES_PER_PIXEL);
		}

		// Write directly to image_out which is the place in the memory where DMA starts reading from
		for (int i = 0; i < p->len; i += BYTES_PER_PIXEL) {
			image_out[img_idx/BYTES_PER_PIXEL] = (((u32) data[i]) << 24) | (((u32) data[i+1]) << 16) | (((u32) data[i+2]) << 8) | (data[i+3]);
			img_idx++;
		}
		Xil_DCacheFlush(); // Flush data caches.

		// if last chunks received
		if (img_idx == (int)PIXELS) {
			img_idx = 0; // reset img idx
			// 4. trigger transfer by setting length to MM2S_LENGTH
			addr = DMA_BASE + MM2S_LENGTH;
			Xil_Out32(addr, pixels_amount*4); // Length is in bytes.


			xil_printf("--- DMA Started! ---\r\n");
			// Start polling idle bit
			addr = DMA_BASE + S2MM_DMASR;

			u32 s2mm_status;
			while(!(s2mm_status = Xil_In32(DMA_BASE + S2MM_DMASR) & 0x1000)) {
				// check if bit 14 (error_irq) or halted (bit 0) are high in status
				if(s2mm_status & 0x4001 ) {
					xil_printf("Error in DMA. Stopping transmission! S2MM_DMA status was 0x%08x\r\n", s2mm_status);
					// Reset DMA by writing into s2mm_dma status register bit 2
					Xil_Out32((DMA_BASE + S2MM_DMACR), 0x4);
					pbuf_free(p); // deallocate memory before returning from function
					return ERR_MEM;
				}
			}

			u32 bytes = Xil_In32(DMA_BASE + S2MM_LENGTH);
			xil_printf("--- IRQ detected: %d bytes received! ---\r\n", bytes);
			Xil_DCacheFlush(); // Flush data caches.

			// Get number of actually received bytes
			u32 recv_len = Xil_In32(DMA_BASE + S2MM_LENGTH)/4;

			// Reset interrupt
			Xil_Out32(DMA_BASE + S2MM_DMASR, Xil_In32(DMA_BASE + S2MM_DMASR) | 0x1000);
			//Xil_Out32(DMA_BASE + S2MM_LENGTH, size*4); // This was not needed!!!


			// send response back to client
			// convert int values form dma back to rgb sequence
			// just like the original input

			// Reusing the data pointer, it is not needed anymore and we don't need to allocate more memory!
			// Also we know that it big enough always, because RX_DATA from network == TX_DATA to network!
			u32 rgb;
			for (int i=0, j=0; i< recv_len; i++, j+=BYTES_PER_PIXEL) {
				rgb = image_in[i];
				data[j] = (u8) ((rgb>>24)&0x0ff); // r
				data[j+1] = (u8) ((rgb>>16)&0x0ff); // g
				data[j+2] = (u8) ((rgb>>8) &0x0ff); // b
				data[j+3] = (u8) ((rgb) &0x0ff); // a
			}

			// test sending all image data back to client
			err = tcp_write(tpcb, image_in, (int)(PIXELS*BYTES_PER_PIXEL), 1);
		} else {
			int ok = 1;
			err = tcp_write(tpcb, &ok, 1, 1);
		}
	} else
		xil_printf("no space in tcp_sndbuf\n\r");

	/* free the received pbuf */
	pbuf_free(p);

	return ERR_OK;
}

err_t accept_callback(void *arg, struct tcp_pcb *newpcb, err_t err)
{
	static int connection = 1;

	/* set the receive callback for this connection */
	tcp_recv(newpcb, recv_callback);

	/* just use an integer number indicating the connection id as the
	   callback argument */
	tcp_arg(newpcb, (void*)(UINTPTR)connection);

	/* increment for subsequent accepted connections */
	connection++;

	return ERR_OK;
}


int networking_start_server()
{
	struct tcp_pcb *pcb;
	err_t err;
	unsigned port = 7;

	/* create new TCP PCB structure */
	pcb = tcp_new_ip_type(IPADDR_TYPE_ANY);
	if (!pcb) {
		xil_printf("Error creating PCB. Out of Memory\n\r");
		return -1;
	}

	/* bind to specified @port */
	err = tcp_bind(pcb, IP_ANY_TYPE, port);
	if (err != ERR_OK) {
		xil_printf("Unable to bind to port %d: err = %d\n\r", port, err);
		return -2;
	}

	/* we do not need any arguments to callback functions */
	tcp_arg(pcb, NULL);

	/* listen for connections */
	pcb = tcp_listen(pcb);
	if (!pcb) {
		xil_printf("Out of memory while tcp_listen\n\r");
		return -3;
	}

	/* specify callback to use for incoming connections */
	tcp_accept(pcb, accept_callback);

	xil_printf("TCP echo server started @ port %d\n\r", port);


			image_in = (u32 *) RX_BUFFER_BASE;
			image_out = (u32 *) TX_BUFFER_BASE;

			// 1. run/stop bit to 1
			addr = DMA_BASE + S2MM_DMACR;
			Xil_Out32(addr, Xil_In32(addr) | 0x1);

			// 2. enable interrupts <- No interrupts, using polling of IRQ bit in status register

			// 3. destination address for received data:
			addr = DMA_BASE + S2MM_DA;
			Xil_Out32(addr, RX_BUFFER_BASE);

			// 4....
			// 5. start receiving
			addr = DMA_BASE + S2MM_LENGTH;

			Xil_Out32(addr, PIXELS*4);
			addr = DMA_BASE + MM2S_DMACR;
			// 1. Start mm2s channel:
			Xil_Out32(addr, Xil_In32(addr) | 0x1);
			// 2. No interrupts...
			// 3. set source address (TX_BUFFER)
			addr = DMA_BASE + MM2S_SA;
			Xil_Out32(addr, TX_BUFFER_BASE);

	return 0;
}
