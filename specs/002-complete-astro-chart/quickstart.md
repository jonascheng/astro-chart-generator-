# Quickstart: Complete Astrological Chart

This guide provides the steps to set up your local environment to work on the "Complete Astrological Chart" feature.

## 1. Backend Setup

### Prerequisites
- Python 3.11+
- Poetry (or pip)

### Dependencies
1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Install the new `pyswisseph` dependency. If you are using `poetry`:
    ```bash
    poetry add pyswisseph
    ```
    Or if you are using `pip` and a `requirements.txt` file:
    ```bash
    pip install pyswisseph
    # And add pyswisseph to your requirements.txt
    ```

3.  **Download Ephemeris Files**:
    The `pyswisseph` library requires data files to run its calculations.
    - Download the files from `https://www.astro.com/ftp/swisseph/ephe/`. The main files needed are `sepl_18.se1`, `semo_18.se1`, and `seas_18.se1`.
    - Create a directory, for example `backend/src/core/ephe`, and place the downloaded files there.
    - In the `calculations.py` file, you will need to set the path to this directory:
      ```python
      import swisseph as swe
      swe.set_ephe_path('path/to/your/backend/src/core/ephe')
      ```

## 2. Frontend Setup

### Prerequisites
- Node.js 20+
- npm

### Dependencies
1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2.  Install the new dependencies for D3.js and internationalization:
    ```bash
    npm install d3 react-i18next i18next
    ```

## 3. Running the Application

1.  **Start the backend server** from the `backend` directory:
    ```bash
    # Assuming you are using uvicorn with FastAPI
    uvicorn src.api.main:app --reload
    ```

2.  **Start the frontend development server** from the `frontend` directory in a separate terminal:
    ```bash
    npm run dev
    ```

You can now access the application in your browser (usually at `http://localhost:5173`) and begin development on the new chart component.
