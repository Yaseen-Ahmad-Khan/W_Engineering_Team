# W_Engineering_team

An autonomous software engineering crew powered by **CrewAI** that collaborates to plan, write, and test responsive full-stack applications (React frontend + FastAPI backend) based on user requirements.

The crew consists of multiple AI agents that work together to analyze the user's prompt, design the application, generate production-ready code for both the frontend and backend, and verify that the generated project runs successfully. The generated application is saved inside the `generated/` directory, where it can be run immediately.

## 🛠️ Prerequisites

Before getting started, make sure you have installed:

* **Python 3.10 - 3.13**
* **Node.js & npm** (required to run and verify the frontend build)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Yaseen-Ahmad-Khan/W_Engineering_team.git
cd W_Engineering_team
```

### 2. Set Up Python Environment

Create a virtual environment and install the required dependencies.

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
pip install .
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

### 3. Add Environment Variables

Create a file named `.env` in the root directory and add your Gemini API Key:

```env
MODEL=your_model_name
GEMINI_API_KEY=your_gemini_api_key_here
```

## 💻 How to Use

### 1. Enter Your Requirements

Open `src/W_Engineering_team/main.py` and replace the value of `user_requirement` in the `inputs` dictionary with your own project requirements. A proper frontend and backend requirement is highly encouraged.

Example:

```python
inputs = {
    "user_requirement": "Build a responsive coffee shop website with a React frontend and FastAPI backend."
}
```

### 2. Run the Crew

To start the autonomous team and generate the full-stack codebase:

```bash
crewai run
```

Once completed, the full-stack code will be generated inside the `generated/` directory.

### 3. Run the Generated Backend

Open a new terminal window:

```bash
cd generated/backend
pip install -r requirements.txt
python main.py
```

The FastAPI backend will start running on http://localhost:8000.

### 4. Run the Generated Frontend

Open another terminal window:

```bash
cd generated/frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser to view your generated responsive web application.
