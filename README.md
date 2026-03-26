# SRE Alert Assistant

#### Video Demo: [Watch here](https://youtu.be/aaZUp5Of2Ks)

#### Description:

SRE Alert Assistant is a web-based application that helps beginners understand technical system alerts in plain English. In many engineering environments, alerts can be hard to interpret, especially for people who are new to Site Reliability Engineering (SRE). These alerts are usually short, technical, and assume you already know what is going on. I wanted to build something that makes those alerts easier to understand by breaking them down into clear explanations, possible causes, and suggested next steps.

I chose this project because I wanted to better understand how SRE alerts work and build a tool that makes them easier to learn for beginners.

This application is built using Flask for the backend, SQLite for data storage, and HTML, CSS, JavaScript, and Bootstrap for the frontend. It also includes optional integration with the OpenAI API. If an alert is not already stored in the system, the app can generate a beginner-friendly explanation using AI.

The main functionality starts on the home page. A user can enter an alert and submit it. The app first checks if that alert already exists in the database. If it does, it retrieves the stored explanation and displays it immediately. If it does not, the app calls the AI helper to generate a response. The response includes severity, explanation, possible causes, and next steps. Once generated, the result is saved to the database so it can be reused later.

To use the AI feature, an OpenAI API key must be set in a `.env` file. If no API key is provided, the application will still function using the knowledge base.

The backend logic is handled in `app.py`. This file defines all of the routes and controls how the application responds to user input. The `/` route handles alert lookups and decides whether to use the database or AI. The `/add` route allows users to manually add alerts to the knowledge base. This route also validates input, prevents duplicate alerts, and keeps user input in the form if there is an error. The `/knowledge_base` route displays all saved alerts sorted by newest first.

The file `ai_helper.py` is responsible for interacting with the OpenAI API. It loads the API key from a `.env` file, sends a prompt asking for structured JSON output, and parses the response. If the API key is missing or the response cannot be parsed correctly, the function returns `None` so the app can handle the situation without crashing.

The database structure is defined in `schema.sql`. The `alerts` table stores the alert text, explanation, severity, possible causes, next steps, source, and a timestamp for when the alert was created. I used SQLite because it is simple and works well for a project like this.

The frontend is built using Jinja templates and Bootstrap. The `layout.html` file provides the shared layout and navigation bar. The `index.html` file handles alert input and displays results. The `add.html` file contains the form for adding alerts and includes validation and form state preservation so users do not lose their input. The `knowledge_base.html` file displays saved alerts in a clean format, including severity badges and timestamps. Custom styling is included in `static/styles.css`.

One of the main design decisions I made was to combine a database with AI-generated responses. If the app only used a database, it would be limited to alerts that were already saved. If it only used AI, it would depend completely on an external service. By combining both approaches, the app is more flexible and reliable. Known alerts are returned instantly, and new alerts can still be explained and then saved.

I also focused on making the app easy to use. The form preserves input when there are errors so users do not have to retype everything. The severity dropdown uses a placeholder so users have to make a clear choice instead of defaulting to a value. I also used color-coded badges to make severity easier to understand at a glance.

For security, the OpenAI API key is stored in a `.env` file and excluded from version control using `.gitignore`.

If I continued working on this project, I would add features like search, filtering by severity, editing and deleting alerts, and grouping alerts by system type. I could also add user accounts so teams could manage their own alert libraries.

Overall, this project combines web development, databases, and AI to create a practical tool that helps beginners understand technical alerts and know what to do next.
