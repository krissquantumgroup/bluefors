# Jaseung Ku
# Read Bluefors log files and plot them 

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta
import textwrap
 
class BlueForsLogLoader:
    """ Load log data from log files """
        
    def __init__(self, log_folder:str, start_date:date, end_date:date):
        self.log_folder = log_folder
        self.start_date = start_date
        self.end_date = end_date

        self._status_column_name = self._get_status_column_name()
        
        self.temperature_datetimes, self.temperatures = self.load_temperature()
        self.resistance_datetimes, self.resistances = self.load_resistance()
        self.pressure_datetime, self.pressures = self.load_pressure()
        self.flowmeter_datetime, self.flowmeter = self.load_flowmeter()
        self.status_datatime, self.status = self.load_status()

        
    def get_full_file_names(self, date:date, type:str):
        """Generate file names.

        Parameters
        ----------
        type : str
            'temperature', 'resistance', 'pressure', 'status', and 'flowmeter'
        """
        
        date_str = date.strftime("%y-%m-%d")
        base_path = os.path.join(self.log_folder, date_str)    

        if type == 'temperature':
            file_names = ['CH1 T ' + date_str + '.log', 
                    'CH2 T ' + date_str + '.log', 
                    'CH5 T ' + date_str + '.log', 
                    'CH6 T ' + date_str + '.log' ]

            full_file_name = [ os.path.join(base_path, file_name) for file_name in file_names ]
        elif type == 'resistance':
            file_names = ['CH1 R ' + date_str + '.log', 
                    'CH2 R ' + date_str + '.log', 
                    'CH5 R ' + date_str + '.log', 
                    'CH6 R ' + date_str + '.log' ]

            full_file_name = [ os.path.join(base_path, file_name) for file_name in file_names ]
        elif type == 'pressure':
            file_name = 'maxigauge ' + date_str + '.log'
            full_file_name = os.path.join(base_path, file_name)
        elif type == 'flowmeter':
            file_name = 'Flowmeter ' + date_str + '.log'
            full_file_name = os.path.join(base_path, file_name)
        elif type=='status':
            file_name = 'Status_' + date_str + '.log'
            full_file_name = os.path.join(base_path, file_name)
        else:
            raise(f"No {type} type is available!!!")
        
        return full_file_name
    
    def load_temperature_oneday(self, date:date):
        """
            Read temperature log files and return two pandas dataframe of datetime and temperatures.
        """
        
               
        full_file_names = self.get_full_file_names(date, 'temperature')
        
        df_datetimes, df_temperatures = pd.DataFrame(), pd.DataFrame()
        
        for file_name in full_file_names:
            # print(file_name)
            try:
                with open(file_name, 'r') as f: 
                    df = pd.read_csv(f, names=['date', 'time', 'temperature'], header=0)

                    try:
                        df_datetime  = pd.to_datetime(df['date'] + df['time'], format=' %d-%m-%y%H:%M:%S')
                    except ValueError:
                        df_datetime  = pd.to_datetime(df['date'] + df['time'], format='%d-%m-%y%H:%M:%S')

                    df_datetimes = pd.concat([df_datetimes, df_datetime], axis=1)             
                    df_temperatures = pd.concat([df_temperatures, df['temperature']], axis=1)
            except FileNotFoundError:
                print(f"FileNotFound: {file_name}")

                df_datetimes = pd.concat([df_datetimes, pd.Series()], axis=1)             
                df_temperatures = pd.concat([df_temperatures, pd.Series(name="temperature")], axis=1)
 

        return df_datetimes, df_temperatures

    def load_resistance_oneday(self, date:date):
        """
            Read resistance log files and return two pandas dataframe of datetime and resistances.
        """
             
        full_file_names = self.get_full_file_names(date, 'resistance')
        
        df_datetimes, df_resistances = pd.DataFrame(), pd.DataFrame()
        
        for file_name in full_file_names:
            # print(file_name)
        
            with open(file_name, 'r') as f: 
                df = pd.read_csv(f, names=['date', 'time', 'resistance'], header=0)

                try:
                    df_datetime  = pd.to_datetime(df['date'] + df['time'], format=' %d-%m-%y%H:%M:%S')
                except ValueError:
                    df_datetime  = pd.to_datetime(df['date'] + df['time'], format='%d-%m-%y%H:%M:%S')

                df_datetimes = pd.concat([df_datetimes, df_datetime], axis=1)             
                df_resistances = pd.concat([df_resistances, df['resistance']], axis=1)
           
        return df_datetimes, df_resistances

    def load_pressure_oneday(self, date:date):
        """
            Read pressure log file and return two pandas dataframe of datetime and pressure.
        """
        # date_str = date.strftime("%y-%m-%d")
        # base_path = os.path.join(self.log_folder, date_str)  
        # file_name = 'maxigauge ' + date_str + '.log'
        # full_file_name = os.path.join(base_path, file_name)

        full_file_name = self.get_full_file_names(date, 'pressure')

        df_datetimes, df_pressures = pd.DataFrame(), pd.DataFrame()

        with open(full_file_name, 'r') as f:
            df = pd.read_csv(f, header=None)
            try:
                df_datetimes  = pd.to_datetime(df.iloc[:,0] + df.iloc[:,1], format='%d-%m-%y%H:%M:%S')
            except ValueError:
                df_datetimes  = pd.to_datetime(df.iloc[:,0] + df.iloc[:,1], format=' %d-%m-%y%H:%M:%S')
            df_pressures = df.iloc[:, [5,11,17,23,29,35]]
        
        # print(df_datetimes.shape)
        # print(df_pressures.shape)   

        return df_datetimes, df_pressures

    def load_flowmeter_oneday(self, date: date):
        """
            Read flowmeter log file and return two pandas dataframe of datetime and flowrate.
        """
        # date_str = date.strftime("%y-%m-%d")
        # base_path = os.path.join(self.log_folder, date_str)  
        # file_name = 'Flowmeter ' + date_str + '.log'
        # full_file_name = os.path.join(base_path, file_name)

        full_file_name = self.get_full_file_names(date, 'flowmeter')
        df_datetimes, df_flowmeter = pd.DataFrame(), pd.DataFrame()
        
        with open(full_file_name, 'r') as f:
            df = pd.read_csv(f, header=None)
            try:
                df_datetimes  = pd.to_datetime(df.iloc[:,0] + df.iloc[:,1], format=' %d-%m-%y%H:%M:%S')
            except ValueError:
                df_datetimes  = pd.to_datetime(df.iloc[:,0] + df.iloc[:,1], format='%d-%m-%y%H:%M:%S')
            df_flowmeter = df.iloc[:,2]
        
        # print(df_datetimes.shape)
        # print(df_flowmeter.shape)   

        return df_datetimes, df_flowmeter

    def load_status_oneday(self, date:date):
        """
        Read status log file and return two pandas dataframe of datetime and status.
        """
        # date_str = date.strftime("%y-%m-%d")
        # base_path = os.path.join(self.log_folder, date_str)  
        # file_name = 'Status_' + date_str + '.log'
        # full_file_name = os.path.join(base_path, file_name)

        full_file_name = self.get_full_file_names(date, 'status')
        
        df_datetimes, df_status = pd.DataFrame(), pd.DataFrame()
        
        with open(full_file_name, 'r') as f:
            if len(self._status_column_name)==23: # for singel compressor
                df = pd.read_csv(f, header=None, delimiter=',', usecols=range(48)) # for some reason, sometimes a certain row of status file has extra columns, making an error.
            else:
                df = pd.read_csv(f, header=None, delimiter=',') # for XLD, i.e., two compressors
            try:
                df_datetimes  = pd.to_datetime(df.iloc[:,0] + df.iloc[:,1], format='%d-%m-%y%H:%M:%S')
            except ValueError:
                df_datetimes  = pd.to_datetime(df.iloc[:,0] + df.iloc[:,1], format=' %d-%m-%y%H:%M:%S')
            
            _, cols = df.shape
            df_status = df.iloc[:, list(np.arange(3, cols,2))]  

        return df_datetimes, df_status

    def _get_status_column_name(self):
        full_file_name = self.get_full_file_names(self.start_date, 'status')
        try:
            with open(full_file_name) as f:
                first_line = f.readline()
            
            return first_line.split(',')[2::2]
        except FileNotFoundError:
            print("No status file found.")
            return None

    def load_temperature(self):
        """
        Return time and temperature dataframes between start_date and end_date
        """
        df_datetimes_all, df_temperatures_all = pd.DataFrame(), pd.DataFrame()
        
        temp_date = self.start_date

        while temp_date <= self.end_date:
            
            # try:
            df_datetimes, df_temperatures = self.load_temperature_oneday(temp_date)
            
            if not df_datetimes.empty:
                try:
                    # df_datetimes_all = df_datetimes_all.reset_index(drop=True)
                    # df_datetimes = df_datetimes.reset_index(drop=True)
                    # df_temperatures_all = df_temperatures_all.reset_index(drop=True)
                    # df_temperatures = df_temperatures.reset_index(drop=True)

                    df_datetimes_all = pd.concat([df_datetimes_all, df_datetimes], axis=0) #, ignore_index=True)
                    df_temperatures_all = pd.concat([df_temperatures_all, df_temperatures]) #, axis=0, ignore_index=True)
                except pd.errors.InvalidIndexError:
                    #
                    duplicated_indexes_pred = df_datetimes_all.index[df_datetimes_all.index.duplicated()]
                    duplicated_indexes_else = df_datetimes.index[df_datetimes.index.duplicated()]
                    print(duplicated_indexes_pred)
                    print(duplicated_indexes_else)
                    print(temp_date)

            temp_date += timedelta(days=1)
        
        df_datetimes_all.columns = ["50K", "4K","still","MCX"]
        df_temperatures_all.columns = ["50K", "4K","still","MCX"]

        return df_datetimes_all, df_temperatures_all

    def load_resistance(self):
        """
        Return time and resistance dataframes between start_date and end_date
        """
        df_datetimes_all, df_resistances_all = pd.DataFrame(), pd.DataFrame()
        temp_date = self.start_date

        while temp_date <= self.end_date:
            try:
                df_datetimes, df_resistances = self.load_resistance_oneday(temp_date)
            except FileNotFoundError:
                df_datetimes, df_resistances = pd.DataFrame(), pd.DataFrame()
                print(f"FileNotFound: {temp_date}, resistance")

            df_datetimes_all = pd.concat([df_datetimes_all, df_datetimes], axis=0)
            df_resistances_all = pd.concat([df_resistances_all, df_resistances], axis=0)
            
            temp_date += timedelta(days=1)

        df_datetimes_all.columns = ["50K", "4K","still","MCX"]
        df_resistances_all.columns = ["50K", "4K","still","MCX"]

        return df_datetimes_all, df_resistances_all

    def load_pressure(self):
        """
        Return time and pressure dataframes between start_date and end_date
        """
        df_datetimes_all, df_pressures_all = pd.DataFrame(), pd.DataFrame()
        temp_date = self.start_date

        while temp_date <= self.end_date:
            try:
                df_datetimes, df_pressures = self.load_pressure_oneday(temp_date)
            except FileNotFoundError:
                df_datetimes, df_pressures = pd.DataFrame(), pd.DataFrame()
                print(f"FileNotFound: {temp_date}, pressure")

            df_datetimes_all = pd.concat([df_datetimes_all, df_datetimes], axis=0)
            df_pressures_all = pd.concat([df_pressures_all, df_pressures], axis=0)
            
            temp_date += timedelta(days=1)
        
        df_pressures_all.columns = ["P1","P2","P3","P4","P5","P6"]

        return df_datetimes_all, df_pressures_all

    def load_flowmeter(self):
        """
        Return time and flowmeter dataframes between start_date and end_date
        """
        df_datetimes_all, df_flowmeters_all = pd.DataFrame(), pd.DataFrame()
        temp_date = self.start_date

        while temp_date <= self.end_date:
            try:
                df_datetimes, df_flowmeters = self.load_flowmeter_oneday(temp_date)
            except FileNotFoundError:
                df_datetimes, df_flowmeters = pd.DataFrame(), pd.DataFrame()
                print(f"FileNotFound: {temp_date}, flowmeter")
        
            df_datetimes_all = pd.concat([df_datetimes_all, df_datetimes], axis=0)
            df_flowmeters_all = pd.concat([df_flowmeters_all, df_flowmeters], axis=0)
            
            temp_date += timedelta(days=1)
        
        df_flowmeters_all.columns = ["flowmeter"]

        return df_datetimes_all, df_flowmeters_all

    def load_status(self):
        """
            Return time and status dataframes between start_date and end_date.
        """
        df_datetimes_all, df_status_all = pd.DataFrame(), pd.DataFrame()
        temp_date = self.start_date

        while temp_date <= self.end_date:
            try:
                df_datetimes, df_status = self.load_status_oneday(temp_date)
            except FileNotFoundError:
                df_datetimes, df_status = pd.DataFrame(), pd.DataFrame()
                print(f"FileNotFound: {temp_date}, status")

            df_datetimes_all = pd.concat([df_datetimes_all, df_datetimes], axis=0)
            df_status_all = pd.concat([df_status_all, df_status], axis=0)
            
            temp_date += timedelta(days=1)

        df_status_all.columns = self._status_column_name

        return df_datetimes_all, df_status_all

    def show_status_names(self):

        print(f"Status names:\n{self._status_column_name}")

