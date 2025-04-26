import requests
import json
import random
import sys
from colorama import Fore, init
from tqdm import tqdm  # Progress bar library

# Initialize colorama
init(autoreset=True)

API_KEY = "d196a6248da7e48c7198ab8be626c694"  # Replace with your actual TMDb API key
MAX_RATED_LENGTH = 512  # Maximum length for the "rated" list

# Rating weights: "like" counts as 1 point, "love" counts as 2 points.
RATING_WEIGHTS = {
    "like": 1,
    "love": 2,
}

# Scoring factors for candidate movie matching
SCORE_FACTORS = {
    "genres": 1.0,
    "keywords": 1.0,
    "directors": 2.0,
    "cast": 0.5,
}

# Global variable to hold the last debug message for DEBUG level.
_last_debug = ""

def debug(message, level='INFO'):
    """Prints debug messages."""
    global _last_debug
    colors = {'INFO': Fore.CYAN, 'ERROR': Fore.RED, 'DEBUG': Fore.YELLOW}
    formatted = colors.get(level, Fore.WHITE) + f"[{level}] {message}"
    if level == "DEBUG":
        sys.stdout.write("\r" + " " * len(_last_debug))  # clear previous line
        sys.stdout.write("\r" + formatted)
        sys.stdout.flush()
        _last_debug = formatted
    else:
        if _last_debug:
            sys.stdout.write("\n")
            _last_debug = ""
        tqdm.write(formatted)

def get_tmdb_data(url, params):
    """Helper function to fetch data from TMDb API."""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json().get("results", [])
        return data
    except requests.exceptions.RequestException as e:
        debug(f"Failed to fetch data: {e}", 'ERROR')
        return []

def get_popular_movies():
    """Fetches currently popular movies."""
    debug("Getting popular movies.", "INFO")
    return get_tmdb_data("https://api.themoviedb.org/3/movie/popular", {
        "api_key": API_KEY,
        "language": "en-US",
        "page": 1
    })

def get_all_time_popular_movies():
    """Fetches all-time popular movies with high ratings."""
    debug("Getting all-time popular movies.", "INFO")
    return get_tmdb_data("https://api.themoviedb.org/3/discover/movie", {
        "api_key": API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": random.randint(1, 5),
        "vote_average.gte": 7,
    })

def save_preferences(preferences):
    """Saves user preferences to a JSON file."""
    debug("Saving preferences to preferences.json", "INFO")
    with open("preferences.json", "w") as file:
        json.dump(preferences, file)

def load_preferences():
    """Loads user preferences from a JSON file."""
    debug("Loading preferences from preferences.json", "INFO")
    try:
        with open("preferences.json", "r") as file:
            prefs = json.load(file)
            return prefs
    except FileNotFoundError:
        debug("Preferences file not found. Using default preferences.", "INFO")
        return {"like": [], "love": [], "dislike": [], "hate": [], "rated": []}

