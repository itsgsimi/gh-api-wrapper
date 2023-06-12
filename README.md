# README.md

## Project Overview

This project acts as a wrapper to API's like GitHub's API for retrieving repository information. This should serve as a utility service which 
helps with data gathering and maintenance activities

## System Requirements

- Python 3.7 or higher
- Docker
- Git

## Installation

First, clone the project repository from GitHub. Open a terminal window, navigate to the directory where you want the project to be located, and run the following command:

    ```
    git clone https://github.com/amex-eng/github-api-wrapper.git
    ```

Navigate into the project directory:

    ```
    cd github-api-wrapper
    ```

## Setting Up the Environment

We recommend using a virtual environment. You can set one up using:

    ```
    python -m venv env
    ```

To activate the virtual environment, run:

For Windows:

    ```
    . env\Scripts\activate
    ```

For Unix or MacOS:

    ```
    source env/bin/activate
    ```
## Installing Dependencies

Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```
## Running the Project Locally

To start the API, run:

    ```
    uvicorn app.main:app --reload
    ```
Now the server is running at `http://127.0.0.1:8000/`.

## Using the Application

Navigate to `http://127.0.0.1:8000/docs` in your web browser to access the interactive FastAPI documentation. This contains a complete list of API endpoints and their expected inputs and outputs.
