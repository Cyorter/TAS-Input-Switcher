-- MultitrackerHawk by Cyorter
-- Based in PCEMultitracker by DarkKobold
-- Current max bits is 32 (Signed Long) 0xFFFFFFFF (Lua 5.1)

-- Works by setting every button to a bit
-- If button is pressed, the bit is 1, otherwise 0
-- All buttons are stored in a single variable
-- Which then is stored in an array (frame)
-- That's why only standard controllers are supported
-- To prevent using too much ram: only a maximum of 16kb is used
-- The playback is self explainable

-- Example: A26 or C64 is used:
-- it has 5 buttons per controller, so it uses 5 * 2 = 10 bits
-- In the LSB order and the remaining 22 bits are ignored
-- If I press Right, Up and Button in Controller 1:
-- ↑↓←→B↑↓←→B (Controller 2 - Controller 1, remember LSB)
-- 0000010011 (0x13/19)
-- Then I do the same with Controller 2:
-- ↑↓←→B↑↓←→B (↑..→B↑..→B)
-- 1001110011 (‭0x273/627‬)
-- That is stored in frame[number of frame]
-- TODO: when BizHawk updates Lua to 5.3 test unstable systems
-- TODO: "frc == limit" or "frc >= limit"?

--[[ Systems supported:

* Atari 2600 & Commodore 64 (not keyboard)
	5 buttons / 2 players
	↑ ↓ ← → B
* Atari 7800 & Game-1000 / Master System
	6 buttons / 2 players
	↑ ↓ ← → 1 2
* Colecovision (not supported yet)
	18 buttons / 2 players
	↑ → ↓ ← l r 0 1 2 3 4 5 6 7 8 9 # *
* Dual Game Boy
	9 buttons / 2 players
	↑ ↓ ← → S s B A P
* Dual Game Gear
	7 buttons / 2 players
	↑ ↓ ← → 1 2 S
* Mega Drive / Genesis
	12 buttons / 4 players
	↑ ↓ ← → A B C S X Y Z M
* NES / Family Computer
	8 buttons / 4 players
	↑ ↓ ← → S s B A
* PC Engine / TurboGrafx-16 / SuperGrafx
	8 buttons / 5 players
	↑ ↓ ← → s R 2 1
* Super NES / Super Famicom
	12 buttons / 5 players
	↑ ↓ ← → s S Y B X A l r
* PC-FX
	14 buttons / 2 players
	↑ → ↓ ← 1 2 3 4 5 6 s R M m

Note: In DualGB P is for Power, I wonder why DualGG doesn't have it...

TODO:
* Colecovision (Coleco)
* PlayStation (PSX)
* Dual NGP (???)

]]--

console.clear()
print('Thank you for testing this script!')
print('This is not fully stable and not all systems are supported.')
print('- Cyorter')
print('')

local current = 1
local oldcur = 0
local frame = {}
local config = {'W', 'S', 'A', 'D', 'Return', 'P', 'J', 'K', 'L', 'I', 'U', 'O', 'N', 'M'}
local stfr = 0
local limit = 0x4000

event.onloadstate(function() stfr = emu.framecount() end)
event.onsavestate(function() for k,v in pairs(frame) do frame[k] = 0 end end)

-------------------------------------[[ DETECTING SYSTEM ]]----------------------------------------

if emu.getsystemid() == 'GB' or emu.getsystemid() == 'Game Gear' then
	local console = emu.getsystemid() == 'GB'
	print((console and 'Game Boy' or 'Game Gear') .. ' Linking!')

elseif emu.getsystemid() == 'PCE' or emu.getsystemid() == 'SGX' or emu.getsystemid() == 'SNES' then
	for np = 1,5 do
		local player = joypad.get(np)
		if player['Up'] ~= nil then
			print('Controller ' .. tostring(np) .. ' Connected!')
		else print('Controller ' .. tostring(np) .. ' Unconnected')
	end end

elseif emu.getsystemid() == 'GEN' or emu.getsystemid() == 'NES' then
	local fs = 0
	local six = false
	for np = 1,4 do
		local player = joypad.get(np)
		if player['Mode'] ~= nil then six = true end
		if player['Up'] ~= nil then
			print('Controller ' .. tostring(np) .. ' Connected!')
			fs = fs + 1
		else print('Controller ' .. tostring(np) .. ' Unconnected')
	end end

	if fs == 3 and emu.getsystemid() == 'NES' then
		print('WARNING! Four Score not set correctly!')
	end
	if emu.getsystemid() == 'GEN' then
		if six then print('6 buttons')
		else print('3 buttons') end
	end

