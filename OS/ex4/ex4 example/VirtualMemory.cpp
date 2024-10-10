#include "VirtualMemory.h"
#include "PhysicalMemory.h"

////debugging
//#include <iostream>
//using std::cout;
//using std::endl;

#define P1 (VIRTUAL_ADDRESS_WIDTH-(TABLES_DEPTH*OFFSET_WIDTH))
#define ROOT 0
#define STARTING_SHIFT (64 - VIRTUAL_ADDRESS_WIDTH)
#define SUCCESS 1
#define FAILURE 0
#define NO_MATCHING_ADDRESS 0




typedef struct traverse_info{
    uint64_t page;
    bool done=false;
    //for all cases
    //for case 1
    uint64_t address_of_parent_line_frame_to_use; // added
    uint64_t frame_to_use;
    uint64_t dont_touch = NO_MATCHING_ADDRESS;
    //for case 2
//    uint64_t address_of_parent_line_frame_max; // added probably isn't required in case 2
    uint64_t max_frame_index = ROOT;
    //for case 3
    uint64_t address_of_parent_line_frame_cyclic_max; // added
    uint64_t max_cyclic_dist=0;
    uint64_t frame_of_max_cyclic=NO_MATCHING_ADDRESS;
    uint64_t page_of_max_cyclic=NO_MATCHING_ADDRESS;
}traverse_info;



uint64_t our_abs(int64_t num){
    return (num >= 0) ? num : (-num);
}

uint64_t min(uint64_t x, uint64_t y){
    return (x <= y) ? x : y;
}

/***
 *  extracts x bits that resides y bits from the msb
 *  note that x+y <= 64 must hold
 * @param value the 64 bit number that we are extracting from
 * @param x the number of bits to extract
 * @param y the place (right from the msb) to extract from
 * @return
 */
uint64_t extract_x_bits_y_from_msb(uint64_t value, int x, int y){
    uint64_t res = value << y;
    return (res >> (64 - x));
}


/**
 *
 * @param physicalAddr the !!physical address!! of the frames head
 */
void fill_with_zeroes(uint64_t physicalAddr){
    for (int i=0; i<PAGE_SIZE; i++){
        PMwrite(physicalAddr+i, 0);
    }
}
/***
 *
 * @param frame_num  the !!frame index!! of the frame to check
 * @return
 */
bool is_frame_empty(uint64_t frame_num){
    word_t some_value;
    for (int i = 0; i < PAGE_SIZE; ++i) {
        PMread(frame_num*PAGE_SIZE+i, &some_value);
        if(some_value != 0){
            return false;}
    }
    return true;
}

/**
 * get the right frame Address according to the case we've encountered while traversing the tree
 * and doing the following actions if necessary:
 * unlinking
 * evicting
 * zeroing?
 * (anything else)?
 * @param info
 * @return
 */
word_t get_frame_num_from_info( const traverse_info& info) {
    word_t addr;
    if (info.done){ ///case 1 in the instructions
        addr=(word_t)info.frame_to_use;
        PMwrite(info.address_of_parent_line_frame_to_use, ROOT);
    }
    else if (info.max_frame_index+1<NUM_FRAMES){ ///case 2 in the instructions

        addr=(word_t)info.max_frame_index+1;
//  PMwrite(info.address_of_parent_line_frame_max, ROOT); /// probably isn't required in case 2
    }
    else{///case 3 in the instructions
        addr=(word_t)info.frame_of_max_cyclic;
        PMwrite(info.address_of_parent_line_frame_cyclic_max, ROOT);
        PMevict(info.frame_of_max_cyclic, info.page_of_max_cyclic);
    }

    return addr;
}

/***
 *
 * @param info
 */
void reset_info(traverse_info &info, uint64_t last_frame_found_dont_touch) {
    info.done=false;
    //for all cases
    //for case 1
    info.address_of_parent_line_frame_to_use=ROOT;
    info.frame_to_use=NO_MATCHING_ADDRESS;
    info.dont_touch = last_frame_found_dont_touch;
    //for case 2
//     info.address_of_parent_line_frame_max=NO_MATCHING_ADDRESS; $probably isn't required in case 2
     info.max_frame_index = ROOT;
    //for case 3
     info.address_of_parent_line_frame_cyclic_max=ROOT;
     info.max_cyclic_dist=0;
     info.frame_of_max_cyclic=NO_MATCHING_ADDRESS;
     info.page_of_max_cyclic=NO_MATCHING_ADDRESS;
}


uint64_t find_cyclic_distance(uint64_t page_swapped_in, uint64_t p){
    auto x = (NUM_PAGES - our_abs((int64_t )page_swapped_in - (int64_t)p));
    auto y = our_abs((int64_t )page_swapped_in - (int64_t )p);
    return min(x,y);
}


