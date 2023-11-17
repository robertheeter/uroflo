import RPi.GPIO as GPIO
import time
# disable warnings
GPIO.setwarnings(False)

# select GPIO mode
GPIO.setmode(GPIO.BCM)

# set buzzer - change to whichever GPIO pin
buzzer = 14
GPIO.setup(buzzer, GPIO.OUT)

# set light
light = 15 # change to whichever GPIO pin
GPIO.setup(light,GPIO.OUT)


# notification trigger conditions

def get_user_input(condition):
        while True:
                try:
                        value = float(input("Enter " + condition + ": "))
                        return value
                except ValueError:
                        print("Please enter a valid number")

def notify(type):
        for i in range(5):
                GPIO.output(type,True)
                time.sleep(0.5)
                GPIO.output(type, GPIO.LOW)
                time.sleep(0.5)

def main():
        supply_bag_volume_threshold = 0.5 # when notification should go off
        supply_bag_volume_number = get_user_input("supply bag volume")

        if supply_bag_volume_number < supply_bag_volume_threshold:
                print("Supply bag needs change")
                # trigger buzzer and light flashing
                notify(light)
                notify(buzzer)
        else:
                print("Supply bag does not require imminent replacement")

        # waste bag volume
        waste_bag_volume_threshold = 4.5 # when notification should go off
        waste_bag_volume_number = get_user_input("waste bag volume")

        if waste_bag_volume_number > waste_bag_volume_threshold:
                print("Waste bag needs change")
                # trigger buzzer and light flashing
                notify(light)
                notify(buzzer)
        else:
                print("Waste bag does not require imminent replacement")


        # severe hematuria
        hematuria_severity_threshold = 60 # when notification should go off
        hematuria_severity_percentage = get_user_input("hematuria severity percentage")
        # input duration of severe hematuria
        severe_hematuria_duration_threshold = 60 # minutes of severe hematuria
        severe_hematuria_duration = get_user_input("duration of this degree of hematuria (minutes)")

        if hematuria_severity_percentage >= hematuria_severity_threshold and severe_hematuria_duration >= severe_hematuria_duration_threshold:
                print("Severe hematuria detected for an hour or more")
                # trigger buzzer and light flashing
                notify(light)
                notify(buzzer)
        elif hematuria_severity_percentage >= hematuria_severity_threshold and severe_hematuria_duration < severe_hematuria_duration_threshold:
                print("The degree of hematuria is severe, but the duration is not long enough to be of concern")
        else:
                print("Severe hematuria is not detected")
        # inflow outflow 
        inflow_rate = get_user_input("inflow rate")
        outflow_rate = get_user_input("outflow rate")
        duration = get_user_input("duration of these flow rates (minutes)")
        duration_threshold = 2 

        if (inflow_rate == 0 or outflow_rate == 0) and duration >= duration_threshold:
                print("Inflow or outflow blockage detected")
                # trigger buzzer and light flashing
                notify(light)
                notify(buzzer)
        else:
                print("No inflow or outflow blockage detected")


        if abs(inflow_rate-outflow_rate) >= 10 and duration >= 10:
                print("Significant discrepancy detected between inflow and outflow rate for 10 minutes or more")
                # trigger buzzer and light flashing
                notify(light)
                notify(buzzer)
        elif abs(inflow_rate-outflow_rate) >= 10 and duration <= 10:
                print("Significant discrepancy detected bewteen inflow and outflow rate but the duration is not long enough to be of concern"),
        else:
                print("No siginificant discrepancy detected between inflow and outflow rate")


if __name__ == "__main__":
        main()
