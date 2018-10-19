// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

//R2 = R0 * R1 = R0 + R0 + R0... R1 times
//Given four numbers (first number, second number, total, and count),
//with total and count equal to zero, repeatedly add the first number to //to total and add one to count until the second number and count are
//the same.

//cnt = 0
//R2 = 0  //Initialize R2 to 0 in case R1 = 0
//while R1 > cnt:
//        goto end
//    R2 = R2 + R0
//    cnt = cnt + 1
//end

//Initialize add counter and R2 to zero
    @cnt
    M = 0
    @R2
    M = 0

(LOOP)
    //Determine if cnt and R1 are equal (ie: R1-cnt=0)
    @R1
    D = M
    @cnt
    D = D - M
    @END
    D;JEQ

    //Add R0 to R2
    @R0
    D = M
    @R2
    M = M + D

    //Add 1 to counter
    @cnt
    M = M + 1

    //Restart (LOOP)
    @LOOP
    0;JMP

(END)
    @END
    0;JMP