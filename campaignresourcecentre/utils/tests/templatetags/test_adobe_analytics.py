from django.test import SimpleTestCase

from campaignresourcecentre.utils.templatetags import adobe_analytics


def create_categories(primary, one, two, three, four):
    return (
        """{"primaryCategory": "%s", "subCategory1": "%s", "subCategory2": "%s", "subCategory3": "%s", "subCategory4": "%s"}"""
        % (
            primary,
            one,
            two,
            three,
            four,
        )
    )


class AdobeAnalyticsTestCase(SimpleTestCase):
    """
    Test adobe_analytics templatetags
    """

    maxDiff = None

    digital_data = """window.digitalData= {"page": {"pageInfo": {"pageName": "%s"}, "category": %s}};"""

    def test_adobe_analytics_returns_output_for_page_with_no_path_segment(self):
        """
        Return fully formed digitalData object when path contains no segments
        """

        path = ""
        categories = create_categories(path, "", "", "", "")
        expected = self.digital_data % ("nhs:phe:campaigns:home", categories)

        output = adobe_analytics.adobe_analytics(path)

        self.assertHTMLEqual(output, expected)

    def test_adobe_analytics_returns_output_for_page_with_one_path_segment(self):
        """
        Return fully formed digitalData object when path contains one segment
        """

        path = "conditions"
        categories = create_categories(path, "", "", "", "")
        expected = self.digital_data % ("nhs:phe:campaigns:%s" % path, categories)

        output = adobe_analytics.adobe_analytics(path)

        self.assertHTMLEqual(output, expected)

    def test_adobe_analytics_returns_output_for_page_with_two_path_segments(self):
        """
        Return fully formed digitalData object when path contains two segments
        """

        path = "conditions/treatments"
        path_segments = path.split("/")
        categories = create_categories(path_segments[0], path_segments[1], "", "", "")
        expected = self.digital_data % (
            "nhs:phe:campaigns:%s" % ":".join(path_segments),
            categories,
        )

        output = adobe_analytics.adobe_analytics(path)

        self.assertHTMLEqual(output, expected)

    def test_adobe_analytics_returns_output_for_page_with_three_path_segments(self):
        """
        Return fully formed digitalData object when path contains three segments
        """

        path = "conditions/treatments/symptoms"
        path_segments = path.split("/")
        categories = create_categories(
            path_segments[0], path_segments[1], path_segments[2], "", ""
        )
        expected = self.digital_data % (
            "nhs:phe:campaigns:%s" % ":".join(path_segments),
            categories,
        )

        output = adobe_analytics.adobe_analytics(path)

        self.assertHTMLEqual(output, expected)

    def test_adobe_analytics_returns_output_for_page_with_four_path_segments(self):
        """
        Return fully formed digitalData object when path contains four segments
        """

        path = "conditions/treatments/symptoms/medicines"
        path_segments = path.split("/")
        categories = create_categories(
            path_segments[0], path_segments[1], path_segments[2], path_segments[3], ""
        )
        expected = self.digital_data % (
            "nhs:phe:campaigns:%s" % ":".join(path_segments),
            categories,
        )

        output = adobe_analytics.adobe_analytics(path)

        self.assertHTMLEqual(output, expected)

    def test_adobe_analytics_returns_output_for_page_with_more_than_four_path_segments(
        self,
    ):
        """
        Return fully formed digitalData object when path contains more than four segments
        """

        path = "conditions/treatments/symptoms/medicines/more/stuff"
        path_segments = path.split("/")
        categories = create_categories(
            path_segments[0],
            path_segments[1],
            path_segments[2],
            path_segments[3],
            path_segments[4],
        )
        expected = self.digital_data % (
            "nhs:phe:campaigns:%s" % ":".join(path_segments),
            categories,
        )

        output = adobe_analytics.adobe_analytics(path)

        self.assertHTMLEqual(output, expected)

    def test_adobe_analytics_returns_escaped_charaters_in_path_segments(
        self,
    ):
        """
        Return fully formed digitalData object when path contains characters that need escaping
        """

        path = 'conditions"/treatments"/symptoms"/medicines"/more"/stuff"'
        categories = create_categories(
            'conditions\\"', 'treatments\\"', 'symptoms\\"', 'medicines\\"', 'more\\"'
        )
        expected = self.digital_data % (
            'nhs:phe:campaigns:conditions\\":treatments\\":symptoms\\":medicines\\":more\\":stuff\\"',
            categories,
        )

        output = adobe_analytics.adobe_analytics(path)

        self.assertHTMLEqual(output, expected)
