
#include "stdio.h"
#include "minimal.h"

int mem[1000];

#define BASE_ADDR (dword_t*)(mem)

int main(){
    set_data(BASE_ADDR, 1);
    if(get_data(BASE_ADDR) != 1) {
        //missmatch
        printf("[ERROR] get_data(BASE_ADDR) != 1   %d != %d", get_data(BASE_ADDR), 1);
        return -1;
    }
    set_data(BASE_ADDR, 0);
    if(get_data(BASE_ADDR) != 0) {
        printf("[ERROR] get_data(BASE_ADDR) != 1   %d != %d", get_data(BASE_ADDR), 0);
        //missmatch
        return -1;
    }
    set_data(BASE_ADDR, 123456);
    if(get_data(BASE_ADDR) != 123456) {
        printf("[ERROR] get_data(BASE_ADDR) != 1   %d != %d", get_data(BASE_ADDR), 123456);
        //missmatch
        return -1;
    }
    
    // Success
    printf("[PASS]");
    return 0;
}