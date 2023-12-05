import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Дефолтные значения
MAX_VOLTAGE = 4.2
MAX_CURRENT = 1.0
MAX_TEMPERATURE = 45

RED_LED_PIN = 1
GREEN_LED_PIN = 2
THERMISTOR_PIN = 3
CHARGE_ENABLE_PIN = 4

# Имитация начальных значений
battery_voltage = 3.5
temperature = 25

# Для хранения данных для графиков
time_points = []
voltage_points = []
temperature_points = []
current_points = []

def measure_temperature():
    # Имитация изменения температуры
    global temperature
    temperature += 0.1
    return temperature

def turn_on_red_led():
    print("Red LED ON")

def turn_on_green_led():
    print("Green LED ON")

def turn_off_red_led():
    print("Red LED OFF")

def turn_off_green_led():
    print("Green LED OFF")

def measure_battery_voltage():
    # Имитация изменения напряжения на батарее
    global battery_voltage
    battery_voltage += 0.05
    return battery_voltage

def calculate_charging_current(voltage):
    # Расчет зарядного тока на основе разницы между текущим и максимальным напряжением
    return min(MAX_CURRENT, MAX_CURRENT * (MAX_VOLTAGE - voltage))

def enable_charging():
    print("Charging enabled")

def stop_charging():
    print("Charging stopped")

def update_plot(frame):
    voltage = measure_battery_voltage()
    temperature = measure_temperature()

    if voltage >= MAX_VOLTAGE:
        turn_off_red_led()
        turn_on_green_led()
        stop_charging()
        anim.event_source.stop()
        print("Charging completed.")

    if temperature >= MAX_TEMPERATURE:
        turn_off_green_led()
        turn_on_red_led()
        stop_charging()
        anim.event_source.stop()
        print("Charging stopped due to high temperature.")

    turn_on_red_led()
    turn_off_green_led()
    enable_charging()

    charging_current = calculate_charging_current(voltage)

    # Сохранение данных для графиков
    time_points.append(time.time())
    voltage_points.append(voltage)
    temperature_points.append(temperature)
    current_points.append(charging_current)

    plt.clf()
    plt.subplot(3, 1, 1)
    plt.plot(time_points, voltage_points, label='Voltage (V)')
    plt.ylabel('Voltage (V)')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(time_points, temperature_points, label='Temperature (°C)', color='orange')
    plt.ylabel('Temperature (°C)')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(time_points, current_points, label='Charging Current (A)', color='green')
    plt.ylabel('Charging Current (A)')
    plt.xlabel('Time (s)')
    plt.legend()

# Создание окна для графиков
plt.figure(figsize=(10, 8))

# Начальные значения
battery_voltage = 3.5
temperature = 25

# Создание анимации
anim = FuncAnimation(plt.gcf(), update_plot, interval=1000)

plt.show()
