"""Synology Photos API wrapper."""


class SynoPhotos:
    """An implementation of a Synology Photos."""

    API_KEY = "SYNO.Foto.*"
    BROWSE_ITEM_API_KEY = "SYNO.Foto.Browse.Item"
    BROWSE_ALBUMS_API_KEY = "SYNO.Foto.Browse.Album"
    SEARCH_API_KEY = "SYNO.Foto.Search.Search"
    THUMBNAIL_API_KEY = "SYNO.Foto.Thumbnail"

    def __init__(self, dsm):
        """Initialize a Photos."""
        self._dsm = dsm

    # Get list of all albums
    def get_albums(self, offset=0, limit=100):
        res = self._dsm.get(
            self.BROWSE_ALBUMS_API_KEY, "list", {"offset": offset, "limit": limit}
        )
        return res["data"]["list"]

    # Get list of all items in an album
    def get_items(self, album_id, offset=0, limit=100, additional=[]):
        res = self._dsm.get(
            self.BROWSE_ITEM_API_KEY, "list", {"album_id": album_id, "offset": offset, "limit": limit, "additional": additional}
        )
        return res["data"]["list"]

    # Search for item with keyword
    def get_search(self, keyword, offset=0, limit=100, additional=[]):
        res = self._dsm.get(
            self.SEARCH_API_KEY, "list_item",
            {"keyword": keyword, "offset": offset, "limit": limit, "additional": additional}
        )
        return res["data"]["list"]

    # Get the image
    def get_thumbnail(self, id, cache_key, size="xl"):
        res = self._dsm.get(
            self.THUMBNAIL_API_KEY, "get",
            {"id": id, "cache_key": cache_key, "size": size, "type": "unit"}
        )
        return res

    # Get the url to request the thumbnail
    def get_thumbnail_url(self, id, cache_key, size="xl"):
        res = self._dsm.get_url(
            self.THUMBNAIL_API_KEY, "get",
            {"id": id, "cache_key": cache_key, "size": size, "type": "unit"}
        )
        return res
