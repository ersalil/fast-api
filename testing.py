import unittest
import api

class TestData(unittest.TestCase):

    def test_voyage(self):
        result = api.voyageData()
        self.assertEqual(result['DF'][0], {
"voyage_id": "DF0546",
"checkedin_time": "14:00",
"onboard_time": "14:00",
"actual_count": 12,
"onboard_couch": 0,
"checkedin_couch": 12
})

    def test_voyage_2(self):
        result = api.voyageData()
        self.assertEqual(result['DW'][0], {
"voyage_id": "DW1888",
"checkedin_time": "17:00",
"onboard_time": "17:00",
"actual_count": 6,
"onboard_couch": 0,
"checkedin_couch": 6
})

    def test_voyage_3(self):
        result = api.voyageData()
        self.assertEqual(result['DM'][5], {
"voyage_id": "DM1372",
"checkedin_time": "08:30",
"onboard_time": "08:30",
"actual_count": 8,
"onboard_couch": 0,
"checkedin_couch": 4
})

    def test_avg_voyage(self):
        result = api.avgVoyageData()
        self.assertEqual(result[0], {
"voyage_id": "DM1370",
"checkedin_time": "08:00",
"onboard_time": "08:00",
"actual_count": 4,
"onboard_couch": 4,
"checkedin_couch": 4,
"avg_checkedin_couch": 1,
"avg_onboard_couch": 0,
"ship": "DM"
})

    def test_avg_voyage_2(self):
        result = api.avgVoyageData()
        self.assertEqual(result[1], {
"voyage_id": "DM1372",
"checkedin_time": "08:00",
"onboard_time": "08:00",
"actual_count": 4,
"onboard_couch": 0,
"checkedin_couch": 4,
"avg_checkedin_couch": 1,
"avg_onboard_couch": 0,
"ship": "DM"
})

    def test_avg_voyage_3(self):
        result = api.avgVoyageData()
        self.assertEqual(result[9], {
"voyage_id": "DM1370",
"checkedin_time": "08:30",
"onboard_time": "08:30",
"actual_count": 4,
"onboard_couch": 0,
"checkedin_couch": 0,
"avg_checkedin_couch": 0,
"avg_onboard_couch": 0,
"ship": "DM"
})

#     def test_overview(self):
#         result = api.voyOverview()
#         print("<<<<<<<<<<<<<<<<<<", type(result), ">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#         self.assertEqual(result[0], {
# "voyage_id": "2bbacf5a-ea8c-44a1-9520-61538e96dac7",
# "added_date": "2022-07-18T23:51:11.152969+00:00",
# "oci_completed_core": 1838,
# "moci_completed_core": 1812,
# "checkedin_couch": 1894,
# "onboard_couch": 1894,
# "expected_couch": 1894,
# "code": "DW",
# "number": "DW1891",
# "end_date": "2022-07-18 18:01:15",
# "start_date": "2022-07-18 17:26:12"
# })
if __name__ == '__main__':
    unittest.main()