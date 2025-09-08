from unittest import TestCase


class LoopTestCase(TestCase):
    def test_loop(self):
        for i in [0, 2, 4]:
            # for i in range(5):
            with self.subTest("Тест на четность", i=i):
                self.assertEqual(i % 2, 0)
