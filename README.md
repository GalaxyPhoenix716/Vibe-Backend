# Vibe Backend

This is the backend for the Vibe music app I am creating. It is built using FastAPI and SQLModel to handle the core server-side operations, including user authentication, song uploads, managing favorites, custom user playlists, and search filtering.

To keep things efficient, the server uploads and hosts media assets (audio files and image thumbnails) directly on Cloudinary, and uses Supabase Auth to safely verify JSON Web Tokens (JWTs) using public signing keys.

---

## Tech Stack

Here is what I am using to build the backend:

- **FastAPI**: The web framework for handling API routes and requests.
- **SQLModel**: The database toolkit that combines SQLAlchemy and Pydantic so I can write pythonic database models.
- **PostgreSQL**: The relational database for storing app data.
- **PyJWT & PyJWKClient**: To fetch Supabase's public signature keys and verify user logins.
- **Cloudinary**: For storing and serving audio files and song covers.
- **Pydantic Settings**: For loading configuration settings from environment files.

---

## Core Features

- **Secure Authentication**: Validates user JWT tokens against Supabase using FastAPI's HTTPBearer middleware.
- **Database Unique Constraints**: Added unique constraints at the database level to prevent duplicate favorites and duplicate songs in the same playlist.
- **Optimized Queries**: Uses SQLAlchemy joinedload options to eagerly load database relations and prevent slow N+1 query execution.
- **Type-Safe Serialization**: Implements custom Pydantic response models to make sure the server returns consistent JSON payloads to the Flutter client.
- **Real-time search**: Offers case-insensitive search filtering across song titles, artists, and tag lists.

---

## File Structure

Here is how the project files are laid out:

```text
server/
├── app/
│   ├── auth/
│   │   └── jwt_handler.py        # Token validation and JWKS key retrieval
│   ├── core/
│   │   └── config.py             # Environment configuration settings
│   ├── db/
│   │   └── database.py           # Database engine setup and session factory
│   ├── middleware/
│   │   └── auth_middleware.py    # Authentication middleware guards
│   ├── models/
│   │   ├── favourite.py          # User favorite songs model
│   │   ├── playlist.py           # Playlist and playlist_songs junction tables
│   │   ├── song.py               # Song metadata model
│   │   └── user.py               # User profile model
│   ├── routes/
│   │   ├── auth_routes.py        # Authentication routes
│   │   ├── playlist_routes.py    # Playlist management routes
│   │   └── song_routes.py        # Song listing, upload, and search routes
│   ├── schemas/
│   │   ├── favourite.py          # Favorite request schemas
│   │   ├── playlist.py           # Playlist request/response schemas
│   │   └── song.py               # Song response schemas
│   └── main.py                   # App entrypoint and database lifespan setup
├── .env                          # Configuration environment variables
├── .gitignore                    # Ignored files for git
├── requirements.txt              # Project dependencies list
└── README.md                     # This file
```

---

## API Endpoints

### Auth Endpoints

| Method | Endpoint      | Requires Token? | Description                                                   |
| :----- | :------------ | :-------------: | :------------------------------------------------------------ |
| `POST` | `/auth/login` |       Yes       | Signs in a user and logs them in our local database.          |
| `GET`  | `/auth/`      |       Yes       | Returns the logged-in user profile with their favorite songs. |

### Song Endpoints

| Method | Endpoint                | Requires Token? | Description                                                          |
| :----- | :---------------------- | :-------------: | :------------------------------------------------------------------- |
| `POST` | `/song/upload`          |       Yes       | Uploads a song audio and thumbnail to Cloudinary and saves metadata. |
| `GET`  | `/song/list`            |       Yes       | Lists all available songs.                                           |
| `GET`  | `/song/search`          |       Yes       | Searches the library case-insensitively by title, artist, or tags.   |
| `POST` | `/song/favourite`       |       Yes       | Toggles a song as a user favorite.                                   |
| `GET`  | `/song/list-favourites` |       Yes       | Returns all the user's favorite songs.                               |

### Playlist Endpoints

| Method   | Endpoint                  | Requires Token? | Description                                |
| :------- | :------------------------ | :-------------: | :----------------------------------------- |
| `POST`   | `/playlist/create`        |       Yes       | Creates a new playlist.                    |
| `GET`    | `/playlist/list`          |       Yes       | Lists all playlists owned by the user.     |
| `GET`    | `/playlist/{playlist_id}` |       Yes       | Returns a playlist with its list of songs. |
| `POST`   | `/playlist/add-song`      |       Yes       | Adds a song to a playlist.                 |
| `DELETE` | `/playlist/remove-song`   |       Yes       | Removes a song from a playlist.            |
| `DELETE` | `/playlist/{playlist_id}` |       Yes       | Deletes a playlist.                        |

---

## Getting Started

### Prerequisites

Make sure you have python (3.10+) and a PostgreSQL instance running locally or hosted online.

### Configuration

Create a `.env` file in the root of the server folder and set these variables:

```ini
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
SUPABASE_URL=https://<your-project-id>.supabase.co
SUPABASE_JWT_SECRET=<your-supabase-jwt-signing-secret>
CLOUDINARY_CLOUD_NAME=<your-cloudinary-cloud-name>
CLOUDINARY_API_KEY=<your-cloudinary-api-key>
CLOUDINARY_API_SECRET=<your-cloudinary-api-secret>
```

### Installation

1. Open your terminal in the server folder and set up a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Linux / macOS:
     ```bash
     source venv/bin/activate
     ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start up the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

The backend server runs locally at `http://127.0.0.1:8000`.

### Live Hosted API & Docs

The backend is publicly hosted and running on Oracle Cloud. You can connect to the API or browse the documentation directly using these links:
* **Live Swagger UI**: [http://152.67.191.54:8000/docs](http://152.67.191.54:8000/docs)
* **Live ReDoc view**: [http://152.67.191.54:8000/redoc](http://152.67.191.54:8000/redoc)

---