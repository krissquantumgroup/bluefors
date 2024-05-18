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

    def get_full_file_names(self, date:date, type:str):
        """Generate file names.

        Parameters
        ----------
        type : str
            'temperature','pressure', 'status', and 'flowmeter'
        """
        
        date_str = date.strftime("%y-%m-%d")
        base_path = os.path.join(self.log_folder, date_str)    

        if type == 'temperature':
            file_names = ['CH1 T ' + date_str + '.log', 
                    'CH2 T ' + date_str + '.log', 
                    'CH5 T ' + date_str + '.log', 
                    'CH6 T ' + date_str + '.log' ]

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
        
        # date_str = date.strftime("%y-%m-%d")
        # base_path = os.path.join(self.log_folder, date_str)    
        # file_names = ['CH1 T ' + date_str + '.log', 
        #             'CH2 T ' + date_str + '.log', 
        #             'CH5 T ' + date_str + '.log', 
        #             'CH6 T ' + date_str + '.log' ]

        # full_file_names = [ os.path.join(base_path, file_name) for file_name in file_names ]
        
        full_file_names = self.get_full_file_names(date, 'temperature')
        
        df_datetimes, df_temperatures = pd.DataFrame(), pd.DataFrame()
        
        for file_name in full_file_names:
            with open(file_name, 'r') as f: 
                df = pd.read_csv(f, names=['date', 'time', 'temperature'], header=0)

                try:
                    df_datetime  = pd.to_datetime(df['date'] + df['time'], format=' %d-%m-%y%H:%M:%S')
                except ValueError:
                    df_datetime  = pd.to_datetime(df['date'] + df['time'], format='%d-%m-%y%H:%M:%S')

                df_datetimes = pd.concat([df_datetimes, df_datetime], axis=1)             
                df_temperatures = pd.concat([df_temperatures, df['temperature']], axis=1)
            

        return df_datetimes, df_temperatures

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
            df = pd.read_csv(f, header=None)
            try:
                df_datetimes  = pd.to_datetime(df.iloc[:,0] + df.iloc[:,1], format='%d-%m-%y%H:%M:%S')
            except ValueError:
                df_datetimes  = pd.to_datetime(df.iloc[:,0] + df.iloc[:,1], format=' %d-%m-%y%H:%M:%S')
            
            _, cols = df.shape
            df_status = df.iloc[:, list(np.arange(3, cols,2))]  

        return df_datetimes, df_status

    def _get_status_column_name(self):
        full_file_name = self.get_full_file_names(self.start_date, 'status')
        with open(full_file_name) as f:
            first_line = f.readline()
        
        return first_line.split(',')[2::2]

    def load_temperature(self):
        """
        Return time and temperature dataframes between start_date and end_date
        """
        df_datetimes_all, df_temperatures_all = pd.DataFrame(), pd.DataFrame()
        
        temp_date = self.start_date

        while temp_date <= self.end_date:
            
            try:
                df_datetimes, df_temperatures = self.load_temperature_oneday(temp_date)
            except FileNotFoundError:
                df_datetimes, df_temperatures = pd.DataFrame(), pd.DataFrame()
                print(f"FileNotFound: {temp_date}, temperature")

            df_datetimes_all = pd.concat([df_datetimes_all, df_datetimes], axis=0)
            df_temperatures_all = pd.concat([df_temperatures_all, df_temperatures], axis=0)
            
            temp_date += timedelta(days=1)
        
        return df_datetimes_all, df_temperatures_all
            
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
        
        return df_datetimes_all, df_status_all

