#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The obspy.fdsn.wadl_parser test suite.

:copyright:
    The ObsPy Development Team (devs@obspy.org)
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""
from obspy import UTCDateTime

from obspy.fdsn.wadl_parser import WADLParser
import os
import unittest
import warnings


class WADLParserTestCase(unittest.TestCase):
    """
    Test cases for obspy.fdsn.wadl_parser.WADL_Parser.
    """
    def setUp(self):
        # directory where the test files are located
        self.data_path = os.path.join(os.path.dirname(__file__), "data")

    def test_dataselect_wadl_parsing(self):
        """
        Tests the parsing of a dataselect wadl.
        """
        filename = os.path.join(self.data_path, "dataselect.wadl")
        with open(filename, "rt") as fh:
            wadl_string = fh.read()
        parser = WADLParser(wadl_string)
        params = parser.parameters

        self.assertTrue("starttime" in params)
        self.assertTrue("endtime" in params)
        self.assertTrue("network" in params)
        self.assertTrue("station" in params)
        self.assertTrue("location" in params)
        self.assertTrue("channel" in params)
        self.assertTrue("quality" in params)
        self.assertTrue("minimumlength" in params)
        self.assertTrue("quality" in params)
        self.assertTrue("longestonly" in params)

        self.assertEqual(params["starttime"]["type"], UTCDateTime)
        self.assertEqual(params["starttime"]["required"], True)

        self.assertEqual(params["endtime"]["type"], UTCDateTime)
        self.assertEqual(params["endtime"]["required"], True)

        self.assertEqual(params["network"]["type"], str)
        self.assertEqual(params["station"]["type"], str)
        self.assertEqual(params["location"]["type"], str)
        self.assertEqual(params["channel"]["type"], str)

        self.assertEqual(sorted(params["quality"]["options"]),
                         sorted(["D", "R", "Q", "M", "B"]))

        # Check that the default values did get read correctly.
        self.assertEqual(params["quality"]["default_value"], "B")
        self.assertEqual(params["minimumlength"]["default_value"], 0.0)
        self.assertEqual(params["longestonly"]["default_value"], False)

    def test_event_wadl_parsing(self):
        """
        Tests the parsing of an event wadl.
        """
        filename = os.path.join(self.data_path, "event.wadl")
        with open(filename, "rt") as fh:
            wadl_string = fh.read()
        parser = WADLParser(wadl_string)
        params = parser.parameters

        # The WADL contains some short forms. In the parameters dictionary
        # these should be converted to the long forms.
        self.assertTrue("starttime" in params)
        self.assertTrue("endtime" in params)
        self.assertTrue("minlatitude" in params)
        self.assertTrue("maxlatitude" in params)
        self.assertTrue("minlongitude" in params)
        self.assertTrue("maxlongitude" in params)
        self.assertTrue("minmagnitude" in params)
        self.assertTrue("maxmagnitude" in params)
        self.assertTrue("magnitudetype" in params)
        self.assertTrue("catalog" in params)

        self.assertTrue("contributor" in params)
        self.assertTrue("maxdepth" in params)
        self.assertTrue("mindepth" in params)
        self.assertTrue("latitude" in params)
        self.assertTrue("longitude" in params)

        self.assertTrue("maxradius" in params)
        self.assertTrue("minradius" in params)
        self.assertTrue("orderby" in params)
        self.assertTrue("updatedafter" in params)

        self.assertTrue("eventid" in params)
        self.assertTrue("originid" in params)
        self.assertTrue("includearrivals" in params)
        self.assertTrue("includeallmagnitudes" in params)
        self.assertTrue("includeallorigins" in params)
        self.assertTrue("limit" in params)
        self.assertTrue("offset" in params)
        self.assertTrue("format" in params)

        # The nodata attribute should not be parsed.
        self.assertFalse("nodata" in params)

        self.assertEqual(
            params["magnitudetype"]["doc_title"],
            "type of Magnitude used to test minimum and maximum limits "
            "(case insensitive)")
        self.assertEqual(params["magnitudetype"]["doc"],
                         "Examples: Ml,Ms,mb,Mw\"")

    def test_station_wadl_parsing(self):
        """
        Tests the parsing of a station wadl.
        """
        filename = os.path.join(self.data_path, "station.wadl")
        with open(filename, "rt") as fh:
            wadl_string = fh.read()
        parser = WADLParser(wadl_string)
        params = parser.parameters

        self.assertTrue("starttime" in params)
        self.assertTrue("endtime" in params)
        self.assertTrue("startbefore" in params)
        self.assertTrue("startafter" in params)
        self.assertTrue("endbefore" in params)
        self.assertTrue("endafter" in params)
        self.assertTrue("network" in params)
        self.assertTrue("station" in params)
        self.assertTrue("location" in params)
        self.assertTrue("channel" in params)
        self.assertTrue("minlatitude" in params)
        self.assertTrue("maxlatitude" in params)
        self.assertTrue("latitude" in params)
        self.assertTrue("minlongitude" in params)
        self.assertTrue("maxlongitude" in params)
        self.assertTrue("longitude" in params)
        self.assertTrue("minradius" in params)
        self.assertTrue("maxradius" in params)
        self.assertTrue("level" in params)
        self.assertTrue("includerestricted" in params)
        self.assertTrue("includeavailability" in params)
        self.assertTrue("updatedafter" in params)
        self.assertTrue("matchtimeseries" in params)
        self.assertTrue("format" in params)

        # The nodata attribute should not be parsed.
        self.assertFalse("nodata" in params)

        self.assertEqual(
            params["endbefore"]["doc_title"],
            "limit to stations ending before the specified time")
        self.assertEqual(
            params["endbefore"]["doc"],
            "Examples: endbefore=2012-11-29 or 2012-11-29T00:00:00 or "
            "2012-11-29T00:00:00.000")

    def test_reading_wadls_without_type(self):
        """
        Tests the reading of WADL files that have no type.
        """
        filename = os.path.join(self.data_path, "station_no_types.wadl")
        with open(filename, "rt") as fh:
            wadl_string = fh.read()
        parser = WADLParser(wadl_string)
        params = parser.parameters

        # Assert that types have been assigned.
        self.assertEqual(params["starttime"]["type"], UTCDateTime)
        self.assertEqual(params["endtime"]["type"], UTCDateTime)
        self.assertEqual(params["startbefore"]["type"], UTCDateTime)
        self.assertEqual(params["startafter"]["type"], UTCDateTime)
        self.assertEqual(params["endbefore"]["type"], UTCDateTime)
        self.assertEqual(params["endafter"]["type"], UTCDateTime)
        self.assertEqual(params["network"]["type"], str)
        self.assertEqual(params["station"]["type"], str)
        self.assertEqual(params["location"]["type"], str)
        self.assertEqual(params["channel"]["type"], str)
        self.assertEqual(params["minlatitude"]["type"], float)
        self.assertEqual(params["maxlatitude"]["type"], float)
        self.assertEqual(params["latitude"]["type"], float)
        self.assertEqual(params["minlongitude"]["type"], float)
        self.assertEqual(params["maxlongitude"]["type"], float)
        self.assertEqual(params["longitude"]["type"], float)
        self.assertEqual(params["minradius"]["type"], float)
        self.assertEqual(params["maxradius"]["type"], float)
        self.assertEqual(params["level"]["type"], str)
        self.assertEqual(params["includerestricted"]["type"], bool)
        self.assertEqual(params["includeavailability"]["type"], bool)
        self.assertEqual(params["updatedafter"]["type"], UTCDateTime)

        # Now read a dataselect file with no types.
        filename = os.path.join(self.data_path, "dataselect_no_types.wadl")
        with open(filename, "rt") as fh:
            wadl_string = fh.read()
        parser = WADLParser(wadl_string)
        params = parser.parameters

        # Assert that types have been assigned.
        self.assertEqual(params["starttime"]["type"], UTCDateTime)
        self.assertEqual(params["endtime"]["type"], UTCDateTime)
        self.assertEqual(params["network"]["type"], str)
        self.assertEqual(params["station"]["type"], str)
        self.assertEqual(params["location"]["type"], str)
        self.assertEqual(params["channel"]["type"], str)
        self.assertEqual(params["quality"]["type"], str)
        self.assertEqual(params["minimumlength"]["type"], float)
        self.assertEqual(params["longestonly"]["type"], bool)

    def test_usgs_event_wadl_parsing(self):
        """
        Tests the parsing of an event wadl.
        """
        filename = os.path.join(self.data_path, "usgs_event.wadl")
        with open(filename, "rt") as fh:
            wadl_string = fh.read()
        parser = WADLParser(wadl_string)
        params = parser.parameters

        # The WADL contains some short forms. In the parameters dictionary
        # these should be converted to the long forms.
        self.assertTrue("starttime" in params)
        self.assertTrue("endtime" in params)
        self.assertTrue("minlatitude" in params)
        self.assertTrue("maxlatitude" in params)
        self.assertTrue("minlongitude" in params)
        self.assertTrue("maxlongitude" in params)
        self.assertTrue("minmagnitude" in params)
        self.assertTrue("maxmagnitude" in params)
        self.assertTrue("magnitudetype" in params)
        self.assertTrue("catalog" in params)

        self.assertTrue("contributor" in params)
        self.assertTrue("maxdepth" in params)
        self.assertTrue("mindepth" in params)
        self.assertTrue("latitude" in params)
        self.assertTrue("longitude" in params)

        self.assertTrue("maxradius" in params)
        self.assertTrue("minradius" in params)
        self.assertTrue("orderby" in params)
        self.assertTrue("updatedafter" in params)

        self.assertTrue("eventid" in params)
        self.assertTrue("includearrivals" in params)
        self.assertTrue("includeallmagnitudes" in params)
        self.assertTrue("includeallorigins" in params)
        self.assertTrue("limit" in params)
        self.assertTrue("offset" in params)

    def test_parsing_dataselect_wadls_with_missing_attributes(self):
        """
        Some WADL file miss required attributes. In this case a warning will be
        raised.
        """
        # This dataselect WADL misses the quality, minimumlength, and
        # longestonly parameters.
        filename = os.path.join(self.data_path,
                                "dataselect_missing_attributes.wadl")
        with open(filename, "rt") as fh:
            wadl_string = fh.read()
        with warnings.catch_warnings(record=True) as w:
            parser = WADLParser(wadl_string)
            # Assert that the warning raised is correct.
            self.assertEqual(len(w), 1)
            msg = w[0].message.message
            self.assertTrue("quality" in msg)
            self.assertTrue("minimumlength" in msg)
            self.assertTrue("longestonly" in msg)

        # Assert that some other parameters are still existant.
        params = parser.parameters
        self.assertTrue("starttime" in params)
        self.assertTrue("endtime" in params)
        self.assertTrue("network" in params)
        self.assertTrue("station" in params)
        self.assertTrue("location" in params)
        self.assertTrue("channel" in params)

    def test_parsing_event_wadls_with_missing_attributes(self):
        """
        Some WADL file miss required attributes. In this case a warning will be
        raised.
        """
        # This event WADL misses the includeallorigins and the updatedafter
        # parameters.
        filename = os.path.join(self.data_path,
                                "event_missing_attributes.wadl")
        with open(filename, "rt") as fh:
            wadl_string = fh.read()
        with warnings.catch_warnings(record=True) as w:
            parser = WADLParser(wadl_string)
            # Assert that the warning raised is correct.
            self.assertEqual(len(w), 1)
            msg = w[0].message.message
            self.assertTrue("includeallorigins" in msg)
            self.assertTrue("updatedafter" in msg)

        # Assert that some other parameters are still existant.
        params = parser.parameters
        self.assertTrue("starttime" in params)
        self.assertTrue("endtime" in params)
        self.assertTrue("minlatitude" in params)
        self.assertTrue("maxlatitude" in params)
        self.assertTrue("minlongitude" in params)
        self.assertTrue("maxlongitude" in params)
        self.assertTrue("minmagnitude" in params)
        self.assertTrue("maxmagnitude" in params)
        self.assertTrue("magnitudetype" in params)
        self.assertTrue("catalog" in params)


def suite():
    return unittest.makeSuite(WADLParserTestCase, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
