from datetime import datetime, date
import pandas as pd
import pathlib


def asses_temperature(temperature):
    """"Judge results of temperature
    value received from the form
    and return an appropriate message

    Parameters
    ----------
    temperature : str
        String convertible to float

    Returns
    -------
    message : str
        Message informing if the
        result was correct.
    temperature : float or str
        Either converted or not.
    """
    try:
        # replace decimal separator if needed
        temperature = temperature.replace(",", ".")
        temperature = float(temperature)
        if temperature > 40:
            message = f"{temperature} °C to trochę za gorąco. " \
                      f"Powtórzyć pomiar?"
        elif temperature < 35:
            message = f"Powiało chłodem (wynik: {temperature} °C). " \
                      f"Powtórzyć pomiar?"
        else:
            message = f"Zmierzono {temperature} °C"
    except ValueError:
        message = "Temperatura wprowadzona niepoprawnie, spróbuj jeszcze raz."

    return message, temperature


def save_temperature(temperature, path="temperatures.csv"):
    """Save temperature with
    a timestamp to file.
    """
    timestamp = date.today().isoformat()
    path = pathlib.Path(__file__).parent / path
    if not path.is_file():
        with open(path, "w") as f:
            f.write("date,temperature\n")
            f.write(f"{timestamp},{temperature}\n")
    else:
        data = pd.read_csv(path, squeeze=True, index_col=0)
        data[timestamp] = temperature
        data.to_csv(path)


def create_plot(path="temperatures.csv"):
    path = pathlib.Path(__file__).parent / path
    #remove old file
    image_folder = pathlib.Path(__file__).parent / "static"
    to_delete = image_folder.glob("temperatures*")
    for image in to_delete:
        image.unlink()

    # read data
    data = pd.read_csv(path)
    # set plot style
    #sns.set_theme()

    # generate plot
    my_plot = data.plot(
        x="date",
        y="temperature",
        xlabel="Data",
        ylabel="Temperatura [°C]",
        title="Pomiary temperatury",
        style="o--",
        legend=False
    )
    my_fig = my_plot.get_figure()
    # timestamp generated to prevent browsers from caching
    image_name = f"temperatures_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.svg"
    save_path = pathlib.Path(__file__).parent / "static" / image_name
    my_fig.savefig(save_path, format="svg")
    return "/static/" + image_name


if __name__ =="__main__":
    #save_temperature(36.8)
    create_plot()
