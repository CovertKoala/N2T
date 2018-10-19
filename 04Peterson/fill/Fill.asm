// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//Outerloop
(SCNST)
@SCREEN
D = A
@pix
M = D - 1 //The minus 1 let me remove 2 lines of code later. 

//Loop through pixels on screen
(LOOP)
    //reset pixel pointer to @SCREEN when end of screen reached.
    @pix
    D = M
    @24575
    D = D - A
    @SCNST
    D;JEQ    

    //if keypress, turn screen black
    @KBD
    D=M
    @KEYPRS
    D;JGT 

    //else turn screen white
    @pix
    AM = M + 1
    M = 0
    @LOOP
    D;JEQ 

    //screen black...
    (KEYPRS)
    @pix
    AM = M + 1
    M = -1
    @LOOP
    0;JMP