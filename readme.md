# YouSync

>  API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

Design methodology:

create an api endpoint and let frontend poll it after every 10 seconds using ajax, during that time, the server will fetch the videos and store the metedata into the database and we will use the django's filtering for sortlisting