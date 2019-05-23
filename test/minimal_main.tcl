source minimal.tcl

variable mem "0 0 0 0 0 0 0 0 0 0"

variable BASE_ADDR 100
#
# Overwrite lowest level register access procedures.
#

#
# Read register: Reads a simple memory mapped register from the given baseaddress and register offset.
#
proc rd_reg {baseAddress regOffset} {
    global mem
    return [lindex mem [expr $baseAddress + $regOffset - $::BASE_ADDR]]
}


#
# Write register: Writes a simple memory mapped register to the given baseaddress and register offset.
#
proc wr_reg {baseAddress regOffset data} {
    global mem
    lset mem [expr $baseAddress + $regOffset - $::BASE_ADDR] $data
}

proc assertt {lval rval message} {
    if {$lval != $rval} { error "ERROR  $message   $lval != $rval" }
}

proc main {} {
    set_data $::BASE_ADDR 1
    assertt [get_data $::BASE_ADDR] 1 "get_data $::BASE_ADDR != 1"
    
    set_data(::BASE_ADDR, 0);
    assertt [get_data $::BASE_ADDR] 0 "get_data $::BASE_ADDR != 0"
    
    set_data(::BASE_ADDR, 123456);
    assertt [get_data $::BASE_ADDR] 123456 "get_data $::BASE_ADDR != 123456"
    
    # Success
    puts "[PASS]"
    return 0
}

main