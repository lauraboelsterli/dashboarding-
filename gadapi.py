""""
File: gadapi.py

Description: The primary API for interacting with the gad dataset.
"""

import pandas as pd
import sankey as sk
from collections import Counter



class GADAPI:

    gad = None  # dataframe

    def load_gad(self, filename):
        self.gad = pd.read_csv(filename)
        print(self.gad)


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