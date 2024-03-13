import cdsapi
import xarray as xr
import matplotlib.pyplot as plt
import cartopy, cartopy.crs as ccrs 
import cartopy.feature as cfeature
from sklearn.linear_model import LinearRegression
import numpy as np
import time

######################################################################################################################
# baixar dados do ciclone #
'''
c = cdsapi.Client()
c.retrieve(
    'reanalysis-era5-pressure-levels',
    {
        'product_type': 'reanalysis',
        'variable': [
            'geopotential', 'temperature', 'u_component_of_wind',
            'v_component_of_wind', 'vertical_velocity', 'vorticity',
        ],
        'pressure_level': [
            '250', '500', '850',
            '1000',
        ],
        'year': '2024',
        'month': '02',
        'day': [
            '14', '15', '16',
            '17', '18', '19',
            '20', '21', '22'
        ],
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
        'area': [
            -10, -60, -50,
            -20,
        ],
        'format': 'grib',
    },
    'download.nc')
'''

nivel=['250', '500', '850', '1000']

######################################################################################################################
# abrir dado netCDF #
ds = xr.open_dataset("download.nc", engine='cfgrib')
print (ds['t'][0,0,0,0])
print (ds['z']) #geopotencial

for nivel_isobarico, tempo in zip(['0', '1', '2', '3'],['0', '1', '2', '3', '4', '5', '6', '7', '8']):
    print (nivel_isobarico)
    print (tempo)
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(6,6))


    # Cria os contornos #	
    ax.coastlines(resolution='10m', color='black', linewidth=0.8, zorder=2) #2
    ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)

	# adicionar limites Brasil
    states_provinces = cfeature.NaturalEarthFeature(category='cultural', name='admin_1_states_provinces_lines', scale='50m', facecolor='none')
    countries = cfeature.NaturalEarthFeature(category='cultural', name='admin_0_countries', scale='50m', facecolor='none')
    ax.add_feature(states_provinces, edgecolor='black', zorder=3)
    ax.add_feature(countries, edgecolor='black', zorder=3)

    # plota os dados # 
    img_temp=ax.contourf(ds['t'].longitude, ds['t'].latitude, ds['t'][0,0,:,:], cmap='coolwarm', zorder=1)
    colorbar=plt.colorbar (img_temp, label='Temperatura (C°)', orientation='vertical', pad=0.05, fraction=0.03, spacing='proportional', extend='both')

    # cria legendas #
    plt.title(f"TEMP. SFC (K) em {nivel[int(nivel_isobarico)]}hPa e GEOPOTENCIAL EM 1000hPa \n \n 03/04/2024 12z (inicialização: 03/04/2024 00h)")
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')



    ######################################################################################################################
    # DADOS #

    # abre o dado #
    ds = xr.open_dataset("download.nc", engine='cfgrib', filter_by_keys={'stepType': 'instant','typeOfLevel': 'isobaricInhPa'})

    # 250hPa e a posicao 17, os outros dois sao latitude e longitude #
    gh= ds['z'][17,:,:]

    ######################################################################################################################
    # FIGURA #

    # cria figura #

    # plota geopotencial #
    gh_fig=plt.contour(ds['t'].longitude, ds['t'].latitude, ds['t'][0,0,:,:], colors='black', transform=ccrs.PlateCarree(), zorder=2)
    plt.clabel(gh_fig, inline=True, fontsize=8, zorder=1)

    plt.show()
    #print ( ds['t'][int(tempo), int(nivel_isobarico),:,:]) 

    ######################################################################################################################
    # regressao linear #
    # mostra a figura #

    temperaturas=[]
    temp_=[]
    dado_tempo=[]
    for lat_index, lat in enumerate(ds['latitude']):
        for lon_index, lon in enumerate(ds['longitude']):

            temp = float(ds['t'][int(tempo), int(nivel_isobarico),lat_index,lon_index].data)
            temperaturas.append(temp)
            print (temperaturas)
            
            dado_tempo = ds['t'][int(tempo), int(nivel_isobarico),lat_index,lon_index].time.data
            dado_tempo_segundos = dado_tempo.astype(np.int64)
            dado_tempo = dado_tempo_segundos.reshape(-1,1)
            print(dado_tempo)

        modelo = LinearRegression()
        modelo.fit (dado_tempo, temperaturas)
        coef_angular = modelo.coef_[0]
  

        print(f'Latitude: {lat}, Longitude: {lon}, Coeficiente Angular: {coef_angular}')




# mostra a figura #
plt.show()

quit()


quit()













######################################################################################################################
# versões #
'''

    c.retrieve(
    'reanalysis-era5-pressure-levels',
    {
        'product_type': 'reanalysis',
        'format': 'grib',
        'year': '2024',
        'month': '02',
        'day': [
            '14'
        ],
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
        'area': [
            -10, -60, -50,
            -20,
        ],
        'pressure_level': [
            '250', '500', '850',
            '1000',
        ],
        'variable': [
            'geopotential', 'temperature', 'u_component_of_wind',
            'v_component_of_wind', 'vertical_velocity', 'vorticity',
        ],
    },
    'download.grib')
'''

