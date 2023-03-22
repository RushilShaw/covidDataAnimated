import pandas as pd
from matplotlib import pyplot as plt
from datetime import date, timedelta


DEATH_FACTOR = 50  # The factor at which deaths are scaled up at
DEATHS_SHIFT = -14
SMOOTHING_FACTOR = 14  # The amount of days the cases that are averaged


def format_day(day):
    """converts dates format to datetime.dates"""
    formatted_day = date.fromisoformat(day)
    return formatted_day


def main():
    df = pd.read_csv("us.csv")
    df["date"] = df["date"].apply(format_day)

    new_cases = [0]
    for index, case_count in enumerate(df["cases"][1:]):
        new_cases.append(case_count - df["cases"][index])
    df["daily_new_cases"] = new_cases

    average_new_cases = [0] * (SMOOTHING_FACTOR - 1)
    for index, case_count in enumerate(df["daily_new_cases"][SMOOTHING_FACTOR - 1:]):
        average_new_cases.append(sum(df["daily_new_cases"][index: index + SMOOTHING_FACTOR]) / SMOOTHING_FACTOR)
    df["average_new_cases"] = average_new_cases

    new_deaths = [0]
    for index, death_count in enumerate(df["deaths"][1:]):
        new_deaths.append(death_count - df["deaths"][index])
    new_deaths = [item * DEATH_FACTOR for item in new_deaths]  # O(n) operation that can easily be removed
    df["daily_deaths"] = new_deaths

    average_deaths = [0] * (SMOOTHING_FACTOR - 1)
    for index, case_count in enumerate(df["daily_deaths"][SMOOTHING_FACTOR - 1:]):
        average_deaths.append(sum(df["daily_deaths"][index: index + SMOOTHING_FACTOR]) / SMOOTHING_FACTOR)
    df["average_deaths"] = average_deaths

    # plt.plot(df["date"], df["daily_new_cases"], "o", label="Cases")
    # plt.plot(df["date"], df["daily_deaths"], "-", label="Deaths")
    plt.plot(df["date"], df["average_new_cases"], "-", label="CasesAverage")
    plt.plot(df["date"] + timedelta(DEATHS_SHIFT), df["average_deaths"], "-", label="AverageDeaths")

    plt.title("Covid Data") 
    plt.xlabel('Date')
    plt.ylabel('Cases/Deaths')
    plt.legend(loc='upper left')
    plt.show()


def animated_main():
    global DEATH_FACTOR, DEATHS_SHIFT, SMOOTHING_FACTOR
    DEATH_FACTOR = int(input("By what factor would you like to increase the amount of Deaths by: "))
    DEATHS_SHIFT = int(input("How much would you like to shift the death dates of the x-axis: "))
    SMOOTHING_FACTOR = int(input("How many days average would you like to use to smooth the graph: "))


if __name__ == '__main__':
    if True:
        animated_main()
    main()
