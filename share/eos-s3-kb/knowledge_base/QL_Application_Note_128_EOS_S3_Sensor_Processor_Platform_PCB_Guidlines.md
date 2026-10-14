---
title: "QuickLogic ArcticLink III VX and BX CSSPs \u2013\u2014 PCB Layout Guidelines"
source_file: "QL Application Note 128 EOS S3 Sensor Processor Platform PCB Guidlines.pdf"
pages: 9
sha256: 8719b9f4a7e0683cbb85999a14adc99d40bd213a6ca89364955107ce1fcf39a9
---

# QuickLogic ArcticLink III VX and BX CSSPs –— PCB Layout Guidelines

# **QuickLogic**<sup>**®**</sup> **EOS S3 Sensor Processing Platform PCB Layout Guidelines** <mark>SS</mark> 

**• • • • • • QuickLogic Application Note 128** 

### **Introduction** 

This document provides guidelines for designing a printed circuit board (PCB) that includes the QuickLogic EOS S3 Sensor Processing Platform. 

When designing a PCB with an EOS S3 Sensor Processing Platform, extreme care must be given to the following areas: 

- Device interface signals: clock routing and other data lines that run between devices on the PCB. 

- Power going into the device from the connector: the power lines to the device must be filtered to pass only low frequency signals of less than 100 kHz. The ground signals must have returned current during data transmission. 

- External clock circuit. 

- Differential pair signals: impedance and length matching. 

This document is divided into two sections: a generic layout and a specific layout for EOS S3 Sensor Processing Platform. 

### **Generic Layout Guidelines** 

The following generic guidelines are from QuickLogic for a board design that contains an EOS S3 Sensor Processing Platform. PCB designers should consult internal PCB design rules and recommendations, as well as other device manufacturers, to produce a working PCB. 

Important PCB design elements include: 

- Type of circuit (analog, digital, etc.) 

- Board size 

- Number of layers 

- Pad stack sizes 

- Hole sizes 

- Layer thickness 

- Board thickness 

- External connections 

<u>www.quicklogic.com</u> **1** ••• ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Sensor Processing Platform PCB Layout Guidelines Rev. A_** 

- Mounting holes 

- Supply and ground layer thickness 

- Component details with specifications 

Important design rules are: 

- Power distribution and coupling 

- Critical signal paths 

- IR [Current (I) x Resistance (R)] drops in signal and power traces 

- Impedance control 

- Pad/land geometries 

- Trace width/spacings 

- Plated/unplated hole sizes 

- Part placement constraints 

- Layer assignments and routing constraints 

- Heat-removal paths 

- Test requirements 

#### **Partitioning** 

The following guidelines are recommended for system partitioning: 

- Divide the system into subsystems for placement. The division is used for layout partitioning of circuitries. Group components belonging to a functional block together. 

- Isolate sensitive circuits (such as clocks and analog supplies) from noisy sources (such as high transition signals and power regulators). 

- Separate analog power supplies from digital power supplies. 

#### **Placement** 

A system with an EOS S3 Sensor Processing Platform is comprised of a set of interacting elements responding to inputs to produce outputs. Good placement for logical data flow is important to keep the number of layers to a minimum. 

The following guidelines are recommended for placement of components: 

- For highly-sensitive circuits, place the critical components first to produce minimum trace-length. 

- For less-critical circuits, arrange the components in the order of the signal flow to minimize the overall connection length. 

- For components that have many connecting points, place these components first and group the remaining ones around them. 

- For components with a fixed position (such as connectors), place these components first followed by components that are connected to the fixed components. 

**2** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Sensor Processing Platform PCB Layout Guidelines Rev. A_** 

- Place the larger components (such as main devices) first. Place the smaller components (such as capacitors and resistors) between the larger components. 

- Place components in rows or columns for good viewing. 

- Place decoupling capacitors as close as possible (preferably adjacent) to the power pins of the device for maximum effectiveness. 

#### **Routing** 

The following guidelines are recommended for routing: 

- Select the shortest interconnection length, especially for high frequency circuits (see **Figure 1** ). 



<!-- Start of picture text -->
Figure 1: Shortest Tracing Examples<br><!-- End of picture text -->



<!-- Start of picture text -->
Not Recommeded Recommended<br>a >o<br>~ L. ON<br>oN KR,<br><!-- End of picture text -->

- Place traces with a minimum angle of 60 degrees (see **Figure 2** ). Figure 2: Trace Angle Examples 

- o— o— o— 

- • Place parallel traces at the same angle to ensure uniformity, and eliminate the variance in the traces spacing. • Distribute the spacing equally when one or more traces pass between pads or other conductive areas. To ~~<u><mark>76 OE</mark></u>~~ obtain maximum spacing, place traces perpendicular to a narrow passage. 

- Place parallel traces at the same angle to ensure uniformity, and eliminate the variance in the traces spacing. 

- Distribute traces widely over the available area to avoid issues in manufacturing (i.e., do not space parallel running traces closely). 

- Avoid unwanted bunching. 

**<mark>PRELIMINARY</mark>** 

• • • ••• 

© 2016 QuickLogic Corporation 

