---
title: "Celeris Studio Integrated Development Environment (IDE) \u2013 FFE-GDB Server and Client Setup"
source_file: "QL Application Note 125 Celeris Studio IDE \u2013 FFE-GDB Server and Client Setup.pdf"
pages: 12
sha256: bd56a46b9eb5dea33ead6cd7a416a23e9034c72784ce9f302a0073a329942724
---

# Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup

# **Celeris Studio Integrated** <mark>N</mark> E QuickLogic” **Development Environment (IDE) – FFE-GDB Server and Client Setup** 

**• • • • • • QuickLogic Application Note 125** 

## **Introduction** 

The Flexible Fuel Engine-GNU Debugger (FFE-GDB) is an extension of the GDB. An FFE-loaded algorithm can be debugged using a J-Link probe for on-chip debugging using the Celeris IDE Tool Suite and the Eclipse plug-in software development environment with ARM<sup>®</sup> M4F support. The debugging is client/server-based, where the client is the user interface and the server interacts with J-Link to read from/write to the device. 

## **Scope** 

This application note provides detailed information about how to configure the FFE-GDB server and client in Celeris Studio IDE. 

- For more information about using the FFE-GDB to debug FFE algorithms, see QuickLogic’s _Flexible Fusion Engine GNU Debugger (FFE-GDB) User Manual._ 

- For more information about using the Flexible Fusion Engine Algorithm Tool (FFEAT), see QuickLogic’s _FFEAT User Manual_ . 

- For more information about installing and using the Celeris Studio IDE, see QuickLogic’s _Celeris Studio Integrated Development Environment (IDE) User Manual_ . 

- For known issues regarding command and feature limitations, see QuickLogic’s _EOS S3 Sensor Processing Platform Errata_ . 

## **Prerequisites** 

The development system must have following software prerequisites installed prior to FFE-GDB setup: 

- Microsoft<sup>®</sup> Windows<sup>®</sup> 7 or 8 (or higher) 

- Celeris Studio IDE 3.0 (or higher) 

- J-Link Debugger 4.91 (or higher) 

- Celeris Studio IDE must be connected to the FFE board using a USB J-Link probe 

<u>www.quicklogic.com</u> **1** ••• ••• 

© 2016 QuickLogic Corporation 

**_Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup Rev. D_** 

## **Setup Procedure** 

The setup procedure includes the following steps: 

- **Building a Project** on page 2 

- **Starting the FFE-GDB Server** on page 3 

- **Starting the FFE-GDB Client** on page 3 

- **Closing a Debug Session** on page 11 

### **Building a Project** 

To set up the FFE-GDB server and FFE-GDB client configuration, generate the configuration files while building the project: 

**1.** From the Eclipse Project Explorer menu, select the project (SimplePedo in this example) and Project Build. 

The configuration file is automatically generated. 

**2.** From the Eclipse Project Explorer menu, select the project and right-click on Refresh. 

   - The configuration settings are applied to the project. 



