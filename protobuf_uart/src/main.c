/*
 * Copyright (c) 2022 Libre Solar Technologies GmbH
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>

#include <string.h>

/* change this to any other UART peripheral if desired */
#define UART_DEVICE_NODE DT_CHOSEN(zephyr_shell_uart)

static const struct device *const uart_dev = DEVICE_DT_GET(UART_DEVICE_NODE);


/*
 * Print a null-terminated string character by character to the UART interface
 */
void print_uart(char *buf)
{
	int msg_len = strlen(buf);
	for (int i = 0; i < msg_len; i++) {
		uart_poll_out(uart_dev, buf[i]);
	}
}

int read_uart(char * buf, size_t n) {
	if (!device_is_ready(uart_dev)) {
		printk("UART device not found!\n");
		return ENODEV;
	}
	int i=0;
	while (true) {
		// if at max length, terminate and return
		if (i >= n - 1) {
			buf[n - 1] = '\0';
			return 0;
		}

		// read a byte
		int ret = uart_poll_in(uart_dev, &buf[i]);

		// if no data, idle, then continue
		if (ret != 0) {
			k_busy_wait(10);
			continue;
		}

		// if character is line end, terminate string
		if ((buf[i] == '\n' || buf[i] == '\r') && i > 0) {
			/* terminate string */
			buf[i] = '\0';
			return 0;
		}
		// next character
		i++;
	}
}

#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

#include <pb_encode.h>
#include <pb_decode.h>
#include "src/simple.pb.h"

bool encode_message(uint8_t *buffer, size_t buffer_size, size_t *message_length)
{
	bool status;

	/* Allocate space on the stack to store the message data.
	 *
	 * Nanopb generates simple struct definitions for all the messages.
	 * - check out the contents of simple.pb.h!
	 * It is a good idea to always initialize your structures
	 * so that you do not have garbage data from RAM in there.
	 */
	SimpleMessage message = SimpleMessage_init_zero;

	/* Create a stream that will write to our buffer. */
	pb_ostream_t stream = pb_ostream_from_buffer(buffer, buffer_size);

	/* Fill in the lucky number */
	message.lucky_number = 13;
	for (int i = 0; i < 8; ++i) {
		message.buffer[i] = (uint8_t)(i * 2);
	}

	/* Now we are ready to encode the message! */
	status = pb_encode(&stream, SimpleMessage_fields, &message);
	*message_length = stream.bytes_written;

	if (!status) {
		printk("Encoding failed: %s\n", PB_GET_ERROR(&stream));
	}

	return status;
}

bool decode_message(uint8_t *buffer, size_t message_length)
{
	bool status;

	/* Allocate space for the decoded message. */
	SimpleMessage message = SimpleMessage_init_zero;

	/* Create a stream that reads from the buffer. */
	pb_istream_t stream = pb_istream_from_buffer(buffer, message_length);

	/* Now we are ready to decode the message. */
	status = pb_decode(&stream, SimpleMessage_fields, &message);

	/* Check for errors... */
	if (status) {
		/* Print the data contained in the message. */
		printk("Your lucky number was %d!\n", (int)message.lucky_number);
		printk("Buffer contains: ");
		for (int i = 0; i < 8; ++i) {
			printk("%s%d", ((i == 0) ? "" : ", "), (int) message.buffer[i]);
		}
		printk("\n");
	} else {
		printk("Decoding failed: %s\n", PB_GET_ERROR(&stream));
	}

	return status;
}

void main(void)
{
	if (!device_is_ready(uart_dev)) {
		printk("UART device not found!\n");
		return;
	}

	/* This is the buffer where we will store our message. */
	uint8_t buffer[SimpleMessage_size];
	size_t message_length;

	/* Encode our message */
	if (!encode_message(buffer, sizeof(buffer), &message_length)) {
		return;
	}

	/* Now we could transmit the message over network, store it in a file or
	 * wrap it to a pigeon's leg.
	 */

	/* But because we are lazy, we will just decode it immediately. */
	decode_message(buffer, message_length);

	char rx_buf[8];

	while (true) {
		printk("reading uart\n");
		read_uart(rx_buf, 8);
		printk("finished reading\n");
		print_uart(rx_buf);
	}
}
