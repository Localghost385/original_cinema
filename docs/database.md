# Database Schema Documentation

This document provides a detailed overview of the schema used for the application. It includes the tables, their columns, relationships, and key attributes.

## Table of Contents

1. [Users Table](#users-table)
2. [Profiles Table](#profiles-table)
3. [Ratings Table](#ratings-table)
4. [Watchlist Table](#watchlist-table)
5. [Preferences Table](#preferences-table)
6. [User Preferences Cache Table](#user-preferences-cache-table)
7. [Movies Table](#movies-table)
8. [Indexes](#indexes)
9. [Triggers](#triggers)

---

### 1. Users Table

Stores basic information about the users.

| Column      | Type        | Description                                              |
|-------------|-------------|----------------------------------------------------------|
| `id`        | UUID        | Primary Key. Unique identifier for the user.             |
| `email`     | TEXT        | Unique email address of the user.                        |
| `password`  | TEXT        | The user's hashed password.                              |
| `created_at`| TIMESTAMP   | Timestamp of when the user was created.                  |
| `updated_at`| TIMESTAMP   | Timestamp of the last time the user information was updated. |

---

### 2. Profiles Table

Stores profile information for users. Each user can have multiple profiles.

| Column      | Type        | Description                                              |
|-------------|-------------|----------------------------------------------------------|
| `id`        | UUID        | Primary Key. Unique identifier for the profile.          |
| `user_id`   | UUID        | Foreign Key referencing the `users` table.               |
| `full_name` | VARCHAR(255)| Full name of the user (optional).                        |
| `avatar_url`| TEXT        | URL to the user's profile picture (optional).            |
| `created_at`| TIMESTAMP   | Timestamp of when the profile was created.               |
| `updated_at`| TIMESTAMP   | Timestamp of the last time the profile was updated.      |

---

### 3. Ratings Table

Stores user ratings for movies.

| Column      | Type        | Description                                              |
|-------------|-------------|----------------------------------------------------------|
| `id`        | UUID        | Primary Key. Unique identifier for the rating.           |
| `profile_id`| UUID        | Foreign Key referencing the `profiles` table.            |
| `movie_id`  | UUID        | Unique identifier for the movie being rated.             |
| `rating`    | INTEGER     | Rating value between 1 and 5.                             |
| `created_at`| TIMESTAMP   | Timestamp of when the rating was made.                   |

---

### 4. Watchlist Table

Stores movies that the user has added to their watchlist.

| Column      | Type        | Description                                              |
|-------------|-------------|----------------------------------------------------------|
| `id`        | UUID        | Primary Key. Unique identifier for the watchlist entry.  |
| `profile_id`| UUID        | Foreign Key referencing the `profiles` table.            |
| `movie_id`  | UUID        | Unique identifier for the movie added to the watchlist.  |
| `created_at`| TIMESTAMP   | Timestamp of when the movie was added to the watchlist.  |

---

### 5. Preferences Table

Stores the user's movie preferences.

| Column      | Type        | Description                                              |
|-------------|-------------|----------------------------------------------------------|
| `id`        | UUID        | Primary Key. Unique identifier for the preferences.      |
| `profile_id`| UUID        | Foreign Key referencing the `profiles` table.            |
| `like`      | TEXT[]      | Array of movie IDs the user likes.                       |
| `love`      | TEXT[]      | Array of movie IDs the user loves.                       |
| `dislike`   | TEXT[]      | Array of movie IDs the user dislikes.                    |
| `hate`      | TEXT[]      | Array of movie IDs the user hates.                       |
| `rated`     | TEXT[]      | Array of movie IDs the user has rated.                   |
| `created_at`| TIMESTAMP   | Timestamp of when the preferences were created.          |

---

### 6. User Preferences Cache Table

Stores cached movie preferences for a user's profile to avoid recalculating preferences on every request.

| Column           | Type        | Description                                              |
|------------------|-------------|----------------------------------------------------------|
| `id`             | UUID        | Primary Key. Unique identifier for the cached preferences.|
| `profile_id`     | UUID        | Foreign Key referencing the `profiles` table.            |
| `liked_genres`   | TEXT[]      | Array of liked genre IDs.                                |
| `liked_keywords` | TEXT[]      | Array of liked keyword IDs.                              |
| `liked_actors`   | TEXT[]      | Array of liked actor IDs.                                |
| `liked_directors`| TEXT[]      | Array of liked director IDs.                             |
| `created_at`     | TIMESTAMP   | Timestamp of when the cache was created.                 |
| `updated_at`     | TIMESTAMP   | Timestamp of the last time the cache was updated.        |

---

### 7. Movies Table

Stores movie information.

| Column        | Type        | Description                                              |
|---------------|-------------|----------------------------------------------------------|
| `id`          | UUID        | Primary Key. Unique identifier for the movie.            |
| `title`       | VARCHAR(255)| Title of the movie.                                      |
| `release_date`| DATE        | Release date of the movie.                               |
| `genres`      | TEXT[]      | Array of genre IDs associated with the movie.            |
| `keywords`    | TEXT[]      | Array of keyword IDs associated with the movie.          |
| `actors`      | TEXT[]      | Array of actor IDs associated with the movie.            |
| `directors`   | TEXT[]      | Array of director IDs associated with the movie.         |
| `overview`    | TEXT        | Brief description or overview of the movie.              |
| `created_at`  | TIMESTAMP   | Timestamp of when the movie was created.                 |

---

### 8. Indexes

To improve performance, the following indexes are created:

- `idx_ratings_movie_id`: Index on `movie_id` in the `ratings` table for fast lookups.
- `idx_watch_list_movie_id`: Index on `movie_id` in the `watch_list` table for fast lookups.
- `idx_preferences_likes`: GIN index on the `like` column in the `preferences` table for efficient querying.
- `idx_preferences_love`: GIN index on the `love` column in the `preferences` table for efficient querying.
- `idx_preferences_dislike`: GIN index on the `dislike` column in the `preferences` table for efficient querying.
- `idx_preferences_hate`: GIN index on the `hate` column in the `preferences` table for efficient querying.
- `idx_preferences_rated`: GIN index on the `rated` column in the `preferences` table for efficient querying.
- `idx_user_preferences_cache_profile_id`: Index on `profile_id` in the `user_preferences_cache` table for fast lookups.

---

### 9. Triggers

To ensure `updated_at` timestamps are automatically updated on table changes:

#### `update_profile_timestamp_trigger`

- **Table**: `profiles`
- **Function**: Automatically updates the `updated_at` column whenever a profile is modified.

#### `update_rating_timestamp_trigger`

- **Table**: `ratings`
- **Function**: Automatically updates the `updated_at` column whenever a rating is modified.

---