<!-- Start of picture text -->
File Edt Source Refactor Navigite Sewrch Project Run Window Help<br>GLI) S58 WINS a 8 ESF OF Or AOS rT Se rds er a<br>QR Project Explorer 52 BeSle-7co cshmaine [2 TinyPedometere 22<br>> aE Bin New > (2) Acoen[9) = ulpenscceteromerer.Daca(o] + ulpenAcceleroneter.sosie(0)?<br>> 0d — Golo | s2  acce1(a} = uipanacceieroneter Dete(1] * ulpshAcceleroneter Scale(1]7<br>- [2 Acces {2} = utpenhoceieronever.Data(2]_ * ulpstAcceleroneter.scaie(2];<br>SI Open inten Window x0<br>Beuy cn ar |)i& Accesmagnssudesge = qhecen{0) + Acoel(0} + Accen{2] + AeseL{t} + AcoeLI2) *<br>Bois Pate cue [53 currentagnitude = sqrt (AccelMagnicudesae):<br>2 sel Dette Delete as _<br>B Te] © Remove rom Contr Clie Ateshit-Down Be ie ceeseterieia<br>ow MoveTiny Source , fase Junkif ((gunk= CurrentMagnitude>= 0) ~ LastMagnitude:<br>ce so Seenottonflag = 1:<br>gil el te ei 5<br>fat Gren pon, |Iss else‘<br>FBT, Build Project ps SeenBottomFlag = 07<br>BT clan Projct = *<br>Ss Te]® Reteh fs ps<br>Bhar)For) CovertCove Unrelated Projets [so(5 aseestmagnttude= maximmtiagnivude= CurrentMagnseude:- currentiagnieude:<br>Bag)ul 20ldconiguatons >| |[exie tr (seenpotcomrieg &¢ Dift >= AccelerationThreshold)<br>Sug, Mike Tages of [Be os<br>up) ines .<br>Baa = i Problems) Tasks (@)earele 62) Prope<br>4 Be aa a _<terminated> Start_ffe-gdbserver_SimplePedo[Program] C:\QuickLogic\CelerisStudiolDE\ Tools\ FFEAT\ffe-gdbserver.exe_<br>> 4 Bin] Profiling Tools » end_target_state() invoked<br>> Ged<br>onB i rofleereas »| | | || stelweitermenory():Eteweite Remory(): WritingWriting 44 bytesbytes vatue(ox0000000F)value(0x00000000) atat targetcazget addressaddress (0x40004080)(0140004080)<br>tte) Ruma » sfe_wrste_menory()iffelwrite menory(): WritingWriting 44 Bytesbytes valuevalue (0x00000000) (0x00000000) atat targettarget addressaddress (0xs004K150) (0x4004A160)<br>oe » | seecwesce memory (): Writing 4 bytes velue(0x00000000) at cazger address (Oxs00SAi64)<br>Fee) resre<br>OB Benetom toc try Efe l_ wr is te _menmen ory(): Writing 4 bB y et es value (0x00000000) at ce a rz ge rt address (Ox #s 004A 1682€C )<br>Be team »<br>Itc]a Properties Ae Enter<br><!-- End of picture text -->

**2** <u>www.quicklogic.com</u> •• •••• 

© 2016 QuickLogic Corporation 

**_Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup Rev. D_** 

### **Starting the FFE-GDB Server** 

**NOTE:** The J-Link GDB Server must be set up correctly for the debugger to run. 

To start the FFE-GDB Server as an “external tool” using Eclipse: 

**1.** Click on the external tools icon pull-down menu and select Start_ffe gdbserver_ 

   - < _WorkspaceName_ >. In this example the workspace name is SimplePedo. 



<!-- Start of picture text -->
2 Search Project Run Window Help<br>y | Oa BG SH O-O-Q+'SSV3)PSTSee<br>Ble FSO Guise1 Start fe-gabserver simplePedo<br>36 Run As ,<br>37 External Tools Configurations... ta[0] * ulpshAc<br>38 . . ita[l] * ulpshAc<br>3940 Organizeme Favorites... jta[2] * ulpshAc<br>41 AccelMagnitudeSqr = (Accel[0] * Accel[0] + Accel<br><!-- End of picture text -->

The Console window displays the generated information. 



<!-- Start of picture text -->
| «<br>If Problems 4)Tasks |G) Console 52 | [T] Properties &y Progress<br>Start FFE [Program] C:\QuickLogic\CelerisStudiolDE\Tools\FFEAT\ffe-gdbserver.exe<br>xsp_init() invoked<br>handle_rsp() invoked<br>Listening for new connections on port 4444...<br><!-- End of picture text -->

### **Starting the FFE-GDB Client** 

To configure the client for FFE debugging: 

**1.** Click on the debug icon pull-down menu and select Debug Configurations. 



