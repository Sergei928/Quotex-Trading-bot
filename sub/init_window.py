import os
def set_window_size(columns, rows):
    #clear_console()
    cmd = f'mode con: cols={columns} lines={rows}' if os.name == 'nt' else f'printf "\\033[8;{rows};{columns}t"'
    os.system(cmd)

def init():
    set_window_size(128, 9999)