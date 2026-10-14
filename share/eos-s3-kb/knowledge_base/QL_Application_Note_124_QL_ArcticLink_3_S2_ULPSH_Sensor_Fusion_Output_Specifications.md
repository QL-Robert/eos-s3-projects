---
title: "QuickLogic\u00ae ArcticLink\u00ae 3 S2 ULPSH Sensor Fusion Output Specifications"
source_file: "QL Application Note 124 QL ArcticLink 3 S2 ULPSH Sensor Fusion Output Specifications.pdf"
pages: 6
sha256: 0d9ccda215a6cf3cefd73a28ef703194c6de41379f428e678556d681a07e56d4
---

# QuickLogic® ArcticLink® 3 S2 ULPSH Sensor Fusion Output Specifications

# **QuickLogic**<sup>**®**</sup> **ArcticLink**<sup>**®**</sup> **3 S2 ULPSH Sensor Fusion Output Specifications • • • • • • QuickLogic Application Note 124**<sup><mark>SS</mark></sup> 

### **Introduction** 

The QuickLogic ArcticLink 3 S2 Ultra-Low Power Sensor Hub (UPLSH) provides a highly flexible solution for a variety of applications. This document details the output specifications when the ArcticLink 3 S2 is customized to perform the sensor fusion of a 3-axis accelerometer, a 3-axis magnetometer and a 3-axis gyro. 

### **Coordinate Frames** 

#### **Body Coordinate Frame** 

The body coordinate frame of a carrier of the UPLSH is defined as: X is right; Y is forward; Z is up; and the origin is located at the center of gravity (CG) of the carrier. This definition is the same as defined in the Google Android OS, as shown in **Figure 1** . 

Figure 1: Body Coordinate Frame 



<!-- Start of picture text -->
y<br>x<br>z<br><!-- End of picture text -->

••• ••• 

**<mark>CONFIDENTIAL</mark>** 

© 2015 QuickLogic Corporation 

<u>www.quicklogic.com</u> **1** 

**_QuickLogic_**<sup>**_®_**</sup> **_ArcticLink_**<sup>**_®_**</sup> **_3 S2 ULPSH Sensor Fusion Output Specifications Rev. A_** 

#### **Local Tangent Navigation Coordinate Frame** 

The local tangent navigation frame is X (East), Y (North), and Z (Up), denoted by ENU, with the origin located at the center of gravity (CG) of the carrier. This definition is the same as defined in the Google Android OS, as shown in **Figure 2** . 

Figure 2: Local Tangent Navigation Coordinate Frame 



<!-- Start of picture text -->
y<br>z<br>Ske<br><!-- End of picture text -->

The attitude of the carrier of the UPLSH is the orientation relationship between the body frame and the local tangent navigation frame. 

**2** <u>www.quicklogic.com</u> •• •••• 

**<mark>CONFIDENTIAL</mark>** 

© 2015 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_ArcticLink_**<sup>**_®_**</sup> **_3 S2 ULPSH Sensor Fusion Output Specifications Rev. A_** 

### **Outputs** 

**Table 1** defines the sensor fusion outputs. 

Table 1: Sensor Fusion Output 

||**Data**|**Unit**|**Size of Data Fields in**<br>**Packet**|**Update**<br>**Rate**<br>**(Hz)**|**Notes**|
|---|---|---|---|---|---|
|Accelerometer|Data|g|6 bytes (2 bytes per<br>axis): Each axis has a<br>16-bit signed integer|200|The integer is scaled into a floating<br>number in the engineering unit.<br>Scale Factor= 2*Range/2^16. For<br>example, if the accelerometer’s<br>range is set to 4g, the scale factor is<br>6.1035e-05 g/LSB.|
|Magnetometer|Data|µT|6 bytes (2 bytes per<br>axis): Each axis has a<br>16-bit signed integer|20|The integer is scaled into a floating<br>number in the engineering unit.<br>Scale Factor= 2*Range/2^16. For<br>example, if the magnetometer’s<br>range is set to 4900 µT, the scale<br>factor is 1.6718 µT/LSB.|
|Gyro Data||degrees/<br>second|6 bytes (2 bytes per<br>axis): Each axis has a<br>16-bit signed integer|200|The integer is scaled into a floating<br>number in the engineering unit.<br>Scale Factor= 2*Range/2^16. For<br>example, if the gyro’s range is set to<br>2000 degrees, the scale factor is<br>0.0610 degrees/LSB.|
||Rotation Vector|unitless|12 bytes (4 bytes for<br>each element of the<br>rotation vector 3X1)|200|Preferred. Same as defined in<br>Android.<br>The 4 bytes represents a 32-bit fixed<br>point Q format of Q15.16.<br>The three elements of the rotation<br>vector are equal to the last three<br>components of a unit quaternion<br>(cos(<br>/2), x*sin(<br>/2), y*sin(<br>/2),<br>z*sin(<br>/2)).<br>θ<br>θ<br>θ<br>θ|
|Orientation<sup>a,b</sup>|Quaternion|unitless|16 bytes (4 bytes for<br>each component of<br>the unit quaternion<br>4X1)|200|The 4 bytes represents a 32-bit fixed<br>point Q format of Q15.16.|
||Euler Angles|degrees|6 bytes (2 bytes per<br>angle): Each angle<br>has a 16-bit signed<br>integer.|200|The integer is scaled into a floating<br>number in the engineering unit with<br>the scale factor of 0.0055<br>degrees/LSB.|
||Rotation<br>Transformation<br>Matrix|unitless|36 bytes (4 bytes for<br>each entries of the<br>matrix 3X3)|200|The 4 bytes represents a 32-bit fixed<br>point Q format of Q15.16.|



