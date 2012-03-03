import pluginInterface

class staticPlugin(pluginInterface.pluginInterface):

    def getAlbums(self):
        return [{"id" : 1, "title": "Jorge Miloslavsky"}]

    def getSongsInfo(self, albumId):
        if not albumId:
            return [{"id":60830458,"artist":"Unknown","title":"Bosco"},{"id": 59317035,"artist":"Mestre Barrao","title":"Sinhazinha"}]
        else:
            return [{"id":60830458,"artist":"Unknown","title":"Bosco"}]

    def getSong(self, audioId):
        return [{"id":audioId,"length":4,"data":"\0\1\2\3"}]