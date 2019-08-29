import unittest
from pycpu.cpuinfo import CPUInfoLinux


class TestCPUInfoLinux(unittest.TestCase):
    def test_something(self):
        c = CPUInfoLinux("unittest_data/linux_cpuinfo.txt")

        self.assertEqual(c.nodes, 1)
        self.assertEqual(c.sockets, 1)

        self.assertEqual(c.cores, 4)
        self.assertEqual(c.cpus, 8)

        self.assertEqual(c.freq, 1046)
        self.assertEqual(c.freq_range[0], 800)
        self.assertEqual(c.freq_range[1], 4000)

        self.assertTrue(c.has_feature("avx2"))
        self.assertFalse(c.has_feature("avx512"))



if __name__ == '__main__':
    unittest.main()
