Just what the title says

## Serial Commands

sm ~{display mode index}: Sets display mode out of 4 possible ones

- 0: Single frame mode
- 1: Effect mode
- 2: Animation mode
- 3: Text mode

sb ~{brightness from 0-255}: Sets the brightness of the matrix
ss ~{delay between frames in miliseconds}: Sets the speed of the things happening on the screen
f: Fills the effect color into the main buffer
o ~{x} ~{y} ~{r} ~{g} ~{b}: Change selected pixels from buffer with full 8bit/channel color informantion
em ~{pattern index}: Sets the pattern for the effect mode

- 0: Rainbow (from corner)
- 1: Checker (line by line) (one is set color and one is rainbow)
- 2: Scammer
- 3: Pulse
- 4: Snake (setcolor)
- 5: Rainbow fill

ec ~{r} ~{g} ~{b}: Set a custom full depth color for patterns, text and fill
as ~{frame count}: Sets the length of the animation sequence
af ~{frame index}: Sets the index for frame to be recivied, frame data should be sent in a new line with a bytearray that uses the low and high nibbles for pixel data storage
ap: Play animation
ac ~{color index 1-9} ~{r} ~{g} ~{}: Build a custom color palette out of 10 full depth colors
ts: Enters into text sending mode, text should be sent afterwards in a new line
	s ~: Set text use "_" for spaces
	c ~:
		0: Solid color from effect color
		1: Rainbow color mode
g: Get info about arduino
	d: Get dimensions, in a new line returns "{X}x{Y}"

