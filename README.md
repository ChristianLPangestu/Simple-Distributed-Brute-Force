# Distributed Brute Force System

This project is a distributed brute force system, which consists of a server and multiple clients. The server automatically distributes brute force tasks to connected clients.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Description
The Distributed Brute Force System is designed to divide the task of brute-forcing a password among multiple clients. The server handles task distribution and coordination, ensuring that the workload is balanced according to the number of connected clients.

## Features
- **Centralized Server**: Manages and distributes tasks to clients.
- **Client-Server Architecture**: Clients connect to the server and receive tasks.
- **Dynamic Task Distribution**: Server dynamically distributes tasks based on the number of connected clients.

## Prerequisites
- Python 3.x
- `socket` library (usually included with Python)
- `threading` library (usually included with Python)

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/distributed-brute-force.git
    ```
2. Navigate to the project directory:
    ```bash
    cd distributed-brute-force
    ```

## Usage

### Server
Run the server script to start the server:
```bash
python server.py
