def color_text(c: str, txt):
    """
        To edit the text color.

        :param c: color.
        :param txt: text.
    """
    if c == 'red':
        return '\033[91m{}\033[m'.format(txt)
    elif c == 'white':
        return '\033[97m{}\033[m'.format(txt)
    elif c == 'green':
        return '\033[92m{}\033[m'.format(txt)
    elif c == 'yellow':
        return '\033[93m{}\033[m'.format(txt)
    elif c == 'blue':
        return '\033[94m{}\033[m'.format(txt)
    elif c == 'cyan':
        return '\033[96m{}\033[m'.format(txt)
    elif c == 'grey':
        return '\033[97m{}\033[m'.format(txt)
    elif c == 'magenta':
        return '\033[95m{}\033[m'.format(txt)
