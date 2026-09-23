import unittest

from common.models import ComicInfo
from tests.common import is_valid_xml


class ComicInfoTests(unittest.TestCase):
    def test_sample_xml_isvalid(self):
        cinfo = ComicInfo()
        cinfo.series = "SeriesName"
        cinfo.writer = "WriterName"

        self.assertTrue(is_valid_xml(cinfo.to_xml()))

    def test_unicode_characters_are_sanitized(self):
        """Test that problematic Unicode characters are properly sanitized"""
        cinfo = ComicInfo()
        cinfo.series = "Tokyo Revengers"
        # Use actual problematic Unicode characters that cause issues
        cinfo.summary = "The scars of \u201cBloody Halloween,\u201d a letter from Keisuke Baji\u2014written on the day"

        xml_output = cinfo.to_xml()

        # Should not contain the Unicode replacement character
        self.assertNotIn('\ufffd', xml_output)

        # Should be valid XML
        self.assertTrue(is_valid_xml(xml_output))

        # Should contain the sanitized quotes
        self.assertIn('"Bloody Halloween,"', xml_output)
        self.assertIn('Baji-', xml_output)

    def test_various_problematic_characters(self):
        """Test various problematic Unicode characters are handled"""
        cinfo = ComicInfo()
        cinfo.series = "Test Series"
        # Test various problematic characters
        cinfo.summary = "\u2018Single quotes\u2019 \u201cdouble quotes\u201d en\u2013dash em\u2014dash ellipsis\u2026 bullet\u2022"

        xml_output = cinfo.to_xml()

        # Should not contain the Unicode replacement character
        self.assertNotIn('\ufffd', xml_output)

        # Should be valid XML
        self.assertTrue(is_valid_xml(xml_output))

        # Check replacements were made
        self.assertIn("'Single quotes'", xml_output)
        self.assertIn('"double quotes"', xml_output)
        self.assertIn("en-dash", xml_output)
        self.assertIn("em-dash", xml_output)
        self.assertIn("ellipsis...", xml_output)

    def test_cjk_and_international_characters(self):
        """Test CJK and other international characters are preserved"""
        cinfo = ComicInfo()
        # Test with Japanese, Chinese, Korean, and other characters
        cinfo.series = "東京リベンジャーズ"  # Japanese
        cinfo.localized_series = "Tokyo Revengers"
        cinfo.summary = "中文字符测试 한국어 테스트 日本語テスト Café résumé"  # Chinese, Korean, Japanese, accented
        cinfo.writer = "和久井健"  # Japanese author name

        xml_output = cinfo.to_xml()

        # Should not contain the Unicode replacement character
        self.assertNotIn('\ufffd', xml_output)

        # Should be well-formed XML (can be parsed)
        import xml.etree.ElementTree as ET
        try:
            ET.fromstring(xml_output)
            xml_is_parseable = True
        except ET.ParseError:
            xml_is_parseable = False
        self.assertTrue(xml_is_parseable, "XML should be parseable")

        # Should preserve CJK characters
        self.assertIn("東京リベンジャーズ", xml_output)
        self.assertIn("中文字符测试", xml_output)
        self.assertIn("한국어", xml_output)
        self.assertIn("日本語", xml_output)
        self.assertIn("和久井健", xml_output)
        self.assertIn("Café", xml_output)

    def test_valid_xml(self):
        TEST_COMIC_INFO_STRING = """<ComicInfo>
            <Title>Title</Title>
            <AlternateSeries>AlternateSeries</AlternateSeries>
            <Summary>Summary</Summary>
            <Notes>Notes</Notes>
            <Writer>Writer</Writer>
            <Inker>Inker</Inker>
            <Colorist>Colorist</Colorist>
            <Letterer>Letterer</Letterer>
            <CoverArtist>CoverArtist</CoverArtist>
            <Editor>Editor</Editor>
            <Translator>Translator</Translator>
            <Publisher>Publisher</Publisher>
            <Imprint>Imprint</Imprint>
            <Genre>Genre</Genre>
            <Tags>Tags</Tags>
            <Web>Web</Web>
            <Characters>Characters</Characters>
            <Teams>Teams</Teams>
            <Locations>Locations</Locations>
            <ScanInformation>ScanInformation</ScanInformation>
            <StoryArc>StoryArc</StoryArc>
            <SeriesGroup>SeriesGroup</SeriesGroup>
            <AgeRating>Unknown</AgeRating>
            <CommunityRating>3</CommunityRating>
            <Other>Other field</Other>
        </ComicInfo>
        """
        self.assertTrue(is_valid_xml(TEST_COMIC_INFO_STRING))

if __name__ == '__main__':
    unittest.main()