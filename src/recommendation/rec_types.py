from typing import List
from pydantic import BaseModel

class Recommendations(BaseModel):
    ...

class Item(BaseModel):
    positive: bool

class Movie(Item):
    title: str

class Song(Item):
    title: str
    artist: str

class Book(Item):
    title: str
    author: str

class MovieRecommendations(Recommendations):
    recommendations: List[Movie]

class SongRecommendations(Recommendations):
    recommendations: List[Song]

class BookRecommendations(Recommendations):
    recommendations: List[Book]

class Feature(BaseModel):
    name: str
    value: str

class FeatureRanking(BaseModel):
    ranking: List[Feature]
