""""
File: gadapi.py

Description: The primary API for interacting with the gad dataset.
"""

import pandas as pd
import sankey as sk
from collections import Counter
import xml.etree.ElementTree as ET
import pandas as pd
from lxml import etree as ET


class GADAPI:

    gad = None  # dataframe

    def load_gad(self, filename):
        # Load and parse XML file
        # tree = ET.parse(filename) 
        tree = ET.parse('music_hm3.xml')
        root = tree.getroot()

        # Create a list to store the extracted data
        data = []

        # Find the 'Tracks' section in the XML and extract track information
        tracks = root.find(".//dict").find("dict")  # Navigate to the track entries
        for track_key in tracks.findall("key"):
            track_dict = track_key.getnext()  # Get the <dict> following the <key>
            track_data = {}
            for i in range(0, len(track_dict), 2):
                key = track_dict[i].text
                value = track_dict[i+1].text
                track_data[key] = value
            data.append(track_data)

        # Create a Pandas DataFrame
        self.df = pd.DataFrame(data)
        columns_to_exclude = [
            'Normalization', 'Sort Album', 'Sort Artist', 'Sort Name', 'Persistent ID', 
            'Track Type', 'Purchased', 'Location', 'File Folder Count', 'Library Folder Count', 
            'Artwork Count', 'Explicit', 'Compilation', 'Part Of Gapless Album', 
            'Apple Music', 'Sort Album Artist', 'Sort Composer', 'Protected', 
            'Favorited', 'Loved', 'Clean', 'Playlist Only', 'Has Video', 'HD', 
            'Music Video', 'Album Loved', 'Disliked', 'Work', 'BPM', 'Grouping', 
            'Movement Number', 'Movement Count', 'Movement Name', 'Comments', 'Release Date', 'Skip Date', 
            'Play Date UTC', 'Play Date', 'Sample Rate', 'Bit Rate', 'Date Modified'
        ]
        self.df = self.df.drop(columns=columns_to_exclude, errors='ignore')
        # print(self.df.tail()
        # df_with_na = self.df[self.df.isna().any(axis=1)]
        # print(df_with_na)

        # Convert 'Date Added' column to datetime (with errors='coerce' to handle invalid data)
        self.df['Date Added'] = pd.to_datetime(self.df['Date Added'], errors='coerce')

        # Remove timezone information, if any
        self.df['Date Added'] = self.df['Date Added'].dt.tz_localize(None)

        # Replace 'Date Added' with Year and Month formatted as 'YYYY-MM'
        self.df['Date Added'] = self.df['Date Added'].dt.to_period('M').astype(str)

        # The DataFrame is updated in place
        print(self.df)



    def get_phenotypes(self):
        """ Fetch the list of unique phenotypes (diseases)
        with at least one positive association in the gad dataset """
        gady = self.gad[self.gad.association == 'Y']
        gady.phenotype = gady.phenotype.str.lower()
        phen = gady.phenotype.unique()
        phen = [str(p) for p in phen if ";" not in str(p)]
        return sorted(phen)

    def extract_local_network(self, phenotype, min_pub, singular):

        # postive associations only!
        gad = self.gad[self.gad.association == 'Y']

        # Focus on a particular set of columns
        gad = gad[['phenotype', 'gene']]

        # Convert the phenotype to lowercase
        gad.phenotype = gad.phenotype.str.lower()

        # Count publications (rows) for each unique disease-gene association
        gad = gad.groupby(['phenotype', 'gene']).size().reset_index(name='npubs')

        # Sort by npubs descending
        gad.sort_values('npubs', ascending=False, inplace=True)

        # discard associations with less than <min_pub> publications
        gad = gad[gad.npubs >= min_pub]

        # phenotype of interest
        gad_pheno = gad[gad.phenotype == phenotype]

        # Find all gad associations involving genes linked to our starting phenotype
        gad = gad[gad.gene.isin(gad_pheno.gene)]


        # print(gad)
        # print("LOCAL NETWORK")

        # Discard singular disease-gene associations
        if not singular:
            counts = Counter(gad.phenotype)
            exclude = [k for k, v in counts.items() if v == 1]
            gad = gad[~gad.phenotype.isin(exclude)]

        return gad


def main():

    gadapi = GADAPI()
    gadapi.load_gad("gad.csv")

    local = gadapi.extract_local_network("asthma", 5)
    print(local)


if __name__ == '__main__':
    main()