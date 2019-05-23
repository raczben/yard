#include <stdio.h>
#include <stdint.h>

// Guard:
#ifndef __REGUTIL_H__
#define __REGUTIL_H__

#ifdef __DTYPE_8__
    typedef uint8_t dword_t;
#endif
#ifdef __DTYPE_16__
    typedef uint16_t dword_t;
#endif
#ifdef __DTYPE_32__
    typedef uint32_t dword_t;
#endif
#ifdef __DTYPE_64__
    typedef uint32_t dword_t;
#endif

/*******************
 * Naming convention: 
 *  All macros are uppercase
 *  All helper macro starts with type
 *
 *  Abbrev:
 *      - CLR: Clear
 *      - TGL: Toggle
 *      - BF: Bit-field
 */

#define BIT(n)                  ( 1UL<<(n) )

#define BIT_CLR(p,n) ((p) & ~BIT(n))
#define BIT_SET(p,n) ((p) | BIT(n))
#define BIT_TGL(p,n) ((p) ^ BIT(n))

// FROM http://www.coranac.com/documents/working-with-bits-and-bitfields/
//! Create a bitmask of length \a len.
#define BIT_MASK(len)           ( BIT(len)-1 )

//! Create a bitfield mask of length \a starting at bit \a start.
#define BF_MASK(start, len)     ( BIT_MASK(len)<<(start) )

//! Prepare a bitmask for insertion or combining.
#define BF_PREP(x, start, len)  ( ((x)&BIT_MASK(len)) << (start) )


//! Extract a bitfield of length \a len starting at bit \a start from \a y.
#define BF_GET(y, start, len)   ( ((y)>>(start)) & BIT_MASK(len) )

//! Clear a bitfield of length \a len starting at bit \a start from \a y.
#define BF_CLR(y, start, len)   ((y) &~ BF_MASK(start, len)) 

//! Insert a new bitfield value \a x into \a y.
#define BF_SET(y, x, start, len)    \
    ( BF_CLR(y, start, len)  | BF_PREP(x, start, len) )

    
/*********************************************
 * END of helper macros
 * follofing macros can be used by the user.
 ********************************************/
 
#define READ_REG(BaseAddress, RegOffset) \
    *(dword_t*)((void*)BaseAddress + (int)RegOffset)
    
#define WRITE_REG(BaseAddress, RegOffset, Data) \
    *(dword_t*)((void*)BaseAddress + (int)RegOffset) = (dword_t)(Data)


#define SET_REG_BIT(BaseAddress, RegOffset, bitpos) \
    WRITE_REG(BaseAddress, RegOffset, BIT_SET(READ_REG(BaseAddress, RegOffset), bitpos))

#define CLR_REG_BIT(BaseAddress, RegOffset, bitpos) \
    WRITE_REG(BaseAddress, RegOffset, BIT_CLR(READ_REG(BaseAddress, RegOffset), bitpos))

#define TGL_REG_BIT(BaseAddress, RegOffset, bitpos) \
    WRITE_REG(BaseAddress, RegOffset, BIT_TGL(READ_REG(BaseAddress, RegOffset), bitpos))

#define WRITE_REG_BF(BaseAddress, RegOffset, start, len, newData) \
    WRITE_REG(BaseAddress, RegOffset, BF_SET(READ_REG(BaseAddress, RegOffset), newData, start, len))

#define READ_REG_BF(BaseAddress, RegOffset, start, len, newData) \
    BF_GET(READ_REG(BaseAddress, RegOffset), start, len)

    
    /*
int main(){
    int i;
    dword_t arr[] = {1, 2, 0, 4, 0, 6, 7, 8, 9};
    
    WRITE_REG_BF(arr, 4*4, 4, 2, 1);
    
    SET_REG_BIT(arr, 4*2, 2);
    for(i=0; i<9; i++){
        printf(" %x ", arr[i]);
    }
    printf("\n");
    return 0;
}
*/

#endif  // ifdef __REGUTIL_H__