else
	p1 = joypad.get(1)
	p2 = joypad.get(2)
	p1 = p1['Up'] ~= nil
	p2 = p2['Up'] ~= nil

	print('Controller 1 ' .. (p1 and 'Connected!' or 'Unconnected'))
	print('Controller 2 ' .. (p2 and 'Connected!' or 'Unconnected'))
end

if emu.getsystemid() == 'SNES' or emu.getsystemid() == 'PCE' or emu.getsystemid() == 'SGX' or emu.getsystemid() == 'GEN' or emu.getsystemid() == 'Coleco' then
	print('WARNING! ' .. emu.getsystemid() .. ' is not stable!')
end

print('')

-------------------------------------[[ PROGRAM PROCESS ]]----------------------------------------

while emu.getsystemid() == 'A26' or emu.getsystemid() == 'C64' do
	local frc = emu.framecount() - stfr
	if frc == limit then
		print('WARNING! too much frames!')
		print('Prevent wasting too much ram by loadstate and input other players.')
		client.togglepause()
	end

	frame[frc] = frame[frc] or 0

	---------------------------------[[ KEYBOARD ]]---------------------------------

	local i = input.get()

		if i['NumberPad0'] then current = 0
	elseif i['NumberPad1'] then current = 1
	elseif i['NumberPad2'] then current = 2 end

	if oldcur ~= current then
		local n = tostring(current)
		print('Current Player: ' .. (current ~= 0 and n or 'NULL'))
		oldcur = current
	end

	if i['NumberPadPeriod'] then
		for k,v in pairs(frame) do frame[k] = 0 end
		print('Input cleared!')
	end

	---------------------------------[[ READING ]]---------------------------------

	for p = 1,2 do
		local lsh = 0
		local n = bit.rshift(frame[frc], (p - 1) * 5) % 32

		if p ~= current then
			local player = joypad.get(p)
			for k,v in pairs(player) do
				player[k] = bit.band(n, bit.lshift(1, lsh)) ~= 0
				lsh = lsh + 1
			end
			joypad.set(player, p)
		end
	end

	---------------------------------[[ WRITING ]]---------------------------------

	if current ~= 0 then
		local player = joypad.get(current)

		for k,v in pairs(player) do player[k] = false end

		if i[config[1]] then player['Up']     = true end
		if i[config[2]] then player['Down']   = true end
		if i[config[3]] then player['Left']   = true end 
		if i[config[4]] then player['Right']  = true end
		if i[config[7]] then player['Button'] = true end

		local btoi = 0
		local lsh = 0
		for k,v in pairs(player) do
			btoi = btoi + bit.lshift(v and 1 or 0, lsh)
			lsh = lsh + 1
		end

		frame[frc] = bit.band(frame[frc], bit.bnot(bit.lshift(0x1F, (current - 1) * 5)))
		frame[frc] = frame[frc] + bit.lshift(btoi, (current - 1) * 5)

		joypad.set(player, current)
	end

	--------------------------------[[ ADV FRAME ]]--------------------------------

	emu.frameadvance()
end