<u>www.quicklogic.com</u> **3** • • • ••• 

**<mark>CONFIDENTIAL</mark>** 

© 2015 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_ArcticLink_**<sup>**_®_**</sup> **_3 S2 ULPSH Sensor Fusion Output Specifications Rev. A_** 

Table 1: Sensor Fusion Output 

||**Data**|**Unit**|**Size of Data Fields in**<br>**Packet**|**Update**<br>**Rate**<br>**(Hz)**|**Notes**|
|---|---|---|---|---|---|
||Delta Position|meters|12 bytes (4 bytes per<br>axis): Each axis has a<br>16-bit signed integer|200|The 4 bytes represents a 32-bit fixed<br>point Q format of Q15.16.|
|Translational<br>Vector<sup>a,b</sup>|Linear<br>Acceleration<br>Vector|g|6 bytes (2 bytes per<br>axis): Each axis has a<br>16-bit signed integer|200|Preferred. Same as defined in<br>Android.<br>The integer is scaled into a floating<br>number in the engineering unit.<br>Scale Factor= 2*Range/2^16. For<br>example, if the accelerometer’s<br>range is set to 4g, the scale factor is<br>6.1035e-05 g/LSB.|



a. The Orientation and Translational Vector comply with the ENU coordinate frames (the definitions are summarized in the Appendix). They can also be configured to be output with the NED frame. The ENU frame is preferred, since it complies with Google Android OS. b. Among the Orientation and Translational Vector options, the Rotation Vector and Linear Acceleration Vector, are preferred in terms of efficiency and flexibility. The Euler angles representation has the singularity issue. 

### **Appendix: Definitions** 

Delta Position Vector: 

The accuracy of the position and velocity of the carrier, which are computed from pure inertial sensors only, drift over time without the integration of external positioning systems (such as GNSS and GPS). The drift can be considerably faster for low cost consumer grade inertial sensors. However, the relative delta position of the carrier can be provided as follows: 



Where, assuming that the average velocity of the carrier is zero, this vector represents the position changes (in ENU frame) of the carrier from the previous time interval to the current time interval. 

Euler Angles: 

Azimuth: Rotation around the Z axis (0<=azimuth<360). It is the angle between the positive Y-axis and magnetic north. 0 = North, 90 = East, 180 = South, 270 = West. 

Pitch: Rotation around X axis (-180<=pitch<=180), with positive values when the z-axis moves toward the y-axis. 

Roll: Rotation around Y axis (-90<=roll<=90), with positive values when the z-axis moves toward the x-axis. 

Linear acceleration vector: 

The accelerations in ENU frame (excluding gravity). 

Quaternion: 

## **<mark>CONFIDENTIAL</mark>** 

**4** <u>www.quicklogic.com</u> •• •••• 

© 2015 QuickLogic Corporation 

**_QuickLogic_**<sup>**_®_**</sup> **_ArcticLink_**<sup>**_®_**</sup> **_3 S2 ULPSH Sensor Fusion Output Specifications Rev. A_** 

The quaternion represents the orientation between the body coordinate and ENU frame, which is 4X1: [cos( θ /2), x*sin(θ /2), y*sin( θ /2), z*sin( θ /2)]<sup>T</sup> 

It represents that the carrier has rotated through an angle θ around an axis defined by (x, y, z). 

Rotational Transformation Matrix: 

It is a 3x3 matrix to transform a vector from the body coordinate frame to ENU. Its entries are the function of the quaternions, or rotation vector, or Euler angles. 

Rotation vector: 

The rotation vector represents the orientation between the body coordinate and ENU frame, which is 3X1. The three elements of the rotation vector are equal to the last three components of a unit quaternion (cos( θ /2), x*sin(θ /2), y*sin( θ /2), z*sin( θ /2)). 

### **References** 

[1] http://developer.android.com/reference/android/hardware/SensorEvent.html 

[2] http://developer.android.com/guide/topics/sensors/sensors_overview.html 

[3] http://developer.android.com/guide/topics/sensors/sensors_motion.html 

### **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8948 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) 

E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> Support: <u>www.quicklogic.com/support</u> 

Internet: <u>www.quicklogic.com</u> 

• • • ••• 

**<mark>CONFIDENTIAL</mark>** 

© 2015 QuickLogic Corporation 

<u>www.quicklogic.com</u> **5** 

**_QuickLogic_**<sup>**_®_**</sup> **_ArcticLink_**<sup>**_®_**</sup> **_3 S2 ULPSH Sensor Fusion Output Specifications Rev. A_** 

### **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|A|August 2015|DongAn, YingWu and Kathleen Bylsma|



### **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

### **Copyright and Trademark Information** 

Copyright © 2015 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic, ArcticLink, and the ArcticLink design are registered trademarks, SenseMe, QuickWorks and the QuickLogic logo are trademarks of QuickLogic. Other trademarks are the property of their respective companies. 

## **<mark>CONFIDENTIAL</mark>** 

**6** <u>www.quicklogic.com</u> •• •••• 

© 2015 QuickLogic Corporation 

