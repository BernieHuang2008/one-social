# one-social
manage all social medias in **ONE** place.

# requirements
- requests

# supported social medias:
|Name|script|document|
|:-:|:-:|:-:|
|instagram|ins.py|https://developers.facebook.com/docs/instagram-api/guides/content-publishing/ / https://blog.csdn.net/qq_23853743/article/details/102481729|
|FaceBook|fb.py|https://developers.facebook.com/docs/graph-api/get-started|
|X|x.py|https://developer.twitter.com/en/docs/twitter-api|
|Youtube|youtube.py|https://developers.google.com/youtube/v3/docs/|


# Contribution Guide
## New Social Media Support:
1. should provide apis below:

|Name|function|parameters|output|desc|
|-|-|-|-|-|
|set token|`set_token`|`token:str`|None|set the access token **ONLY** in this session|