while emu.getsystemid() == 'A78' do
	local frc = emu.framecount() - stfr
	if frc == limit then
		print('WARNING! too much frames!')
		print('Prevent using too much frames by loadstate and input other players.')
		client.togglepause()
	end

	frame[frc] = frame[frc] or 0

	---------------------------------[[ KEYBOARD ]]---------------------------------

	local i = input.get()

		if i['NumberPad0'] then current = 0
	elseif i['NumberPad1'] then current = 1
	elseif i['NumberPad2'] then current = 2 end

	if oldcur ~= current then
		local n = tostring(current)
		print('Current Player: ' .. (current ~= 0 and n or 'NULL'))
		oldcur = current
	end

	if i['NumberPadPeriod'] then
		for k,v in pairs(frame) do frame[k] = 0 end
		print('Input cleared!')
	end

	---------------------------------[[ READING ]]---------------------------------

	for p = 1,2 do
		local lsh = 0
		local n = bit.rshift(frame[frc], (p - 1) * 6) % 64

		if p ~= current then
			local player = joypad.get(p)
			for k,v in pairs(player) do
				player[k] = bit.band(n, bit.lshift(1, lsh)) ~= 0
				lsh = lsh + 1
			end
			joypad.set(player, p)
		end
	end

	---------------------------------[[ WRITING ]]---------------------------------

	if current ~= 0 then
		local player = joypad.get(current)

		for k,v in pairs(player) do player[k] = false end

		if i[config[1]] then player['Up']        = true end
		if i[config[2]] then player['Down']      = true end
		if i[config[3]] then player['Left']      = true end 
		if i[config[4]] then player['Right']     = true end
		if i[config[7]] then player['Trigger']   = true end
		if i[config[8]] then player['Trigger 2'] = true end

		local btoi = 0
		local lsh = 0
		for k,v in pairs(player) do
			btoi = btoi + bit.lshift(v and 1 or 0, lsh)
			lsh = lsh + 1
		end

		frame[frc] = bit.band(frame[frc], bit.bnot(bit.lshift(0x3F, (current - 1) * 6)))
		frame[frc] = frame[frc] + bit.lshift(btoi, (current - 1) * 6)

		joypad.set(player, current)
	end

	--------------------------------[[ ADV FRAME ]]--------------------------------

	emu.frameadvance()
end

while emu.getsystemid() == 'Coleco' do
	break -- TODO
end

while emu.getsystemid() == 'GB' do
	local frc = emu.framecount() - stfr
	if frc == limit then
		print('WARNING! too much frames!')
		print('Prevent using too much frames by loadstate and input other players.')
		client.togglepause()
	end

	frame[frc] = frame[frc] or 0

	---------------------------------[[ KEYBOARD ]]---------------------------------

	local i = input.get()

		if i['NumberPad0'] then current = 0
	elseif i['NumberPad1'] then current = 1
	elseif i['NumberPad2'] then current = 2 end

	if oldcur ~= current then
		local n = tostring(current)
		print('Current Player: ' .. (current ~= 0 and n or 'NULL'))
		oldcur = current
	end

	if i['NumberPadPeriod'] then
		for k,v in pairs(frame) do frame[k] = 0 end
		print('Input cleared!')
	end

	---------------------------------[[ READING ]]---------------------------------

	for p = 1,2 do
		local lsh = 0
		local n = bit.rshift(frame[frc], (p - 1) * 9) % 512

		if p ~= current then
			local player = joypad.get(p)
			for k,v in pairs(player) do
				player[k] = bit.band(n, bit.lshift(1, lsh)) ~= 0
				lsh = lsh + 1
			end
			joypad.set(player, p)
		end
	end

	---------------------------------[[ WRITING ]]---------------------------------

	if current ~= 0 then
		local player = joypad.get(current)

		for k,v in pairs(player) do player[k] = false end

		if i[config[1]] then player['Up']     = true end
		if i[config[2]] then player['Down']   = true end
		if i[config[3]] then player['Left']   = true end
		if i[config[4]] then player['Right']  = true end
		if i[config[5]] then player['Start']  = true end
		if i[config[6]] then player['Select'] = true end
		if i[config[7]] then player['B']      = true end
		if i[config[8]] then player['A']      = true end
		if i[config[9]] then player['Power']  = true end

		local btoi = 0
		local lsh = 0
		for k,v in pairs(player) do
			btoi = btoi + bit.lshift(v and 1 or 0, lsh)
			lsh = lsh + 1
		end

		frame[frc] = bit.band(frame[frc], bit.bnot(bit.lshift(0x1FF, (current - 1) * 9)))
		frame[frc] = frame[frc] + bit.lshift(btoi, (current - 1) * 9)

		joypad.set(player, current)
	end

	--------------------------------[[ ADV FRAME ]]--------------------------------

	emu.frameadvance()
end

