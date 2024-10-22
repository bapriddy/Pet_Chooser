import pymysql.cursors
from creds import *  
from pets import Pets  

# Connect to the database
try:
    myConnection = pymysql.connect(
        host=hostname,
        user=username,
        password=password,
        db=database,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Database connection established.")  

except Exception as e:
    print(f"An error has occurred. Exiting: {e}")
    exit()

# Create a list for pet objects
pet_list = []

# Retrieve sql data
try:
    with myConnection.cursor() as cursor:
        # Modify the SQL query to perform a LEFT JOIN to include pets without matching owners
        sqlSelect = """
            SELECT pets.name, pets.animal_type_id, pets.age, owners.name as owner_name
            FROM pets
            LEFT JOIN owners ON pets.owner_id = owners.id;
        """
        cursor.execute(sqlSelect)

        # Use the fetchall() method to retrieve all results as list of tuples.
        rows = cursor.fetchall()

        if not rows:
            print("Sorry no pets found in database.")
        else:
            pet_list.clear()  # Clear the list
            # Create pet objects
            for row in rows:
                owner_name = row['owner_name'] if row['owner_name'] else "Unknown Owner"  # Handle NULL owner
                pet = Pets(row['name'], row['animal_type_id'], owner_name, row['age'])
                pet_list.append(pet)  # Use append method to add to list

except Exception as e:
    print(f"An error occurred while attempting to retrieve pet data: {e}")

# Function to display pet list
def display_pet_choice():
    print("\nChoose a pet by the corresponding number or enter 'Q' to quit:")
    for index, pet in enumerate(pet_list, start=1):
        print(f"[{index}] {pet.name}")

# Display list then select pet
while True:
    # Display pet choices
    display_pet_choice()
    user_input = input("Enter a number here: ").strip()  # Get user input

    if user_input.lower() == 'q':
        print("Exiting the program. Goodbye!")
        break  # Exit

    try:
        number = int(user_input) - 1  # Convert to index

        if 0 <= number < len(pet_list):

            choice = pet_list[number]
            print(f"\nYou have chosen {choice.name}, the {choice.animal_type}. {choice.name} is {choice.age} years old. {choice.name}'s owner is {choice.owner}.")
            input("Press [ENTER] to continue.")
        else:
            print("Invalid choice. Please select a number the list.")
    except ValueError:
        print("Invalid input. Please enter a number corresponding to your choice or 'Q' to quit.")

# Close the database connection
myConnection.close()
print("Database connection closed.")


