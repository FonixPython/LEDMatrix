s
	m
		0: Fill mode
		1: Single frame mode
		2: Effect mode
		3: Animation mode
	s
		h: Frequency of strobe
		f: Fill in percent???
	b ~: Set brightness of the led strip
		0-255
	d ~: Set bit depth
		0: 8 bit per channel
		1: 4 bit per channel
		2: 8 color mode (0: black, 1:red, 2:green,3:blue,4:yellow,5:purple,6:cyan,7:white)
		3 ~ ~ ~: Monochrome colors with a set color to use
f: ~ ~ ~, depending on bit depth
o: ~(address of led) ~ ~ ~ (depending on bit depth)
e
	m: Set the mode
		0: Rainbow
		1: Theater chase
		2: Scammer
		3: Color wipe
		4: Pulse
		5: Checker
	s: Speed in miliseconds
a: Only supports 8 color mode and monochrome mode
	s ~: This defines the number of frames in the sequence maximum 10
	f ~ ~{Number of pixels}: Sets a frames buffer indexed from 0
	w ~: Sets delay between frames
d: Displays the current buffer(doesn't apply to animated effects)