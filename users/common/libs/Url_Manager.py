
class UrlManager(object):
    @staticmethod
    def buildUrl( path ):
        config_domain = "http://127.0.0.1:5000/"
        return "%s%s"%( config_domain['www'], path )

    @staticmethod
    def buildStaticUrl( path ):
        path = "/static" + path
        return UrlManager.buildUrl(path)