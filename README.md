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
