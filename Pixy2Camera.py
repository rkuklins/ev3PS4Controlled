from pixycamev3.pixy2.py import Pixy2

class Pixy2Camera:
    Pixy2 pixy;


    def __init__(self):
        self.pixy = Pixy2(port=1, i2c_address=0x54)
        self.pixy.init()

    def get_blocks(self):
            """
            Retrieves the blocks detected by the PixyCam.

            Returns:
                A list of blocks detected by the PixyCam.
            """
            blocks = []
            frame = self.pixy.get_frame()
            if frame:
                for i in range(frame.block_count):
                    block = frame.blocks[i]
                    blocks.append(block)
            return blocks

    def print_blocks(self):
        blocks = self.get_blocks()
        for block in blocks:
            print("Block ID:", block.id)
            print("Block X:", block.x)
            print("Block Y:", block.y)
            print("Block Width:", block.width)
            print("Block Height:", block.height)
            print()

    def get_block_count(self):
        frame = self.pixy.get_frame()
        if frame:
            return frame.block_count
        return 0

    def close(self):
        self.pixy.close()
