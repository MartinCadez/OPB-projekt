[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Compatibility](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/)
[![Docker Compatibility](https://img.shields.io/badge/Docker-20.10%2B-0db7ed)](https://docs.docker.com)
[![Docker Compose Compatibility](https://img.shields.io/badge/Docker_Compose-2.0%2B-1ad1b9)](https://docs.docker.com/compose)

<div align="center">
<h2> Project OPB, data warehouse</h2>
</div>

_Project was developed as part of course 'OPB' at the 
University of Ljubljana, Faculty of Mathematics and Physics, during the 
academic year 2024/2025. It aims to ilustrate simple data warehouse, with 
dash framework creating dashboard._

## 🛠️ Setup Guide

- 📋Pre-requisites:
    - [Python 3.6+](https://www.python.org/downloads/)
    - [Docker 20.10+](https://docs.docker.com/get-docker/)
    - [Docker Compose 2.0+](https://docs.docker.com/compose/install/)

- 🔧 Environment Configuration:
    
    1. 🛠 Configure Environment Variables
    ```bash
    cp .env.example .env
    ```
  
    2. 🐳 Deploy Docker Compose Services
    ```bash
    docker compose up -d
    ```
>[!NOTE]
> Current configuration ([`docker-compose.yml`](./docker-compose.yml)) defines
a service which deploys PostgreSQL 17.5 database container with named volume. 
This way we have persistent storage, which can be used 
across container restarts.

> [!TIP]
> Before proceeding with any operations, ensure the Docker service is running
> and verify its status.
> 
> ```bash
> docker ps --filter "name=postgres_db"
> ``````

## 💨 Execution

- 🚀 Run Dashboard
    ```bash
    python3 index.py
    ```

## 💡 Advisors
Project was developed under the guidance of:
- doc. dr. Janos Vidali
- asist. 
