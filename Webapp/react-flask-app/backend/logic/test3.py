from datetime import datetime
import pause
import pandas as pd

def main():
    token_list = ["1234", "element","test"]
    data_list = []
    for element in token_list:
        data_list.append(["name", element, "service"])
    columns = ['name', 'token', 'service']
    df = pd.DataFrame(data_list, columns=columns)

    df2 = pd.DataFrame(columns=columns)

    print(df)


if __name__ == "__main__":
    main()