def get_movie_details(movie_id):
    """
    Fetches detailed information for a given movie.
    Appends credits and keywords to include cast, crew, and keywords data.
    """
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={"api_key": API_KEY, "append_to_response": "credits,keywords"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        debug(f"Failed to fetch details for movie ID {movie_id}: {e}", 'ERROR')
        return {}

def build_preference_profile(preferences):
    """
    Builds a weighted profile from liked movies.
    Returns a dictionary with aggregated counts for genres, keywords, directors, and cast.
    """
    debug("Building preference profile.", "INFO")
    profile = {
        "genres": {},
        "keywords": {},
        "directors": {},
        "cast": {},
    }
    for rating_type in ["like", "love"]:
        weight = RATING_WEIGHTS.get(rating_type, 1)
        for movie_id in preferences.get(rating_type, []):
            details = get_movie_details(movie_id)
            if not details:
                continue
            for genre in details.get("genres", []):
                g_id = genre.get("id")
                if g_id:
                    profile["genres"][g_id] = profile["genres"].get(g_id, 0) + weight
            for keyword in details.get("keywords", {}).get("keywords", []):
                k_id = keyword.get("id")
                if k_id:
                    profile["keywords"][k_id] = profile["keywords"].get(k_id, 0) + weight
            for crew in details.get("credits", {}).get("crew", []):
                if crew.get("job") == "Director":
                    d_id = crew.get("id")
                    if d_id:
                        profile["directors"][d_id] = profile["directors"].get(d_id, 0) + weight
            cast_list = details.get("credits", {}).get("cast", [])
            for cast in cast_list[:5]:
                c_id = cast.get("id")
                if c_id:
                    profile["cast"][c_id] = profile["cast"].get(c_id, 0) + weight
    return profile

def get_candidate_movies(num_movies=1000):
    """
    Loads a number of candidate movies from the discover endpoint.
    Due to TMDb API limitations, we randomly choose pages (each page returns 20 movies).
    A progress bar displays the loading progress.
    """
    debug(f"Loading {num_movies} candidate movies.", "INFO")
    candidates = []
    pages_needed = num_movies // 20
    with tqdm(total=pages_needed, desc="Loading candidate movies") as pbar:
        for _ in range(pages_needed):
            page = random.randint(1, 500)
            movies = get_tmdb_data("https://api.themoviedb.org/3/discover/movie", {
                "api_key": API_KEY,
                "language": "en-US",
                "page": page,
            })
            candidates.extend(movies)
            pbar.update(1)
    return candidates

def score_movie(movie, profile):
    """
    Scores a candidate movie based on its similarity to the preference profile.
    Returns a tuple of (total_score, breakdown_dict).
    A progress bar shows progress while scoring individual features.
    """
    details = get_movie_details(movie["id"])
    if not details:
        return 0, {"genres": 0, "keywords": 0, "directors": 0, "cast": 0}

    score = 0
    breakdown = {"genres": 0, "keywords": 0, "directors": 0, "cast": 0}
    total_items = (len(details.get("genres", [])) +
                   len(details.get("keywords", {}).get("keywords", [])) +
                   len([crew for crew in details.get("credits", {}).get("crew", []) if crew.get("job") == "Director"]) +
                   len(details.get("credits", {}).get("cast", [])))
   
    with tqdm(total=total_items, desc="Scoring features", leave=False) as pbar:
        for genre in details.get("genres", []):
            g_id = genre.get("id")
            if g_id and g_id in profile["genres"]:
                pts = profile["genres"][g_id] * SCORE_FACTORS["genres"]
                breakdown["genres"] += pts
                score += pts
            pbar.update(1)
        for keyword in details.get("keywords", {}).get("keywords", []):
            k_id = keyword.get("id")
            if k_id and k_id in profile["keywords"]:
                pts = profile["keywords"][k_id] * SCORE_FACTORS["keywords"]
                breakdown["keywords"] += pts
                score += pts
            pbar.update(1)
        for crew in details.get("credits", {}).get("crew", []):
            if crew.get("job") == "Director":
                d_id = crew.get("id")
                if d_id and d_id in profile["directors"]:
                    pts = profile["directors"][d_id] * SCORE_FACTORS["directors"]
                    breakdown["directors"] += pts
                    score += pts
            pbar.update(1)
        cast_list = details.get("credits", {}).get("cast", [])
        for cast in cast_list[:5]:
            c_id = cast.get("id")
            if c_id and c_id in profile["cast"]:
                pts = profile["cast"][c_id] * SCORE_FACTORS["cast"]
                breakdown["cast"] += pts
                score += pts
            pbar.update(1)
    return score, breakdown

def get_best_matching_movies(preferences):
    """
    Builds the user preference profile, loads candidate movies,
    scores them based on similarity, and returns the top matches.
    Each match is returned along with its score breakdown.
    """
    debug("Getting best matching movies based on preference profile.", "INFO")
    profile = build_preference_profile(preferences)
    candidates = get_candidate_movies(1000)
    scored = []
    with tqdm(total=len(candidates), desc="Scoring candidate movies") as pbar:
        for movie in candidates:
            if movie["id"] in preferences.get("rated", []):
                continue
            s, breakdown = score_movie(movie, profile)
            scored.append((s, breakdown, movie))
            pbar.update(1)
    scored.sort(key=lambda x: x[0], reverse=True)
    top_matches = [(s, b, m) for s, b, m in scored if s > 0]
    sample_size = min(len(top_matches), 10, 50)
    debug(f"Returning a random sample of {sample_size} movies from top matches.", "INFO")
    return random.sample(top_matches[:50], sample_size)

def get_random_recommendations(preferences):
    """
    Uses the best matching movies approach if there are liked movies,
    otherwise falls back to popular movies.
    Returns a list of tuples: (total_score, breakdown, movie).
    """
    liked = preferences.get("like", []) + preferences.get("love", [])
    if liked:
        debug("Generating recommendations based on liked movies.", "INFO")
        return get_best_matching_movies(preferences)
    else:
        debug("No liked movies found; using popular movies.", "INFO")
        popular = get_popular_movies()
        return [(0, None, m) for m in popular]

def rate_movies():
    """Allows users to rate movies and store preferences."""
    preferences = load_preferences()
    while True:
        if not preferences["like"] and not preferences["love"]:
            debug("No liked movies found; fetching all-time popular movies for rating.", "INFO")
            movies = get_all_time_popular_movies()
        else:
            debug("Fetching recommendations for rating.", "INFO")
            movies = [m for _, _, m in get_random_recommendations(preferences)]
        movies_to_rate = [m for m in movies if m["id"] not in preferences["rated"]]
        if not movies_to_rate:
            debug("No more movies to rate.", 'INFO')
            return
        for movie in movies_to_rate:
            print(Fore.MAGENTA + f"\n{movie['title']} ({movie['release_date'][:4]})")
            rating = input(Fore.CYAN + "Like, Love, Dislike, Hate, or Not Seen? ").strip().lower()
            if rating == "stop":
                save_preferences(preferences)
                return
            elif rating in ["like", "love", "dislike", "hate"]:
                debug(f"Recording rating '{rating}' for movie ID {movie['id']}.", "INFO")
                preferences[rating].append(movie["id"])
                preferences["rated"].append(movie["id"])
                if len(preferences["rated"]) > MAX_RATED_LENGTH:
                    preferences["rated"].pop(0)
        save_preferences(preferences)

def recommend_movies():
    """Displays movie recommendations based on user preferences along with a breakdown of points."""
    preferences = load_preferences()
    recs = get_random_recommendations(preferences)
    movies_to_recommend = [(s, b, m) for s, b, m in recs if m["id"] not in preferences["rated"]]
    if not movies_to_recommend:
        debug("No recommendations available. Try rating more movies!", 'INFO')
        return
    for total_score, breakdown, movie in movies_to_recommend:
        print(Fore.MAGENTA + f"{movie['title']} ({movie['release_date'][:4]}) - Total Score: {total_score}")
        if breakdown:
            print(Fore.BLACK + "   Breakdown:")
            print(Fore.BLACK + f"     Genres: {breakdown['genres']} points")
            print(Fore.BLACK + f"     Keywords: {breakdown['keywords']} points")
            print(Fore.BLACK + f"     Directors: {breakdown['directors']} points")
            print(Fore.BLACK + f"     Cast: {breakdown['cast']} points")
        else:
            print(Fore.BLACK + "   No detailed breakdown available.")

if __name__ == "__main__":
    while True:
        action = input(Fore.CYAN + "\nDo you want to rate movies or get recommendations? (rate/recommend/exit): ").strip().lower()
        if action == "rate":
            rate_movies()
        elif action == "recommend":
            recommend_movies()
        elif action == "exit":
            break
        else:
            debug("Invalid input. Please enter 'rate', 'recommend', or 'exit'.", 'ERROR')