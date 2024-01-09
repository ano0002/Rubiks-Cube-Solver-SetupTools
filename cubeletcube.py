class CubeletCube:
    def __init__(self, state: list=None):
        if state is None:
            self.cube = [[[]],[[]],[[]]]