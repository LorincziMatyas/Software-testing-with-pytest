<!-- @format -->

# My PyTests for Software Testing Subject

This project contains Python tests for a software testing subject.

## Setting up the Project

Before setting up the project, make sure you have Python installed on your machine. You can download Python from the [official website](https://www.python.org/downloads/).

You can set up the virtual environment on a Linux distribution either automatically with `set_up_env.sh`, or manually with the following steps:

1. Create a new directory for your project. Replace `folder_name` with the name you want for your directory:

    ```bash
    mkdir folder_name
    ```

2. Navigate into the directory:

    ```bash
    cd folder_name
    ```

3. Create the virtual environment. Replace venv_name with the name you want for your virtual environment:

    ```bash
    python3 -m venv venv_name
    ```

4. Activate the virtual environment. Replace venv_name with the name you of your virtual environment:

    ```bash
    source venv_name/bin/activate
    ```

5. Install pip, with that pytest, sqlalchemy in the virtual environment:

    ```bash
    python3 -m pip install --upgrade pip
    pip3 install pytest sqlalchemy
    ```

6. Run your tests with pytest. Replace test_file_name.py with the name of your actual test file:

    ```bash
    pytest test_file_name.py
    ```

## Project Structure

This project is organized into two main directories:

1. `src`: This directory contains the source code of the application. The `calculator.py` file in this directory implements some basic functions.

2. `tests`: This directory contains all the test files for the application. The `calculator_test.py` file contains tests for the basic functions implemented in `calculator.py`. As a convention, test file names should follow the pattern `*_test.py` or `test_*.py`.
