"""Twitch Extractor
Decision: Twitch has some limitiations it does not use the same Google API format and cannot be built like the Youtube ONE.
There is 
"""
# 1. Authenticate client by creating HTTP requests structured this way:
# header(s) : Client ID and Authorization key# payload: the intention
# 2. Two auth flows: one for client credentials and user Oauth token flow for private account data like subscriber count, bits, revenue-related figures
# 3. Twitch video endpoints come bundled with the view count so there's no need to make videos id list and batch fetch the stats.
# 4. Twitch has no public like and comments system. # Views are this platforms commodity