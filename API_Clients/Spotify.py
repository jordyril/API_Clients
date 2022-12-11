import requests
import base64
import datetime
import os
import re

import pandas as pd

# WRITING CLASS MYSELF
# https://www.youtube.com/watch?v=xdq6Gz33khQ&list=PLEsfXFp6DpzQjDBvhNy5YbaBx9j-ZsUe6&index=20
# https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
# CLIENT CREDENTIALS FLOW

class SpotifyObject(object):
    _open_url = "https://open.spotify.com/{_type}/{id}"
    _api_url = "https://api.spotify.com/v1/{_type}s/{id}"
    _uri = "spotify:{_type}:{id}"

    id = None
    _type = None

    def __init__(self, id, _type):
        self.id = id
        self._type = _type

    def _format_type_id_string(self, string):
        return string.format(_type=self._type, id=self.id)

    @property
    def api_url(self):
        return self._format_type_id_string(self._api_url)

    @property
    def open_url(self):
        return self._format_type_id_string(self._open_url)

    @property
    def uri(self):
        return self._format_type_id_string(self._uri)


class Artist(object):
    name = None
    # tracks = []
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Artist: {self.name}"
    
    def __str__(self):
        return self.name

    def __gt__(self, right):
        return self.name > right.name

    def __lt__(self, right):
        return self.name < right.name

    def __eq__(self, right):
        return self.name == right.name


class SpotifyArtist(Artist, SpotifyObject):
    def __init__(self, name, id):
        Artist.__init__(self, name)
        SpotifyObject.__init__(self, id=id, _type="artist")

    def __eq__(self, right):
        if (self.id) and (right.id):
            return self.id == right.id
        else:
            return Artist.__eq__(self, right)


class SpotifyAlbum(SpotifyObject):
        def __init__(self, name=None, id=None, release_date=None, images=None, info_dic={}):
            self.name = info_dic.get("name") if not name else name
            self.id = info_dic.get("id") if not id else id
            self.release_date = info_dic.get("release_date") if not release_date else release_date
            self.release_date = pd.to_datetime(self.release_date)
            self.images = info_dic.get("images") if not images else images
            self.artists = info_dic.get("artists")

        @property
        def release_year(self):
            return self.release_date.year if self.release_date else None
        
        def __repr__(self) -> str:
            return f"Album: '{self.name}'"


class Track(object):
    def __init__(self, name, artists=[], release_year=None, album={}):
        self.artists = artists
        self.name = self._verify_clean_name(name)
        self.album = SpotifyAlbum(info_dic=album)
        self._release_year=release_year
        self.release_date_other_sources = {}

    def get_release_year(self):
        return self._release_year

    def set_release_year(self, value):
        self._release_year = value
    
    def del_release_year(self):
        del self._release_year
    
    release_year = property(get_release_year, set_release_year, del_release_year)

    def __repr__(self):
        return f"Track: '{self.name}' by {' & '.join([x.name for x in self.artists])}"

    def __gt__(self, right):
        return self.name > right.name

    def __lt__(self, right):
        return self.name < right.name
    
    def __eq__(self, right):
        return (self.name == right.name) and (self.artists == right.artists)

    _clean_name_list = ["remastered","Remastered", "radio edit", "Radio edit", "Radio Edit", "Single version", "Single Version","Remastered Version", "Soundtrack", "Remaster", "Version Revisited", "!", "?"]

    def _verify_clean_name(self, name):
        name = name.capitalize()
        name = re.sub("\[.*?\]", "", name).strip()
        name = re.sub(" - .*", "", name).strip()
        name = re.sub("\(feat. .*\)", "", name).strip()
        for item in self._clean_name_list:
            name = name.replace(item, "").strip()

        return name


class SpotifyTrack(Track, SpotifyObject):
    def __init__(self, name, artists=[], id=None, release_year=None, album={}):
        artists = self._verify_artists(artists)
        Track.__init__(self, name, artists, release_year=release_year, album=album)
        SpotifyObject.__init__(self,id=id, _type="track")
    
    def _verify_artists(self, artists):
        return [self._verify_artist(artist) for artist in artists]

    def _verify_artist(self, artist):
        if isinstance(artist, SpotifyArtist):
            new_artist = artist
        elif isinstance(artist, str):
            new_artist = SpotifyArtist(name=artist, id=None)
        elif isinstance(artist, dict):
            new_artist = SpotifyArtist(name=artist.get("name"), id=artist.get("id"))
        else: 
            raise Exception("Artist type is unknown")
        return new_artist

    def __eq__(self, right):
        if (self.id) and (right.id):
            return self.id == right.id
        else:
            return Track.__eq__(self, right)

class Playlist(object):
    name = None
    tracks = []
    artists = []
    release_years = []
    
    def __init__(self, name, tracks=[]):
        self.name = name
        self.tracks=tracks
        self.artists, self.release_years = self._get_info_from_tracks(tracks)
    
    def _get_info_from_tracks(self, tracks):
        artists, release_years = [], []
        for track in tracks:
            if track.release_year is not None:
                release_years.append(track.release_year)
            for artist in track.artists:
                if (artist not in artists) and (artist is not None):
                    artists.append(artist)
        return artists, release_years
    
    def renew_infos(self):
        self.artists, self.release_years = self._get_info_from_tracks(self.tracks)
    
    def __contains__(self, item):
        return item in self.tracks
    
    def __getitem__(self, key):
        return self.tracks[key]

    def __setitem__(self,track, idx=None):
        if idx:
            self.tracks[idx] = track
        else:
            self.tracks.append(track)

    def __iter__(self):
        self._i = -1
        return self
    
    def __next__(self):
        self._i += 1
        if self._i >= len(self.tracks):
            raise StopIteration
        else:
            return self.tracks[self._i]
    
    def __len__(self):
        return len(self.tracks)
    
    def add_track(self, track):
        if track not in self.tracks:
            self.__setitem__(track)



