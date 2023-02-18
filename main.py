from src.presenter import Presenter
from src.view import View
from src.model import Model

if __name__ == '__main__':
    presenter = Presenter(input_csv_path="data/2020.CSV",
                          model=Model(),
                          view=View())

    presenter.create_report()