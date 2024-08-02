#Code below is base used to collect the maintenance event data and that is the first step
#Next is to include a "shop" that would allow the user to allocate resources to the unit

import uuid
import random
import string

# Function to generate a short serial number
def generate_serial_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

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
        "Maintenance Events": []
    }

    # Add the equipment to the list
    equipment_list.append(equipment)

    # Display entered data
    print("\nEquipment Registered:")
    for key, value in equipment.items():
        if key != "Maintenance Events":
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
                else:
                    print(f"{key}: {value}")
            return equipment
    print("No equipment found with that Serial Number.")
    return None

# Main function to handle user interaction
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
                log_maintenance = input("Would you like to log a maintenance event? (y/n): ").strip().lower()
                if log_maintenance in ['yes', 'y']:
                    log_maintenance_event(equipment)
        elif choice == '3':
            break
        else:
            print("Invalid option. Please select again.")

if __name__ == "__main__":
    main()
