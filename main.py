from src.model import Model
from src.presenter import Presenter
from src.view import View

if __name__ == '__main__':
    presenter = Presenter(input_csv_path="data/2022.CSV",
                          model=Model(spending_dict_path="config/spending.json"),
                          view=View())
    # TODO December is missing in the dashboard, maybe something with the mapping went wrong because index starts at 0
    presenter.create_report()