<u>www.quicklogic.com</u> **3** 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Sensor Processing Platform PCB Layout Guidelines Rev. A_** 

- Match signal impedance for all high-speed signals. 

- Ensure that power lines are as thick as possible. Check the current requirements for the line. 

- Ensure that the ground traces are always two times wider than the power traces. 

- Distribute the routing pattern equally between the various layers of the PCB to achieve uniform plating in the manufacturing process. 

- Route adjacent signal layers orthogonally to each other. 

- Place ground or power planes to isolate signal layers when possible. 

- Route traces directly to a connector pad without line branching to prevent reflections and impedance changes. 

- Use curves or two 45º turns to avoid minor line reflections. 

- Avoid line-width changes that can affect trace impedance. 

- Make pads with soldered signal traces tear-dropped at the pad junction. 

#### **Power** 

Switching power regulators are noisy and can cause noise-coupling issues if placed close to sensitive areas on the PCB. Keep these circuits away from the sensitive traces, clock circuits and connectors. 

#### **Clock Routing** 

The following guidelines are recommended for clock routing: 

- Use series terminator resistors to eliminate reflections. Obtain the final value by looking at the waveform using a high-speed oscilloscope to obtain minimum distortion on the signal. 

- Use the 3W spacing rule when routing clock traces from one device to another to minimize cross-talk (see **Figure 3** ). 



<!-- Start of picture text -->
Figure 3: Clock Traces Spacing<br><!-- End of picture text -->



<!-- Start of picture text -->
—_ w™+>.<br>|<br>}i<br>|<br>—— ——— =<br>|<br>Trace +— w—><br>i |<br><!-- End of picture text -->

- Do not use 90º angles for bending. 

- Include guard traces (ground) to surround the clock signal if possible. 

- Place clock routing on an internal layer without stubs. 

## **<mark>PRELIMINARY</mark>** 

**4** <u>www.quicklogic.com</u> •• •••• 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Sensor Processing Platform PCB Layout Guidelines Rev. A_** 

#### **High-Speed Differential Pair** 

The following guidelines are recommended for high-speed input and output signal layout: 

- For low-swing signals (<300 mV), place the as close to the driving source as possible (such as the flexible printed circuit or processor) to minimize the cross-talk, impedance mismatch, and differential noise pick-up. Keep the total trace-length <4 inches. 

- Traces must always be matched lengths. 

- Route the pair as close together as possible for noise rejection. 

- Trace impedance must be 100 Ohm ± 10% to produce a 50 Ohm ± 10% pair. 

- Signals must not have extra components to maintain signal integrity. 

#### **Vias** 

The following guidelines are recommended for via usage: 

- Increase the clearance around the via to minimize capacitance. 

- Minimize the number of vias per signal connection. Each via introduces discontinuities in the signal transmission line and increases the chance to pick up interference from other layers of the PCB. 

- Avoid using a through-hole via as a test point if possible. 

#### **Isolations** 

Isolation is referred to as the separation between power and ground planes. The following guidelines are recommended for isolation: 

- Isolate between digital and analog power planes. 

- Do not route traces across planes (see **Figure 4** ). This can cause a broken RF path for the return signal, which can result in severe EMI issues. Route high-speed sensitive signals parallel to solid power or ground planes. 

Figure 4: Routing Over Isolation Planes 



<!-- Start of picture text -->
Not Recommended Recommended<br>PLANE 1 PLANE 1<br>0 0 0 0<br>1 a1 Vcc 1 b1 5 1 a1 Vcc 1 b1 5 1 a1 Vcc 1 b1 5 1 a1 Vcc 1 b1 5<br>2 a2 b2 6 2 a2 b2 6 2 a2 b2 6 2 a2 b2 6<br>3 a3 b3 7 3 a3 b3 7 3 a3 b3 7 3 a3 b3 7<br>4 a4 GND b4 8 4 a4 GND b4 8 4 a4 GND b4 8 4 a4 GND b4 8<br>0 0 0 0<br>0 0<br>1 a1 Vcc 1 b1 5 1 a1 Vcc 1 b1 5<br>2 a2 b2 6 2 a2 b2 6<br>3 a3 b3 7 3 a3 b3 7<br>4 a4 GND b4 8 4 a4 GND b4 8<br>0 0<br>PLANE 2 PLANE 2<br><!-- End of picture text -->



<!-- Start of picture text -->
PRELIMINARY<br><!-- End of picture text -->

<u>www.quicklogic.com</u> **5** • • • ••• 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Sensor Processing Platform PCB Layout Guidelines Rev. A_** 

- Fill unused areas of a layer with copper and connect to ground planes using vias. 

- Do not overlap planes between layers. These overlap areas can produce unwanted capacitance that passes RF emissions between the planes. 

- Do not route signals over the slot-plane (see **Figure 5** ). 

Figure 5: Routing Over Cut-Out Area Examples 



<!-- Start of picture text -->
/] | \ re Retum RF Return<br>¢+J | | \\_Surrencurrent>) e Current2)<br>Slot in image Plane Slot in image Plane<br><!-- End of picture text -->

#### **Electrostatic Discharge (ESD)** 

The following guidelines are recommended for ESD: 

