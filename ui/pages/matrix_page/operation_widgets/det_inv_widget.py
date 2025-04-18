from ui.pages.matrix_page.operation_widgets.add_sub_widget import MatrixAddSubWidget

class MatrixDeterminantWidget(MatrixAddSubWidget):
    def __init__(self, manager, controller):
        super().__init__(manager, controller, allow_multiple_matrices=False)

class MatrixInverseWidget(MatrixAddSubWidget):
    def __init__(self, manager, controller):
        super().__init__(manager, controller, allow_multiple_matrices=False)
