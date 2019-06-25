# -*- coding: utf-8 -*-

import unittest
import sys
from main import main

class TestMain(unittest.TestCase):
    
    def setUp(self):
        self.query = myQuery()
    
    def test_string(self):
        string = 'select * from imoveis'
        valor = self.query.get(string)
        self.assertEqual(valor,string)
    
if __name__ == '__main__':
    unittest.main()