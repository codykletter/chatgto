# ChatGTO

ChatGTO is a web application for interactive poker training based on Game Theory Optimal (GTO) principles.

## Tech Stack

*   **Frontend**: Next.js, shadcn/ui, Tailwind CSS
*   **Backend**: Python, FastAPI, MongoDB
*   **Authentication**: Firebase

## Setup Instructions

### Backend

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create and activate a Python virtual environment:
    ```bash
    python3.12 -m venv venv
    source venv/bin/activate
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file and add the `DATABASE_URL`:
    ```
    DATABASE_URL=mongodb+srv://codykletter:PASSWORD_PLACEHOLDER@cluster0.inth0e5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
    ```
    **Note**: Replace `PASSWORD_PLACEHOLDER` with your actual MongoDB password.
5.  Start the backend server:
    ```bash
    uvicorn app.main:app --reload
    ```

### Frontend

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install the required dependencies:
    ```bash
    npm install
    ```
3.  Create a `.env.local` file and add the Firebase configuration:
    ```
    NEXT_PUBLIC_FIREBASE_API_KEY="AIzaSyC7pZ489SLz4Ztza0hbKLr7WtZ0fMyrUJ8"
    NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN="chatgto-3ef2d.firebaseapp.com"
    NEXT_PUBLIC_FIREBASE_PROJECT_ID="chatgto-3ef2d"
    NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET="chatgto-3ef2d.firebasestorage.app"
    NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID="1048191728358"
    NEXT_PUBLIC_FIREBASE_APP_ID="1:1048191728358:web:fb6f385b18d0fe970c5927"
    NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID="G-B1P4F9B7NF"
    ```
4.  Start the frontend development server:
    ```bash
    npm run dev