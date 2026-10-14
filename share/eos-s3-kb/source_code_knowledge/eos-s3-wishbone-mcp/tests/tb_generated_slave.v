`timescale 1ns/1ps
module tb;
 reg clk=0, rst=1; always #50 clk=~clk;
 reg [16:0] adr; reg cyc=0,stb=0,we=0; reg [3:0] bs; reg [31:0] wd;
 wire [31:0] rd, ctrl; wire ack, pulse; integer acks=0, pulses=0;
 my_regs u(.WB_CLK(clk),.WB_RST(rst),.WBs_ADR(adr),.WBs_CYC(cyc),.WBs_STB(stb),.WBs_WE(we),.WBs_BYTE_STB(bs),
   .WBs_WR_DAT(wd),.ctrl_o(ctrl),.status_i(32'hA5A5_0001),.fifo_rst_pulse_o(pulse),.WBs_RD_DAT(rd),.WBs_ACK(ack));
 always @(posedge clk) begin if(ack) acks=acks+1; if(pulse) pulses=pulses+1; end
 // bridge-like master: hold CYC/STB until ACK sampled, clear on that edge
 task xfer(input w, input [16:0] a, input [3:0] b, input [31:0] d, output [31:0] q);
  begin @(posedge clk); adr<=a; we<=w; bs<=b; wd<=d; cyc<=1; stb<=1;
   @(posedge clk); while(!ack) @(posedge clk); q=rd; cyc<=0; stb<=0; we<=0; repeat(3) @(posedge clk); end endtask
 reg [31:0] q;
 initial #100000 begin $display("FAIL timeout"); $finish; end
 initial begin repeat(2) @(posedge clk); rst=0;
  xfer(0,17'h0,4'hF,0,q); if(q!==32'hC0DE0001) $display("FAIL id %h",q);
  xfer(1,17'h4,4'hF,32'h12345678,q); xfer(0,17'h4,4'hF,0,q); if(q!==32'h12345678) $display("FAIL rw %h",q);
  xfer(1,17'h6,4'b0100,32'h00FF0000,q); xfer(0,17'h4,4'hF,0,q); if(q!==32'h12FF5678) $display("FAIL byte %h",q);
  xfer(0,17'h8,4'hF,0,q); if(q!==32'hA5A50001) $display("FAIL ro %h",q);
  xfer(1,17'hC,4'h1,1,q); xfer(0,17'h1000,4'hF,0,q); if(q!==32'hBADFABAC) $display("FAIL other %h",q);
  if(acks!==8) $display("FAIL acks=%0d",acks); else $display("acks=8 OK: one per access");
  $display("pulses=%0d ctrl=%h", pulses, ctrl); $finish; end
endmodule