class BlueForPlotter:
    """ Plot log data. """

    def __init__(self, log_loader=None):
        self.log_loader = log_loader

    def plot_temperature(self, yscale='linear'):
        """
        Plot temperature.
        """
        df_df_datetimes_all, df_temperatures_all = self.log_loader.load_temperature()

        if df_temperatures_all.size == 0:
            print("No temperature data available!")
            return
        
        fig, ax = plt.subplots()
        
        text = "Temperature from " + self.log_loader.start_date.strftime("%y-%m-%d") + " to " + self.log_loader.end_date.strftime("%y-%m-%d")
        title = "Click on legend line to toggle line on/off" + "\n" + "\n".join(textwrap.wrap(text, 60))
        ax.set_title(title)
        ax.set_xlabel('Datetime')
        ax.set_ylabel('Temperature(K)')
        ax.set_yscale(yscale)
        ax.grid()
        
        line1, = ax.plot(df_df_datetimes_all.iloc[:,0], df_temperatures_all.iloc[:,0], '.-',label="50 K")
        line2, = ax.plot(df_df_datetimes_all.iloc[:,1], df_temperatures_all.iloc[:,1], label="4 K")
        line3, = ax.plot(df_df_datetimes_all.iloc[:,2], df_temperatures_all.iloc[:,2], label="Still")
        line4, = ax.plot(df_df_datetimes_all.iloc[:,3], df_temperatures_all.iloc[:,3], label="MCX")
        leg = ax.legend(fancybox=True, shadow=True)
        
        lines = [line1, line2, line3, line4]
        lined = {}  # Will map legend lines to original lines.
        for legline, origline in zip(leg.get_lines(), lines):
            legline.set_picker(True)  # Enable picking on the legend line.
            lined[legline] = origline
        
        def on_pick(event):
            # On the pick event, find the original line corresponding to the legend
            # proxy line, and toggle its visibility.
            legline = event.artist
            origline = lined[legline]
            visible = not origline.get_visible()
            origline.set_visible(visible)
            # Change the alpha on the line in the legend so we can see what lines
            # have been toggled.
            legline.set_alpha(1.0 if visible else 0.2)
            fig.canvas.draw()

        fig.canvas.mpl_connect('pick_event', on_pick)
        plt.show(block=False)

        return fig, ax   

    def plot_pressure(self, yscale='linear'):
        """
        Plot pressure
        """
        df_datetimes_all, df_pressures_all = self.log_loader.load_pressure()

        if df_pressures_all.size == 0:
            print("No pressure data available!")
            return

        fig, ax = plt.subplots()
        
        text = "Pressures from " + self.log_loader.start_date.strftime("%y-%m-%d") + " to " + self.log_loader.end_date.strftime("%y-%m-%d")
        title = "Click on legend line to toggle line on/off" + "\n" + "\n".join(textwrap.wrap(text, 60))
        ax.set_title(title)
        ax.set_xlabel('Datetime')
        ax.set_ylabel('Pressure (mBar)')
        ax.set_yscale(yscale)
        ax.grid()
        
        line1, = ax.plot(df_datetimes_all, df_pressures_all.iloc[:,0], label="P1")
        line2, = ax.plot(df_datetimes_all, df_pressures_all.iloc[:,1], label="P2")
        line3, = ax.plot(df_datetimes_all, df_pressures_all.iloc[:,2], label="P3")
        line4, = ax.plot(df_datetimes_all, df_pressures_all.iloc[:,3], label="P4")
        line5, = ax.plot(df_datetimes_all, df_pressures_all.iloc[:,4], label="P5")
        line6, = ax.plot(df_datetimes_all, df_pressures_all.iloc[:,5], label="P6")
        leg = ax.legend(fancybox=True, shadow=True)
        
        lines = [line1, line2, line3, line4, line5, line6]
        lined = {}  # Will map legend lines to original lines.
        for legline, origline in zip(leg.get_lines(), lines):
            legline.set_picker(True)  # Enable picking on the legend line.
            lined[legline] = origline
        
        def on_pick(event):
            # On the pick event, find the original line corresponding to the legend
            # proxy line, and toggle its visibility.
            legline = event.artist
            origline = lined[legline]
            visible = not origline.get_visible()
            origline.set_visible(visible)
            # Change the alpha on the line in the legend so we can see what lines
            # have been toggled.
            legline.set_alpha(1.0 if visible else 0.2)
            fig.canvas.draw()

        fig.canvas.mpl_connect('pick_event', on_pick)
        plt.show(block=False)

    def plot_flowmeter(self, yscale='linear'):
        """
        Plot flowmeter.
        """
        df_datetimes_all, df_flowmeters_all = self.log_loader.load_flowmeter()

        if df_flowmeters_all.size == 0:
            print("No flowmeter data available!")
            return
            
        fig, ax = plt.subplots()
        
        text = "Flowmeter from " + self.log_loader.start_date.strftime("%y-%m-%d") + " to " + self.log_loader.end_date.strftime("%y-%m-%d")
        title = "Click on legend line to toggle line on/off" + "\n" + "\n".join(textwrap.wrap(text, 60))
        ax.set_title(title)
        ax.set_xlabel('Datetime')
        ax.set_ylabel('Flowrate (mmol/s)')
        ax.set_yscale(yscale)
        ax.grid()
        
        line1, = ax.plot(df_datetimes_all, df_flowmeters_all.iloc[:,0], label="Flowmeter")
        leg = ax.legend(fancybox=True, shadow=True)
        plt.show(block=False)

    def plot_status(self, yscale='linear'):
        """
        Plot status.
        """
        df_datetimes_all, df_status_all = self.log_loader.load_status()

        if df_status_all.size == 0:
            print("No status data available!")
            return

        fig, ax = plt.subplots()
        
        text = "Status from " + self.log_loader.start_date.strftime("%y-%m-%d") + " to " + self.log_loader.end_date.strftime("%y-%m-%d")
        title = "Click on legend line to toggle line on/off" + "\n" + "\n".join(textwrap.wrap(text, 60))
        ax.set_title(title)
        ax.set_xlabel('Datetime')
        ax.set_ylabel('Status')
        ax.set_yscale(yscale)
        ax.grid()
        

        # s = "01-01-22,00:14:17,cptempwi,1.450000E+1,cptempwo,2.480000E+1,cptemph,7.050000E+1,cptempo,3.090000E+1,cpttime,2.548976E+6,cperrcode,2.800000E+1,cpavgl,8.840000E+1,cpavgh,2.748000E+2,nxdsf,3.000000E+1,nxdsct,4.100000E+1,nxdst,4.910500E+4,nxdsbs,4.050300E+4,nxdstrs,2.185700E+4,tc400remoteprio,1.000000E+0,tc400spdswptatt,1.000000E+0,tc400errorcode,0.000000E+0,tc400ovtempelec,0.000000E+0,tc400ovtemppump,0.000000E+0,tc400setspdatt,1.000000E+0,tc400pumpaccel,0.000000E+0,tc400heating,0.000000E+0,tc400standby,0.000000E+0,tc400pumpstatn,1.000000E+0,tc400commerr,0.000000E+0"
        # legend_labels = s.split(',')[2::2]

        legend_labels = self.log_loader._status_column_name

        lines = []
        _, column = df_status_all.shape
        for i in range(column):
            line, = ax.plot(df_datetimes_all, df_status_all.iloc[:,i], label=legend_labels[i])
            lines.append(line)

        leg = ax.legend(fancybox=True, shadow=True)
        
        lined = {}  # Will map legend lines to original lines.
        for legline, origline in zip(leg.get_lines(), lines):
            legline.set_picker(True)  # Enable picking on the legend line.
            lined[legline] = origline
        
        def on_pick(event):
            # On the pick event, find the original line corresponding to the legend
            # proxy line, and toggle its visibility.
            legline = event.artist
            origline = lined[legline]
            visible = not origline.get_visible()
            origline.set_visible(visible)
            # Change the alpha on the line in the legend so we can see what lines
            # have been toggled.
            legline.set_alpha(1.0 if visible else 0.2)
            fig.canvas.draw()

        fig.canvas.mpl_connect('pick_event', on_pick)
        plt.show(block=False)

    def plot_compressor_pressure(self, yscale='linear'):
        """
        Plot status.
        """
        df_datetimes_all, df_status_all = self.log_loader.load_status()

        if df_status_all.size == 0:
            print("No status data available!")
            return

        fig, ax = plt.subplots()
        
        text = "Status from " + self.log_loader.start_date.strftime("%y-%m-%d") + " to " + self.log_loader.end_date.strftime("%y-%m-%d")
        title = "Compressor pressure" + "\n" + "\n".join(textwrap.wrap(text, 60))
        ax.set_title(title)
        ax.set_xlabel('Datetime')
        ax.set_ylabel('Pressure')
        ax.set_yscale(yscale)
        ax.grid()
                
        low_pressure = df_status_all.iloc[:,6]
        high_pressure = df_status_all.iloc[:,7]
        delta_pressure = high_pressure - low_pressure

        ax.plot(df_datetimes_all, low_pressure, label="low")
        ax.plot(df_datetimes_all, high_pressure, label="high")
        ax.plot(df_datetimes_all, delta_pressure, label="delta")
        ax.legend()
        
        plt.show(block=False)

    def plot_temperature_pressure_flowmeter(self, yscale='linear'):

        fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex=True)
        
        # temperature
        df_df_datetimes_all, df_temperatures_all = self.log_loader.load_temperature()
        
        if df_temperatures_all.size == 0:
            print("No temperature data available!")
        else:
            title = "Click on legend line to toggle line on/off" 
            ax1.set_title(title)
        #     ax1.set_xlabel('Datetime')
            ax1.set_ylabel('Temperature(K)')
            ax1.set_yscale(yscale)
            ax1.grid()
            
            line1, = ax1.plot(df_df_datetimes_all.iloc[:,0], df_temperatures_all.iloc[:,0], label="50 K")
            line2, = ax1.plot(df_df_datetimes_all.iloc[:,1], df_temperatures_all.iloc[:,1], label="4 K")
            line3, = ax1.plot(df_df_datetimes_all.iloc[:,2], df_temperatures_all.iloc[:,2], label="Still")
            line4, = ax1.plot(df_df_datetimes_all.iloc[:,3], df_temperatures_all.iloc[:,3], label="MCX")
            leg1 = ax1.legend(fancybox=True, shadow=True)
        
        # pressure
        df_datetimes_all, df_pressures_all = self.log_loader.load_pressure()
    
        if df_pressures_all.size == 0:
            print("No pressure data available!")
        else:
        #     ax2.set_xlabel('Datetime')
            ax2.set_ylabel('Pressure (mBar)')
            ax2.set_yscale(yscale)
            ax2.grid()
            
            line11, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,0], label="P1")
            line12, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,1], label="P2")
            line13, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,2], label="P3")
            line14, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,3], label="P4")
            line15, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,4], label="P5")
            line16, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,5], label="P6")
            leg2 = ax2.legend(fancybox=True, shadow=True)

        # flowmeter
        df_datetimes_all, df_flowmeters_all = self.log_loader.load_flowmeter()

        if df_flowmeters_all.size == 0:
            print("No pressure data available!")
        else:
            ax3.set_xlabel('Datetime')
            ax3.set_ylabel('Flowrate (mmol/s)')
            ax3.grid()
            
            line21, = ax3.plot(df_datetimes_all, df_flowmeters_all.iloc[:,0], label="Flowmeter")
            leg3 = ax3.legend(fancybox=True, shadow=True)

        plt.show(block=False)
        
    def plot_temperature_pressure_flowmeter_status(self, yscale='linear'):

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1,sharex=True)

        title = "Click on legend line to toggle line on/off" 
        fig.suptitle(title)

        # temperature
        df_df_datetimes_all, df_temperatures_all = self.log_loader.load_temperature()
        
        if df_temperatures_all.size == 0:
            print("No flowmeter data available!")
        else:
            ax1.set_ylabel('Temperature(K)')
            ax1.set_yscale(yscale)
            ax1.grid()
            
            line1, = ax1.plot(df_df_datetimes_all.iloc[:,0], df_temperatures_all.iloc[:,0], label="50 K")
            line2, = ax1.plot(df_df_datetimes_all.iloc[:,1], df_temperatures_all.iloc[:,1], label="4 K")
            line3, = ax1.plot(df_df_datetimes_all.iloc[:,2], df_temperatures_all.iloc[:,2], label="Still")
            line4, = ax1.plot(df_df_datetimes_all.iloc[:,3], df_temperatures_all.iloc[:,3], label="MCX")
            leg1 = ax1.legend(fancybox=True, shadow=True)

        # pressure
        df_datetimes_all, df_pressures_all = self.log_loader.load_pressure()

        if df_pressures_all.size == 0:
            print("No flowmeter data available!")
        else:
            ax2.set_ylabel('Pressure (mBar)')
            ax2.set_yscale(yscale)
            ax2.grid()
            
            line11, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,0], label="P1")
            line12, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,1], label="P2")
            line13, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,2], label="P3")
            line14, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,3], label="P4")
            line15, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,4], label="P5")
            line16, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,5], label="P6")
            leg2 = ax2.legend(fancybox=True, shadow=True)

        # flowmeter
        df_datetimes_all, df_flowmeters_all = self.log_loader.load_flowmeter()
        
        if df_flowmeters_all.size == 0:
            print("No flowmeter data available!")
        else:        
            ax3.set_ylabel('Flowrate (mmol/s)')
            ax3.grid()
            line21, = ax3.plot(df_datetimes_all, df_flowmeters_all.iloc[:,0], label="Flowmeter")
            leg3 = ax3.legend(fancybox=True, shadow=True)


        # status
        df_datetimes_all, df_status_all = self.log_loader.load_status()

        if df_status_all.size == 0:
            print("No status data available!")
        else:                
            ax4.set_xlabel('Datetime')
            ax4.set_ylabel('Stauts')
            ax4.set_yscale(yscale)
            ax4.grid()

            # s = "01-01-22,00:14:17,cptempwi,1.450000E+1,cptempwo,2.480000E+1,cptemph,7.050000E+1,cptempo,3.090000E+1,cpttime,2.548976E+6,cperrcode,2.800000E+1,cpavgl,8.840000E+1,cpavgh,2.748000E+2,nxdsf,3.000000E+1,nxdsct,4.100000E+1,nxdst,4.910500E+4,nxdsbs,4.050300E+4,nxdstrs,2.185700E+4,tc400remoteprio,1.000000E+0,tc400spdswptatt,1.000000E+0,tc400errorcode,0.000000E+0,tc400ovtempelec,0.000000E+0,tc400ovtemppump,0.000000E+0,tc400setspdatt,1.000000E+0,tc400pumpaccel,0.000000E+0,tc400heating,0.000000E+0,tc400standby,0.000000E+0,tc400pumpstatn,1.000000E+0,tc400commerr,0.000000E+0"
            # legend_labels = s.split(',')[2::2]

            legend_labels = self.log_loader._status_column_name

            _, column = df_status_all.shape
            lines = []
            for i in range(column):
                # line, = ax4.plot(df_datetimes_all, df_status_all.iloc[:,i], label=legend_labels[i])
                line, = ax4.plot(df_datetimes_all, df_status_all.iloc[:,i])
                lines.append(line)

            leg4 = ax4.legend(fancybox=True, shadow=True)

        plt.show(block=False)

    def plot_temperature_pressure_status(self, yscale='linear'):

        fig, (ax1, ax2, ax3) = plt.subplots(3,1,sharex=True)

        title = "Click on legend line to toggle line on/off" 
        fig.suptitle(title)

        # temperature
        df_df_datetimes_all, df_temperatures_all = self.log_loader.load_temperature()
        
        if df_temperatures_all.size == 0:
            print("No flowmeter data available!")
        else:
            ax1.set_ylabel('Temperature(K)')
            ax1.set_yscale(yscale)
            ax1.grid()
            
            line1, = ax1.plot(df_df_datetimes_all.iloc[:,0], df_temperatures_all.iloc[:,0], label="50 K")
            line2, = ax1.plot(df_df_datetimes_all.iloc[:,1], df_temperatures_all.iloc[:,1], label="4 K")
            line3, = ax1.plot(df_df_datetimes_all.iloc[:,2], df_temperatures_all.iloc[:,2], label="Still")
            line4, = ax1.plot(df_df_datetimes_all.iloc[:,3], df_temperatures_all.iloc[:,3], label="MCX")
            leg1 = ax1.legend(fancybox=True, shadow=True)

        # pressure
        df_datetimes_all, df_pressures_all = self.log_loader.load_pressure()

        if df_pressures_all.size == 0:
            print("No flowmeter data available!")
        else:
            ax2.set_ylabel('Pressure (mBar)')
            ax2.set_yscale(yscale)
            ax2.grid()
            
            line11, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,0], label="P1")
            line12, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,1], label="P2")
            line13, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,2], label="P3")
            line14, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,3], label="P4")
            line15, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,4], label="P5")
            line16, = ax2.plot(df_datetimes_all, df_pressures_all.iloc[:,5], label="P6")
            leg2 = ax2.legend(fancybox=True, shadow=True)

        # status
        df_datetimes_all, df_status_all = self.log_loader.load_status()

        if df_status_all.size == 0:
            print("No status data available!")
        else:                
            ax3.set_xlabel('Datetime')
            ax3.set_ylabel('Stauts')
            ax3.set_yscale(yscale)
            ax3.grid()

            # s = "01-01-22,00:14:17,cptempwi,1.450000E+1,cptempwo,2.480000E+1,cptemph,7.050000E+1,cptempo,3.090000E+1,cpttime,2.548976E+6,cperrcode,2.800000E+1,cpavgl,8.840000E+1,cpavgh,2.748000E+2,nxdsf,3.000000E+1,nxdsct,4.100000E+1,nxdst,4.910500E+4,nxdsbs,4.050300E+4,nxdstrs,2.185700E+4,tc400remoteprio,1.000000E+0,tc400spdswptatt,1.000000E+0,tc400errorcode,0.000000E+0,tc400ovtempelec,0.000000E+0,tc400ovtemppump,0.000000E+0,tc400setspdatt,1.000000E+0,tc400pumpaccel,0.000000E+0,tc400heating,0.000000E+0,tc400standby,0.000000E+0,tc400pumpstatn,1.000000E+0,tc400commerr,0.000000E+0"
            # legend_labels = s.split(',')[2::2]

            legend_labels = self.log_loader._status_column_name

            _, column = df_status_all.shape
            lines = []
            for i in range(column):
                # line, = ax3.plot(df_datetimes_all, df_status_all.iloc[:,i], label=legend_labels[i])
                line, = ax3.plot(df_datetimes_all, df_status_all.iloc[:,i])
                lines.append(line)

            leg3 = ax3.legend(fancybox=True, shadow=True)

        plt.show(block=False)

if __name__ == "__main__":
    log_folder = r'/home/jaseung/Downloads/Logfiles'
    log_folder = r"C:\Users\jaseung\Downloads\20240518_Bluefors_log"
    start_date = date(2024,5,13)
    end_date   = date(2024,5,14)

    log_loader = BlueForsLogLoader(log_folder, start_date, end_date)
    plotter = BlueForPlotter(log_loader = log_loader)

    plotter.plot_temperature_pressure_flowmeter(yscale='log')
    plotter.plot_temperature_pressure_flowmeter_status(yscale='log')
    plotter.plot_temperature_pressure_status(yscale='log')

    # plotter.plot_temperature(yscale='log')
    # plotter.plot_pressure(yscale='log')
    # plotter.plot_flowmeter(yscale='linear')
    # plotter.plot_status(yscale='log')