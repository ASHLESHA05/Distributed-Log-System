# Distributed log analysis
How to run ??

## 1️⃣ **Backend (FastAPI)**

**Location:** `backend/app/main.py`

### Steps:

1. Install dependencies (create a virtual environment):

```bash
cd distributed-log-system/backend
python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows
pip install -r requirements.txt
pip install python-dotenv uvicorn fastapi
```

2. Create `.env` or copy `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` if needed.

3. Run the FastAPI app:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Open in browser:

```
http://localhost:8000/docs
```

You should see **Swagger UI** for your APIs.

---

## 2️⃣ **AI Report Service (FastAPI)**

**Location:** `ai_report/app/main.py`

### Steps:

1. Install dependencies:

```bash
cd distributed-log-system/ai_report
python -m venv venv
source venv/bin/activate
pip install -r model/requirements.txt
pip install fastapi uvicorn python-dotenv
```

2. Copy `.env`:

```bash
cp .env.example .env
```

3. Run the app:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8500
```

4. Open Swagger UI:

```
http://localhost:8500/docs
```

---

## 3️⃣ **Kafka Consumer (Python)**

**Location:** `ingestion/consumer/main.py`

> Requires **Kafka broker running** locally or in Docker.

### Steps:

1. Install dependencies:

```bash
cd distributed-log-system/ingestion/consumer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env`:

```bash
cp .env.example .env
```

Edit `.env` to point to your Kafka broker.

3. Run the consumer:

```bash
python main.py
```

You should see output when messages arrive on the Kafka topic.

> ⚠️ If Kafka is not running locally, you can use Docker:

```bash
docker run -d --name kafka -p 9092:9092 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 wurstmeister/kafka
```

---

## 4️⃣ **C++ Agent**

**Location:** `agent_cpp/src/main.cpp`

### Steps:

1. Build with `CMake`:

```bash
cd distributed-log-system/agent_cpp
mkdir build && cd build
cmake ..
make
```

2. Run the agent:

```bash
./agent_cpp
```

You should see:

```
C++ Agent started...
Monitoring system...
Agent stopped.
```

> 🔹 You can expand `monitor.cpp` for real monitoring tasks later.

---

### ✅ Quick Summary:

| Service        | Run Command                                                |
| -------------- | ---------------------------------------------------------- |
| Backend        | `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` |
| AI Report      | `uvicorn app.main:app --reload --host 0.0.0.0 --port 8500` |
| Kafka Consumer | `python main.py`                                           |
| C++ Agent      | `cmake && make && ./agent_cpp`                             |

---