class BlueForPlotter:
    """ Plot log data. """

    def __init__(self, log_loader:BlueForsLogLoader):
        self.log_loader = log_loader

    def _plot_temperature(self, axes, axe_index, yscale="linear"):
        
        if self.log_loader.temperatures.size == 0:
            print("No temperature data available!")
        else:
            axes[axe_index].set_ylabel('Temperature(K)')
            axes[axe_index].set_yscale(yscale)
            axes[axe_index].grid()
            
            plot_symbol = '.-'
            axes[axe_index].plot(self.log_loader.temperature_datetimes["50K"], self.log_loader.temperatures["50K"], plot_symbol, label="50 K")
            axes[axe_index].plot(self.log_loader.temperature_datetimes["4K"], self.log_loader.temperatures["4K"], plot_symbol, label="4 K")
            axes[axe_index].plot(self.log_loader.temperature_datetimes.still, self.log_loader.temperatures.still, plot_symbol, label="Still")
           
            if self.log_loader.temperatures.shape[1]==4:
                try:
                    axes[axe_index].plot(self.log_loader.temperature_datetimes.MCX, self.log_loader.temperatures.MCX, plot_symbol, label="MCX")
                except ValueError:
                    pass

            axes[axe_index].legend(fancybox=True, shadow=True)
    
    def _plot_resistance(self, axes, axe_index, yscale="linear"):
        
        if self.log_loader.resistances.size == 0:
            print("No resistance data available!")
        else:
            axes[axe_index].set_ylabel('Resistance(Ohm)')
            axes[axe_index].set_yscale(yscale)
            axes[axe_index].grid()
            
            plot_symbol = '.-'
            axes[axe_index].plot(self.log_loader.resistance_datetimes["50K"], self.log_loader.resistances["50K"], plot_symbol, label="50 K")
            axes[axe_index].plot(self.log_loader.resistance_datetimes["4K"], self.log_loader.resistances["4K"], plot_symbol, label="4 K")
            axes[axe_index].plot(self.log_loader.resistance_datetimes.still, self.log_loader.resistances.still, plot_symbol, label="Still")
           
            if self.log_loader.resistances.shape[1]==4:
                try:
                    axes[axe_index].plot(self.log_loader.resistance_datetimes.MCX, self.log_loader.resistances.MCX, plot_symbol, label="MCX")
                except ValueError:
                    pass

            axes[axe_index].legend(fancybox=True, shadow=True)

    def _plot_pressure(self, axes, axe_index, yscale="linear"):

        
        if self.log_loader.pressures.size == 0:
            print("No pressure data available!")
        else:

            axes[axe_index].set_ylabel('Pressure (mBar)')
            axes[axe_index].set_yscale(yscale)
            axes[axe_index].grid()
            
            plot_symbol = '.-'
            axes[axe_index].plot(self.log_loader.pressure_datetime, self.log_loader.pressures.P1, plot_symbol, label="P1")
            axes[axe_index].plot(self.log_loader.pressure_datetime, self.log_loader.pressures.P2, plot_symbol, label="P2")
            axes[axe_index].plot(self.log_loader.pressure_datetime, self.log_loader.pressures.P3, plot_symbol, label="P3")
            axes[axe_index].plot(self.log_loader.pressure_datetime, self.log_loader.pressures.P4, plot_symbol, label="P4")
            axes[axe_index].plot(self.log_loader.pressure_datetime, self.log_loader.pressures.P5, plot_symbol, label="P5")
            axes[axe_index].plot(self.log_loader.pressure_datetime, self.log_loader.pressures.P6, plot_symbol, label="P6")
          
            axes[axe_index].legend(fancybox=True, shadow=True)

    def _plot_flowmeter(self, axes, axe_index, yscale="linear"):

        if self.log_loader.flowmeter.size == 0:
            print("No pressure data available!")
        else:
            axes[axe_index].set_xlabel('Datetime')
            axes[axe_index].set_ylabel('Flowrate (mmol/s)')
            axes[axe_index].grid()
            
            axes[axe_index].plot(self.log_loader.flowmeter_datetime, self.log_loader.flowmeter.flowmeter, label="Flowmeter")
            
            axes[axe_index].legend(fancybox=True, shadow=True)

    def _plot_status(self, axes, axe_index, yscale="linear", status_list=None):
         
        if self.log_loader.status.size == 0:
            print("No status data available!")
        else:                
            axes[axe_index].set_xlabel('Datetime')
            axes[axe_index].set_ylabel('Stauts')
            axes[axe_index].set_yscale(yscale)
            axes[axe_index].grid()

            legend_labels = self.log_loader._status_column_name

            for i, label in enumerate(legend_labels):
                if status_list is not None:
                    if label in status_list:
                        axes[axe_index].plot(self.log_loader.status_datatime, self.log_loader.status[label], label=label)  
                else:
                    axes[axe_index].plot(self.log_loader.status_datatime, self.log_loader.status[label], label=label)  

            axes[axe_index].legend(fancybox=True, shadow=True)

    def _plot_compressor_pressure(self, axes, axe_index, yscale='linear'):
    
        if self.log_loader.status.size == 0:
            print("No status data available!")
        else:                
            axes[axe_index].set_xlabel('Datetime')
            axes[axe_index].set_ylabel('Stauts')
            axes[axe_index].set_yscale(yscale)
            axes[axe_index].grid()

            legend_labels = self.log_loader._status_column_name

            for i, label in enumerate(legend_labels):
                if label=="cpalp" or label=="cpavgl":  cpalp_index = i
                if label=="cpahp" or label=="cpavgh":  cpahp_index = i
                if label=="cpalp_2":  cpalp_2_index = i
                if label=="cpahp_2":  cpahp_2_index = i

            axes[axe_index].plot(self.log_loader.status_datatime, self.log_loader.status.iloc[:,cpalp_index], label="Low P")            
            axes[axe_index].plot(self.log_loader.status_datatime, self.log_loader.status.iloc[:,cpahp_index], label="High P")            
            axes[axe_index].plot(self.log_loader.status_datatime, self.log_loader.status.iloc[:,cpahp_index] - self.log_loader.status.iloc[:,cpalp_index], label="Delta P")        
            
            if "cpalp_2" in self.log_loader._status_column_name:
                axes[axe_index].plot(self.log_loader.status_datatime, self.log_loader.status.iloc[:,cpalp_2_index], label="Low P")            
                axes[axe_index].plot(self.log_loader.status_datatime, self.log_loader.status.iloc[:,cpahp_2_index], label="High P")            
                axes[axe_index].plot(self.log_loader.status_datatime, self.log_loader.status.iloc[:,cpahp_2_index] - self.log_loader.status.iloc[:,cpalp_2_index], label="Delta P")        
            
            axes[axe_index].legend(fancybox=True, shadow=True)

    def plot(self, what_to_plot:list[str], yscale="linear", status_list=None):
        
        num_plot = len(what_to_plot)
        
        fig, axes = plt.subplots(num_plot, 1,sharex=True, figsize=(8, 3*num_plot))
        if num_plot==1: axes = [axes]

        title = " \ " .join(what_to_plot)
        fig.suptitle(title)

        axe_index = 0
        for what in what_to_plot:
            if what=="temperature":
               self._plot_temperature(axes, axe_index, yscale=yscale)
            elif what=="pressure":
                self._plot_pressure(axes, axe_index, yscale=yscale)
            elif what=="flowmeter":
                self._plot_flowmeter(axes, axe_index, yscale=yscale)
            elif what=="status":
                self._plot_status(axes, axe_index, yscale=yscale, status_list=status_list)                 
            elif what=="resistance":
                self._plot_resistance(axes, axe_index, yscale=yscale)
            elif what=="compressor_pressure":
                self._plot_compressor_pressure(axes, axe_index, yscale=yscale)


            axe_index += 1

        fig.show()

if __name__ == "__main__":
    
    # parameters
    log_folder = r"Z:\logs\BF4\Logfiles"
    start_date = date(2025,4,22)
    end_date   = date(2025,4,22)

    # create data loader and plotter
    log_loader = BlueForsLogLoader(log_folder, start_date, end_date)
    log_loader.show_status_names()
    plotter = BlueForPlotter(log_loader=log_loader)

    ######### plot what you want

    plotter.plot(what_to_plot=["temperature", "pressure", "flowmeter"], yscale="linear")
    # plotter.plot(what_to_plot=["status"], yscale="linear")
    # plotter.plot(what_to_plot=["resistance"], yscale="linear")
    # plotter.plot(what_to_plot=["temperature","compressor_pressure"], yscale="linear") 
    # plotter.plot(what_to_plot=["temperature","status"], status_list=["cpalp","cpalpa","cpahp","cpalpa", "cpahpa"])

    # fig, ax = plotter.plot_resistance(temperature_stage="MCX", yscale='linear')

   