while emu.getsystemid() == 'Game Gear' do
	local frc = emu.framecount() - stfr
	if frc == limit then
		print('WARNING! too much frames!')
		print('Prevent using too much frames by loadstate and input other players.')
		client.togglepause()
	end

	frame[frc] = frame[frc] or 0

	---------------------------------[[ KEYBOARD ]]---------------------------------

	local i = input.get()

		if i['NumberPad0'] then current = 0
	elseif i['NumberPad1'] then current = 1
	elseif i['NumberPad2'] then current = 2 end

	if oldcur ~= current then
		local n = tostring(current)
		print('Current Player: ' .. (current ~= 0 and n or 'NULL'))
		oldcur = current
	end

	if i['NumberPadPeriod'] then
		for k,v in pairs(frame) do frame[k] = 0 end
		print('Input cleared!')
	end

	---------------------------------[[ READING ]]---------------------------------

	for p = 1,2 do
		local lsh = 0
		local n = bit.rshift(frame[frc], (p - 1) * 7) % 128

		if p ~= current then
			local player = joypad.get(p)
			for k,v in pairs(player) do
				player[k] = bit.band(n, bit.lshift(1, lsh)) ~= 0
				lsh = lsh + 1
			end
			joypad.set(player, p)
		end
	end

	---------------------------------[[ WRITING ]]---------------------------------

	if current ~= 0 then
		local player = joypad.get(current)

		for k,v in pairs(player) do player[k] = false end

		if i[config[1]] then player['Up']    = true end
		if i[config[2]] then player['Down']  = true end
		if i[config[3]] then player['Left']  = true end 
		if i[config[4]] then player['Right'] = true end
		if i[config[5]] then player['Start'] = true end
		if i[config[7]] then player['B1']    = true end
		if i[config[8]] then player['B2']    = true end

		local btoi = 0
		local lsh = 0
		for k,v in pairs(player) do
			btoi = btoi + bit.lshift(v and 1 or 0, lsh)
			lsh = lsh + 1
		end

		frame[frc] = bit.band(frame[frc], bit.bnot(bit.lshift(0x7F, (current - 1) * 7)))
		frame[frc] = frame[frc] + bit.lshift(btoi, (current - 1) * 7)

		joypad.set(player, current)
	end

	--------------------------------[[ ADV FRAME ]]--------------------------------

	emu.frameadvance()
end

while emu.getsystemid() == 'GEN' do
	local frc = emu.framecount() - stfr
	if frc == limit then
		print('WARNING! too much frames!')
		print('Prevent using too much frames by loadstate and input other players.')
		client.togglepause()
	end

	frame[frc] = frame[frc] or 0

	---------------------------------[[ KEYBOARD ]]---------------------------------

	local i = input.get()

		if i['NumberPad0'] then current = 0
	elseif i['NumberPad1'] then current = 1
	elseif i['NumberPad2'] then current = 2
	elseif i['NumberPad3'] then current = 3
	elseif i['NumberPad4'] then current = 4 end

	if oldcur ~= current then
		local n = tostring(current)
		print('Current Player: ' .. (current ~= 0 and n or 'NULL'))
		oldcur = current
	end

	if i['NumberPadPeriod'] then
		for k,v in pairs(frame) do frame[k] = 0 end
		print('Input cleared!')
	end

	---------------------------------[[ READING ]]---------------------------------

	for p = 1,4 do
		local lsh = 0
		local n = bit.rshift(frame[frc], (p - 1) * 12) % 4096

		if p ~= current then
			local player = joypad.get(p)
			for k,v in pairs(player) do
				player[k] = bit.band(n, bit.lshift(1, lsh)) ~= 0
				lsh = lsh + 1
			end
			joypad.set(player, p)
		end
	end

	---------------------------------[[ WRITING ]]---------------------------------

	if current ~= 0 then
		local player = joypad.get(current)

		for k,v in pairs(player) do player[k] = false end

		if i[config[ 1]] then player['Up']    = true end
		if i[config[ 2]] then player['Down']  = true end
		if i[config[ 3]] then player['Left']  = true end
		if i[config[ 4]] then player['Right'] = true end
		if i[config[ 5]] then player['Start'] = true end
		if i[config[ 7]] then player['A']     = true end
		if i[config[ 8]] then player['B']     = true end
		if i[config[ 9]] then player['C']     = true end
		if i[config[ 6]] then player['Mode']  = true end
		if i[config[11]] then player['X']     = true end
		if i[config[10]] then player['Y']     = true end
		if i[config[12]] then player['Z']     = true end

		local btoi = 0
		local lsh = 0
		for k,v in pairs(player) do
			btoi = btoi + bit.lshift(v and 1 or 0, lsh)
			lsh = lsh + 1
		end

		frame[frc] = bit.band(frame[frc], bit.bnot(bit.lshift(0xFFF, (current - 1) * 12)))
		frame[frc] = frame[frc] + bit.lshift(btoi, (current - 1) * 12)

		joypad.set(player, current)
	end

	--------------------------------[[ ADV FRAME ]]--------------------------------

	emu.frameadvance()
