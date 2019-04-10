##########################################################################################
#
#   BIT MANIPULATORS
#
##########################################################################################

#
# Returns the n-th power of 2. (an integer with all-zero except one '1' in the n-th bitposition)
# Ex: [bit 2] == 0b100 = 0x4
#
proc bit {n} {
  return [ expr 1 << $n ]
}


#
# Clear bit: Clears to '0' the n-th bit in the 'p' integer
# Ex: [clr_b 0xff 3] = 0xf7
#
proc clr_b {p n} {
  return [ expr $p & ~[bit $n] ]
}


#
# Set bit: Set to '1' the n-th bit in the 'p' integer
# Ex: [set_b 0xf0 3] = 0xf8
#
proc set_b {p n} {
  return [ expr $p | [bit $n] ]
}


#
# Toggle bit: Toggles '0' <-> '1' the n-th bit in the 'p' integer
# Ex: [tgl_b 0xf0 3] = 0xf8
#
proc tgl_b {p n} {
  return [ expr $p  ^ [bit $n] ]
}


##############################################################################
#
#   BIT-FIELD MANIPULATORS
#
##############################################################################

#
# Mask of lsb bits: Returns an integer which contains 'len' count '1' from bitpos 0 to len-1
# Same as [bf_mask 0 len]
# Ex: [lsb_mask 3] = 0x7
#
proc lsb_mask {len} {
  return [expr [ bit $len ] -1]
}


#
# Bit field mask: Returns an integer containing ones at given bitpositions.
# Ex: [bf_mask 4 2] == 0x30
#
proc bf_mask {start len} {
  return [expr [ lsb_mask $len ] << $start]
}


#
# Get bitfield: Returns value of 'x' in the given bitpositions.
# Ex: [get_bf 0xaaba 4 8] == 0xab
#
proc get_bf {x start len} {
  return [expr [expr $x >> $start] & [lsb_mask $len]]
}


#
# Clear bitfield: Returns a copy of 'x', just with '0'-s in the given bitpositions.
# Ex: [clr_bf 0xbeef 4 8] == 0xb00f
#
proc clr_bf {x start len} {
  return [expr $x & ~[bf_mask $start $len] ]
}


#
# Set bitfield: Insterts the 'x' into 'y' in the given bitpositions.
# Ex: [set_bf 0xbeef 0x11 4 8] == 0xb11f
#
proc set_bf {y x start len} {
  return [expr [clr_bf $y $start $len] | [expr [get_bf $x 0 $len] << $start ] ]
}


##############################################################################
#
#   REGISTER (fields) MANIPULATORS
#
##############################################################################

#
# Read register: Reads a simple memory mapped register from the given baseaddress and register offset.
#
proc rd_reg {baseAddress regOffset} {
  return [mrd -value [expr $baseAddress + $regOffset]]
}


#
# Write register: Writes a simple memory mapped register to the given baseaddress and register offset.
#
proc wr_reg {baseAddress regOffset data} {
  mwr [expr $baseAddress + $regOffset] $data
}


#
# Set bit in register: Sets to '1' single bit in a register (with given address). (Read-Modify-Write)
#
proc set_reg_b {baseAddress regOffset bitPos} {
  wr_reg $baseAddress  $regOffset [set_b [rd_reg $baseAddress  $regOffset] $bitPos]
}


#
# Clears bit in register: Clears to '0' single bit in a register (with given address).
# (Read-Modify-Write)
#
proc clr_reg_b {baseAddress regOffset bitPos} {
  wr_reg $baseAddress  $regOffset [clr_b [rd_reg $baseAddress  $regOffset] $bitPos]
}


#
# Toggles bit in register: Toggles to '0' <-> '1' single bit in a register (with given address).
# (Read-Modify-Write)
#
proc tgl_reg_b {baseAddress regOffset bitPos} {
  wr_reg $baseAddress  $regOffset [tgl_b [rd_reg $baseAddress  $regOffset] $bitPos]
}


#
# Write bitfield in register: Overwrite bitfield (in given position) with given data in a register
# (with given address) (Read-Modify-Write)
#
proc wr_reg_bf {baseAddress regOffset start len newData} {
  wr_reg $baseAddress  $regOffset [set_bf [rd_reg $baseAddress  $regOffset] $newData $start $len]
}


#
# Read bitfield from register: Returns bitfield (given position) of a register (with given address).
#
proc rd_reg_bf {baseAddress regOffset start len} {
  return [get_bf [rd_reg $baseAddress  $regOffset] $start $len]
}

