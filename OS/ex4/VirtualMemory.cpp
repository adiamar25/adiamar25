#include "PhysicalMemory.cpp"
#include "VirtualMemory.h"

#define FAILURE 0
#define SUCCESS 1
#define P_i(i, vAddr) ((vAddr >> (OFFSET_WIDTH * (TABLES_DEPTH-i)) % PAGE_SIZE))
#define SHIFT_START (64 - VIRTUAL_ADDRESS_WIDTH)
#define ROOT 0
#define NO_MATCHING_ADDRESS 0

void configure_frame(uint64_t physicalAddress);


/**
 *
 * @param physicalAddress the !!physical address!! of the frames head
 */
void configure_frame(uint64_t physicalAddress)
{
  int i = 0;
  while (i < PAGE_SIZE)
  {
    PMwrite (physicalAddress + i, 0);
    ++i;
  }ִִ
}

uint64_t min(uint64_t a, uint64_t b)
{
  if (b >= a)
  {
    return a;
  }
  return b;
}

uint64_t abs(int64_t a)
{
  if (a < 0)
  {
    return -a;
  }
  return a;
}

uint64_t cyclic_distance(uint64_t page_swapped_in, uint64_t p)
{
  return min(NUM_PAGES - abs((int64_t)(page_swapped_in - p)),
             abs((int64_t)(page_swapped_in - p)));
}

//int DFS(uint64_t curFrameNum, uint64_t potentialVictim, int depth,)

uint64_t find_or_evict_frame(uint64_t cur_frame_num, uint64_t potential_victim, int depth,
                             uint64_t parent, uint64_t offset)
{
  bool empty_frame = false;

}

uint64_t a_bits_from_b(uint64_t value, int a, int b)
{
  return (value << a) >> (64 - b);
}

uint64_t val_to_physical_address(uint64_t virtualAddress)
{
  word_t curAddress = 0;
  uint64_t pageIndex = virtualAddress >> OFFSET_WIDTH;
  for (int i = 0; i < TABLES_DEPTH; i++)
  {
    uint64_t pi = P_i(i, virtualAddress);
    PMread(curAddress*PAGE_SIZE + pi, &curAddress);
    if (curAddress == 0)
    {
      // find unused frame or evict a page from some frame.
      // suppose this frame number is f1.
      // write 0 in all of it's content (only necessary if next layer  is a table)
      uint64_t f = find_or_evict_frame();
      if (TABLES_DEPTH - i > 1) // The next layer is a table
      {
        configure_frame (f * PAGE_SIZE);
      }
      else
      {
        PMrestore (f, pageIndex);
      }
      PMwrite (curAddress*PAGE_SIZE +pi, curAddress);
      curAddress = f;
    }
  }
}

/*
 * Initialize the virtual memory, fill frame0 with zeroes
 */
void VMinitialize()
{
  configure_frame(0);
}

/* reads a word from the given virtual address
 * and puts its content in *value.
 *
 * returns 1 on success.
 * returns 0 on failure (if the address cannot be mapped to a physical
 * address for any reason)
 */
int VMread(uint64_t virtualAddress, word_t* value)
{
  if (virtualAddress >= VIRTUAL_MEMORY_SIZE)
  {
    return FAILURE;
  }

}