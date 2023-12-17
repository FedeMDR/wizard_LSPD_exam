# Code Wizards Project

## Table of Contents

1. [Group composition](#1-group-composition)
2. [Name and scope of the project](#2-name-and-scope-of-the-project)
3. [Description of the project](#3-description-of-the-project)
4. [Architecture](#4-architecture)
5. [Project structure](#5-project-structure)
6. [Datasets](#6-datasets)
7. [Prerequisites](#7-prerequisites)
8. [Usage](#8-usage)
9. [Testing](#9-testing)
10. [License](#10-license)

## 1. Group composition

- Aleccia Martina 889901
- Blasut Giovanni 889942
- Di Lorenzo Simone 889833
- Federico Madaro 888863

## 2. Name and scope of the project

### Wizard BnB: Safer, Greener and Closer to You

The primary goal of this project is to enhance user experience on the Airbnb platform by introducing innovative filters like air quality, crime rates, trees location and local attractions.

## 3. Description of the project

### **Home Page**

The Home Page serves as the entry point into our project. This page is only the beginning of the user's experience. On the screen we can see the name of the project, the home page button, the search button, the advanced search button and 5 boxes representing the five neighbourhoods of New York City:

1. Manhattan
2. Queens
3. Bronx
4. Brooklyn
5. Staten Island

Each borough section includes the current for the area ***Air Quality Index (AQI)*** and its associated level.

> **NOTE:** loading the Home Page might take up to 30 seconds or more, depending on the speed of the OpenWeather API. Please wait for it to fully load.

Interactive buttons for each borough lead to a new page where users can search for Airbnb accommodations. Users can sort and order these accommodations by price or reviews, either in ascending or descending order.

> **EXAMPLE**: To find the cheapest accommodation in Manhattan, click on "Manhattan Airbnb", select "Price" as sorting key, choose "Ascending" under as sorting order, and then click "Search". The list will then be displayed.

### **Search Page**

The Search Page, accessible from the main menu, allows users to apply three filters and two sort functions to find accommodations that suit the preference of the users.

[Below](#6-datasets) you can find the explanation about the datasets we used and how we extracted data from them

Here you can find out how the filters in the search page affect the results that the users will be displayed

#### How much do you care for a crime-free area?

Users can decide if the crime rate is important, selecting one of the four different options:

- Not at all
- Very little
- Enough
- Extremely

According to what the user chooses he will see bnbs that are located in areas that are rated with the corresponding crime rate.

#### How many attractions do you plan on visiting?

The second choice a user can do is decide how many attractions he want to visit. With this filter he can decide between three options:

- "0-5"
- "5-10"
- "10-20"

According to what the user chooses he will see bnbs that are located in areas in which are located a number of attraction included in the selected range.

#### Do you want to be in a green area?

The user can select if being in a green area is important or not, clicking one of the two options:

- True
- False

According to what the user chooses he will see bnbs that are located in areas in which the number of trees is above or below the mean of trees located among all boroughs.

#### Sort by

Users can decide to sort the list considering the price or the reviews.

#### Sorting Order

Users can decide to display the higher or the lowest solutions, based on the selection **Sort by**

### **Advance Search**

In this page, the user can select the attractions they want to visit from a list, choose the radius for their search, and then sort the results by price or review in both descending and ascending order.

With these choices, a list and an interactive map will be displayed. The list of results will appear at the bottom of the page, showing accommodations that are within the radius of the central point in relation to all the attractions.

The map is displayed at the top of the page.

## 4. Architecture

The project follows a simple client-server architecture:

1. **Frontend (Flask):**
   - Represents the user interface.
   - Built with Flask, a lightweight web framework for Python.
   - Responsible for rendering web pages and user interaction, including the form for querying the backend.

2. **Backend (FastAPI):**
   - Represents the backend of the application.
   - Built with FastAPI, a modern web framework for building APIs with Python.
   - Handles requests from the frontend, including specific parameters on Airbnb in New York City.

3. **Docker Compose:**
   - Orchestrates the deployment of both frontend and backend as separate containers.
   - Ensures seamless communication between frontend and backend containers.
   - Simplifies the deployment and management of the entire application.

### Communication

Bidirectional communication is established between the Frontend (Flask) and Backend (FastAPI). Docker Compose facilitates this communication, allowing the components to work together seamlessly.

## 5. Project Structure

Here you can see the our project structure, illustrating every forlder, sub-folder and file

```bash
wizard_LSPD_exam
|-- backend/
|   |-- app/
|   |   |-- package/
|   |   |   |-- __init__.py
|   |   |   |-- advanced_search.py
|   |   |   |-- air_quality.py
|   |   |   `-- data_handling.py
|   |   `-- main.py
|   |-- tests/
|   |   |-- attractions.py
|   |   |-- test_air_quality.py
|   |   |-- test_GeoCoords.py
|   |   `-- test_main.py
|   |-- Dockerfile
|   `-- requirements.txt
|-- frontend/
|   |-- app/
|   |   |-- static/
|   |   |   |-- attraction_icon.png
|   |   |   |-- Bronx.webp
|   |   |   |-- Brooklyn.webp
|   |   |   |-- Manhattan.avif
|   |   |   |-- popup.css
|   |   |   |-- Queens.jpg
|   |   |   `-- StatenIsland.jpg
|   |   |-- templates/
|   |   |   |-- advanced.html
|   |   |   |-- base.html
|   |   |   |-- index.html
|   |   |   |-- neighbourhood.html
|   |   |   `-- search.html
|   |   `-- main.py
|   |-- Dockerfile
|   `-- requirements.txt
|-- .gitattributes
|-- .gitignore
|-- docker-compose.yml
|-- LICENSE.txt
`-- README.md
```

## 6. Datasets

In the developing of our project we began by searching some csv files that could help us do deliver the best possible combination of bnbs to our users.

We came up with four datasets:

1. AirBnb.csv
2. CrimeCount.csv
3. Locations.csv
4. Trees.csv

### AirBnb.csv

Contains a list of all AirBnbs listed in the NYC area, including various data like the listing url, reviews, price, house ameneties ecc.

### CrimeCount.csv

Contains two columns:

1. **Zipcode**: a list of zipcodes in the NYC area
2. **Count**: the number of crimes registered for each zipcode

### Location.csv

A list of tourist locations with the corresponding data:

1. **Tourist_Spot**: the name of the location
2. **Address**: the address of the location
3. **Latitude**: the latitude of the location
4. **Longitude**: the longitude of the location
5. **Zipcode**: the zipcode of the location

### Trees.csv

Contains two columns:

1. **Zipcode**: a list of zipcodes in the NYC area
2. **Count**: the number of trees for each zipcode

## 7. Prerequisites

- Download the [dataset's folder](https://drive.google.com/drive/folders/1rBa1dcj_KIfOrYpVGIKuLA_glkTgy47f?usp=share_link/).
- Docker: To build and run the containerized application.
- Visual Studio Code (suggested).
- Python (latest version).
- Git: For cloning and managing the project repository.
- Web Browser: to use the application.

## 8. Usage

> **NOTE:** Before start, remember to **download the datasets**. Since some of them are large datasets, we decided to upload them in this GoodleDrive [folder](https://drive.google.com/drive/folders/1rBa1dcj_KIfOrYpVGIKuLA_glkTgy47f?usp=share_link/).

1. Clone the repository and navigate to the directory:

    ```bash
    git clone https://github.com/FedeMDR/wizard_LSPD_exam.git
    ```

1. After downloading the datasets, move inside the /backend/app/folder and paste the dataset folder inside it.
    >**NOTE:** You must renaime the folder containing the datasets as "Datasets".

1. Open the project folder using Visual Studio Code, install the following extentions using VS:

    - [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
    - [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

1. Open the terminal from the menu and type the following command:

    ```bash
    docker compose build backend
    ```

    ```bash
    docker compose build frontend
    ```

    ```bash
    docker compose up backend
    ```

     >**NOTE:** Execute the following command in another Terminal window.

    ```bash
    docker compose up frontend
    ```

    This will start both the frontend and backend containers as defined in your docker-compose.yml file.

1. Open the docker extention in VS Code, under the containers tab you should by now see two containers that are running (the ones with the green arrows).\
Right click on both of them an then click on "attach visual studio".\
Now you should have two new VS Code windows, one for the backend and one for the frontend.

1. This step must be replicated in both frontend and backend: Open folder /app/app, and there you will find the working area.

1. Go to the run and debug section and run the backend and then the frontend.

    >**NOTE:** Is foundamental to execute the backend first and only after it is fully loaded you can run and debug the frontend.

    When the backend is fully loaded you should see in the terminal an output that look like this:

    ```bash
    INFO:     Will watch for changes in these directories: ['/app']
    INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
    INFO:     Started reloader process [8030] using StatReload
    INFO:     Started server process [8323]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    ```

    Now run and debug the frontend, wait until this message appears.

    ```bash
    * Serving Flask app 'main'
    * Debug mode: on
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:80
    * Running on http://172.19.0.2:80
    Press CTRL+C to quit
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 374-045-381
    ```

1. Open your web browser and navigate to [http://localhost:8080](http://localhost:8080) to access the `frontend`.

1. On the frontend, you can use the provided forms to:

- Search for Airbnb listings based on criteria like proximity to attractions, green areas, and crime rates.
- Perform advanced searches within a specified radius from selected attractions.
- View listings by neighbourhood and sort them according to price or ratings.

>**NOTE:** Remember to shut down the Docker containers when you're done by typing:

```bash
CTRL + C
```

>in both the frontend and backend terminal to shutdown the runnig processes.

## 9. Testing

We've implemented some tests to verify the correct funcitionality of our backend. To run those tests, open the backend VS Code window, open the terminal and type the following command:

```bash
    pytest --cov=app --cov-report=html tests/
```

## 10. License

Distributed under GNU GPL licence. See LICENSE.txt for more information.