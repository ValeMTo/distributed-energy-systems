import pandas as pd

class localDataParserClass:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("Local Data parser initialized")
    
    def get_already_installed_powerplants_data(self, countries):
        self.logger.debug("Getting powerplants data")

        data = pd.read_csv('./data/custom_powerplants_ssp126_2050.csv', index_col=0)

        filtered_data = data[data['DateIn'] <= 2020]
        filtered_data = filtered_data[filtered_data['DateOut'] >= 2030]
        filtered_data = filtered_data[filtered_data['Country'].isin(countries)]
        
        grouped_data = filtered_data.groupby(['Fueltype', 'Country'])['Capacity'].sum().reset_index()
        grouped_data['Fueltype'] = grouped_data['Fueltype'].str.replace(' ', '')
        grouped_data = grouped_data.rename(columns={'Fueltype': 'fueltype', 'Country': 'country', 'Capacity': 'already_installed_capacity'})

        grouped_data['fueltype'] = grouped_data['fueltype'].apply(lambda x: x + '_RunOfRiver' if x == 'Hydro' else x)

        return grouped_data
    
    def get_annual_demand_data(self, year, countries):
        self.logger.debug("Getting demand data")

        if not isinstance(year, str) or len(year) != 4 or not year.isdigit():
            raise ValueError("Year must be a string of 4 digits")

        if not isinstance(countries, list) or not all(isinstance(country, str) and len(country) == 2 for country in countries):
            raise ValueError("Countries must be a list of strings with exactly 2 characters each")

        df = pd.read_csv('./data/demand_TEMBA_SSP1-2.6.csv', index_col=0, sep=';')

        df = df.map(lambda x: round((x/(365*24*60*60))*10**6, 3)) # Convert from PJ/year to GW

        df['country'] = df.index.map(lambda x: x[:2])
        filtered_data = df[df['country'].isin(countries)]
        filtered_data = filtered_data[[str(year), 'country']]
        filtered_data.reset_index(drop=True, inplace=True)
        filtered_data = filtered_data.rename(columns={str(year): f'annual_demand_{year}_GW'})

        return filtered_data

    