end

while emu.getsystemid() == 'NES' do
	local frc = emu.framecount() - stfr
	if frc == limit then
		print('WARNING! too much frames!')
		print('Prevent using too much frames by loadstate and input other players.')
		client.togglepause()
	end

	frame[frc] = frame[frc] or 0

	---------------------------------[[ KEYBOARD ]]---------------------------------

	local i = input.get()

		if i['NumberPad0'] then current = 0
	elseif i['NumberPad1'] then current = 1
	elseif i['NumberPad2'] then current = 2
	elseif i['NumberPad3'] then current = 3
	elseif i['NumberPad4'] then current = 4 end

	if oldcur ~= current then
		local n = tostring(current)
		print('Current Player: ' .. (current ~= 0 and n or 'NULL'))
		oldcur = current
	end

	if i['NumberPadPeriod'] then
		for k,v in pairs(frame) do frame[k] = 0 end
		print('Input cleared!')
	end

	---------------------------------[[ READING ]]---------------------------------

	for p = 1,4 do
		local lsh = 0
		local n = bit.rshift(frame[frc], (p - 1) * 8) % 256

		if p ~= current then
			local player = joypad.get(p)
			for k,v in pairs(player) do
				player[k] = bit.band(n, bit.lshift(1, lsh)) ~= 0
				lsh = lsh + 1
			end
			joypad.set(player, p)
		end
	end

	---------------------------------[[ WRITING ]]---------------------------------

	if current ~= 0 then
		local player = joypad.get(current)

		for k,v in pairs(player) do player[k] = false end

		if i[config[1]] then player['Up']     = true end
		if i[config[2]] then player['Down']   = true end
		if i[config[3]] then player['Left']   = true end
		if i[config[4]] then player['Right']  = true end
		if i[config[5]] then player['Start']  = true end
		if i[config[6]] then player['Select'] = true end
		if i[config[7]] then player['B']      = true end
		if i[config[8]] then player['A']      = true end

		local btoi = 0
		local lsh = 0
		for k,v in pairs(player) do
			btoi = btoi + bit.lshift(v and 1 or 0, lsh)
			lsh = lsh + 1
		end

		frame[frc] = bit.band(frame[frc], bit.bnot(bit.lshift(0xFF, (current - 1) * 8)))
		frame[frc] = frame[frc] + bit.lshift(btoi, (current - 1) * 8)

		joypad.set(player, current)
	end

	--------------------------------[[ ADV FRAME ]]--------------------------------

	emu.frameadvance()
end

while emu.getsystemid() == 'PCE' or emu.getsystemid() == 'SGX' do
	local frc = emu.framecount() - stfr
	if frc == limit then
		print('WARNING! too much frames!')
		print('Prevent using too much frames by loadstate and input other players.')
		client.togglepause()
	end

	frame[frc] = frame[frc] or 0

	---------------------------------[[ KEYBOARD ]]---------------------------------

	local i = input.get()

		if i['NumberPad0'] then current = 0
	elseif i['NumberPad1'] then current = 1
	elseif i['NumberPad2'] then current = 2
	elseif i['NumberPad3'] then current = 3
	elseif i['NumberPad4'] then current = 4
	elseif i['NumberPad5'] then current = 5 end

	if oldcur ~= current then
		local n = tostring(current)
		print('Current Player: ' .. (current ~= 0 and n or 'NULL'))
		oldcur = current
	end

	if i['NumberPadPeriod'] then
		for k,v in pairs(frame) do frame[k] = 0 end
		print('Input cleared!')
	end

	---------------------------------[[ READING ]]---------------------------------

	for p = 1,5 do
		local lsh = 0
		local n = bit.rshift(frame[frc], (p - 1) * 8) % 256

		if p ~= current then
			local player = joypad.get(p)
			for k,v in pairs(player) do
				player[k] = bit.band(n, bit.lshift(1, lsh)) ~= 0
				lsh = lsh + 1
			end
			joypad.set(player, p)
		end
	end

	---------------------------------[[ WRITING ]]---------------------------------

	if current ~= 0 then
		local player = joypad.get(current)

		for k,v in pairs(player) do player[k] = false end

		if i[config[1]] then player['Up']     = true end
		if i[config[2]] then player['Down']   = true end
		if i[config[3]] then player['Left']   = true end
		if i[config[4]] then player['Right']  = true end
		if i[config[5]] then player['Run']    = true end
		if i[config[6]] then player['Select'] = true end
		if i[config[7]] then player['B2']     = true end
		if i[config[8]] then player['B1']     = true end

		local btoi = 0
		local lsh = 0
		for k,v in pairs(player) do
			btoi = btoi + bit.lshift(v and 1 or 0, lsh)
			lsh = lsh + 1
		end

		frame[frc] = bit.band(frame[frc], bit.bnot(bit.lshift(0xFF, (current - 1) * 8)))
		frame[frc] = frame[frc] + bit.lshift(btoi, (current - 1) * 8)

		joypad.set(player, current)
	end

	--------------------------------[[ ADV FRAME ]]--------------------------------

	emu.frameadvance()
