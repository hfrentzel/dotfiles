def print_grid(header, rows):
    if len(rows) == 0:
        return ""
    max_lengths = [0] * len(header)
    for row in [header, *rows]:
        for i in range(len(max_lengths)):
            max_lengths[i] = max(max_lengths[i], len(row[i]))

    line = ''
    for row in [header, *rows]:
        line += ' '.join([f'{r: <{max(13, max_lengths[i])}}'
                             for i, r in enumerate(row)]) + '\n'
    line += '\n'
    return line
