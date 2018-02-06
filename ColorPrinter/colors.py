class SystemColors(object):

    HEADER = 95
    OKBLUE = 94
    OKGREEN = 92
    WARNING = 93
    FAIL = 91
    BOLD = 1
    UNDERLINE = 4


class Colors(object):

    grey = 30
    red = 31
    green = 32
    yellow = 33
    blue = 34
    magenta = 35
    cyan = 36
    white = 37


class Highlights(object):

    grey = 40
    red = 41
    green = 42
    yellow = 43
    blue = 44
    magenta = 45
    cyan = 46
    white = 47

ENDC = '\033[0m'


def help():

    print "Colors"
    color_print("grey: ", Colors.grey, "grey")
    color_print("red: ", Colors.red, "red")
    color_print("green: ", Colors.green, "green")
    color_print("yellow: ", Colors.yellow, "yellow")
    color_print("blue: ", Colors.blue, "blue")
    color_print("magenta: ", Colors.magenta, "magenta")
    color_print("cyan: ", Colors.cyan, "cyan")
    color_print("white: ", Colors.white, "white")
    print
    print "Highlights"
    color_print("grey: ", Highlights.grey, "grey")
    color_print("red: ", Highlights.red, "red")
    color_print("green: ", Highlights.green, "green")
    color_print("yellow: ", Highlights.yellow, "yellow")
    color_print("blue: ", Highlights.blue, "blue")
    color_print("magenta: ", Highlights.magenta, "magenta")
    color_print("cyan: ", Highlights.cyan, "cyan")
    color_print("white: ", Highlights.white, "white")
    print
    print "SystemColors"
    color_print("HEADER: ", SystemColors.HEADER, "HEADER")
    color_print("OKBLUE: ", SystemColors.OKBLUE, "OKBLUE")
    color_print("OKGREEN: ", SystemColors.OKGREEN, "OKGREEN")
    color_print("WARNING: ", SystemColors.WARNING, "WARNING")
    color_print("FAIL: ", SystemColors.FAIL, "FAIL")
    color_print("BOLD: ", SystemColors.BOLD, "BOLD")
    color_print("UNDERLINE: ", SystemColors.UNDERLINE, "UNDERLINE")


def _get_color(color):

    return "\033[%sm" % color


def _get_colored_text(color, string):

    return _get_color(color) + string + ENDC


def color_print(*args):
    prev_arg = None
    output = ""
    for arg in args:
        if prev_arg is None:
            assert isinstance(arg, str) or isinstance(arg, int), "Input arguments must be colors (int) or text (string)"
            if isinstance(arg, str):
                output += arg
            else:
                prev_arg = arg
        else:
            assert isinstance(arg, str), "Input arguments must be colors (int) or text (string)"
            assert isinstance(prev_arg, int)
            output += _get_colored_text(prev_arg, arg)
            prev_arg = None
            if isinstance(arg, int):
                prev_arg = arg
    print output


# Use color_print to print text with colors
# What we do is
# color_print("no_color_text, ", Colors.red, "the next text is red, ", Highlights.red, "Need to highlight this, ", "no color again, ", "still no color, ", Colors.blue, "and see some blue.")

# if we want to know the color, use help()

if __name__ == "__main__":

    help()
    print
    color_print("no_color_text, ", Colors.red, "the next text is red, ", Highlights.red, "Need to highlight this, ", "no color again, ", "still no color, ", Colors.blue, "and see some blue.")
