from os import path
import unittest

from comp61542.database import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_read(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        self.assertEqual(len(db.publications), 1)

    def test_read_invalid_xml(self):
        db = database.Database()
        self.assertFalse(db.read(path.join(self.data_dir, "invalid_xml_file.xml")))

    def test_read_missing_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_year.xml")))
        self.assertEqual(len(db.publications), 0)

    def test_read_missing_title(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_title.xml")))
        # publications with missing titles should be added
        self.assertEqual(len(db.publications), 1)

    def test_get_average_authors_per_publication(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-1.xml")))
        _, data = db.get_average_authors_per_publication(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.3, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 2, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MODE)
        self.assertEqual(data[0], [2])

    def test_get_average_publications_per_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
        _, data = db.get_average_publications_per_author(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MODE)
        self.assertEqual(data[0], [0, 1, 2, 3])

    def test_get_average_publications_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-3.xml")))
        _, data = db.get_average_publications_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.5, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [3])

    def test_get_average_authors_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        _, data = db.get_average_authors_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.8, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [0, 2, 4, 5])
        # additional test for union of authors
        self.assertEqual(data[-1], [0, 2, 4, 5])

    def test_get_publication_summary(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publication_summary()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data[0]), 6,
            "incorrect number of columns in data")
        self.assertEqual(len(data), 2,
            "incorrect number of rows in data")
        self.assertEqual(data[0][1], 1,
            "incorrect number of publications for conference papers")
        self.assertEqual(data[1][1], 2,
            "incorrect number of authors for conference papers")

    def test_get_average_authors_per_publication_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "three-authors-and-three-publications.xml")))
        header, data = db.get_average_authors_per_publication_by_author(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 3,
            "incorrect average of number of conference papers")
        self.assertEqual(data[0][1], 1.5,
            "incorrect mean journals for author1")
        self.assertEqual(data[1][1], 2,
            "incorrect mean journals for author2")
        self.assertEqual(data[2][1], 1,
            "incorrect mean journals for author3")

    def test_get_publications_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_author()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 2,
            "incorrect number of authors")
        self.assertEqual(data[0][-1], 1,
            "incorrect total")

    def test_get_average_publications_per_author_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_average_publications_per_author_by_year(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_publications_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_average_authors_per_publication_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_author_totals_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")
        self.assertEqual(data[0][1], 2,
            "incorrect number of authors in result")

    def test_get_author_totals_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_author_totals_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")
        self.assertEqual(data[0][1], 2,
            "incorrect number of authors in result")
    
    # testing how many times an author appears first
    def test_get_times_author_appears_first(self):
        # expected results for authros
        expected_results = {
            'Meng': 2,
            'Mohammed': 0,
            'Aris': 0,
            'Maryam': 3,
        }
        
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "2014_sprint1_test_first_last.xml")))
        authors = db.get_all_authors()
        for author in authors:
            times = db.get_times_author_appears_first(author)
            expected = expected_results.get(author) if expected_results.get(author) != None else 0
            self.assertEqual(times, expected, 'Incorrect result for {}, {}. Expected is: {}'.format(author, times, expected))
    
    # testing how many times an author appears last
    def test_get_times_author_appears_last(self):
        # expected results for authros
        expected_results = {
            'Meng': 3,
            'Mohammed': 2,
            'Aris': 0,
            'Maryam': 0,
        }
        
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "2014_sprint1_test_first_last.xml")))
        authors = db.get_all_authors()
        for author in authors:
            times = db.get_times_author_appears_last(author)
            expected = expected_results.get(author) if expected_results.get(author) != None else 0
            self.assertEqual(times, expected, 'Incorrect result for {}, {}. Expected is: {}'.format(author, times, expected))
    
    def test_get_times_author_appears_sole(self):
        # expected results for authros
        expected_results = {
            'Meng': 0,
            'Mohammed': 0,
            'Aris': 1,
            'Maryam': 0,
        }
        
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "2014_sprint1_test_first_last.xml")))
        authors = db.get_all_authors()
        for author in authors:
            times = db.get_times_author_appears_sole(author)
            expected = expected_results.get(author) if expected_results.get(author) != None else 0
            self.assertEqual(times, expected, 'Incorrect result for {}, {}. Expected is: {}'.format(author, times, expected))
    
    def test_get_publications_by_author_name(self):
        # expected results for authros
        expected_results = {
            'Meng': [5, 0, 0, 0, 5],
            'Mohammed': [5, 0, 0, 0, 5],
            'Aris': [1, 0, 0, 0, 1],
            'Maryam': [4, 0, 0, 0, 4],
        }
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "2014_sprint1_test_first_last.xml")))
        authors = db.get_all_authors()
        for author in authors:
            stats = db.get_publications_by_author_name(author)
            expected = expected_results.get(author) if expected_results.get(author) != None else [0, 0, 0, 0, 0]
            self.assertEqual(stats, expected, 'Incorrect stats for {}: {}. Expected {}'.format(author, stats, expected))
            
    def test_get_detailed_publications_by_author_name(self):
        expected_results = {
            'Author A':[
                [2, 1, 0, 0, 3], # stats for fist
                [0, 0, 1, 1, 2], # stats for last
                [1, 1, 0, 0, 2] # stats for sole
            ],
            'Author B': [
                [0, 0, 1, 1, 2], 
                [2, 1, 0, 0, 3],
                [1, 1, 1, 1, 4]
            ],
        }
        
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint_2_fls_stats.xml")))
        authors = db.get_all_authors()
        for author in authors:
            stats = db.get_detailed_publications_by_author_name(author)
            expected = expected_results.get(author) if expected_results.get(author) != None else [[0, 0, 0, 0, 0] for i in range(0, 3)]
            self.assertEqual(stats, expected, 'Incorrect stats for {}: {}. Expected {}'.format(author, stats, expected))
    
    def test_build_Graph(self):
        import networkx as nx
        G = nx.Graph()
        G.add_nodes_from(['Author A', 'Author B', 'Author C', 'Author D', 'Author E', 'Author F'])
        G.add_edges_from([(u'Author A', u'Author B'), (u'Author B', u'Author D'), (u'Author A', u'Author E'),
                          (u'Author A', u'Author D'), (u'Author B', u'Author C')])
        
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint3_test.xml")))
        gg = db._build_graph()
        self.assertEqual(gg.nodes(), G.nodes(), 'Incorrect result')
        self.assertEqual(gg.edges(), G.edges(), 'Incorrect result')
        
    def test_get_degrees_of_separation(self):
        expected_results = [
        ['Author C', 'Author D', 1],
        ['Author A', 'Author B', 0],
        ['Author E', 'Author C', 2],
        ['Author A', 'Author F', 'X']]
        
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint3_test.xml")))
        for index in expected_results:
            result = db.get_degrees_of_separation(index[0], index[1])
            self.assertEqual(result, index[2], 'Incorrect result for {} and {}: {}. Expected is {}'.format(index[0], index[1], result, index[2]))

if __name__ == '__main__':
    unittest.main()
