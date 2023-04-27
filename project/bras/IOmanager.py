class IOmanager:
    def origin(self):
        with open("bras/config.txt") as lines:
        
            values = [float(n.split(' ')[-1]) for n in lines]

        return values[0], values[1]

    def sudoku(self):
        with open(f"generated_data/resolved_sudoku.txt") as lines:
            sudoku = [
                [int(number) for number in n if (number != '\n')]
            for n in lines
            ]
        return sudoku
