import unittest
import api
import random

class TestData(unittest.TestCase):

#     def testVoyage1(self):
#         result = api.voyageData()
#         self.assertEqual(result['DF'][0], {
# "voyage_id": "DF0546",
# "checkedin_time": "14:00",
# "onboard_time": "14:00",
# "actual_count": 12,
# "onboard_couch": 0,
# "checkedin_couch": 12
# })

#     def testVoyage2(self):
#         result = api.voyageData()
#         self.assertEqual(result['DW'][0], {
# "voyage_id": "DW1888",
# "checkedin_time": "17:00",
# "onboard_time": "17:00",
# "actual_count": 6,
# "onboard_couch": 0,
# "checkedin_couch": 6
# })

#     def testVoyage3(self):
#         result = api.voyageData()
#         self.assertEqual(result['DM'][5], {
# "voyage_id": "DM1372",
# "checkedin_time": "08:30",
# "onboard_time": "08:30",
# "actual_count": 8,
# "onboard_couch": 0,
# "checkedin_couch": 4
# })

#     def testAvgVoyage1(self):
#         result = api.avgVoyageData()
#         self.assertEqual(result[0], {
# "voyage_id": "DM1370",
# "checkedin_time": "08:00",
# "onboard_time": "08:00",
# "actual_count": 4,
# "onboard_couch": 4,
# "checkedin_couch": 4,
# "avg_checkedin_couch": 1,
# "avg_onboard_couch": 0,
# "ship": "DM"
# })

#     def testAvgVoyage2(self):
#         result = api.avgVoyageData()
#         self.assertEqual(result[1], {
# "voyage_id": "DM1372",
# "checkedin_time": "08:00",
# "onboard_time": "08:00",
# "actual_count": 4,
# "onboard_couch": 0,
# "checkedin_couch": 4,
# "avg_checkedin_couch": 1,
# "avg_onboard_couch": 0,
# "ship": "DM"
# })

#     def testAvgVoyage3(self):
#         result = api.avgVoyageData()
#         self.assertEqual(result[9], {
# "voyage_id": "DM1370",
# "checkedin_time": "08:30",
# "onboard_time": "08:30",
# "actual_count": 4,
# "onboard_couch": 0,
# "checkedin_couch": 0,
# "avg_checkedin_couch": 0,
# "avg_onboard_couch": 0,
# "ship": "DM"
# })

#     def testOverview1(self):
#         result = list(api.voyOverview())
#         self.assertEqual(result[0]['code'], 
#  "DW")

#     def testOverview2(self):
#         result = list(api.voyOverview())
#         self.assertEqual(result[20]['code'], 
#  "DW")


    def testVoyage1(self):
        result = api.voyageData()
        self.assertEqual(list(result.keys()), ['DF', 'DM', 'DW', 'DD', 'WW'])
    
    def testVoyage2(self):
        result = api.voyageData()
        keysOfResult = list(result.keys())
        self.assertEqual(list(result[keysOfResult[0]][0].keys()), ['voyage_id', 'checkedin_time', 'onboard_time', 'actual_count', 'onboard_couch', 'checkedin_couch'])

    def testVoyage3(self):
        result = api.voyageData()
        keysOfResult = list(result.keys())
        # select random element from list of keys
        randomKey = random.choice(keysOfResult)
        self.assertEqual(list(result[randomKey][0].keys()), ['voyage_id', 'checkedin_time', 'onboard_time', 'actual_count', 'onboard_couch', 'checkedin_couch'])


    def testOverview1(self):
            result = list(api.voyOverview())
            # select random index from result
            randomIndex = random.randint(0, len(result)-1)
            self.assertEqual(list(result[randomIndex].keys()), ['voyage_id', 'added_date', 'oci_completed_core','moci_completed_core', 'checkedin_couch', 'onboard_couch', 'expected_couch', 'code', 'number' ,'end_date', 'start_date'])

    def testOverview2(self):
        result = list(api.voyOverview())
        self.assertEqual(list(result[0].keys()), ['voyage_id', 'added_date', 'oci_completed_core','moci_completed_core', 'checkedin_couch', 'onboard_couch', 'expected_couch', 'code', 'number' ,'end_date', 'start_date'])

    def testOverview3(self):
        result = list(api.voyOverview())
        self.assertEqual(list(result[10].keys()), ['voyage_id', 'added_date', 'oci_completed_core','moci_completed_core', 'checkedin_couch', 'onboard_couch', 'expected_couch', 'code', 'number' ,'end_date', 'start_date'])

if __name__ == '__main__':
    unittest.main()