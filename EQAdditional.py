import uuid
import random
import string

# Constants, can be changed based on what testing is needed
normal_wear_rate_per_50_hours = 5.0  # 5% degradation per 50 hours
extra_degradation_rate = 10.0  # Extra wear rate applied randomly
maintenance_threshold = 25.0  # Threshold for maintenance event

# Function to generate a short serial number, ok so most equipment has serial numbers I know but for this example I did not want to go through it
def generate_serial_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

# Function to initialize systems with starting health percentage
def initialize_systems():
    return {
        "Engine System": 0,
        "Hydraulic System": 0,
        "Brake System": 0,
        "Lubrication System": 0,
        "Drivetrain System": 0
    }

# Function to collect equipment data
def collect_equipment_data(equipment_list):
    print("\nEnter details for new equipment:")
    model = input("Equipment Model: ")
    year = input("Equipment Year: ")
    manufacturer = input("Manufacturer: ")
    current_hours = input("Current Hours (assuming no meter change): ")

    # Generate a unique serial number
    serial_number = generate_serial_number()

    # Store the equipment details in a dictionary
    equipment = {
        "Serial Number": serial_number,
        "Model": model,
        "Year": year,
        "Manufacturer": manufacturer,
        "Current Hours": current_hours,
        "Systems": initialize_systems(),
        "Maintenance Events": []
    }

    # Add the equipment to the list
    equipment_list.append(equipment)

    # Display entered data
    print("\nEquipment Registered:")
    for key, value in equipment.items():
        if key != "Maintenance Events" and key != "Systems":
            print(f"{key}: {value}")

    # Optionally enter maintenance events
    while True:
        add_event = input("\nWould you like to log a maintenance event for this equipment? (y/n): ").strip().lower()
        if add_event in ['yes', 'y']:
            log_maintenance_event(equipment)
        elif add_event in ['no', 'n']:
            break
        else:
            print("Invalid input, please enter 'y' or 'n'.")

# Function to log a maintenance event for an equipment unit
def log_maintenance_event(equipment):
    while True:
        event_description = input("Describe the maintenance event: ")
        event = {
            "Event ID": len(equipment["Maintenance Events"]) + 1,
            "Description": event_description
        }
        equipment["Maintenance Events"].append(event)
        print(f"Maintenance event logged: Event {event['Event ID']}")

        # Ask if the user wants to log another maintenance event
        another_event = input("Would you like to log another maintenance event? (y/n): ").strip().lower()
        if another_event not in ['yes', 'y']:
            break

# Function to apply random degradation to a system
def apply_random_degradation(equipment):
    system_to_degrade = random.choice(list(equipment["Systems"].keys()))
    equipment["Systems"][system_to_degrade] += extra_degradation_rate
    print(f"Random degradation applied: {system_to_degrade} increased by {extra_degradation_rate}%.")
    check_for_maintenance(equipment, system_to_degrade)

# Function to update system conditions based on operation hours
def update_system_conditions(equipment, hours):
    increments = hours / 50  # Calculate how many 50-hour increments
    for system in equipment["Systems"].keys():
        equipment["Systems"][system] += increments * normal_wear_rate_per_50_hours

    apply_random_degradation(equipment)

    # Display all systems and their updated conditions
    print("\nUpdated System Conditions:")
    for system, health in equipment["Systems"].items():
        print(f"{system}: {health:.2f}% health")

# Function to check if any system needs maintenance
def check_for_maintenance(equipment, system):
    if equipment["Systems"][system] >= maintenance_threshold:
        print(f"Maintenance required for {system}: System health at {equipment['Systems'][system]}%")
        log_maintenance_event(equipment)

# Function to call up an existing unit's details
def call_up_unit(equipment_list):
    serial_number = input("Enter Serial Number of the unit: ").strip().upper()
    for equipment in equipment_list:
        if equipment["Serial Number"] == serial_number:
            print("\nEquipment Details:")
            for key, value in equipment.items():
                if key == "Maintenance Events":
                    print(f"{key}:")
                    for event in value:
                        print(f"  Event {event['Event ID']}: {event['Description']}")
                elif key == "Systems":
                    print(f"{key}:")
                    for system, health in value.items():
                        print(f"  {system}: {health:.2f}% health")
                else:
                    print(f"{key}: {value}")
            return equipment
    print("No equipment found with that Serial Number.")
    return None

# User interface and entry screen
def main():
    equipment_list = []
    while True:
        print("\nOptions:")
        print("1. Enter new equipment")
        print("2. Call up existing unit")
        print("3. Exit")
        choice = input("Select an option: ").strip()

        if choice == '1':
            collect_equipment_data(equipment_list)
        elif choice == '2':
            equipment = call_up_unit(equipment_list)
            if equipment:
                add_hours = input("Enter additional operation hours to update conditions (or 'skip' to skip): ").strip().lower()
                if add_hours.isdigit():
                    update_system_conditions(equipment, int(add_hours))
                log_maintenance = input("Would you like to log a maintenance event? (y/n): ").strip().lower()
                if log_maintenance in ['yes', 'y']:
                    log_maintenance_event(equipment)
        elif choice == '3':
            break
        else:
            print("Invalid option. Please select again.")

if __name__ == "__main__":
    main()
