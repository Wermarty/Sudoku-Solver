class serWriter:
    def __init__(self, ser):
        self.ser = ser

    def draw(self, number, x_coord, y_coord):
        msg = "draw:" +str(number) + ":" + str(y_coord) + ":" + str(x_coord) + ":null"
        self.ser.write(msg.encode('utf-8'))
        self.ser.reset_input_buffer()
        
    def init(self, case_size):
        msg = "init_case_size:" + str(case_size) + ":null"
        self.ser.write(msg.encode('utf-8'))
        self.ser.reset_input_buffer()

    def reset(self):
        msg = "reset:null"
        self.ser.write(msg.encode('utf-8'))
        self.ser.reset_input_buffer()
