from retriever import Retriever

class TestRetriever(object):
    def est_retrieve_app_aws(self):
        r = Retriever('APP','app-aws')
        assert r.get_latest_pkg_name()
        assert r.get_latest_pkg_date()
        r.download_latest_pkg()

    def test_retrieve_ta_aws(self):
        r = Retriever('TA','ta-aws')
        assert r.get_latest_pkg_name()
        assert r.get_latest_pkg_date()
        r.download_latest_pkg()

