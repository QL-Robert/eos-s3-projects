---
title: "Microsoft Word - Microchip Customer Reseller Rights Request Form for WHQL Driver_030913.doc"
source_file: "QuickThingPlus/TinyFPGA-Programmer-Application/a-series-programmer/firmware/mcc_generated_files/usb/utilities/USB - Obtaining a WHQL Certified USB Driver Package.pdf"
pages: 2
sha256: a843240b7bcaa267a374a6d0365852bcce9d664c77704b7682bb0c3e23b5225e
---

# Microsoft Word - Microchip Customer Reseller Rights Request Form for WHQL Driver_030913.doc

# **<u>Obtaining a WHQL Certified Driver Package</u>** 

When developing a USB application that relies on a user supplied driver package (such as CDC and WinUSB based devices), it is often desirable if the driver package contains a Microsoft Windows Hardware Quality Labs (WHQL) signature.  Driver packages that contain a WHQL signature are the most trusted by Microsoft OSes, and install without generating user warnings/prompts, and are normally allowed to be distributed via the Windows Update website.  However, obtaining a WHQL signature can often be a time consuming and expensive process, as the driver package and device must be subjected to a large quantity of semi-automated tests (using the Microsoft “Windows Hardware Certification Kit” [HCK]).  This testing process can often take several weeks, and requires significant financial investment on things such as Windows OS licenses, possible capital costs associated with buying new computer hardware to run the tests, and direct submission fees to Microsoft. 

Fortunately, Microchip has already conducted the necessary testing for the CDC and WinUSB driver packages included in the Microchip Libraries for Applications (MLA), on the Windows 7 and Windows 8 platforms (both 32 and 64-bit variants), and these driver packages are already WHQL certified.  However, when you modify the driver package in any way (ex: by editing the .inf file to change the VID, PID, manufacturer and product strings), this automatically invalidates the driver package signature, and the package must be re-signed. 

Fortunately, Microsoft does not require complete driver package retesting in all cases. Driver packages containing minor changes from a previously certified package do not necessarily require full retesting to be re-certified, provided that the changes are not expected to adversely effect the functionality or reliability of the driver package (such as changing VID/PID and strings in the .inf file).  In these cases, driver packages can be recertified (at a much reduced submission fee) through a Microsoft Driver Update Acceptable (DUA) submission. 

In order to modify a driver package .inf file (ex: to change VID/PID values, and to change product and manufacturer strings), and then do a Driver Update Acceptable submission to get a newly WHQL certified driver package, it will be necessary to do the following: 

1. Read the latest version of the Microsoft documentation “hardware-certificationpolicies-processes.docx”, with specific attention to the sections pertaining to “Reseller submissions” and “Driver update acceptable”.  This document is currently available at: http://msdn.microsoft.com/en- <u>us/library/windows/hardware/hh852370.aspx</u> 

2. If one has not already been created, establish a “Winqual” account with Microsoft, so as to be able to log into the sysdev.microsoft.com website.  See: <u>http://msdn.microsoft.com/en-us/windows/hardware/gg463054.aspx</u> 

1 

3. Update your driver package: 

   - a. Open the .inf file in a text editor and remove all existing Microchip VID (0x04D8) and PID entries in the 32-bit and 64-bit device lists in the file. 

   - b. Add you own company’s VID/PID(s) for the product(s) you intend to use with the driver package.  PID(s) obtained from Microchip through the PID sub-licensing program cannot be included in the .inf file.  Applications for reseller rights will be rejected if they contain Microchip’s VID (0x04D8) in any of the hardware IDs in the .inf file. 

   - c. Update the manufacturer and product strings in the .inf file to match your device. 

   - d. Test the driver package thoroughly with your device, under all OS variants that your driver and device are intended to work with. 

   - e. Package the entire driver package contents (including the .inf file and any other files that are part of the package) into a .zip file. 

4. Fill out all fields in the “Reseller Rights Request Form”, print it out, sign it, scan or take a legible photo of it, then email both the driver package .zip file and the filled out application form to: USBDrivers@microchip.com 

5. After you have received confirmation that your organization has been granted reseller rights, you will need to log into the sysdev.microsoft.com website, accept the reseller rights, then create and submit a DUA package to Microsoft. 

   - a. For details on creating the DUA package, see: <u>http://msdn.microsoft.com/library/windows/hardware/BR230784.aspx</u> 

   - b. Be aware that Microsoft charges a submission fee for DUA submissions. Please see the latest version of the “hardware-certification-policiesprocesses.docx” or equivalent Microsoft document for current fee pricing. 

   - c. Microsoft currently requires that DUA submission packages (.hckx files) be signed using a Microsoft Authenticode code signing certificate, obtained from VeriSign (now part of Symantec Corporation).  If your organization does not already have a Microsoft Authenticode code signing certificate from VeriSign, you will need to obtain one.  It is recommended to search for possible promotional discounts for first time purchasers. 

2 

