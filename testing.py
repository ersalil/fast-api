# import unittest
# import main

# class TestData(unittest.TestCase):
#     def test_data(self):
#         result = main.tableView()
#         self.assertEqual(result, [
# {
# "voyage_id": "2bbacf5a-ea8c-44a1-9520-61538e96dac7",
# "added_date": "2022-07-18 23:51:11.152969+00:00",
# "oci_completed_core": 1838,
# "moci_completed_core": 1812,
# "checkedin_couch": 1894,
# "onboard_couch": 1894,
# "number": "DW1891",
# "expected_couch": 1894,
# "code": "DW",
# "end_date": "2022-07-18 18:01:15",
# "start_date": "2022-07-18 17:26:12"
# },
# {
# "voyage_id": "2a6cc378-1b83-4a67-aac3-246dcd7190b2",
# "added_date": "2022-07-18 23:21:16.973035+00:00",
# "oci_completed_core": 2447,
# "moci_completed_core": 2392,
# "checkedin_couch": 2561,
# "onboard_couch": 2561,
# "number": "DD1181",
# "expected_couch": 2561,
# "code": "DD",
# "end_date": "2022-07-18 15:51:17",
# "start_date": "2022-07-18 14:47:14"
# },
# {
# "voyage_id": "a661fbd3-9353-4308-9764-1600bcc476f3",
# "added_date": "2022-07-18 23:07:31.201988+00:00",
# "oci_completed_core": 1413,
# "moci_completed_core": 1405,
# "checkedin_couch": 1561,
# "onboard_couch": 1561,
# "number": "DM1375",
# "expected_couch": 1561,
# "code": "DM",
# "end_date": "2022-07-18 09:05:18",
# "start_date": "2022-07-18 08:58:15"
# },
# {
# "voyage_id": "f2d36022-5fc5-41fe-8169-c630f7c38f3a",
# "added_date": "2022-07-16 23:21:18.343009+00:00",
# "oci_completed_core": 3297,
# "moci_completed_core": 3269,
# "checkedin_couch": 3386,
# "onboard_couch": 3386,
# "number": "DF0552",
# "expected_couch": 3386,
# "code": "DF",
# "end_date": "2022-07-16 15:11:15",
# "start_date": "2022-07-16 14:37:16"
# },
# {
# "voyage_id": "9ff1629b-515a-4e9d-8508-0479af92fde0",
# "added_date": "2022-07-14 23:50:30.623831+00:00",
# "oci_completed_core": 2702,
# "moci_completed_core": 2700,
# "checkedin_couch": 2752,
# "onboard_couch": 2752,
# "number": "WW0162",
# "expected_couch": 2752,
# "code": "WW",
# "end_date": "2022-07-14 14:30:09",
# "start_date": "2022-07-14 14:21:38"
# },
# {
# "voyage_id": "c075fa3c-574c-472d-b25e-e6ab687a049b",
# "added_date": "2022-07-14 21:37:09.935208+00:00",
# "oci_completed_core": 2756,
# "moci_completed_core": 2749,
# "checkedin_couch": 2996,
# "onboard_couch": 2996,
# "number": "DD1180",
# "expected_couch": 2999,
# "code": "DD",
# "end_date": "2022-07-14 15:49:08",
# "start_date": "2022-07-14 14:43:20"
# },
# {
# "voyage_id": "3b0ee011-3ec5-4f80-bc6d-b28faf47d835",
# "added_date": "2022-07-11 23:49:14.438877+00:00",
# "oci_completed_core": 1769,
# "moci_completed_core": 1763,
# "checkedin_couch": 1813,
# "onboard_couch": 1806,
# "number": "DW1890",
# "expected_couch": 1818,
# "code": "DW",
# "end_date": "2022-07-11 18:33:09",
# "start_date": "2022-07-11 18:12:30"
# },
# {
# "voyage_id": "92a1a960-e641-4c59-b5eb-6a84088d3934",
# "added_date": "2022-07-10 23:00:47.391833+00:00",
# "oci_completed_core": 1876,
# "moci_completed_core": 1859,
# "checkedin_couch": 2289,
# "onboard_couch": 2289,
# "number": "WW0193",
# "expected_couch": 2289,
# "code": "WW",
# "end_date": "2022-07-10 14:39:09",
# "start_date": "2022-07-10 12:49:26"
# },
# {
# "voyage_id": "afdc67d8-abce-4089-8d26-3a43e75fff3f",
# "added_date": "2022-07-09 23:20:27.777601+00:00",
# "oci_completed_core": 3266,
# "moci_completed_core": 3260,
# "checkedin_couch": 3346,
# "onboard_couch": 3346,
# "number": "DF0551",
# "expected_couch": 3346,
# "code": "DF",
# "end_date": "2022-07-09 16:02:12",
# "start_date": "2022-07-09 14:50:09"
# },
# {
# "voyage_id": "593c69bb-712a-4ca4-bb48-6c74fad21536",
# "added_date": "2022-07-09 23:00:43.669871+00:00",
# "oci_completed_core": 2741,
# "moci_completed_core": 2725,
# "checkedin_couch": 2900,
# "onboard_couch": 2900,
# "number": "DD1179",
# "expected_couch": 2900,
# "code": "DD",
# "end_date": "2022-07-09 15:13:11",
# "start_date": "2022-07-09 14:38:13"
# },
# {
# "voyage_id": "e80ad647-b918-493e-854c-8c21c5615326",
# "added_date": "2022-07-06 23:12:20.569281+00:00",
# "oci_completed_core": 1803,
# "moci_completed_core": 1800,
# "checkedin_couch": 1876,
# "onboard_couch": 1876,
# "number": "DM1374",
# "expected_couch": 1876,
# "code": "DM",
# "end_date": "2022-07-06 09:13:05",
# "start_date": "2022-07-06 09:05:28"
# },
# {
# "voyage_id": "f766fedd-9eac-42be-a25d-068090bc3597",
# "added_date": "2022-07-04 23:32:36.704989+00:00",
# "oci_completed_core": 2504,
# "moci_completed_core": 2482,
# "checkedin_couch": 2608,
# "onboard_couch": 2608,
# "number": "DD1178",
# "expected_couch": 2608,
# "code": "DD",
# "end_date": "2022-07-04 15:42:10",
# "start_date": "2022-07-04 15:10:12"
# },
# {
# "voyage_id": "6dd11e2f-6f43-4745-ae8d-9a3b3c750ab5",
# "added_date": "2022-07-04 23:11:26.986616+00:00",
# "oci_completed_core": 1707,
# "moci_completed_core": 1693,
# "checkedin_couch": 1772,
# "onboard_couch": 1772,
# "number": "DW1889",
# "expected_couch": 1772,
# "code": "DW",
# "end_date": "2022-07-04 17:58:33",
# "start_date": "2022-07-04 17:23:15"
# },
# {
# "voyage_id": "e5b55824-6ae6-490f-98f2-61188357b8ac",
# "added_date": "2022-07-02 23:53:16.161207+00:00",
# "oci_completed_core": 3251,
# "moci_completed_core": 3250,
# "checkedin_couch": 3344,
# "onboard_couch": 3344,
# "number": "DF0550",
# "expected_couch": 3344,
# "code": "DF",
# "end_date": "2022-07-02 15:46:21",
# "start_date": "2022-07-02 15:02:11"
# },
# {
# "voyage_id": "0123b608-fa20-4ea5-8c97-6cd664039b50",
# "added_date": "2022-06-30 23:25:19.033447+00:00",
# "oci_completed_core": 2896,
# "moci_completed_core": 2876,
# "checkedin_couch": 3077,
# "onboard_couch": 3077,
# "number": "DD1177",
# "expected_couch": 3077,
# "code": "DD",
# "end_date": "2022-06-30 15:11:18",
# "start_date": "2022-06-30 14:34:38"
# },
# {
# "voyage_id": "374b4aa4-582a-4f47-85f2-3a66ef441452",
# "added_date": "2022-06-27 23:51:33.385526+00:00",
# "oci_completed_core": 1787,
# "moci_completed_core": 1769,
# "checkedin_couch": 1868,
# "onboard_couch": 1868,
# "number": "DW1888",
# "expected_couch": 1869,
# "code": "DW",
# "end_date": "2022-06-27 18:03:32",
# "start_date": "2022-06-27 17:26:31"
# },
# {
# "voyage_id": "5f24bdee-25eb-4e71-80b8-338b5ffc16de",
# "added_date": "2022-06-27 23:46:42.604009+00:00",
# "oci_completed_core": 1771,
# "moci_completed_core": 1758,
# "checkedin_couch": 1840,
# "onboard_couch": 1840,
# "number": "DM1373",
# "expected_couch": 1841,
# "code": "DM",
# "end_date": "2022-06-27 09:20:21",
# "start_date": "2022-06-27 08:32:28"
# },
# {
# "voyage_id": "871a3d1a-ae68-430b-b96d-86abe21a4c11",
# "added_date": "2022-06-25 23:51:21.052881+00:00",
# "oci_completed_core": 3191,
# "moci_completed_core": 3177,
# "checkedin_couch": 3272,
# "onboard_couch": 3272,
# "number": "DF0549",
# "expected_couch": 3280,
# "code": "DF",
# "end_date": "2022-06-25 15:09:10",
# "start_date": "2022-06-25 14:25:57"
# },
# {
# "voyage_id": "6dfd330b-3e64-4164-b552-501c8bdf4091",
# "added_date": "2022-06-25 23:46:43.890735+00:00",
# "oci_completed_core": 2399,
# "moci_completed_core": 2383,
# "checkedin_couch": 2494,
# "onboard_couch": 2494,
# "number": "DD1176",
# "expected_couch": 2500,
# "code": "DD",
# "end_date": "2022-06-25 14:58:23",
# "start_date": "2022-06-25 14:35:40"
# },
# {
# "voyage_id": "b351ebcb-c1c9-47d4-b19e-4b665553ca78",
# "added_date": "2022-06-20 23:37:29.775050+00:00",
# "oci_completed_core": 1780,
# "moci_completed_core": 1764,
# "checkedin_couch": 1885,
# "onboard_couch": 1885,
# "number": "DW1887",
# "expected_couch": 1885,
# "code": "DW",
# "end_date": "2022-06-20 18:01:17",
# "start_date": "2022-06-20 17:31:41"
# },
# {
# "voyage_id": "1915979e-e6c2-458c-b72f-cf8ba1572db4",
# "added_date": "2022-06-18 23:45:16.211931+00:00",
# "oci_completed_core": 3284,
# "moci_completed_core": 3280,
# "checkedin_couch": 3385,
# "onboard_couch": 3385,
# "number": "DF0548",
# "expected_couch": 3385,
# "code": "DF",
# "end_date": "2022-06-18 15:07:28",
# "start_date": "2022-06-18 14:32:09"
# },
# {
# "voyage_id": "a132f51e-facd-459c-9a5e-9a65e3e8a4db",
# "added_date": "2022-06-18 23:26:37.276677+00:00",
# "oci_completed_core": 1565,
# "moci_completed_core": 1563,
# "checkedin_couch": 1657,
# "onboard_couch": 1657,
# "number": "DM1372",
# "expected_couch": 1659,
# "code": "DM",
# "end_date": "2022-06-18 09:00:19",
# "start_date": "2022-06-18 08:25:25"
# },
# {
# "voyage_id": "c29b4d24-7638-4a0d-a788-14bb0e5ee4a2",
# "added_date": "2022-06-13 23:32:57.257709+00:00",
# "oci_completed_core": 1764,
# "moci_completed_core": 1763,
# "checkedin_couch": 1807,
# "onboard_couch": 1805,
# "number": "DW1886",
# "expected_couch": 1807,
# "code": "DW",
# "end_date": "2022-06-13 18:00:38",
# "start_date": "2022-06-13 17:35:19"
# },
# {
# "voyage_id": "fc57f7da-f406-4e72-b5de-b7370909c942",
# "added_date": "2022-06-11 23:29:07.659402+00:00",
# "oci_completed_core": 3092,
# "moci_completed_core": 3090,
# "checkedin_couch": 3188,
# "onboard_couch": 3188,
# "number": "DF0547",
# "expected_couch": 3188,
# "code": "DF",
# "end_date": "2022-06-11 15:07:14",
# "start_date": "2022-06-11 14:35:35"
# },
# {
# "voyage_id": "a0ec8faf-7a9b-4579-bdd7-91b4fffc1a67",
# "added_date": "2022-06-10 23:54:00.663714+00:00",
# "oci_completed_core": 1619,
# "moci_completed_core": 1612,
# "checkedin_couch": 1725,
# "onboard_couch": 1725,
# "number": "DM1371",
# "expected_couch": 1728,
# "code": "DM",
# "end_date": "2022-06-10 09:06:58",
# "start_date": "2022-06-10 08:50:12"
# },
# {
# "voyage_id": "336dd004-2962-4309-847e-52be335eb56e",
# "added_date": "2022-06-06 23:55:51.880105+00:00",
# "oci_completed_core": 1728,
# "moci_completed_core": 1718,
# "checkedin_couch": 1793,
# "onboard_couch": 1785,
# "number": "DW1885",
# "expected_couch": 1793,
# "code": "DW",
# "end_date": "2022-06-06 18:40:09",
# "start_date": "2022-06-06 18:40:09"
# },
# {
# "voyage_id": "23dc7624-44b6-4336-9d09-84a2ee14068f",
# "added_date": "2022-06-04 23:56:08.033594+00:00",
# "oci_completed_core": 2951,
# "moci_completed_core": 2926,
# "checkedin_couch": 3032,
# "onboard_couch": 3032,
# "number": "DF0546",
# "expected_couch": 3032,
# "code": "DF",
# "end_date": "2022-06-04 15:25:37",
# "start_date": "2022-06-04 14:18:31"
# },
# {
# "voyage_id": "eb0c262f-1a0c-4f4f-955f-ec40c046d3cd",
# "added_date": "2022-06-04 23:10:25.688690+00:00",
# "oci_completed_core": 1208,
# "moci_completed_core": 1199,
# "checkedin_couch": 1288,
# "onboard_couch": 1288,
# "number": "DM1370",
# "expected_couch": 1294,
# "code": "DM",
# "end_date": "2022-06-04 09:03:35",
# "start_date": "2022-06-04 08:35:44"
# },
# {
# "voyage_id": "28b7327b-5671-400e-8ca1-e78220bc4f57",
# "added_date": "2022-05-28 23:40:20.518101+00:00",
# "oci_completed_core": 1228,
# "moci_completed_core": 1219,
# "checkedin_couch": 1310,
# "onboard_couch": 1310,
# "number": "DM1369",
# "expected_couch": 1314,
# "code": "DM",
# "end_date": "2022-05-28 09:21:39",
# "start_date": "2022-05-28 09:07:33"
# },
# {
# "voyage_id": "c7506966-e472-4193-9475-f796a36eca5b",
# "added_date": "2022-05-21 23:47:59.995394+00:00",
# "oci_completed_core": 1185,
# "moci_completed_core": 1178,
# "checkedin_couch": 1300,
# "onboard_couch": 1300,
# "number": "DM1368",
# "expected_couch": 1310,
# "code": "DM",
# "end_date": "2022-05-21 10:02:27",
# "start_date": "2022-05-21 10:02:27"
# }
# ])

#     def test_line(self):
#         result = main.lineGraph()
#         print("LINE GRAPHHHHHHHHHHHHHHHHHHHH")
#         self.assertEqual(result['DF'][0], {
# "voyage_id": "DF0546",
# "checkedin_time": "14:00",
# "onboard_time": "14:00",
# "actual_count": 12,
# "onboard_couch": 0,
# "checkedin_couch": 12
# })

#     def test_line_2(self):
#         result = main.lineGraph()
#         print("LINE GRAPHHHHHHHHHHHHHHHHHHHH")
#         self.assertEqual(result['DW'][0], {
# "voyage_id": "DW1888",
# "checkedin_time": "17:00",
# "onboard_time": "17:00",
# "actual_count": 6,
# "onboard_couch": 0,
# "checkedin_couch": 6
# })
    
# "voyage_id": "DF0546",
# "checkedin_time": "14:00",
# "onboard_time": "14:00",
# "actual_count": 12,
# "onboard_couch": 0,
# "checkedin_couch": 12
# })

# if __name__ == '__main__':
#     unittest.main()