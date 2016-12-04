from enum import Enum

class SectionType(Enum):
    declare_var = 1
    if_control = 2
    else_control = 3
    while_control = 4
    io_operation = 5
    arithmetic_operation = 6