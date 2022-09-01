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
        return self._dsm.get(self.BROWSE_ALBUMS_API_KEY, "list", {"offset": offset, "limit": limit})

    # Get list of all items in an album
    def get_items(self, album_id, offset=0, limit=100, additional=[]):
        res = self._dsm.get(
            self.BROWSE_ITEM_API_KEY, "list", {"album_id": album_id, "offset": offset, "limit": limit, "additional": additional}
        )
        return res

    # Search for item with keyword
    def get_search(self, keyword, offset=0, limit=100, additional=[]):
        res = self._dsm.get(
            self.SEARCH_API_KEY, "list_item",
            {"keyword": keyword, "offset": offset, "limit": limit, "additional": additional}
        )
        return res

    # Get the image
    def get_thumbnail(self, id, cache_key, size="xl"):
        res = self._dsm.get(
            self.THUMBNAIL_API_KEY, "get",
            {"id": id, "cache_key": cache_key, "size": size, "type": "unit"}
        )
        return res
