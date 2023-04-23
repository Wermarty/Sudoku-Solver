class IOmanager:
    def origin():
        with open("integration\drawer\config.txt") as lines:
        
            values = [float(n.split(' ')[-1]) for n in lines]

        return values[0], values[1]

    def sudoku():
        with open(f".txt") as lines:
            sudoku = [
                [int(number) for number in n if (number != '\n')]
            for n in lines
            ]
        return sudoku