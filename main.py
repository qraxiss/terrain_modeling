from matplotlib.pyplot import figure, show
from warnings import simplefilter
from threading import Thread
import pandas as pd
import bll


ratio = 112000

def terrain(data, fig):
    # Plot
    ax = fig.add_subplot(projection='3d')
    ax.scatter(data['lat'], data['lng'], data['elevation'])

    # Config
    ax.set_xlabel('lat')
    ax.set_ylabel('lng')
    ax.set_zlabel('elevation')

    # Show
    show()


def menu():
    # Inputs
    lat = input("Lat: ")
    lng = input("Long: ")
    extend = input("Taranacak Alan Genişliği: ")
    gap = input("Aralık: ")
    
    return lat, lng, extend, gap


def main():
    while True:
        # Get values
        lat, lng, extend, gap = list(map(lambda x: float(x), menu()))

        # Calculate Locations
        locations = list()
        points = bll.parser(lat, lng, extend, gap)
        
        # Get elevation datas
        bll.elevation(points, locations, 400, 'google')

        # Json to file
        data=pd.DataFrame(list(pd.DataFrame(locations)['location']))
        data['elevation'] = pd.DataFrame(locations)['elevation']

        # Start Plot
        fig = figure()
        simplefilter("ignore")
        Thread(target=terrain, args=(data,fig)).start()

        save=input("Kaydetmek İstiyor musunuz? \nE/H: ")

        if save.lower() == "e":
            file_name = input("Lütfen Dosya Adı Giriniz: ")
            data.to_csv("outputs/"+file_name+".dat", sep=",", index=False, header=False)
            print(file_name, ".dat uzantısıyla outputs klasörüne kaydedildi...")

        elif save.lower() == "h":
            continue


if __name__ == "__main__":
    main()