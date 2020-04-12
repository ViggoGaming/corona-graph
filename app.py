import requests, json
import matplotlib.pyplot as plt

BASE_URL = "https://pomber.github.io/covid19/timeseries.json"

countries = ["Denmark", "Sweden", "Norway", "Finland", "Iceland"]

r = requests.get(BASE_URL).json()

def main():
    for country in countries:
        deaths = [x["deaths"] for x in r[country][-11:]]
        dates = [x["date"][5:].replace("-", "/") for x in r[country][-11:]]
        plt.plot(dates, deaths, label = country) 
    
    plt.xlabel('Date')
    plt.ylabel('Deaths')
    plt.title('Corona graph') 
    plt.legend()
    plt.show()
    #plt.savefig('graph.png') # Uncomment this line if you want to save the graph as an image.

if __name__ == "__main__":
    main()