void find_frame(traverse_info &info, int depth, uint64_t curr_frame_num, uint64_t potential_victim,
                                                    uint64_t parent , uint64_t offset){
    if (info.done){ return; }
    if ((TABLES_DEPTH)<=depth){ //todo -+1? important
         if((TABLES_DEPTH+1)==depth){return;}
        uint64_t curr_cyclic_dist = find_cyclic_distance(info.page, potential_victim);
        if(curr_cyclic_dist>info.max_cyclic_dist){
            info.max_cyclic_dist=curr_cyclic_dist;
            info.frame_of_max_cyclic=curr_frame_num;
            info.page_of_max_cyclic=potential_victim;
            info.address_of_parent_line_frame_cyclic_max = (parent * PAGE_SIZE + offset);
        }

    }
    if (curr_frame_num != info.dont_touch  && is_frame_empty(curr_frame_num)&& depth <TABLES_DEPTH){
        info.done= true;
        info.frame_to_use=curr_frame_num;
        info.address_of_parent_line_frame_to_use= (parent * PAGE_SIZE + offset);
        return;
    }
    if (curr_frame_num > info.max_frame_index){
        info.max_frame_index=curr_frame_num;
    }
    for (int i=0; i<PAGE_SIZE; i++){
        word_t content;
        PMread(curr_frame_num*PAGE_SIZE+i, &content); //if row not zero
        if (content!=0){
         uint64_t new_p= potential_victim;
         if(depth < TABLES_DEPTH){
             new_p= (potential_victim << OFFSET_WIDTH) + i;}
             find_frame(info, (depth+1), content, new_p, curr_frame_num , i );
        }
    }
}


uint64_t reach_a_leaf(uint64_t virtualAddress) { // TODO TODO how can it fail
    word_t addr = 0;
    if(TABLES_DEPTH != 0) {
        word_t previous_addr;
        uint64_t p1 = extract_x_bits_y_from_msb(virtualAddress, P1, STARTING_SHIFT);
        traverse_info info;
        info.page =
                virtualAddress >> OFFSET_WIDTH;// extracting the page index from the virtualAddress
        PMread(ROOT + p1, &addr);
        if (addr == 0) {
            find_frame(info, 0, ROOT, addr, 0, 0);
            addr = get_frame_num_from_info(info);
            if(TABLES_DEPTH == 1){ //todo added
                PMrestore(addr, info.page);//todo added
            }
            else {
                fill_with_zeroes(addr * PAGE_SIZE); //(only necessary if next layer is a table)
            }
            PMwrite(ROOT + p1, addr);
        }
        reset_info(info, addr);
        uint64_t pi;
        for (int i = 0; i < (TABLES_DEPTH - 1); i++) { //todo +-1??
            auto shift = STARTING_SHIFT + P1 + OFFSET_WIDTH * i;
            pi = extract_x_bits_y_from_msb(virtualAddress, OFFSET_WIDTH, shift);
            previous_addr = addr;
            PMread(previous_addr * PAGE_SIZE + pi, &addr);
            if (addr == 0) {
                find_frame(info, 0, ROOT, 0, 0, 0);
                addr = get_frame_num_from_info(info);
                if (i == TABLES_DEPTH - 2) {// Restore the page we are looking for to frame  (only
                    //necessary pointing to a page)
                    PMrestore(addr, info.page);
                } else { //(only  necessary if next layer is a table)
                    fill_with_zeroes(addr * PAGE_SIZE);
                }
                PMwrite(previous_addr * PAGE_SIZE + pi, addr);

            }
            reset_info(info, addr);
        }
    }
    auto shift  = STARTING_SHIFT + P1 + OFFSET_WIDTH * (TABLES_DEPTH-1);
    uint64_t offset=extract_x_bits_y_from_msb(virtualAddress, OFFSET_WIDTH,shift);
    return addr*PAGE_SIZE+offset; // the address of the leaf
}




/* Initialize the virtual memory.
*/
void VMinitialize(){
//    cout <<  "table depth is: " << TABLES_DEPTH << "\nP! is : " << P1 << "\nnum of  frames : " <<
//    NUM_FRAMES << "\nnum of pages is : " << NUM_PAGES << "\nvirtual memory size is : " <<
//    VIRTUAL_ADDRESS_WIDTH << "  " << VIRTUAL_MEMORY_SIZE <<"\nphysical memory size = " <<
//    PHYSICAL_ADDRESS_WIDTH << "  " << RAM_SIZE << " \noffset width = " << OFFSET_WIDTH <<
//    "\npage size : " << PAGE_SIZE << endl;
     fill_with_zeroes(0);
}

/* Reads a word from the given virtual address
 * and puts its content in *value.
 *
 * returns 1 on success.
 * returns 0 on failure (if the address cannot be mapped to a physical
 * address for any reason)
 */
int VMread(uint64_t virtualAddress, word_t* value){
    uint64_t res = reach_a_leaf(virtualAddress);
    if( virtualAddress >= VIRTUAL_MEMORY_SIZE ||TABLES_DEPTH > NUM_FRAMES){
        return FAILURE;
    }
    PMread(res, value);
    return SUCCESS;
}

/* Writes a word to the given virtual address.
 *
 * returns 1 on success.
 * returns 0 on failure (if the address cannot be mapped to a physical
 * address for any reason)
 */
int VMwrite(uint64_t virtualAddress, word_t value){
    uint64_t res = reach_a_leaf(virtualAddress);
    if( virtualAddress >= VIRTUAL_MEMORY_SIZE ||TABLES_DEPTH > NUM_FRAMES ){
        return FAILURE;
    }
    PMwrite(res, value);
    return SUCCESS;
}




//todo todo todo   delete all printing and include