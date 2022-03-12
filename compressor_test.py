import compressor
import tempfile
import csv
import unittest

class TestCompressor(unittest.TestCase):

    def test_compressor(self):
        output_file = tempfile.NamedTemporaryFile()
        compressor.compress_csv("./test.csv", output_file.name)

        rows = []
        with open(output_file.name) as output_file_handle:
            output_csv = csv.reader(output_file_handle)

            for row in output_csv:
                rows.append(row)

        self.assertEqual(len(rows), 10) # 9 rows + 1 header row

        # Make sure that the headers were preserved in the expected order
        header_row = rows.pop(0)
        self.assertEqual(len(header_row), 14)

        self.assertEqual(["Precinct", 
                            "Last Name", 
                            "First Name", 
                            "New First", 
                            "Hs Num", 
                            "Pre Direction",
                            "Street Name",
                            "Street Type",
                            "Unit Type",
                            "Unit Num",
                            "City (RA)",
                            "State (RA)",
                            "Zip (RA)",
                            "Column1"], header_row)
        
        self.assertEqual(["47",
                            "",
                            "",
                            "NAVANI GAVILAR AND DALINAR KHOLIN",
                            "100",
                            "N",
                            "KING'S",
                            "WAY",
                            "",
                            "",
                            "KHOLINAR",
                            "AK",
                            "87483",
                            "100 N KING'S WAY KHOLINAR AK 87483"], rows[0])

        self.assertEqual(["56",
                            "",
                            "",
                            "MR AND MS PAINT",
                            "1",
                            "",
                            "MICROSOFT",
                            "WAY",
                            "",
                            "",
                            "REDMOND",
                            "WA",
                            "98052",
                            "1 MICROSOFT WAY REDMOND WA 98052"], rows[1])

        self.assertEqual(["66",
                            "",
                            "",
                            "BREHA ORGANA",
                            "10",
                            "",
                            "MONARCH",
                            "PL",
                            "",
                            "",
                            "ALDERAAN",
                            "AL",
                            "421",
                            # Deliberately misspelled to ensure that this data is being preserved and not generated dynamically
                            "10 MONARC PL ALDERAAN AL 421"], rows[2])

        self.assertEqual(["66",
                            "",
                            "",
                            "BAIL ORGANA",
                            "1",
                            "",
                            "SENATOR",
                            "PL",
                            "",
                            "",
                            "ALDERAAN",
                            "AL",
                            "421",
                            "1 SENATOR PL ALDERAAN AL 421"], rows[3])

        self.assertEqual(["72",
                            "",
                            "",
                            "ADOLIN KHOLIN",
                            "100",
                            "S",
                            "KING'S",
                            "WAY",
                            "APT",
                            "82",
                            "KHOLINAR",
                            "AK",
                            "87483",
                            "100 S KING'S WAY KHOLINAR APT 82 AK 87483"], rows[4])

        self.assertEqual(["88",
                            "",
                            "",
                            "PERRIN AYBARA",
                            "1000",
                            "",
                            "WOLF'S DEN",
                            "DR",
                            "",
                            "",
                            "MANETHEREN",
                            "MN",
                            "467374",
                            "1000 WOLF'S DEN DR MANETHERN MN 467374"], rows[5])

        self.assertEqual(["88",
                            "",
                            "",
                            "RAND AL'THOR",
                            "1000",
                            "",
                            "DRAGON",
                            "DR",
                            "",
                            "", 
                            "TWO RIVERS",
                            "MN",
                            "47832",
                            "1000 DRAGON DR TWO RIVERS MN"], rows[6])

        self.assertEqual(["88",
                            "",
                            "",
                            "EGWENE AL'VERE",
                            "1000",
                            "",
                            "AMYRLIN",
                            "ST",
                            "",
                            "",
                            "TAR VALON",
                            "AS",
                            "7483",
                            "1000 AMYRLIN ST TAR VALON AS 7483"], rows[7])

        self.assertEqual(["92",
                            "",
                            "",
                            "JAN, MARCIA, AND MIKE BRADY",
                            "4222",
                            "",
                            "CLINTON",
                            "WAY",
                            "",
                            "",
                            "LOS ANGELES",
                            "CA", 
                            "90001",
                            "4222 CLINTON WAY LOS ANGELES CA 90001"], rows[8])
if __name__ == '__main__':
    unittest.main()