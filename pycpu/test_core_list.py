import unittest
from pycpu.cpucores import CoreList


class TestCPUCoreList(unittest.TestCase):
    def test_range(self):
        s_core_list = "50,21,0,10-12,15,16,20-18"
        cl = CoreList(s_core_list)
        self.assertEqual("0,10-12,15-16,18-21,50", cl.core_range)

    def test_mask(self):
        s_core_list = "1,2,3,8"
        cl = CoreList(s_core_list)
        self.assertEqual(cl.core_mask, 0x10E)
        self.assertEqual(str(cl), "1-3,8")

    def test_list(self):
        s_core_list = 0x70F
        cl = CoreList(s_core_list)
        self.assertEqual(cl.core_list, "0,1,2,3,8,9,10")
        self.assertEqual(cl.core_range, "0-3,8-10")

    def test_iter(self):
        cl = CoreList(0xFFFFFFF)
        for i, c in enumerate(cl):
            self.assertEqual(i, c)

    def test_str_input(self):
        cl = CoreList("11")
        self.assertEqual(cl.core_list, "11")

        cl = CoreList("12,11")
        self.assertEqual(cl.core_list, "11,12")


if __name__ == '__main__':
    unittest.main()
