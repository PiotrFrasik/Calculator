from sympy import sympify

# check if pointer is over button
def check_cursor(master, buttons_list):
    x, y = master.winfo_pointerx(), master.winfo_pointery()  # Pointer position
    widget = master.winfo_containing(x, y)  # Posisiton widget under pointer
    # Change bg button
    for button in buttons_list:
        if button == widget:
            button.config(bg="#666569")
        else:
            button.config(bg="#77767a")

    master.after(50, check_cursor)

#Send txt to buttons_function
def on_click(buttons_list, buttons_function):
    for index, button in enumerate(buttons_list):
        button.bind('<Button-1>', lambda event, i=index: buttons_function(i))


def delete_zeros(number):
    if str(number) == "0":
        return number

    if "e" in str(number):
        return number

    try:
        if type(number) != str:
            number = str(number)

        while number[-1] == "0":
            number = number[:-1]

        if number[-1] == ".":
            number = number[:-1]
    except IndexError:
        return "0"

    return number


def round_number(number):
    if str(number) == "0":
        return number

    # max thirteen number on the screen in time fg = 39
    # max sixteen number on the screen in time fg = 27
    number = sympify(number).evalf()
    if len(str(number)) > 15:

        index_dot = str(number).find(".")
        index_e = str(number).find("e")

        if index_e != -1:
            number_to_round_e = 15 - (len(str(number)) - index_e) - index_dot
            return str(sympify(number).evalf(number_to_round_e))
        else:
            number_to_round = 15 - index_dot
            return str(round(number, number_to_round))

