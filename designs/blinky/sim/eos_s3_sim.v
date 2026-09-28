// Simulation stand-ins for the EOS S3 primitives the blinky uses.
// The design takes its clock and reset from the SoC interface cell; here they
// are generated locally so the testbench can run on a laptop.
`timescale 1us/1us

module qlal4s3b_cell_macro (
    output reg Sys_Clk0,
    output reg Sys_Clk0_Rst
);
    parameter HALF_PERIOD_US = 50;   // 10 kHz, matching the testbench CLK_HZ

    initial begin
        Sys_Clk0     = 1'b0;
        Sys_Clk0_Rst = 1'b1;
        #1000 Sys_Clk0_Rst = 1'b0;
    end

    always #HALF_PERIOD_US Sys_Clk0 = ~Sys_Clk0;
endmodule

// Global clock buffer: a plain wire in simulation
module gclkbuff (input A, output Z);
    assign Z = A;
endmodule
