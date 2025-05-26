# Distributed-logging-system 

This repository contains a set of microservices for inventory management, order processing, payment, and shipping, along with a Pub-Sub system for communication and monitoring. It also includes an alerting system and Kibana for log visualization.


## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

Ensure you have the following installed:installation guide is included in README 

- Python 3.12 or higher
- pip (Python package manager)
- Kafka
- Fluentd
- ElasticSearch
- Kibana


### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Cloud-Computing-Big-Data/RR-Team-48-distributed-logging-system.git
   cd Cloud-Computing-Big-Data/RR-Team-48-distributed-logging-system
   ```

2. Install required Python packages for all services and the Pub-Sub system:

   ```bash
   pip install -r requirements.txt
   ```
  [ Debug if any error occurs or try with --break-system-packages ]
  

### Running the Services

From the parent directory, you can start each service and the Pub-Sub system.

1. **Inventory Service**:
   ```bash
   python inventory_service/inventory_service.py
   ```

2. **Order Service**:
   ```bash
   python order_service/order_service.py
   ```

3. **Payment Service**:
   ```bash
   python payment_service/payment_service.py
   ```

4. **Shipping Service**:
   ```bash
   python shipping_service/shipping_service.py
   ```

5. **Pub-Sub System** (handles communication and logging):
   ```bash
   python PUB-SUB/app.py
   ```

### Monitoring and Alerting

- Open your browser and navigate to **http://localhost:5000** for the alerting system.
- For log visualization with Kibana, ensure your Elasticsearch and Kibana services are running, then open **http://localhost:5601**.

### Additional Notes

- Configuration files for Fluentd and Elasticsearch are included in the root directory. You may need to update `fluentd.conf` and `update_conf.sh` to match your environment.
- Log data is managed using `log_accumulator.py` in each service and aggregated in the Pub-Sub system.


To install **Fluentd** and set it up for use with Python (using the `fluent-logger` library), here’s how you can include the installation and configuration steps in your README:

### Installation of Fluentd

1. **Install Fluentd** using the package manager for your operating system.

   **On Ubuntu/Debian:**

   ```bash
   # Install dependencies
   sudo apt-get update
   sudo apt-get install -y sudo gnupg2 curl

   # Add the Fluentd APT repository
   curl -fsSL https://packages.fluentd.org/fluentd-apt-source.sh | sudo bash

   # Install Fluentd
   sudo apt-get install -y fluentd
   ```

   **On CentOS/RHEL:**

   ```bash
   # Install Fluentd
   sudo yum install -y https://packages.fluentd.org/fluentd.rpm
   ```

   **On macOS (via Homebrew):**

   ```bash
   brew install fluentd
   ```

2. **Verify Fluentd installation**:

   After installation, you can verify that Fluentd is installed correctly by checking the version:

   ```bash
   fluentd --version
   ```

   You should see the Fluentd version displayed in the terminal.

### Fluentd Configuration

1. **Fluentd Configuration File:**

   Fluentd’s configuration is typically stored in `/etc/fluent/fluentd.conf`. You'll need to define input sources, output destinations, and possibly filters for your use case.

   Example `fluentd.conf` for a simple logging setup:

   ```ini
   # fluentd.conf

   # Input Plugin (e.g., listening on a TCP port for logs)
   <source>
     @type tcp
     port 24224
     bind 0.0.0.0
     tag fluentd.test
   </source>

   # Output Plugin (e.g., sending logs to Elasticsearch)
   <match fluentd.test>
     @type elasticsearch
     host localhost
     port 9200
     logstash_format true
     index_name fluentd-test
   </match>
   ```

   In this configuration:
   - **Input Plugin**: Fluentd listens for logs over TCP on port 24224.
   - **Output Plugin**: Logs are sent to an Elasticsearch instance running locally on port 9200.

2. **Restart Fluentd** to apply the configuration:

   After updating the configuration, restart Fluentd to apply changes.

   ```bash
   sudo service fluentd restart
   ```

### Additional Setup (For Fluentd with Python)

To connect Fluentd with your Python application, you'll need the `fluent-logger` library. If you have already added it to `requirements.txt`, you can install it as follows:


## Fluentd Installation and Configuration

### 1. Install Fluentd

Follow the instructions below to install Fluentd:

#### On Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y sudo gnupg2 curl
curl -fsSL https://packages.fluentd.org/fluentd-apt-source.sh | sudo bash
sudo apt-get install -y fluentd
```

