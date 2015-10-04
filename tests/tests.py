import unittest 
import os, sys

sys.path.insert( 0, os.path.realpath("..") )
import utils


class TestUtils( unittest.TestCase ):

    def test_boolean(self):
        self.assertTrue( utils.parse_boolean("yes") )
        self.assertTrue( utils.parse_boolean("Yes") )
        self.assertTrue( utils.parse_boolean("True") )
        self.assertTrue( utils.parse_boolean("true") )
        self.assertTrue( utils.parse_boolean(1) )
        self.assertTrue( utils.parse_boolean("1") )
        self.assertTrue( utils.parse_boolean(True) )

        self.assertFalse( utils.parse_boolean("no") )
        self.assertFalse( utils.parse_boolean("No") )
        self.assertFalse( utils.parse_boolean("False") )
        self.assertFalse( utils.parse_boolean("false") )
        self.assertFalse( utils.parse_boolean(0) )
        self.assertFalse( utils.parse_boolean("0") )
        self.assertFalse( utils.parse_boolean(False) )
        self.assertFalse( utils.parse_boolean() )
        self.assertFalse( utils.parse_boolean(None) )


    def test_chunk(self):
        chunk_length = 140
        t = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras imperdiet nec erat ac condimentum. Nulla vel rutrum ligula. Sed hendrerit interdum orci a posuere. Vivamus ut velit aliquet, mollis purus eget, iaculis nisl. Proin posuere malesuada ante. Proin auctor orci eros, ac molestie lorem dictum nec. Vestibulum sit amet erat est. Morbi luctus sed elit ac luctus. Proin blandit, enim vitae egestas posuere, neque elit ultricies dui, vel mattis nibh enim ac lorem. Maecenas molestie nisl sit amet velit dictum lobortis. Aliquam erat volutpat."
        chunks = utils.chunk_string( t, chunk_length )
        self.assertIsNotNone( chunks )
        l = len(chunks)
        self.assertGreaterEqual( l, l/chunk_length )

if __name__ == '__main__':
    unittest.main()