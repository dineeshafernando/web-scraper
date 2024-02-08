import requests
from bs4 import BeautifulSoup

# Define the base URL of the webpage with pagination
base_url = 'https://community.chocolatey.org/packages'

# Initialize a variable to track the current page number
current_page = 1

# Open a text file for writing
with open('output.txt', 'w') as output_file:
    while True:
        # Construct the URL for the current page
        url = f'{base_url}?page={current_page}'

        # Send an HTTP GET request to the webpage
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find and extract the installation commands as before
            input_elements = soup.find_all('input', class_='form-control text-bg-theme-elevation-1 user-select-all border-start-0 ps-1')

            # Extract and write the commands to the text file with -params '"/DesktopIcon"'
            for input_element in input_elements:
                command = input_element['value'] + ' -y'
                output_file.write(command + '\n')
                print(command)

            # Check if there's a "Next" button on the current page
            next_button = soup.find('a', class_='btn btn-outline-primary', text='Next')
            if next_button:
                current_page += 1
            else:
                break  # Exit the loop if there's no "Next" button
        else:
            print(f'Failed to retrieve page {current_page}.')
            break  # Exit the loop on any error

# Close the text file when done
output_file.close()