end

while emu.getsystemid() == 'SG' or emu.getsystemid() == 'SMS' do
	local frc = emu.framecount() - stfr
	if frc == limit then
		print('WARNING! too much frames!')
		print('Prevent using too much frames by loadstate and input other players.')
		client.togglepause()
	end

	frame[frc] = frame[frc] or 0

	---------------------------------[[ KEYBOARD ]]---------------------------------

	local i = input.get()

		if i['NumberPad0'] then current = 0
	elseif i['NumberPad1'] then current = 1
	elseif i['NumberPad2'] then current = 2 end

	if oldcur ~= current then
		local n = tostring(current)
		print('Current Player: ' .. (current ~= 0 and n or 'NULL'))
		oldcur = current
	end

	if i['NumberPadPeriod'] then
		for k,v in pairs(frame) do frame[k] = 0 end
		print('Input cleared!')
	end

	---------------------------------[[ READING ]]---------------------------------

	for p = 1,2 do
		local lsh = 0
		local n = bit.rshift(frame[frc], (p - 1) * 6) % 64

		if p ~= current then
			local player = joypad.get(p)
			for k,v in pairs(player) do
				player[k] = bit.band(n, bit.lshift(1, lsh)) ~= 0
				lsh = lsh + 1
			end
			joypad.set(player, p)
		end
	end

	---------------------------------[[ WRITING ]]---------------------------------

	if current ~= 0 then
		local player = joypad.get(current)

		for k,v in pairs(player) do player[k] = false end

		if i[config[1]] then player['Up']    = true end
		if i[config[2]] then player['Down']  = true end
		if i[config[3]] then player['Left']  = true end
		if i[config[4]] then player['Right'] = true end
		if i[config[7]] then player['B1']    = true end
		if i[config[8]] then player['B2']    = true end

		local btoi = 0
		local lsh = 0
		for k,v in pairs(player) do
			btoi = btoi + bit.lshift(v and 1 or 0, lsh)
			lsh = lsh + 1
		end

		frame[frc] = bit.band(frame[frc], bit.bnot(bit.lshift(0x3F, (current - 1) * 6)))
		frame[frc] = frame[frc] + bit.lshift(btoi, (current - 1) * 6)

		joypad.set(player, current)
	end

	--------------------------------[[ ADV FRAME ]]--------------------------------

	emu.frameadvance()
end

