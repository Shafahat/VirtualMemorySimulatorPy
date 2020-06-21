import re

def find_int(str):
    integers_list = list(map(int, re.findall(r'\d+', str)))
    return integers_list

def createVirtualMemory(virtual_memory_size, page_size): 
    virtual_memory = [[0 for count in range(page_size)] for count in range(virtual_memory_size)] 
    return virtual_memory
    
def createPhysicalMemory(physical_memory_size):
    physical_memory = [None for count in range(physical_memory_size)] 
    return physical_memory

def createSwapArea(swap_area_size):
    swap_area = [None for count in range(swap_area_size)]
    return swap_area

def get_value_from(page_number, address_index):
    virtual_memory
    value_at = virtual_memory[page_number][address_index]
    return value_at

def update_value_at_virtual_memory(page_number, address, value):
    virtual_memory
    virtual_memory[page_number][address] = value

def update_physical_memory(page_index, page_number):
    physical_memory[page_index] = page_number

def update_swap_area(page_index, page_number):
    swap_area[page_index] = page_number

def is_dirty(page_number):
    virtual_memory
    i = 0
    while i < len(virtual_memory[page_number]):
        if virtual_memory[page_number][i] != 0:
            result = True
            break
        else:
            result = False
        i += 1
    return result
    
def handle_fault(A, page_number):
    print("Page fault at " + str(A) + "\n")
    free_frame_index = free_frame()
    loading_page = page_number
    load_page(loading_page, free_frame_index)
    return free_frame_index

def free_frame():
    temp = next_page_to_evict
    free_frame_index = check_memory(None)
    if free_frame_index == -1:
        temp = 0
        while temp < physical_memory_size:
            if second_chance(temp) == False:
                result = temp
                break
            else:
                result = 0
            temp+=1             
        evict_page(result)
        free_frame_index = result
    return free_frame_index
   
def second_chance(temp):
    page_to_evict = physical_memory[temp]
    second_chance = []
    second_chance.append(page_to_evict)
    if is_referenced(page_to_evict) == False:
        # evict_page(temp)
        return False
    else:
        referenced_page_numbers.remove(page_to_evict)
        return True
        

def evict_page(temp):    
    page_to_evict = physical_memory[temp]
    update_physical_memory(temp, None)
    print("Evicting page " + str(page_to_evict) + " from frame " + str(temp) + "\n")
    if is_dirty(page_to_evict) == True:
        free_swap_index = check_swap(None)
        if free_swap_index == -1:
            free_swap_index = 0
        else:
            free_swap_index = free_swap_index
        update_swap_area(free_swap_index, page_to_evict)
        print("Saving page " + str(page_to_evict) + " to swap block " + str(free_swap_index) + "\n")

def increase_page_index(temp):
    if temp == physical_memory_size - 1:
        temp = 0
    else:
        temp += 1  
    return temp

def load_page(loading_page, free_frame_index):
    index_swap = check_swap(loading_page)
    if index_swap != -1:
        update_swap_area(index_swap, None)
    update_physical_memory(free_frame_index, loading_page)
    if index_swap == -1:
        result = ""
    else:
        result = " from swap block " + str(index_swap)
    print("Loading page " + str(loading_page) + result + " to frame " + str(free_frame_index) + "\n")        


referenced_page_numbers = []

def is_referenced(page_number):
    if page_number not in referenced_page_numbers:
        result = False
    else:
        result = True
    return result

def add_referenced(page_number):
    if page_number not in referenced_page_numbers:
        referenced_page_numbers.append(page_number)

def check_memory(page_number):
    i = 0
    while i < len(physical_memory):
        if physical_memory[i] == page_number:
            result = i
            break
        else:
            result = -1
        i += 1  
    return result

def check_swap(page_number):
    i = 0
    while i < len(swap_area):
        if swap_area[i] == page_number:
            result = i
            break
        else:
            result = -1
        i += 1  
    return result

def init(V,M,S,P):
    global page_size
    page_size = P*1000
    virtual_memory_size = V//P
    global physical_memory_size
    physical_memory_size = M//P
    swap_area_size = S//P  
    global virtual_memory
    virtual_memory = createVirtualMemory(virtual_memory_size, page_size)
    global physical_memory
    physical_memory = createPhysicalMemory(physical_memory_size)
    global swap_area
    swap_area = createSwapArea(swap_area_size)
    global next_page_to_evict
    next_page_to_evict = 0
    print('initilazied \n')
    # print('initilazied\n')

def read(A):
    page_number = A // page_size 
    address_index = A % page_size
    add_referenced(page_number)
    page_index = check_memory(page_number)
    if page_index == -1:
        page_index = handle_fault(A, page_number)
    value_at = get_value_from(page_number, address_index)
    print("Value at address " + str(A) + " is " + str(value_at) + "\n")
    
def write(A, X):
    page_number = A // page_size 
    address_index = A % page_size
    add_referenced(page_number)
    update_value_at_virtual_memory(page_number, address_index, X)
    page_index = check_memory(page_number)
    if page_index == -1:
        page_index = handle_fault(A, page_number)
    print("Written " + str(X) + " to address " + str(A) + "\n")

def print_memory():
    physical_memory
    i = 0
    while i < len(physical_memory):
        print(physical_memory[i])
        i+=1
def print_swap():
    swap_area
    i = 0
    while i < len(swap_area):
        print(swap_area[i])
        i+=1

def exit():
    print("memory -" + str(physical_memory))
    print("swap -" + str(swap_area))

def log(str):
    f = open('desktop/os/input.txt','w')
    f.write(str)

with open ('input.txt', 'r') as myfile:
        for line in myfile:
            if 'Init' in line:
                sizes_list = find_int(line)
                V = sizes_list[0]
                M = sizes_list[1]
                S = sizes_list[2]
                P = sizes_list[3]
                init(V, M, S, P)
            elif 'Read' in line:
                address = find_int(line)
                A = address[0]
                read(A)
            elif 'Write' in line:
                address_value = find_int(line)
                A = address_value[0]
                X = address_value[1]
                write(A, X)
            elif 'Exit' in line:
                exit()  
            else:
                break