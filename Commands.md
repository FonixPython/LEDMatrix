s
	m
		0: Single frame mode
		1: Effect mode
		2: Animation mode
		3: Text mode
	s
		h: Frequency of strobe
		f: Fill in percent???
	b ~: Set brightness of the led strip
		0-255
f: ~ ~ ~, depending on bit depth
o: ~{x} ~{y} ~ ~ ~ (depending on bit depth)
e
	m ~: Set the mode
		0: Rainbow (from corner)
		1: Checker (line by line) (one is set color and one is rainbow)
		2: Scammer
		3: Pulse
		4: Snake (setcolor)
		5: Rainbow fill
	s ~: Speed in miliseconds
	c ~ ~ ~: Set a custom color for the effects
a: Only supports 8 color mode
	s ~: This defines the number of frames in the sequence maximum 10
	f ~ ~{Number of pixels}: Sets a frames buffer indexed from 0
	w ~: Sets delay between frames
d: Displays the current buffer(doesn't apply to animated effects)
t
	s ~: Set text use "_" for spaces