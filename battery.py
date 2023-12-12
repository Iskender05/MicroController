import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


class BatterySimulator:
    def __init__(self, capacity_mAh, voltage, discharge_rate, charge_rate):
        self.capacity_mAh = capacity_mAh
        self.voltage = voltage
        self.nominal_voltage = voltage
        self.discharge_rate = discharge_rate
        self.charge_rate = charge_rate
        self.current_capacity = capacity_mAh

    def discharge(self, time_interval):
        discharge_current = self.discharge_rate  # Convert discharge rate from mA to A
        discharge_capacity = discharge_current * time_interval / 3600  # Convert time from seconds to hours
        self.current_capacity -= discharge_capacity

        if self.current_capacity < 0:
            self.current_capacity = 0

        self.voltage = (self.current_capacity / self.capacity_mAh) * self.nominal_voltage
        return discharge_capacity

    def charge(self, time_interval):
        charge_current = self.charge_rate  # Convert charge rate from mA to A
        charge_capacity = charge_current * time_interval / 3600  # Convert time from seconds to hours
        self.current_capacity += charge_capacity

        if self.current_capacity > self.capacity_mAh:
            self.current_capacity = self.capacity_mAh

        self.voltage = (self.current_capacity / self.capacity_mAh) * self.nominal_voltage
        return charge_capacity


# Задаем параметры вашей батареи
capacity_mAh = 2500  # емкость в миллиампер-часах
initial_voltage = 4.2  # начальное напряжение в вольтах
discharge_rate = 500  # скорость разряда в миллиамперах
charge_rate = 1500  # скорость заряда в миллиамперах

# Создаем объект BatterySimulator
battery_simulator = BatterySimulator(capacity_mAh, initial_voltage, discharge_rate, charge_rate)

# Интервал времени для обновления состояния батареи
time_interval = 50  # интервал времени в секундах для обновления состояния батареи

# Создаем списки для хранения данных
window_size = 100  # Размер окна для отображения скользящего графика
time_data = np.zeros(window_size)
voltage_data = np.zeros(window_size)
capacity_data = np.zeros(window_size)
charge = False


# Функция для обновления данных и графиков
def update(frame):
    global charge

    # Добавляем новые данные
    time_data[:-1] = time_data[1:]  # Сдвигаем все значения влево
    voltage_data[:-1] = voltage_data[1:]
    capacity_data[:-1] = capacity_data[1:]

    time_data[-1] = frame * time_interval
    voltage_data[-1] = battery_simulator.voltage
    capacity_data[-1] = battery_simulator.current_capacity

    if battery_simulator.voltage < 2.4:
        charge = True

    if battery_simulator.voltage > 4.0:
        charge = False

    discharged_capacity = battery_simulator.discharge(time_interval)

    if charge is True:
        charged_capacity = battery_simulator.charge(time_interval)
    else:
        charged_capacity = 0

    print(
        f"Time: {frame * time_interval} s, Discharged Capacity: {discharged_capacity:.5f} Ah, Charged Capacity: {charged_capacity:.5f} Ah, Voltage: {battery_simulator.voltage:.2f} V, Current Capacity: {battery_simulator.current_capacity:.2f} mAh")

    # Обновляем графики
    plt.clf()

    plt.subplot(211)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.plot(time_data, voltage_data, label='Voltage (V)')
    plt.legend()

    plt.subplot(212)
    plt.xlabel('Time (s)')
    plt.ylabel('Capacity (mAh)')
    plt.plot(time_data, capacity_data, label='Capacity (mAh)')
    plt.legend()


# Задаем параметры анимации
plt.figure(figsize=(10, 8))
animation = FuncAnimation(plt.gcf(), update, interval=time_interval)

# Показываем графики
plt.show()