#### On macOS:

```bash
brew install fluentd
```

#### Verify Fluentd Installation:

```bash
fluentd --version
```
#### Configuring Fluentd
After installation run the bash (.sh) file provided for fluentd installation
```bash
chmod +x update_conf.sh
./update_conf.sh
```

## Kafka Installation Guide

Follow the steps below to install and set up Kafka on your system.

## Prerequisites
- **Java 8 or later** must be installed on your system.
- **Zookeeper**: Kafka requires Zookeeper to manage its cluster. The `kafka.sh` script will handle the setup of Zookeeper if it's not already installed.

## Steps for Kafka Installation

### 1. **Download Kafka**

   Download the Kafka binary from the official website:
   
   [Kafka Downloads](https://kafka.apache.org/downloads)

   Choose the appropriate version for your system and download the `.tgz` file.

### 2. **Extract Kafka**

   After downloading the `.tgz` file, extract it to a directory of your choice. For example:

   ```bash
   tar -xvf kafka_2.13-3.0.0.tgz
   cd kafka_2.13-3.0.0
```
#### Kafka Configuration:
in /usr/local/kafka/config/serever.properties
add:
```bash
advertised.listeners=PLAINTEXT://<hostname>:9092
listeners=PLAINTEXT://0.0.0.0:9092
```


## Elasticsearch Installation
```bash
sudo su
apt update
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt-get update && sudo apt-get install elasticsearch
sudo update-rc.d elasticsearch defaults 95 10
service elasticsearch restart
service elasticsearch status
tail -f /var/log/elasticsearch/elasticsearch.log
curl localhost:9200
```

### Kibana Installation
```bash
sudo apt-get update && sudo apt-get install kibana
sudo update-rc.d kibana defaults 95 10
sudo -i service kibana start
service kibana status
```

[Refer any other fources for proper configuration of kafka service file]

## Start The services
```bash
service elasticsearch restart
service kibana status
sudo systemctl start fluentd
sudo systemclt start kafka
```

# About the Project

## Project Overview

In a microservices architecture, effective log management is crucial for operational excellence. This project aims to streamline the collection, storage, and analysis of logs generated by various services, enhancing the ability to track application behavior and identify errors quickly. By capturing relevant metadata alongside each log entry and enabling real-time ingestion and querying, the system improves operational visibility and facilitates proactive responses to potential issues. Ultimately, this distributed logging framework enhances resilience and maintainability in a dynamic application landscape.

## System Architecture and Flow

### Key Components:

1. **Microservices (Processes)**: 
   - Independent nodes (services) that generate logs and send heartbeat signals to monitor their health and status.
   
2. **Log Accumulator**: 
   - Collects logs from each node, structures the log data, and forwards it to the Pub-Sub model for centralized log management.

3. **Pub-Sub Model**:
   - A communication layer that ensures the reliable and asynchronous distribution of log data from the accumulator to the storage system.

4. **Log Storage**:
   - A centralized system for indexing, storing, and making logs searchable. The logs are stored in a format that is optimized for querying, providing easy access for monitoring and analysis.

5. **Alerting System**:
   - Monitors logs for specific events, such as `ERROR` or `FATAL` log levels. When such events are detected, the system generates real-time alerts to facilitate quick response.

6. **Heartbeat Mechanism**:
   - Detects failures by monitoring the heartbeat signals from each node. If a node stops sending heartbeats, an alert is triggered, indicating a potential failure.

### System Flow:
1. **Log Generation**: Each microservice generates logs along with relevant metadata (e.g., service name, timestamp, severity).
2. **Log Accumulation**: Logs are collected by the log accumulator.
3. **Log Distribution**: The Pub-Sub model forwards logs to the storage and alerting system.
4. **Log Storage and Querying**: Logs are indexed and stored in a centralized database, making it easy to query and analyze them.
5. **Real-time Alerting**: The alerting system watches for critical errors and generates notifications for the relevant teams.
6. **Failure Detection**: The heartbeat mechanism detects service failures and triggers alerts.

## Features

- **Centralized Log Management**: Collect and manage logs from all microservices in one place.
- **Real-Time Log Processing**: Log data is ingested and processed in real-time.
- **Queryable Log Storage**: Indexed logs allow fast and efficient querying.
- **Real-Time Alerting**: Alerts on critical log entries (e.g., ERROR, FATAL).
- **Failure Detection via Heartbeats**: Automatically detect when a service fails to send a heartbeat.
- **Scalable**: Easily scale to support an increasing number of microservices and logs.
- **Asynchronous Communication**: Uses a Pub-Sub model for non-blocking log processing.

## Technologies Used

- **Microservices**: Various backend services that produce logs.
- **Kafka**: For Pub-Sub communication and real-time log streaming.
- **Elasticsearch**: For indexing and storing logs in a searchable format.



## Architecture Diagram
![image](https://github.com/user-attachments/assets/010c4221-955c-411c-88e5-efdf86bae1b7)


## Running Microservices:
eg: payment service:
![image](https://github.com/user-attachments/assets/228d6180-28e4-44ba-bfac-08c3c31bedf0)


## PUB model:
![image](https://github.com/user-attachments/assets/c765e998-b7c9-4a62-82cc-5257c922f864)
![image](https://github.com/user-attachments/assets/e2ec6898-bec5-4dbe-a8dd-95318295e34e)
![image](https://github.com/user-attachments/assets/72cbba22-b2fb-4575-b1d1-466cf36274f5)


## Alerting UI:
![image](https://github.com/user-attachments/assets/f1bea336-1b08-41ce-bd57-704d6deb3059)

## Kibana Visualization:
![image](https://github.com/user-attachments/assets/9be5223a-12a3-4558-9243-936bdb34f2a7)

## Future Improvements

- **Distributed Tracing**: Integrate distributed tracing tools like Jaeger for better visibility across microservices.
- **Data Anomaly Detection**: Implement anomaly detection to identify unexpected patterns in logs.
- **Log Retention and Archiving**: Implement log retention policies for managing the size of log data over time.



## References & Documentation

To better understand and configure the components of the Distributed Logging System, here are the official documentation links for the key technologies used in this project:

### 1. **Fluentd**
Fluentd is a powerful open-source data collector for unified logging layers. It allows you to collect logs, parse them, and route them to various destinations like Elasticsearch.

- **Fluentd Documentation**:  
  - [Official Fluentd Documentation](https://docs.fluentd.org/)
  - [Fluentd Quick Start Guide](https://docs.fluentd.org/v1.0/articles/quickstart)
  - [Fluentd Configuration Reference](https://docs.fluentd.org/v1.0/articles/config-file)

### 2. **Kibana**
Kibana is a data visualization and exploration tool used for visualizing log data stored in Elasticsearch. It offers a powerful interface for querying and analyzing logs in real-time.

- **Kibana Documentation**:  
  - [Official Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
  - [Kibana Quick Start Guide](https://www.elastic.co/guide/en/kibana/current/getting-started.html)
  - [Kibana Tutorials and Examples](https://www.elastic.co/webinars/getting-started-kibana?baymax=default&elektra=docs&storm=top-video)

### 3. **Elasticsearch**
Elasticsearch is a distributed, RESTful search and analytics engine that is designed to store and index large volumes of data. It powers the log storage and searching in this system.

- **Elasticsearch Documentation**:  
  - [Official Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/index.html)
  - [Elasticsearch Installation Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)
  - [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)

### 4. **Kafka**
Apache Kafka is a distributed streaming platform used for building real-time data pipelines and streaming applications. Kafka enables the Pub-Sub communication model in this system, allowing logs to be asynchronously distributed.

- **Kafka Documentation**:  
  - [Official Kafka Documentation](https://kafka.apache.org/documentation/)
  - [Kafka Quick Start Guide](https://kafka.apache.org/quickstart)
  - [Kafka Configuration Documentation](https://kafka.apache.org/documentation/#configuration)

---

Feel free to explore the documentation of these tools for a deeper understanding of how they work and how to configure them effectively for your logging system. These resources will help you troubleshoot, extend functionality, and leverage advanced features of each tool as needed.


## Contact Me

Feel free to reach out with any questions, suggestions, or collaborations!

- **Email**: [ashleshat5@gmail.com](mailto:ashleshat5@gmail.com.com)

## Thank You!
Thank you for checking out our project! If you find it helpful, please give it a ⭐️ and share your feedback. 😊
