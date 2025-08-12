# Code Summary

This document provides a comprehensive overview of the ChatGTO application, detailing its architecture, key components, data flow, and current limitations.

## 1. Overall Architecture

The application follows a modern client-server architecture, with a React-based frontend and a Python-based backend.

### Frontend

The frontend is a [Next.js](https://nextjs.org/) application, which provides server-side rendering and a rich development environment for React. It is responsible for the user interface, client-side state management, and communication with the backend API. User authentication is handled on the client-side using Firebase Authentication.

### Backend

The backend is a [FastAPI](https://fastapi.tiangolo.com/) application, which is a high-performance Python web framework. It is responsible for the application's business logic, data storage, and serving the API that the frontend consumes. It uses a MongoDB database for data persistence and the Firebase Admin SDK for secure authentication and user management.

### Interaction

The frontend and backend communicate via a RESTful API. The frontend sends HTTP requests to the backend to fetch data, submit user actions, and manage user accounts. The backend processes these requests, interacts with the database, and returns JSON responses to the frontend.

## 2. Key Modules, Classes, and Functions

### Backend

-   **`main.py`**: The entry point of the FastAPI application. It initializes the FastAPI app, sets up CORS middleware, connects to the MongoDB database on startup, and includes the API routers.
-   **`api/v1/`**: This directory contains the API endpoints, organized by resource.
    -   **`users.py`**: Handles user creation.
    -   **`practice.py`**: Contains the core logic for the poker training, including fetching scenarios and evaluating user attempts.
    -   **`health.py`**: A simple health check endpoint.
-   **`models/`**: This directory contains the Pydantic data models that define the structure of the data used in the application.
    -   **`User`**: Represents a user with a `firebase_uid` and `email`.
    -   **`Scenario`**: Represents a poker training scenario.
    -   **`GtoAction`**: Represents a possible action within a scenario.
    -   **`Attempt`**: Represents a user's attempt at a scenario.
-   **`scripts/seed_db.py`**: A script to populate the database with initial data.

### Frontend

-   **`pages/`**: This directory contains the main pages of the application.
    -   **`_app.tsx`**: The root component of the application, which wraps all pages with the `AuthProvider`.
    -   **`index.tsx`**: The landing page.
    -   **`login/page.tsx`**: The user login page.
    -   **`register/page.tsx`**: The user registration page.
    -   **`dashboard/page.tsx`**: The user dashboard, which displays stats and provides a link to the training page.
    -   **`training/page.tsx`**: The main training interface where users interact with poker scenarios.
-   **`context/AuthContext.tsx`**: A React context that provides authentication state (`user` and `loading`) to the entire application. It uses Firebase's `onAuthStateChanged` to listen for changes in the user's authentication state.
-   **`lib/firebase.ts`**: Initializes and configures the Firebase SDK for the frontend.
-   **`components/`**: This directory contains reusable React components.

## 3. Data Flow

1.  **User Registration**: A new user signs up on the registration page. The frontend uses Firebase Authentication to create a new user account. It then sends a request to the backend's `/api/v1/users` endpoint to store the user's information in the MongoDB database.
2.  **User Login**: A user logs in on the login page. The frontend uses Firebase Authentication to sign the user in. The `AuthContext` is updated with the user's information, which is then available to all components.
3.  **Training Session**:
    -   The user navigates to the training page.
    -   The frontend sends a GET request to `/api/v1/practice/scenarios` to fetch a random poker scenario.
    -   The backend retrieves the scenarios (currently from mock data) and sends one back to the frontend.
    -   The frontend displays the scenario to the user.
    -   The user chooses an action (e.g., "Raise", "Fold").
    -   The frontend sends a POST request to `/api/v1/practice/attempt` with the `scenario_id` and the chosen `action`.
    -   The backend evaluates the action against the correct action for the scenario and returns feedback, including whether the action was correct, the EV difference, and an explanation.
    -   The frontend displays the feedback to the user.

## 4. Current Limitations

-   **Mock Data**: The backend currently uses mock data for the practice scenarios. This should be replaced with a system that retrieves scenarios from the MongoDB database. The `seed_db.py` script provides a starting point for this.
-   **No User-Specific Data**: The dashboard displays static, hardcoded stats. There is no system in place to track a user's progress or performance over time.
-   **Limited Scenarios**: The variety of scenarios is very limited. A larger and more diverse set of scenarios is needed to provide effective training.
-   **Basic UI**: The user interface is functional but could be improved with better styling and more interactive elements.
-   **No Error Handling**: While some basic error handling exists, it could be made more robust and user-friendly.