# -----------------------------
# Enhanced AI Finder Page with OMDB Integration - SIMPLIFIED
# -----------------------------
def show_enhanced_ai_finder_page():
    """Enhanced AI Finder page with cinematic styling, OMDB search + Gemini chatbot."""
    st.markdown("""
    <div class="hero-container">
        <h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 1rem;">🔍 ENHANCED AI FINDER</h2>
        <p style="text-align: center; font-size: 1.3rem; color: #FFD93D; margin: 0;">
            Discover Movies & Anime Across All Platforms
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Two columns: left = search (old behaviour), right = Gemini chatbot
    col1, col2 = st.columns([2, 1])

    # -----------------------------
    # LEFT – your existing simple search + popular/theater tabs
    # -----------------------------
    with col1:
        st.markdown("### 🤖 ENHANCED MOVIE & ANIME SEARCH")

        search_query = st.text_input(
            "🎬 Search movies or anime.",
            placeholder="Enter movie title, anime, or genre.",
            key="enhanced_ai_search",
        )

        if search_query:
            with st.spinner("🔍 Searching across all platforms."):
                # OMDB search
                omdb = RateLimitedOMDbAPI()
                movie_results = omdb.search_movies(search_query, "movie", None)

                # Anime search
                anime_integration = AnimeIntegration()
                anime_results = anime_integration.search_anime(search_query)

                if movie_results or anime_results:
                    st.markdown(
                        f"### 🎯 Found {len(movie_results) + len(anime_results)} Results"
                    )

                    if movie_results:
                        st.markdown("#### 🎬 Movies & Series")
                        for i, movie in enumerate(movie_results):
                            display_enhanced_search_result(movie, "movie", i)

                    if anime_results:
                        st.markdown("#### 🍥 Anime")
                        for i, anime in enumerate(anime_results):
                            display_enhanced_search_result(anime, "anime", i)
                else:
                    st.warning(
                        "No results found. Try a different search term or check our recommendations below."
                    )
                    # If you have this helper it will still work;
                    # if not, this will just be skipped.
                    try:
                        show_search_recommendations(search_query)
                    except NameError:
                        pass
        else:
            # Old behaviour: show tabs with Popular / In Theaters etc.
            show_popular_content()

    # -----------------------------
    # RIGHT – Gemini movie chatbot
    # -----------------------------
    with col2:
        st.markdown("### 💬 Movie Help Chatbot (Gemini)")

        # Lazy init so we don't touch your global init_session_state
        if "gemini_chat" not in st.session_state:
            st.session_state.gemini_chat = GeminiMovieChat()
        if "ai_history" not in st.session_state:
            st.session_state.ai_history = []

        chat = st.session_state.gemini_chat

        # Show chat history
        for msg in st.session_state.ai_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # User input (works like before)
        user_msg = st.chat_input(
            "Tell me your mood, a plot, or actor names…\nExample: 'Sad mood, recommend 3 sci-fi movies' or 'Movie like Interstellar but with more romance'."
        )

        if user_msg:
            # Store + show user message
            st.session_state.ai_history.append({"role": "user", "content": user_msg})
            with st.chat_message("user"):
                st.markdown(user_msg)

            # Gemini-only backend (ONE API KEY)
            answer_text, movie_titles = chat.generate_ai_response(user_msg)

            # Store + show assistant answer
            st.session_state.ai_history.append(
                {"role": "assistant", "content": answer_text}
            )
            with st.chat_message("assistant"):
                st.markdown(answer_text)

                # Show only the movie names (up to 3)
                if movie_titles:
                    st.markdown("**🎬 Suggested movies (max 3):**")
                    for title in movie_titles:
                        st.markdown(f"- {title}")
                else:
                    st.markdown(
                        "_No specific movie titles could be found for this query._"
                    )

        st.markdown("---")
        st.markdown("##### ℹ️ What can I ask?")
        st.caption(
            """
- *"I feel lonely, suggest 3 movies."*
- *"Give me 3 comedy movies with Jim Carrey."*
- *"Anime where the main character travels through time."*
- *"Movie similar to Inception but easier to understand."*
"""
        )


# -----------------------------
# Enhanced AI Chat System
# -----------------------------
class AdvancedAIChat:
    def __init__(self):
        self.conversation_history = []
        self.omdb = RateLimitedOMDbAPI()
        self.user_preferences = {
            "favorite_genres": [],
            "watch_habits": {},
            "recent_interests": []
        }
        self.streaming_finder = EnhancedStreamingServiceFinder()
        
    def generate_ai_response(self, user_input, movie_data):
        """Generate intelligent AI response with streaming integration"""
        user_input_lower = user_input.lower()
        
        # Update user preferences based on conversation
        self._update_user_preferences(user_input, movie_data)
        
        # Enhanced response system with streaming integration
        if any(word in user_input_lower for word in ['watch', 'stream', 'where to watch', 'netflix', 'amazon', 'hulu', 'disney', 'youtube']):
            return self._get_streaming_response(user_input, movie_data)
        
        elif any(word in user_input_lower for word in ['ticket', 'theater', 'cinema', 'buy ticket']):
            return self._get_ticketing_response(user_input, movie_data)
        
        elif any(word in user_input_lower for word in ['anime', 'crunchyroll']):
            return self._get_anime_response(user_input, movie_data)
        
        elif any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return self._get_greeting_response(movie_data)
        
        elif any(word in user_input_lower for word in ['recommend', 'suggest', 'what should i watch', 'what to watch']):
            return self._get_recommendation_response(user_input, movie_data)
        
        elif any(word in user_input_lower for word in ['action', 'comedy', 'drama', 'sci-fi', 'romance', 'horror', 'thriller']):
            return self._get_genre_response(user_input_lower, movie_data)
        
        elif any(word in user_input_lower for word in ['details', 'info', 'about movie', 'tell me about']):
            return self._get_movie_details_response(user_input)
        
        elif any(word in user_input_lower for word in ['search', 'find movie', 'look for']):
            return self._get_movie_search_response(user_input)
        
        elif any(word in user_input_lower for word in ['analyze', 'stats', 'statistics', 'my collection', 'how many']):
            return self._get_analysis_response(movie_data)
        
        elif any(word in user_input_lower for word in ['watched', 'unwatched', 'watchlist']):
            return self._get_watch_status_response(movie_data)
        
        elif any(word in user_input_lower for word in ['help', 'what can you do', 'features']):
            return self._get_help_response()
        
        elif any(word in user_input_lower for word in ['best', 'top', 'greatest']):
            return self._get_best_movies_response(user_input_lower)
        
        else:
            return self._get_intelligent_fallback(user_input, movie_data)
    
    def _get_streaming_response(self, user_input, movie_data):
        """Handle streaming-related queries"""
        words = user_input.split()
        movie_keywords = [word for word in words if word.lower() not in 
                         ['watch', 'stream', 'where', 'to', 'on', 'netflix', 'amazon', 'prime', 'disney', 'hulu', 'hbo', 'youtube', 'crunchyroll']]
        
        if movie_keywords:
            movie_title = " ".join(movie_keywords[:4])
            
            # Check if movie is in collection
            collection_movie = None
            if movie_data:
                for movie in movie_data:
                    if movie_title.lower() in movie[1].lower():
                        collection_movie = movie
                        break
            
            if collection_movie:
                title = collection_movie[1]
                year = collection_movie[3]
                genre = collection_movie[2]
                
                watch_options = self.streaming_finder.get_watch_options(title, year, genre)
                available_streaming = [s for s in watch_options['streaming'].values() if s['available']]
                
                response = f"🎬 **{title}** ({year})\n\n"
                
                if available_streaming:
                    response += "**Available on:**\n"
                    for service in available_streaming:
                        response += f"• {service['icon']} **{service['name']}** - [Watch Now]({service['url']})\n"
                else:
                    response += "**Streaming:** Not currently available on major platforms\n"
                
                if watch_options['in_theaters']:
                    response += "\n**🎟️ In Theaters Now!**\n"
                    response += "Get tickets from:\n"
                    for service in watch_options['ticketing'].values():
                        response += f"• {service['icon']} **{service['name']}** - [Buy Tickets]({service['url']})\n"
                
                # Check for anime
                if 'anime' in watch_options:
                    response += "\n**🍥 Anime Streaming:**\n"
                    for service in watch_options['anime'].values():
                        response += f"• {service['icon']} **{service['name']}** - [Watch Anime]({service['url']})\n"
                
                response += f"\n💡 *Click the 'Watch Now' button on the movie card for more options!*"
                return response
            else:
                return f"🎬 I couldn't find '{movie_title}' in your collection. Try searching for it in the AI Finder or add it to your collection first!"
        
        return "🎬 Tell me which movie you'd like to watch! For example: 'Where can I watch Inception?' or 'Is The Dark Knight on Netflix?'"

    def _get_ticketing_response(self, user_input, movie_data):
        """Handle ticketing-related queries"""
        current_year = datetime.now().year
        in_theaters_movies = [movie for movie in movie_data if len(movie) > 3 and movie[3] >= current_year - 1]
        
        if not in_theaters_movies:
            return "🎟️ No recent movies found in your collection that might be in theaters. Recent releases from 2023-2024 are most likely to be in theaters!"
        
        response = "🎟️ **Movies That Might Be In Theaters**\n\n"
        response += "These recent movies from your collection might be in theaters:\n\n"
        
        for movie in in_theaters_movies[:5]:  # Show top 5
            title = movie[1]
            year = movie[3]
            response += f"• **{title}** ({year})\n"
            response += f"  [Get Tickets](https://www.fandango.com/search?q={quote(title)})\n\n"
        
        response += "💡 *Click 'Watch Now' on any movie card to check all ticketing options!*"
        return response

    def _get_anime_response(self, user_input, movie_data):
        """Handle anime-related queries"""
        anime_integration = AnimeIntegration()
        
        words = user_input.split()
        anime_keywords = [word for word in words if word.lower() not in ['anime', 'watch', 'find', 'search']]
        
        if anime_keywords:
            anime_query = " ".join(anime_keywords)
            anime_results = anime_integration.search_anime(anime_query)
            
            if anime_results:
                response = f"🍥 **Anime Results for '{anime_query}'**\n\n"
                for anime in anime_results[:3]:
                    response += f"• **{anime['title']}** ({anime['year']}) - {anime['genre']}\n"
                    response += f"  [Watch on Crunchyroll]({anime['url']})\n\n"
                response += "💡 *Visit the AI Finder for more anime content!*"
                return response
            else:
                return f"🍥 No anime found for '{anime_query}'. Try popular anime like 'Demon Slayer', 'Jujutsu Kaisen', or 'Attack on Titan'."
        
        return "🍥 I can help you find anime! Try asking: 'Find anime Demon Slayer' or 'Search for Jujutsu Kaisen anime'"

    def _get_greeting_response(self, movie_data):
        """Personalized greeting based on user's collection"""
        total_movies = len(movie_data) if movie_data else 0
        watched_count = sum(1 for movie in movie_data if len(movie) > 4 and movie[4] == 1) if movie_data else 0
        
        greetings = [
            f"🎬 Welcome back, cinephile! I see you have {total_movies} movies in your collection ({watched_count} watched). I can help you search for movies, get details, and recommend films!",
            f"🌟 Hello there! With {total_movies} movies in your collection, we've got quite the film festival ahead! I can search for any movie you're curious about.",
            f"👋 Hey movie lover! Your collection of {total_movies} films is impressive! I can fetch detailed info or help you discover new movies.",
            f"🎭 Greetings, film enthusiast! {total_movies} movies and counting. I'm here with movie database integration to provide detailed information and recommendations!"
        ]
        
        return random.choice(greetings)

    def _get_recommendation_response(self, user_input, movie_data):
        """Intelligent movie recommendations"""
        if not movie_data:
            return "🎬 I'd love to recommend some movies! First, let's build your collection. You can also ask me to search for any movie, or try adding a few movies you enjoy!"
        
        # Get popular movies from enhanced database
        popular_movies = [m for m in MOVIE_DATABASE if m.get('streaming_service') or m.get('in_theaters')][:6]
        
        response = "🎯 **Popular Movies You Might Like**\n\n"
        
        for i, movie in enumerate(popular_movies, 1):
            streaming_info = ""
            if movie.get('streaming_service'):
                streaming_info = f" - 📺 {movie['streaming_service']}"
            elif movie.get('in_theaters'):
                streaming_info = " - 🎟️ In Theaters"
            
            response += f"{i}. **{movie['title']}** ({movie['year']}) - {movie['genre']}{streaming_info}\n"
        
        response += "\n🔍 *Use the AI Finder to search for these movies and add them to your collection!*"
        return response

    def _get_movie_details_response(self, user_input):
        """Get movie details from OMDB API based on user query"""
        words = user_input.split()
        movie_keywords = [word for word in words if word.lower() not in ['details', 'info', 'about', 'movie', 'get', 'tell', 'me']]
        
        if movie_keywords:
            movie_title = " ".join(movie_keywords[:4])
            
            with st.spinner(f"🔍 Searching for '{movie_title}'..."):
                movie_data = self.omdb.get_movie_details(movie_title)
            
            if movie_data:
                response = f"🎬 **{movie_data.get('Title', 'Movie')}** ({movie_data.get('Year', 'N/A')})\n\n"
                response += f"**Director:** {movie_data.get('Director', 'N/A')}\n"
                response += f"**Genre:** {movie_data.get('Genre', 'N/A')}\n"
                response += f"**Runtime:** {movie_data.get('Runtime', 'N/A')}\n"
                
                # Display ratings
                ratings = movie_data.get('Ratings', [])
                imdb_rating = movie_data.get('imdbRating', 'N/A')
                
                if imdb_rating != 'N/A':
                    response += f"**IMDB Rating:** {imdb_rating}/10\n"
                
                for rating in ratings:
                    source = rating.get('Source', '')
                    value = rating.get('Value', '')
                    if 'Rotten Tomatoes' in source:
                        response += f"**Rotten Tomatoes:** {value}\n"
                    elif 'Metacritic' in source:
                        response += f"**Metacritic:** {value}\n"
                
                response += f"**Plot:** {movie_data.get('Plot', 'N/A')}\n\n"
                
                response += f"💡 *Want to add this to your collection? Use the AI Finder feature!*"
                return response
            else:
                return f"❌ I couldn't find detailed information for '{movie_title}'. Try using the AI Finder feature for better results!"
        
        return "🎬 Please specify which movie you'd like details about! For example: 'Get details about Inception' or 'Tell me about The Dark Knight'"

    def _get_movie_search_response(self, user_input):
        """Handle movie search requests"""
        return "🔍 I'd be happy to help you search for movies! Use the AI Finder section to explore the database and find new movies to add to your collection."

    def _get_analysis_response(self, movie_data):
        """Analyze user's movie preferences and provide insights"""
        if not movie_data:
            return "📊 I'd love to analyze your movie taste! Start by adding some films to your collection, or use the AI Finder to discover and add new movies!"
        
        stats = get_stats()
        
        analysis = f"🎯 **Your Cinema Profile**\n\n"
        analysis += f"• **Collection Size**: {stats['total_movies']} films\n"
        analysis += f"• **Completion Rate**: {stats['watched_count']}/{stats['total_movies']} watched ({stats['completion_rate']:.1f}%)\n"
        analysis += f"• **In Theaters**: {stats['in_theaters_count']} movies\n"
        analysis += f"• **Average Rating**: {stats['average_rating']:.1f} ⭐\n"
        
        analysis += "\n🌟 **Recommendation**: Explore the AI Finder to discover more movies!"
        
        return analysis

    def _get_watch_status_response(self, movie_data):
        """Provide information about watched and unwatched movies"""
        if not movie_data:
            return "📝 Your collection is empty. Add some movies using the AI Finder feature to start tracking your watch progress!"
        
        watched_movies = [movie for movie in movie_data if len(movie) > 4 and movie[4] == 1]
        unwatched_movies = [movie for movie in movie_data if len(movie) > 4 and movie[4] == 0]
        
        response = f"📊 **Watch Status Overview**\n\n"
        response += f"• **Watched**: {len(watched_movies)} movies\n"
        response += f"• **Unwatched**: {len(unwatched_movies)} movies\n"
        response += f"• **Completion Rate**: {len(watched_movies)/len(movie_data)*100:.1f}%\n\n"
        
        if unwatched_movies:
            response += "🎬 **Top Unwatched Movies**:\n"
            for movie in unwatched_movies[:3]:
                response += f"• {movie[1]} ({movie[3]}) - {movie[2]}\n"
        
        response += f"\n🔍 *Find more movies to watch using AI Finder!*"
        
        return response

    def _get_help_response(self):
        """Comprehensive help guide"""
        return """
🤖 **Movie Assistant with Enhanced Features**

Here's what I can help you with:

🔍 **AI Finder Movie Search & Details**
• "Search for Inception on AI Finder"
• "Get details about The Dark Knight"
• "Find information about Parasite"

🎯 **Streaming & Watching**
• "Where can I watch Oppenheimer?"
• "Is Barbie on Netflix?"
• "Get tickets for Dune 2"

🍥 **Anime Content**
• "Find anime Demon Slayer"
• "Search for Jujutsu Kaisen"
• "Watch Attack on Titan on Crunchyroll"

📊 **Collection Management**
• "Analyze my movie taste"
• "What haven't I watched?"
• "My watchlist status"

🎬 **Recommendations**
• "Recommend action movies"
• "What should I watch tonight?"
• "Popular movies on Netflix"

💡 **Pro Tips**: 
• Use AI Finder to discover new movies
• Click "Watch Now" for streaming options
• Search for anime in AI Finder

What would you like to explore today?
        """

    def _get_best_movies_response(self, user_input):
        """Recommend best movies based on categories"""
        best_movies = {
            'all_time': [
                "The Godfather (1972) - Crime epic masterpiece",
                "The Shawshank Redemption (1994) - Ultimate story of hope",
                "The Dark Knight (2008) - Superhero cinema perfected",
                "Parasite (2019) - Brilliant social thriller",
                "Pulp Fiction (1994) - Revolutionary storytelling"
            ],
            'recent': [
                "Oppenheimer (2023) - Historical drama masterpiece",
                "Spider-Man: Across the Spider-Verse (2023) - Animation revolution",
                "Dune (2021) - Epic sci-fi spectacle",
                "Everything Everywhere All At Once (2022) - Multiverse madness",
                "The Batman (2022) - Dark detective thriller"
            ]
        }
        
        if 'recent' in user_input or 'new' in user_input:
            category = 'recent'
            title = "🎬 Best Recent Movies (2020s)"
        else:
            category = 'all_time'
            title = "🏆 All-Time Greatest Movies"
        
        response = f"{title}\n\n"
        for i, movie in enumerate(best_movies[category], 1):
            response += f"{i}. {movie}\n"
        
        response += f"\n🔍 *Search AI Finder for any of these movies to get detailed information!*"
        
        return response

    def _get_intelligent_fallback(self, user_input, movie_data):
        """Intelligent fallback for unexpected queries"""
        fallbacks = [
            f"🎬 That's an interesting question! I can help you search AI Finder for movies, get detailed information, or manage your collection. What would you like to know?",
            f"🤔 I'm not sure I understand completely. I'm here to help with movie searches, recommendations, and collection management using movie database data.",
            f"🔍 I specialize in movie information from databases and collection management. Try asking me to search for a movie, get details, or recommend something to watch!",
            f"🌟 Great question! I can fetch movie details from databases, help you discover new films, or analyze your collection. What movie-related topic can I assist with?"
        ]
        
        return random.choice(fallbacks)

    def _update_user_preferences(self, user_input, movie_data):
        """Learn from user interactions"""
        # Basic preference tracking
        genre_keywords = {
            'action': ['action', 'fight', 'adventure', 'thriller', 'exciting'],
            'comedy': ['comedy', 'funny', 'laugh', 'humor', 'hilarious'],
            'drama': ['drama', 'emotional', 'serious', 'story', 'deep'],
            'sci-fi': ['sci-fi', 'science fiction', 'future', 'space', 'alien'],
            'romance': ['romance', 'love', 'relationship', 'romantic', 'couple'],
            'anime': ['anime', 'manga', 'japanese animation']
        }
        
        for genre, keywords in genre_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                if genre not in self.user_preferences["favorite_genres"]:
                    self.user_preferences["favorite_genres"].append(genre)
