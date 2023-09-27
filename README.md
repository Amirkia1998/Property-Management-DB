# Urban Transformation Information System

This is the final project for the university DBMS course. It keeps track of property owners, properties to be demolished, construction companies, and associated financial data.

## Table of Contents

- [Features](#features)
- [Database Schema](#database-schema)
- [Entity-Relationship Diagram](#entity-relationship-diagram)
- [Getting Started](#getting-started)

## Features

- **Property Owners**: Store information about property owners, including their identification number (TC), names, surnames, phone numbers, and associated property (PID).

- **Properties**: Record details about properties, such as property name (PName), property address (PAddress), and construction date (CONS_DATE).

- **Construction Companies**: Manage data about construction companies, including company name (CName) and location (CLocation).

- **Demolition Projects**: Track information about demolition projects, including demolition date (DDate) and demolition price (DPrice), associated with specific properties and construction companies.

- **Building Projects**: Record data about building projects, including build date (BDate) and build price (BPrice), linked to properties and construction companies.

## Database Schema

The database schema for this project consists of the following tables:

- `OWNERS`: Stores information about property owners.
- `PROPERTY`: Contains details about properties.
- `COMPANY`: Manages data related to construction companies.
- `DEMOLISH`: Tracks demolition projects.
- `BUILD`: Records building projects.

Please refer to the provided SQL code for the complete schema definition and relationships between these tables.

## Entity-Relationship Diagram

## Getting Started

To get started with the Urban Transformation Information System, follow these steps:

1. **Database Setup**: Create a PostgreSQL database and execute the provided SQL code to set up the necessary tables, sequences, and relationships. Ensure that your PostgreSQL server is running and accessible.

2. **Configuration**: Update the database connection configuration in your application code to match your PostgreSQL database credentials and connection details.

3. **Data Entry**: Use the provided functions or application interface to add property owners, properties, construction companies, demolition projects, and building projects to the database.


