class ExperimentData():
    def __init__(self, data, name):
        self.name = name
        self.data = data

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __repr__(self):
        return self.__str__()