<!-- Start of picture text -->
File Edit Source Refactor Navigate Search Project Run Window He<br>[RS Project Explorer 5 © %&| & >% = GB Bulpshmaine [2 TinyPedometer.c [Sir<br>4 @ ArrayBug 1 extern void SetUlpshProperty(ch<br>> Binaries 2 extern int @_ sim:<br>> @ Debug 3° void SetUlpshProperties()<br>>> [@[S MathtcMathis cmt]5 SevUlpehProperty ("UipebType<br><!-- End of picture text -->

<u>www.quicklogic.com</u> **3** • • • ••• 

© 2016 QuickLogic Corporation 

**_Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup Rev. D_** 

By default, the Main tab of the Debug Configurations dialog is displayed and the project is added on the GDB Hardware Debugging tree. 



<!-- Start of picture text -->
x<br>Create, manage. and run configurations -<br>Cexl|ex- ‘Name: | SimplePedo_Debug<br>(nee [5<br>[E) C/C++ Application ' G Oege] > So]sre] ElGmer<br>TEL C/C++ Attach to Applicat || | Project<br>[E] C/C++ Postmortem Debu ||| SimplePedo Browse...<br>[C/C++ Remote Applicatic Gon ee<br>44 TE) GDB Harhovare Deki || eee sa<br>[E] E)SimplePedoGDB SEGGER J-LinkDebug] Debuc ||| | Debug\SimplePedo.ELF ‘Search Project. ]<br>® Launch Group Build (if required) before launching<br>Enable auto build O Disable auto build<br>@ Use workspace settings Configure Workspace Settings...<br>Fatm e ssreie matched8 of 8 ares > | singing GDBGDB (DSF)(O5F) Hardware re DebuggingDebugging LauncherLauncher - Select other... AyPhy R‘evert<br>® =<br><!-- End of picture text -->

**2.** Click on the project in the GDB Hardware Debugging Tree that needs to be debugged 

   - (<WorkspaceName>_Debug, in this example SimplePedo_Debug) click on Debug. 

**4** <u>www.quicklogic.com</u> •• •••• 

© 2016 QuickLogic Corporation 

**_Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup Rev. D_** 

#### When the debugging session starts, the following screen appears. 



<!-- Start of picture text -->
le ft Source Relacor Nviate Seych Project Bun Window Help<br>ES SSO<br>“Debug £2 He Wt] BO | SycoVerabies8aBrestpoints AP Egres o nsBEIcxRegites |Z recePeipheals]| a2mA | tacModi s ce- [Reba]=D<br>4 Q Start fe-gabserve [Program] eHe|+ x ela +<br>«4 [E] WBT1 ProjectCAGuildogi DebugCelersutioEToolAFFEATMfe-gebseverne [GDB Hardware Debugging] — 1a<br>oer (er femaitor! int<br>“4 uP$Threadmmang#1 <main>at pean (Suspended258 oa00s0078 : Breakpoint) ab Ast new voresion<br>18 C/QuiclL ogiClereStudloDE/Tool/FFEATHe qucklogc-e-gdb. 78) < 5<br>al stack & Function Adsress 5<br>DupnmaneH (e]oamsoxe [2 TinyPecometere<br>¢ a BARRY eke ><br>ps2 © a Boutnes ea<br>3 pak © ° 1 upsnn<br>56 Seeblpsntropersiesi): TisusingabreakPone Seen<br>bes | dg(tteet_time_anit = 0) © , abrogates: Vespa<br>bss 2 le<br>< > 2 m seeoint ’<br>Eiconsole £3 |G] Tasks f] Problems @ Becutbles Q Memory Browser ( Memory ex S/R RB)" o-n-s0<br>Sty te gene (rota)savokedCAGcCelertoiETol FEATMe gabrener<br>handlehandle write rap) dava() :Received comand "WRITE_DATA(id:102)" from client i<br>rop_client_request() savored<br>panaie_rep()rop_client requestinvored () invoked<br>handle write dava() :Received comand "WRITE_DATA(id:102)" from client<br>rap_clienthandle_rap()request invoked () invoked ¥<br>UpdateRPM<br>pactage propos lst mS<br><!-- End of picture text -->

<u>www.quicklogic.com</u> **5** • • • ••• 

© 2016 QuickLogic Corporation 

**_Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup Rev. D_** 

### **Debugging an Algorithm C Program** 

The quickest way to debug an Algorithm C program is to use the Project Explorer view. 

**1.** In the Project Explorer view, right-click on the project and select Debug As>Debug Configurations. 



<!-- Start of picture text -->
» {8 SamsungMFBbatch we os<br>>  SenProgram ect byte ot<br>> GS SimpleAMG2 ae<br>>  SimplePedo Sf143 byteome10<br>> &S Testa 145 wbyte 3<br>> lige Tiny New > 146 © slong g_output<br>> ES trigfun: —_einto 5247 «byte 3<br>“342 slong Linfo_strings<br>Open in New Window “119° byte 5<br>Copy 150 byte 4<br>Paste CtrecCtrev Pise“151 slongsbyte 2.Linfo_stringé<br>% Delete Delete ee vhong 208<br>Remove from Context Ctrle<br>Source Alt+ Shift+Down : 55 wbyte 1<br>a » (355157 bytebyte 5it<br>PEs “158 wbyte 3<br>Rp (159° lieng tempi<br>a 160 byte 3<br>pon he 4261 slong. Linfo_stringé<br>a Bport.. 162 byte 5<br>Build Project<br>Clean Project Hl Problems $2) Tasks E Console 5% p<br>2) Refresh 5 CDT Build Console [TinyPedometer]<br>Close Project<br>Close Unrelated Projects<br>Build Configurations ><br>Make Targets »<br>Index »<br>‘Show in Remote Systems view<br>Profiling Tools ><br>Profile As ><br>Debug As >| TE) 1 Local C/C++ Application<br>Cras , Debug Configurations...<br>Compare With »<br>Restore from Local History.<br>SP Run C/C++ Code Analysis<br>Team ,<br><!-- End of picture text -->

**6** <u>www.quicklogic.com</u> •• •••• 

© 2016 QuickLogic Corporation 

**_Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup Rev. D_** 

**2.** Alternatively, from the toolbar menu, select Run>Debug Configurations. 



<!-- Start of picture text -->
File Edit Source Refactor Navigate Search Project Run| Window Help<br>Oy iS) Sy 4-a: SAT ae Run Ctrl+F11 oY<br>7 % Debug Fl<br>[Bs Project. Explorer 23| qFQ Profile in .gHai<br>> (9 BatchingSupport inpu<br>> fe Calib Profile History »<br>> & LSM Profile As » binfo.<br>> {= Math Profile Configurations...<br>> Math1<br>> GF proj Run History |<br>> fF proj2 Run As » panto,<br>> {2 SamsungMFBbatch Run Configurations...<br>> © SenProgram<br>> @ SimpleAMG2 Debug History t<br>> & SimplePedo Debug As »<br>> GS Test2 =<br>» [feoTinyPedometer Deg Connon. outp<br>»> & trigfuns © Toggle Breakpoint Ctrl+Shift+B<br>© Toggle Line Breakpoint info<br>© Toggle Method Breakpoint<br>©} Toggle Watchpoint<br>1% Skip All Breakpoints info<br>2% Remove All Breakpoints DS<br>Breakpoint Types ><br>Q, External Tools »<br>se «byte 3<br><!-- End of picture text -->

**3.** Select the project and click on Debug. 



<!-- Start of picture text -->
©‘Create,Progr manage.det net itand un coniguations<br>ypeTE] fier c+ tet Appetion | | Bainsome | TyPedomee3 Debs Debug Setup Source] commen)<br>{E]cce>TE]TE) C/C++C/C++ Postmortem AttachRemotetoAppcation Application Debugger BrojectSSTinyPedometer Browse.<br>4, 6 ardor Ootging<br>[ear cad [Deowtinpedomews<br>Dispos1Bcot.Math ebogDebog detBul eontgurioneitereRcing (wie| [SerenPejea|[ rome.|<br>poi Debug<br>ome{Sanghasngeb Ofnable© Useworapceauto buildstings Disableis Watcoaceauto build Stig<br>IB Spb Gebug<br>Ter detug<br>» TE© G8tigfursSEG  Debugint Debugging<br>© Lach Group<br>Fiter matched 21 of 2 tems Using GDB (DSF Hardware Debugging Launcher Seis tes. ‘pp a<br>) | oe)<br><!-- End of picture text -->

> © 2016 QuickLogic Corporation 

<u>www.quicklogic.com</u> **7** • • • ••• 

**_Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup Rev. D_** 

#### The debugging session begins. 



<!-- Start of picture text -->
Sosa<br>Ble Eat Souce Refer avgate Seach Breet [Bun] Window Hep<br>aedeg £2|.emeryeconMovetetine serrca (Cee) tee Eo C1JPaieT ina eVerubesin abtekFeltdEeatpoins 7, Pepe__ Seesuckacces | as | Ghcrce~ea(Rebuy)<br>4 St tegen pe Pega) Pag ® Nae Tye vate<br>14 MH CAQutadage Celeste Took FEAT eg<br>2 1paperpreiP TexdDebug 608 1 <muin> Hardvae Guspended:Contne)Debugging] | 2TomineaDisconnect cure<br>15 cigutogeCeenscDe 2 maint promsincl? OHOTot FFEAT Hed |> SeGem thot Sara 5 .<br>Sep Ove ® e<br>[i7 AccerometeLSMEO5LK Common .swgns.n “| SteeFuntoti e n ownA Fp ‘ SB) Femme VORRY eR Too,<br>Ao se Sep ites ay<br>i Stemi = 8: Step Secon cues © siete<br>202a tema e Geaptmplmp = 8) Fa ctortal2(eaectortali(gtnput):teensyinp); &% hnDetug owena foccanepipestein<br>a bs Eoutptoutput == -100;(Cenptetenp2)/2s fundseae i> 1© factoramind nt<br>2 return goutputs [ae<br>be abu eto 5<br>. Debug as > ae<br>SCREENED Debug Coniguations. ral<br>ro Debug 08 Hardwaretous  Debugging C/uichtogi celerER Protons © Be c © TOM Bakponk cuss exkiaa Gi@Oere-o--5<br>Llcense 6PL3+: aw GPL version > or later <nee ® Toggle reap, 5<br>This is free soferre: jou are fee to thonge ¢ © TogyeMhod Beipont<br>There'sTypeBndThis Ge"show‘show woshowarranty" waar,cnflgratconfiguredfortodeatosthe2--hostei686-pe-ningextent persieeed © ShipTeale128 Al Besiponsotc a a<br>ion” for Configuration det pete gape -<br>reer Des a | wate | smarinset 1721<br><!-- End of picture text -->

When the program is started in the debug mode, the user is prompted to switch to the debug perspective. The debug perspective offers additional views that can be used to troubleshoot the application. 

**4.** To restart the program, from the toolbar menu, select Run>Resume or press F8 on the keyboard. 

**8** <u>www.quicklogic.com</u> •• •••• 

© 2016 QuickLogic Corporation 

**_Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup Rev. D_** 

**5.** To set a breakpoint, in the editor area right-click on the marker bar and select Toggle Breakpoint. 



<!-- Start of picture text -->
C-LUSIGiN PT ENS S OPS STH I<br>#$ Debug 22<br>4 Q, Start. ffe-gdbserver_proj2 [Program]<br>pi C:\QuickLogic\CelerisStudiolDE\Tools\FFEAT\ fe-gdbserver.exe<br>44 [2] proj2_Debug [GDB Hardware Debugging]<br>4 ® projelrF<br>4 oP ©Threadfactoriall()#1 <main>at proj2_srcl.c:14 (Suspended: 040050448 Step)<br>= main() at proj2_main.c:20 0x40050040<br>WH C/QuickLogic/CelerisStudiolDE/Tools/FFEAT/#fe-quicklogic-elf-gdb.exe= _start() at40050000 (79)<br>[Accelerometer LSM6DSLh [>] Common LSMEDSLh [=] LSMEDSL_AccelAn«<br>7 {<br>it templ = @;<br>19 temp2 = @;<br>20 templ = factorial1(g_input);<br>21 temp2 = factorial2(g input);<br>Toggle Breakpoint Ctrle Shift+B<br>‘Add Breakpoint... Ctrl Double Click<br>Add Dynamic Print.<br>Enable Breakpoint Shift+Double Click<br>Breakpoint Properties... Ctrl+Double Click<br>Breakpoint Types ><br>] Goto Annotation Crt fh Memory<br>Prd Add Bookmark. sStudiolDE/Tools/FFEAT/tfe<br>r ASS less previously adjust<br>38) ¥_ Show Quick Diff PersraeeDe it: 170m enseeseee to<br>17 ¥_ Show Line Numbers<br>«| Folding ><br>Preferences...<br><!-- End of picture text -->

Breakpoints are shown on the marker bar. They are also visible in the Breakpoints view. When the execution of code reaches a breakpoint, the C program suspends the execution of the program. 

**6.** When the execution of a program is paused, inspect the memory and execute the program in a controlled manner. 

<u>www.quicklogic.com</u> **9** • • • ••• 

© 2016 QuickLogic Corporation 

**_Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup Rev. D_** 

**7.** Additionally, when the execution of a program is paused, use the Debug view to inspect the call stack. 



<!-- Start of picture text -->
wa Rr)race! oat 22.2 S| S1#-O-G-'96 9-B<br>#6 Debug £2 Rel yO<br>4 Q, Start_ffe-gdbserver_proj2 [Program]<br>pC: QuickLogic\CelerisStudiolDE\Tools\FFEAT\ffe-gdbserver.exe<br>4 [E] proj2_Debug [GDB Hardware Debugging]<br>4B proj2.ELF<br>4 g@ Thread#1 <main> (Suspended<br>factoriall() at proj2_srcl.c:14 0x40050448<br>= : Step)<br>= main at proj2_main.c:20 04005000<br>pi) C:/QuickLogic/CelerisStudiolDE/Tools/FFEAT/ffe-quicklogic-elf-gdb.exe= _start() at 0x40050000 (7.9)<br><!-- End of picture text -->

**8.** Use the Variables view to inspect the value of the variables. 



<!-- Start of picture text -->
(0Variables 5% |p Breakpoints "2, Peripherals H*ee| se eR Ie yoo<br>Name Type Value<br>69 inp int<br>(9 result int<br>« *<br><!-- End of picture text -->

**9.** Use the Run menu options to Resume or Terminate execution, Step Into a function, Step Over a line of code, and so forth. 



<!-- Start of picture text -->
in| Window Help :<br>o> Resume F8<br>{@ Suspend<br>@ Terminate Ctri+F2<br>4% Disconnect<br>2. Step Into F5<br>© Step Over F6<br>-& Step Retum F7<br>| Run to Line Ctrl+R<br>BE Use Step Filters Shift+F5<br><!-- End of picture text -->

**10** <u>www.quicklogic.com</u> •• •••• 

© 2016 QuickLogic Corporation 

**_Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup Rev. D_** 

### **Closing a Debug Session** 

To close a debug session: 

**1.** Click on the Disconnect icon <mark>oy</mark> in the toolbar menu to terminate the connection between the debugger and the remote target. 

**2.** Right-click on the Debug icon and select Close to close the Debug perspective. 



<!-- Start of picture text -->
B | Facies<br>|r ve i<br><!-- End of picture text -->

## **Contact Information** 

Phone: (408) 990-4000 (US) +(44) 1932-21-3160 (Europe) +(886) 26-603-8948 (Taiwan) +(86) 139-0517-5302 (China) +(81) 3-5875-0547 (Japan) +(82) 31-601-4225 (Korea) E-mail: <u>info@quicklogic.com</u> Sales: <u>America-sales@quicklogic.com Europe-sales@quicklogic.com Asia-sales@quicklogic.com Japan-sales@quicklogic.com Korea-sales@quicklogic.com</u> 

Support: <u>www.quicklogic.com/support</u> Internet: <u>www.quicklogic.com</u> 

## **Revision History** 

|**Revision**|**Date**|**Originator and Comments**|
|---|---|---|
|A|December 2015|Initial release.<br>Jaishankar Rajendran and Kathleen Bylsma|
|B|February 2016|Jaishankar Rajendran and Kathleen Bylsma<br>Updated the configuration image onpage 6.|
|C|May 2016|Jaishankar Rajendran and Kathleen Bylsma<br>Updated the entireprocedure.|
|D|June 2016|Jaishankar Rajendran and Kathleen Bylsma<br>Added Debuggingan Algorithm C Program section.|



<u>www.quicklogic.com</u> **11** • • • ••• 

© 2016 QuickLogic Corporation 

**_Celeris Studio Integrated Development Environment (IDE) – FFE-GDB Server and Client Setup Rev. D_** 

## **Notice of Disclaimer** 

QuickLogic is providing this design, product or intellectual property "as is." By providing the design, product or intellectual property as one possible implementation of your desired system-level feature, application, or standard, QuickLogic makes no representation that this implementation is free from any claims of infringement and any implied warranties of merchantability or fitness for a particular purpose. You are responsible for obtaining any rights you may require for your system implementation. QuickLogic shall not be liable for any damages arising out of or in connection with the use of the design, product or intellectual property including liability for lost profit, business interruption, or any other damages whatsoever. QuickLogic products are not designed for use in life-support equipment or applications that would cause a life-threatening situation if any such products failed. Do not use QuickLogic products in these types of equipment or applications. 

QuickLogic does not assume any liability for errors which may appear in this document. However, QuickLogic attempts to notify customers of such errors. QuickLogic retains the right to make changes to either the documentation, specification, or product without notice. Verify with QuickLogic that you have the latest specifications before finalizing a product design. 

## **Copyright and Trademark Information** 

Copyright © 2016 QuickLogic Corporation. All Rights Reserved. 

The information contained in this document is protected by copyright. All rights are reserved by QuickLogic Corporation. QuickLogic Corporation reserves the right to modify this document without any obligation to notify any person or entity of such revision. Copying, duplicating, selling, or otherwise distributing any part of this product without the prior written consent of an authorized representative of QuickLogic is prohibited. 

QuickLogic, ArcticLink, and the ArcticLink design are registered trademarks, SenseMe, QuickWorks and the QuickLogic logo are trademarks of QuickLogic. Other trademarks are the property of their respective companies. 

**12** <u>www.quicklogic.com</u> •• •••• 

© 2016 QuickLogic Corporation 

