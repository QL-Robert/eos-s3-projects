---
title: "USBserialport_FPGA_register_map"
source_file: "qorc-sdk/s3-gateware/usb2serial/docs/USBserialport_FPGA_register_map.pdf"
pages: 2
sha256: 3819c771f59cc3ea4a7fc748d8f9b4a5b90710076c49490f8a442d2e64ae48ee
---

# USBserialport_FPGA_register_map

# **QuickFeather FPGA – USB Serial Port** 

# **Register Map** 

Offsets shown are for the FPGA base address, as seen by the M4 (I believe this to be 0x4002_0000). 

Note: Registers may be accessed 8, 16 or 32 bits at a time. To avoid confusion, 16-bit accesses should be 16-bit aligned (offsets 0x0, 0x2, 0x4, 0x6, 0x8, etc. only), and 32-bit accesses should be 32-bit aligned (offsets 0x0, 0x4, 0x8, 0xC only). 

The least-significant byte (LSB) is always on the “right”, so a 32-bit register at offset 0x00 has bits [7:0] = offset 0x00, bits [15:8] = offset 0x01, etc. 

|**Offset**|**Name**|**Bits**|**R/W **|**Default Val**|**Description**|
|---|---|---|---|---|---|
|0x00|Device ID|[31:0]|R|0x0000A5BD|Device ID.|
|0x04|Revision Number|[31:0]|R|_<br>0x0000_0200|Revision Number.<br>0x0000_0100: initial release.<br>0x0000_0200: Added support for multi-byte packets (up to<br>8 bytes) from device to host over USB (previously only<br>1 byte per packet). Added support for Clock Select (see<br>register offset 0x0C).|
|0x08|Scratch Register|[15:0]|R/W|0x0000|Scratch Register. May be used to test out FPGA register<br>accesses.|
|0x0A|Reserved|[15:0]|R|0x0000|Reserved,always 0.|
|0x0C|Clock Control|[0]|R/W|0|Bit 0: Clock select<br>0 = [defaut] Use raw eFPGA clock (the HSOSC must be set<br>to 48MHz).<br>1 = Divide by 1.5 (the HSOSC must be set to 72MHz).<br>This allows the HSOSC, and therefore the M4 clock, to be<br>run at a faster rate for better performance, while keeping<br>the USB clock at 48MHz.|
||||||Bits 31 downto 1: reserved,always 0.|
|0x10|USB PID|[15:0]|R/W|0x6140|Bits [15:0]: USB ProductID (PID).<br>Bits[31:16]: Reserved,always 0.|
|0x14 –<br>0x3C|Reserved|[31:0]|R|N/A|Reserved.|
|0x40|USB2M4 FIFO Flags|[3:0]|R|0x0|Pop flag:<br>0b0000 = empty<br>0b0001 = 1 entry in FIFO<br>0b0010 = at least 2 entries<br>0b0011 = at least 4 entries<br>0b0100 = at least 8 entries<br>0b0101 = at least 16 entries<br>0b0110 = at least 32 entries<br>0b1000 = less than 1/4 to 64 entries<br>0b1101 = 1/4 or more full<br>0b1110 = 1/2 or more full<br>0b1111 = full<br>others  = reserved|
|0x41 –<br>0x43|Reserved||R|0x0|Reserved, always 0.|
|0x44|USB2M4 FIFO Read<br>Data|[7:0]|R|N/A|USB-to-M4 FIFO Read Data.|
|0x45 –<br>0x47|Reserved||R|0x0|Reserved, always 0.|
|0x80|M42USB FIFO Flags|[3:0]|R|0x1|Push flag:<br>0b0000 = full<br>0b0001 = empty<br>0b0010 = room for more than 1/2<br>0b0011 = room for more than 1/4<br>0b0100 = room for less than 1/4 to 64<br>0b1010 = room for 32 to 63<br>0b1011 = room for 16 to 31<br>0b1100 = room for 8 to 15<br>0b1101 = room for 4 to 7<br>0b1110 = room for at least 2|



||||||0b1111 = room for at least 1<br>others  = reserved|
|---|---|---|---|---|---|
|0x81 –<br>0x83|Reserved||R|0x0|Reserved, always 0.|
|0x84|M42USB FIFO Write<br>Data|[7:0]|W|N/A|M4-to-USB FIFO Write Data.|
|0x85 –<br>0x87|Reserved||R|N/A|Reserved.|
|0x88 –<br>0xBC|Reserved|[31:0]|R|N/A|Reserved.|
|0xC0|USB2M4 FIFO Data<br>Interrupt Enable|[0]|R/W|0x0|USB-to-M4 FIFO Data Interrupt Enable.<br>0 = disable interrupt to M4 when U2M FIFO data is<br>available.<br>1 = enable interrupt to M4 when U2M FIFO data is<br>available.|
|0xC1 –<br>0xC3|Reserved||R|0x0|Reserved, always 0.|



