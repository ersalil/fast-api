import unittest
import api
import random
import db.crud as crud

class TestData(unittest.TestCase):

    def testVoyage1(self):
        result = crud.getShip()
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