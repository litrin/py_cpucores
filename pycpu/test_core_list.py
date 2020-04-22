import unittest

from pycpu.cpucores import CPUcores


class TestCPUCoreList(unittest.TestCase):
    def test_range(self):
        s_core_list = "50,21,0,10-12,15,16,20-18"
        cl = CPUcores.from_desc(s_core_list)

        self.assertEqual("0,10-12,15,16,18-21,50", str(cl))

    def test_mask(self):
        s_core_list = "1,2,3,8"
        cl = CPUcores.from_desc(s_core_list)
        self.assertEqual(str(cl), "1-3,8")

    def test_list(self):
        s_core_list = 0x70F
        cl = CPUcores(s_core_list)
        self.assertEqual(cl.all_cores(), "0,1,2,3,8,9,10")
        self.assertEqual(str(cl), "0-3,8-10")

    def test_iter(self):
        cl = CPUcores(0xFFFFFFF)
        for i, c in enumerate(cl):
            self.assertEqual(i, c)

    def test_str_input(self):
        cl = CPUcores.from_desc("11")
        self.assertEqual(str(cl), "11")
        cl = CPUcores.from_desc("12,11")
        self.assertEqual(cl.all_cores(), "11,12")

    def test_mask_to_list(self):
        self.assertEqual(str(CPUcores(0xFFFF00)), "8-23")
        self.assertEqual(str(CPUcores(0x100)), "8")


if __name__ == '__main__':
    unittest.main()