class SpotifyPlaylist(Playlist, SpotifyObject):
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    secret_id = os.getenv("SPOTIFY_CLIENT_SECRET")
    def __init__(self, name, id=None, tracks=[]):
        if (id is None) and (len(tracks) == 0):
            raise Exception("Either a spotify id or a tracklist should be provided")
        tracks = self._verify_tracks(tracks)
        Playlist.__init__(self, name, tracks)
        SpotifyObject.__init__(self,id, _type="playlist")
    
    def _verify_tracks(self, tracks):
        return [self._verify_track(track) for track in tracks]

    def _verify_track(self, track):
        if isinstance(track, SpotifyTrack):
            new_track = track
        elif isinstance(track, str):
            new_track = SpotifyTrack(name=track, artists=[], id=None)
        elif isinstance(track, dict):
            new_track = SpotifyTrack(name=track.get("name"), artists=track.get("artists"), id=track.get("id"), album=track.get("album"))
        else: 
            raise Exception("Track type is unknown")
        return new_track


    def __repr__(self):
        return f"Playlist: {self.name}"
    
    def collect_tracks_from_spotify(self):
        spotify_api = SpotifyAPI(self.client_id, self.secret_id)
        tracks = spotify_api.playlist_tracks(playlist_id=self.id)
        self.tracks= self._verify_tracks(tracks)
        self.renew_infos()

        return True

class SpotifyAPI(object):
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    secret_id = os.getenv("SPOTIFY_CLIENT_SECRET")
    token_url = "https://accounts.spotify.com/api/token"
    resource_lookup_root = "https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
    base_search_root = "https://api.spotify.com/v1/search?{query}"
    client_id = None
    secret_id = None
    access_token = None
    access_token_expires=datetime.datetime.now()


    def __init__(self, client_id, secret_id):
        self.client_id = client_id
        self.secret_id = secret_id

    @property
    def _access_token_expired(self):
        return datetime.datetime.now() > self.access_token_expires

    def _get_token_headers(self):
        return {
            "Authorization":f"Basic {self._get_client_credentials()}", 
        }
    
    def _get_token_body(self):
        return {"grant_type": "client_credentials"}

    def _get_client_credentials(self):
        client_cred = f"{self.client_id}:{self.secret_id}"
        client_cred_b64 = base64.b64encode(client_cred.encode())
        return client_cred_b64.decode()
    
    def _get_resource_headers(self):
        access_token = self.get_access_token()
        return {"Authorization": f"Bearer {access_token}"}

    def _make_get_request(self, endpoint, headers=None):
        response = requests.get(endpoint, headers=headers)
        if response.status_code not in range(200, 299):
            raise Exception("No valid request received")
        return response.json()

    def _format_search_params(self, extra_search_params):
        if extra_search_params is None:
            return ""
        if not isinstance(extra_search_params, dict):
            raise Exception("Additional parameters should be specified in a dictionary object")
        
        return "&".join([f"{key}={value}" for key, value in extra_search_params.items()])

    def authenticate(self):
        if (self.client_id is None) | (self.secret_id is None):
            raise Exception("Check your identifiers one more time, something is wrong!")
        
        headers = self._get_token_headers()
        body = self._get_token_body()
        token_url = self.token_url
        response = requests.post(url=token_url, data=body, headers=headers)
        
        if response.status_code not in range(200, 299):
            raise Exception("Client could not be authenticated")
        
        json = response.json()
        self.access_token = json["access_token"]
        self.access_token_expires = datetime.datetime.now() + datetime.timedelta(seconds=json["expires_in"])

        return True

    def get_access_token(self):
        if (self.access_token is None) | (self._access_token_expired):
            self.authenticate()
            return self.get_access_token()
        return self.access_token

    def get_resource(self, lookup_id, resource_type, version='v1', extra_search=None, extra_search_params=None):
        headers = self._get_resource_headers()
        endpoint = self.resource_lookup_root.format(version=version, resource_type=resource_type, lookup_id=lookup_id)

        if extra_search is not None:
            endpoint += f"/{extra_search}?{self._format_search_params(extra_search_params)}"

        return self._make_get_request(endpoint, headers)

    def playlist_tracks(self, playlist_id):
        resource_type = "playlists"
        extra_search = "tracks"
        _next, i = True, 0

        tracks=[]
        while _next:
            extra_search_params = {"offset":i*100, "limit":100}
            tracks_dic = SpotifyAPI(self.client_id, self.secret_id).get_resource(lookup_id=playlist_id, resource_type=resource_type, extra_search=extra_search, extra_search_params=extra_search_params)

            for item in tracks_dic["items"]:
                if not item["track"]:
                    continue
                tracks.append(item["track"])
            
            _next = True if tracks_dic["next"] else False
            i +=1
        
        return tracks