- Provide ESD protection for PCB handling. The typical provision is an ESD strip around the board. The strip must connect to the PCB ground plane. 

- Apply ESD protection to all connectors. The ground of the connector body must be connected to the PCB ground plane. 

### **Layout Guidelines Specific to the EOS S3 Sensor Processing Platform** 

#### **Critical Signals** 

The following guidelines are recommended for the layout of critical signals: 

- Keep the EOS S3 Sensor Processing Platform reference clock circuits as close to the device as possible. 

- Follow the minimum spacing rules for reset lines from adjacent signals on the same and adjacent layers. 

- Keep reset lines away from noisy sources (such as long clock traces, high energy signals and fast transition edges signals). 

- Keep interrupt lines away from noisy sources (such as long clock traces, high energy signals and fast transition edges signals). 

#### **Vias** 

Use via-in-pad for the layout of vias and device connections. 

**6** <u>www.quicklogic.com</u> •• •••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Sensor Processing Platform PCB Layout Guidelines Rev. A_** 

#### **Power** 

The following guidelines are recommended for the layout of power: 

- Use the power island or plane as much as possible. 

- If using a power trace to connect to the EOS S3 Sensor Processing Platform power pins, make the trace as wide as possible, and follow current requirements to prevent excessive IR drop. 

- Since the number of capacitors for the design is at a minimum, place all of the capacitors as close to the power pins as possible. 

### **Reducing the Number of PCB Layers** 

The cost-reduction requirements common to PCB design and manufacturing requires the PCB designer to look for a solution to produce PCBs at the lowest cost possible. This section discusses areas that a PCB designer needs to consider when using an EOS S3 Sensor Processing Platform in the system. 

There are several factors that contribute to the cost of a bare PCB: 

- Volume: the number of PCBs per run. 

- PCB size: the smaller, the less costly. 

- PCB material: readily available material is less expensive. 

- Number of layers: thickness reduction and quicker manufacturing time. 

- PCB shapes: odd shape and slots require more processes. 

- Copper size and spacing: the dimension of pads and spacing demand better PCB producing equipment. 

- Via: current PCB technology is capable to handle more advanced via types: blind, buried, etc. These require more manufacturing time which translates into a more costly PCB. 

Work with the PCB manufacturer to understand the trade-offs between PCB cost and these factors before finalizing PCB specifications. 

#### **Device Placement** 

Placement of devices is critical for good flow to nets routing, thus reducing the number of layers required. The placement must follow the flow of data between components. Critical components must be placed first, followed by support components such capacitors. Less critical components are placed last. 

Make sure the device orientation is correct. If the device is in the correct location, but with the wrong orientation, the intended result may not be achieved. Always choose the orientation that has the most signals flowing in the same direction. Crossing signals require multiple layers to complete routing. 

#### **Via Technology** 

While advanced via technologies are more expensive that regular thru-hole via, they can be used to improve layers routing. Use blind via and/or buried via for a design that has constraints on PCB size (thus requiring routing of a signal under the EOS S3 Sensor Processing Platform). Using via-in-pad for EOS S3 Sensor Processing Platform pins that need internal layer connections. 

• • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

<u>www.quicklogic.com</u> **7** 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Sensor Processing Platform PCB Layout Guidelines Rev. A_** 

#### **Power and Ground Planes** 

Dedicated power and ground planes yield the best impedance control and zero IR drop. However, these dedicated planes increases the thickness, and layers count for the PCB. 

To reduce the need for a dedicated power plane, use thick traces for power routing. The thickness must meet the current requirements and be as wide as space allows. 

To reduce the need for a dedicated ground plane, provide guards around the traces for each layer and fill the rest of the layer with copper (see **Figure 6** ). Where possible, provide vias to tie these ground islands on each layer together. While this grounding method is not effective for EMI and trace impedance control, it provides plenty of grounding for the logics. 

Figure 6: Fill-In Ground Examples 



#### **PCB Size** 

While increasing the board size can increase the cost of the PCB, this increase can be offset by the reduction of layers. Increasing board size provides additional routing areas and room for parts placement. 

### **Contact Information** 

Phone: (408) 990-4000 (US) (647) 367-1014 (Canada) +(44) 1932-21-3160 (Europe) +(886) 26-603-8948 (Taiwan) +(86) 21-5179-8474 (China) E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> Internet: <u>www.quicklogic.com</u> 

•• •••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

**8** <u>www.quicklogic.com</u> 

**_QuickLogic_**<sup>**_®_**</sup> **_EOS S3 Sensor Processing Platform PCB Layout Guidelines Rev. A_** 

### **Revision History** 

|**Revision**<br>**Date**|**Originator and Comments**|
|---|---|
|A<br>June 2016|AnthonyLe and Kathleen Bylsma|



### **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

### **Copyright and Trademark Information** 

Copyright © 2016 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic is a registered trademark, and the EOS design and QuickLogic logo are trademarks of QuickLogic. Other trademarks are the property of their respective companies. 

<u>www.quicklogic.com</u> **9** • • • ••• 

**<mark>PRELIMINARY</mark>** 

© 2016 QuickLogic Corporation 

