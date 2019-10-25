-- Make input with tempo
-- FCEUX Version

-- Useful variables, feel free to change as they are easy
-- to understand and won't affect negatively this script.

local sec = 60000 -- 60.000 seconds (1 minute)
local reg = false -- false = NTSC / true = PAL
local bpm = 180.0 -- Beats per Minute
local div = 4 -- Beat divisor (1/3, 1/4, 1/6, etc)
local cfg = {'Z', 'X'} -- B & A buttons

do
	-- emu.softreset()
	print('Welcome to Inputempo!')
	print('Made by Cyorter')
	print('')
	print('Settings:')
	print(tostring(bpm) .. ' BPM (1/' .. tostring(div) .. ')')
	print(reg and 'PAL' or 'NTSC' .. ' mode')
	print('B: ' .. cfg[1] .. ' - A: ' .. cfg[2])
end

-- CHANGE reg INSTEAD OF THIS!
local fps = reg and 50.0069779682683 or 60.0988138974405
local clockb = math.huge
local clocka = math.huge
local rate = sec / bpm / div

while true do
	i = input.get()
	c = joypad.get(1)
	for k,v in pairs(c) do c[k] = false end

	-- c['B'] = false
	-- c['A'] = false

	if not i[cfg[1]] then clockb = math.huge end
	if not i[cfg[2]] then clocka = math.huge end

	if i[cfg[1]] then
		if clockb > rate then
			if clockb == math.huge then clockb = 0
			else clockb = clockb - rate end

			c['B'] = true
		end

		clockb = clockb + (1 / fps * 1000)
	end

	if i[cfg[2]] then
		if clocka > rate then
			if clocka == math.huge then clocka = 0
			else clocka = clocka - rate end

			c['A'] = true
		end

		clocka = clocka + (1 / fps * 1000)
	end

	if i['up']    then c['up']     = true end
	if i['down']  then c['down']   = true end
	if i['left']  then c['left']   = true end
	if i['right'] then c['right']  = true end
	if i['shift'] then c['start']  = true end
	if i['enter'] then c['select'] = true end

	joypad.set(1, c)

	emu.frameadvance()
end
