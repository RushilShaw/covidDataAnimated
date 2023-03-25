import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


def format_day(day):
    """Converts date string to datetime.date object."""
    formatted_day = date.fromisoformat(day)
    return formatted_day


def main(deaths_shift, smoothing_factor):
    """Generates and displays a graph of Covid deaths and cases."""
    df = pd.read_csv("us.csv")

    # Convert date strings to datetime.date objects
    df["date"] = df["date"].apply(format_day)

    # Calculate daily new cases and 14-day rolling average
    df["daily_new_cases"] = df["cases"].diff().fillna(0)
    df["average_new_cases"] = df["daily_new_cases"].rolling(smoothing_factor).mean().fillna(0)

    # Calculate daily new deaths and 14-day rolling average with an offset
    df["daily_new_deaths"] = df["deaths"].diff().fillna(0)
    df["average_new_deaths"] = df["daily_new_deaths"].rolling(smoothing_factor).mean().fillna(0)
    df["average_new_deaths"] = df["average_new_deaths"].shift(deaths_shift).fillna(0)

    # Plot the data on two y-axes
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.plot(df["date"], df["average_new_cases"], "b-", label="Average Cases")
    ax2.plot(df["date"], df["average_new_deaths"], "r-", label="Average Deaths")

    # Add axis labels and legend
    ax1.set_xlabel('Date of Cases')
    ax1.set_ylabel('Cases', color='b')
    ax2.set_ylabel('Deaths', color='r')
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend(loc='upper left')

    # Show the graph
    plt.show()


def animated_main():
    """Allows user to input graph parameters interactively."""
    while True:
        try:
            deaths_shift = int(input("How much would you like to shift the death dates of the x-axis? "))
            smoothing_factor = int(input("How many days average would you like to use to smooth the graph? "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    main(deaths_shift, smoothing_factor)


if __name__ == '__main__':
    animated_main()
