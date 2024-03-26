import os.path


def get_epc_label(consumption):
    if consumption == 0:
        return "A+", os.path.join('images', 'aplus.png')
    elif consumption <= 100:
        return "A", os.path.join('images', 'a.png')
    elif consumption <= 200:
        return "B", os.path.join('images', 'b.png')
    elif consumption <= 300:
        return "C", os.path.join('images', 'c.png')
    elif consumption <= 400:
        return "D", os.path.join('images', 'd.png')
    elif consumption <= 500:
        return "E", os.path.join('images', 'e.png')
    elif consumption <= 600:
        return "F", os.path.join('images', 'f.png')
    else:
        return "G", os.path.join('images', 'g.png')