while emu.getsystemid() == 'SNES' do
	local frc = emu.framecount() - stfr
	if frc == limit then
		print('WARNING! too much frames!')
		print('Prevent using too much frames by loadstate and input other players.')
		client.togglepause()
	end

	frame[frc] = frame[frc] or 0

	---------------------------------[[ KEYBOARD ]]---------------------------------

	local i = input.get()

		if i['NumberPad0'] then current = 0
	elseif i['NumberPad1'] then current = 1
	elseif i['NumberPad2'] then current = 2
	elseif i['NumberPad3'] then current = 3
	elseif i['NumberPad4'] then current = 4
	elseif i['NumberPad5'] then current = 5 end

	if oldcur ~= current then
		local n = tostring(current)
		print('Current Player: ' .. (current ~= 0 and n or 'NULL'))
		oldcur = current
	end

	if i['NumberPadPeriod'] then
		for k,v in pairs(frame) do frame[k] = 0 end
		print('Input cleared!')
	end

	---------------------------------[[ READING ]]---------------------------------

	for p = 1,5 do
		local lsh = 0
		local n = bit.rshift(frame[frc], (p - 1) * 12) % 4096

		if p ~= current then
			local player = joypad.get(p)
			for k,v in pairs(player) do
				player[k] = bit.band(n, bit.lshift(1, lsh)) ~= 0
				lsh = lsh + 1
			end
			joypad.set(player, p)
		end
	end

	---------------------------------[[ WRITING ]]---------------------------------

	if current ~= 0 then
		local player = joypad.get(current)

		for k,v in pairs(player) do player[k] = false end

		if i[config[ 1]] then player['Up']     = true end
		if i[config[ 2]] then player['Down']   = true end
		if i[config[ 3]] then player['Left']   = true end
		if i[config[ 4]] then player['Right']  = true end
		if i[config[ 5]] then player['Start']  = true end
		if i[config[ 6]] then player['Select'] = true end
		if i[config[ 7]] then player['Y']      = true end
		if i[config[ 8]] then player['B']      = true end
		if i[config[ 9]] then player['A']      = true end
		if i[config[10]] then player['X']      = true end
		if i[config[11]] then player['L']      = true end
		if i[config[12]] then player['R']      = true end

		local btoi = 0
		local lsh = 0
		for k,v in pairs(player) do
			btoi = btoi + bit.lshift(v and 1 or 0, lsh)
			lsh = lsh + 1
		end

		frame[frc] = bit.band(frame[frc], bit.bnot(bit.lshift(0xFFF, (current - 1) * 12)))
		frame[frc] = frame[frc] + bit.lshift(btoi, (current - 1) * 12)

		joypad.set(player, current)
	end

	--------------------------------[[ ADV FRAME ]]--------------------------------

	emu.frameadvance()
end

while emu.getsystemid() == 'PCFX' do
	local frc = emu.framecount() - stfr
	if frc == limit then
		print('WARNING! too much frames!')
		print('Prevent using too much frames by loadstate and input other players.')
		client.togglepause()
	end

	frame[frc] = frame[frc] or 0

	---------------------------------[[ KEYBOARD ]]---------------------------------

	local i = input.get()

		if i['NumberPad0'] then current = 0
	elseif i['NumberPad1'] then current = 1
	elseif i['NumberPad2'] then current = 2 end

	if oldcur ~= current then
		local n = tostring(current)
		print('Current Player: ' .. (current ~= 0 and n or 'NULL'))
		oldcur = current
	end

	if i['NumberPadPeriod'] then
		for k,v in pairs(frame) do frame[k] = 0 end
		print('Input cleared!')
	end

	---------------------------------[[ READING ]]---------------------------------

	for p = 1,2 do
		local lsh = 0
		local n = bit.rshift(frame[frc], (p - 1) * 14) % 16384

		if p ~= current then
			local player = joypad.get(p)
			for k,v in pairs(player) do
				player[k] = bit.band(n, bit.lshift(1, lsh)) ~= 0
				lsh = lsh + 1
			end
			joypad.set(player, p)
		end
	end

	---------------------------------[[ WRITING ]]---------------------------------

	if current ~= 0 then
		local player = joypad.get(current)

		for k,v in pairs(player) do player[k] = false end

		if i[config[ 1]] then player['Up']     = true end
		if i[config[ 2]] then player['Down']   = true end
		if i[config[ 3]] then player['Left']   = true end
		if i[config[ 4]] then player['Right']  = true end
		if i[config[ 5]] then player['Run']    = true end
		if i[config[ 6]] then player['Select'] = true end
		if i[config[ 7]] then player['III']    = true end
		if i[config[ 8]] then player['II']     = true end
		if i[config[ 9]] then player['I']      = true end
		if i[config[10]] then player['V']      = true end
		if i[config[11]] then player['IV']     = true end
		if i[config[12]] then player['VI']     = true end
		if i[config[13]] then player['Mode 1'] = true end
		if i[config[14]] then player['Mode 2'] = true end

		local btoi = 0
		local lsh = 0
		for k,v in pairs(player) do
			btoi = btoi + bit.lshift(v and 1 or 0, lsh)
			lsh = lsh + 1
		end

		frame[frc] = bit.band(frame[frc], bit.bnot(bit.lshift(0x3FFF, (current - 1) * 14)))
		frame[frc] = frame[frc] + bit.lshift(btoi, (current - 1) * 14)

		joypad.set(player, current)
	end

	--------------------------------[[ ADV FRAME ]]--------------------------------

	emu.frameadvance()
end

while emu.getsystemid() == 'NGP' do -- Someday ;w;
	break -- TODO
end

do -- if not supported system / if failed
	print('System not supported! Exiting... :(')
	return
end
