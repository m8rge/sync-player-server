class pluginInterface:

    def getAlbums(self):
        raise NotImplementedError

    def getSongsInfo(self, albumId):
        raise NotImplementedError

    def getSong(self, audioId):
        raise NotImplementedError