// Qomu / QuickFeather (QuickLogic EOS S3) FPGA-only blinky.
//
// Cycles the on-board RGB LED red -> yellow -> green, one step every 1 s.
// Yellow is red and green lit together, so the steps are colors rather than
// single LEDs.
//
// Clocking: the eFPGA fabric has no oscillator pin of its own. The clock comes
// from the M4 side through the qlal4s3b_cell_macro. When the bootloader runs an
// FPGA-only image ("--mode fpga") it enables clock C16, which appears here as
// Sys_Clk0, at 12 MHz.
//
// LEDs: the RGB LED's cathodes are switched by N-channel MOSFETs whose gates are
// driven by the EOS S3, so a '1' on the pin turns the LED on (active high).

module top #(
    parameter CLK_HZ  = 12_000_000,
    parameter STEP_MS = 1000          // time on each color
) (
    output wire red_led,
    output wire green_led,
    output wire blue_led
);

    // 12 MHz -> 12,000,000 ticks = 1 s
    localparam [31:0] TICKS_PER_STEP = (CLK_HZ / 1000) * STEP_MS;

    localparam [1:0] STEP_RED    = 2'd0;
    localparam [1:0] STEP_YELLOW = 2'd1;
    localparam [1:0] STEP_GREEN  = 2'd2;

    wire sys_clk;
    wire sys_rst;
    wire clk;
    wire rst;

    // Only the clock/reset outputs of the SoC interface macro are used.
    qlal4s3b_cell_macro u_qlal4s3b_cell_macro (
        .Sys_Clk0     (sys_clk),
        .Sys_Clk0_Rst (sys_rst)
    );

    // Route clock and reset on the FPGA's global clock network
    gclkbuff u_gclkbuff_clock (.A(sys_clk), .Z(clk));
    gclkbuff u_gclkbuff_reset (.A(sys_rst), .Z(rst));

    reg [31:0] count = 32'd0;
    reg [1:0]  step  = STEP_RED;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            count <= 32'd0;
            step  <= STEP_RED;
        end else if (step > STEP_GREEN) begin
            // Initial values are not guaranteed on this flow and reset may not
            // be pulsed, so recover from an out-of-range power-up state.
            count <= 32'd0;
            step  <= STEP_RED;
        end else if (count >= TICKS_PER_STEP - 1) begin
            count <= 32'd0;
            step  <= (step == STEP_GREEN) ? STEP_RED : step + 2'd1;
        end else begin
            count <= count + 32'd1;
        end
    end

    // red -> yellow -> green; blue stays off throughout
    assign red_led   = (step == STEP_RED)   || (step == STEP_YELLOW);
    assign green_led = (step == STEP_GREEN) || (step == STEP_YELLOW);
    assign blue_led  = 1'b0;

endmodule
