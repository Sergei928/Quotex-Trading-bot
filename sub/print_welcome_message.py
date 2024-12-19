from termcolor import colored
def print_welcome_message(border_length=77):
    border_line = colored('*' * border_length, 'cyan')
    empty_line = colored('*' + ' ' * (border_length - 2) + '*', 'cyan')
    
    welcome_text = colored('Welcome to ', 'white') + colored('Auto Trading Bot', 'green')
    contact_text = colored('Contact us on ', 'white') + colored('Telegram', 'magenta') + colored(' to implement any strategy on your bot', 'white')

    # Calculate the spaces needed on each side of the centered text
    welcome_spaces = (border_length - 2 - len('Welcome to Auto Trading Bot')) // 2
    contact_spaces = (border_length - 2 - len('Contact us on Telegram to implement any strategy on your bot')) // 2

    # Create welcome and contact lines with proper spacing
    welcome_line = colored('*', 'cyan') + ' ' * welcome_spaces + welcome_text + ' ' * welcome_spaces + colored('*', 'cyan')
    contact_line = colored('*', 'cyan') + ' ' * contact_spaces + contact_text + ' ' * contact_spaces + colored(' *', 'cyan')

    print(border_line)
    print(empty_line)
    print(welcome_line)
    print(empty_line)
    print(contact_line)
    print(empty_line)
    print(border_line)