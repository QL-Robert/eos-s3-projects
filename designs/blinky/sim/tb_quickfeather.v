// Self-checking testbench for the blinky: red -> yellow -> green, 1 s each.
//
// Runs the real top.v with a 10 kHz clock instead of 12 MHz (CLK_HZ is scaled to
// match), so one simulated second is one real second of behavior.
`timescale 1us/1us

module tb;   // same logic on both boards; only the pin file differs

    localparam MS = 1000;          // 1 ms in time units (us)

    wire red_led, green_led, blue_led;

    top #(.CLK_HZ(10_000), .STEP_MS(1000)) dut (
        .red_led(red_led), .green_led(green_led), .blue_led(blue_led)
    );

    wire clk = dut.clk;

    integer errors = 0;

    task check(input ok, input [8*64-1:0] what);
        begin
            if (ok) $display("  ok    %0s", what);
            else begin
                $display("  FAIL  %0s   (t=%0d ms)", what, $time / MS);
                errors = errors + 1;
            end
        end
    endtask

    // Wait for the next color change and report how long the current color lasted
    task next_change(output integer held_ms, output integer r, output integer g, output integer b);
        integer t0;
        reg r0, g0, b0;
        begin
            t0 = $time;
            r0 = red_led; g0 = green_led; b0 = blue_led;
            while (red_led === r0 && green_led === g0 && blue_led === b0)
                @(posedge clk);
            held_ms = ($time - t0) / MS;
            r = red_led; g = green_led; b = blue_led;
        end
    endtask

    function integer about_one_second(input integer ms);
        about_one_second = (ms >= 980) && (ms <= 1020);
    endfunction

    // Blue must stay off for the whole run
    always @(posedge clk)
        if (blue_led !== 1'b0) begin
            $display("  FAIL  blue LED turned on");
            errors = errors + 1;
        end

    integer held, r, g, b, i;

    initial begin
        $dumpfile("tb.vcd");
        $dumpvars(0, tb);

        #(5 * MS);
        $display("start-up");
        check(red_led === 1'b1 && green_led === 1'b0, "starts on red");

        $display("sequence and timing");
        // Two full laps: red -> yellow -> green -> red ...
        for (i = 0; i < 6; i = i + 1) begin
            next_change(held, r, g, b);
            case (i % 3)
                0: check(r === 1 && g === 1 && b === 0, "red is followed by yellow (red + green)");
                1: check(r === 0 && g === 1 && b === 0, "yellow is followed by green");
                2: check(r === 1 && g === 0 && b === 0, "green is followed by red");
            endcase
            if (i > 0)   // the first interval starts mid-step at time zero
                check(about_one_second(held), "each color is held for 1 s");
        end

        $display("");
        if (errors == 0) $display("ALL TESTS PASSED");
        else             $display("%0d TEST(S) FAILED", errors);
        $finish;
    end

endmodule
