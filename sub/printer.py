import re
from termcolor import colored

class PrettyTablePrint:
    def __init__(self, header):
        self.header = header
        self.column_widths = [0] * len(header)

    def strip_ansi(self, text):
        # Strip ANSI color codes from a string
        return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', text)

    def get_column_widths(self, rows):
        # Calculate the maximum width of each column based on the header and rows
        self.column_widths = [len(self.strip_ansi(field)) for field in self.header]
        for row in rows:
            for i, cell in enumerate(row):
                cell_length = len(self.strip_ansi(str(cell)))
                self.column_widths[i] = max(self.column_widths[i], cell_length)
        return self.column_widths

    def print_separator(self):
        # Print a row separator
        separator = '+'.join(['-' * (w + 2) for w in self.column_widths])
        print(f"+{separator}+")

    def print_header(self):
        # Create the header row and separator
        self.print_separator()
        header_row = "| " + " | ".join([field.center(width) for field, width in zip(self.header, self.column_widths)]) + " |"
        print(header_row)
        self.print_separator()

    def print_row(self, row):
        # Format and print a single row
        if len(row) != len(self.header):
            raise ValueError("Row length does not match header length.")
        
        formatted_cells = []
        for cell, width in zip(row, self.column_widths):
            cell_text = str(cell)
            cell_length = len(self.strip_ansi(cell_text))
            padding = width - cell_length
            left_padding = padding // 2
            right_padding = padding - left_padding
            formatted_cell = ' ' * left_padding + cell_text + ' ' * right_padding
            formatted_cells.append(formatted_cell)
        
        formatted_row = "| " + " | ".join(formatted_cells) + " |"
        print(formatted_row)

    def print_footer(self):
        # Print the table footer
        self.print_separator()
def print_user_info_message(user_info):
    print('\nWelcome back!')
    print('User: ' + colored(user_info['data']['email'], 'blue'))
    print('Country: ' + colored(user_info['data']['countryName'], 'blue'))
    print('Token: ' + colored(user_info['data']['token'], 'blue'))
    print('LiveBalance: ' + colored(user_info['data']['liveBalance'], 'green'))
    print('DemoBalance: ' + colored(user_info['data']['demoBalance'], 'cyan'))