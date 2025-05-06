from model.graph_model import GraphModel

class GraphManager:
    def __init__(self):
        self.current_model = None

    def create_model(self, expressions, x_range, y_range=None):
        self.current_model = GraphModel(expressions, x_range, y_range)
        
    def get_model(self):
        return self.current_model

    def clear(self):
        self.current_model = None
