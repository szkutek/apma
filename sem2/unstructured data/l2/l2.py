import urllib.request
from bs4 import BeautifulSoup
import networkx as nx
import itertools
import pylab
import unidecode

if __name__ == '__main__':
    url = 'http://prac.im.pwr.wroc.pl/~hugo/HSC/Publications.html'
    page = urllib.request.urlopen(url)

    soup = BeautifulSoup(page, 'html.parser')
    cooperation_network = nx.Graph()

    for year in range(2017, 1994, -1):

        research_per_year = soup.find('a',
                                      attrs={'name': str(year)}).next_sibling  # returns whole <ol start="1" type="1">
        # print(research_per_year.prettify())
        # print(research_per_year.contents[1].find_all('b')[0].text)

        for c in research_per_year.contents:  # one year
            if c != '\n':
                names_per_paper = [unidecode.unidecode(x.text).replace(' ', '')  # remove accents and spaces
                                   for x in c.find_all('b')]  # authors of one paper
                comb = [*itertools.combinations(names_per_paper, 2)]  # create pairs
                if comb:  # if comb is not empty # cooperation_network.add_edges_from(comb)
                    for a1, a2 in comb:
                        if cooperation_network.has_edge(a1, a2):
                            cooperation_network[a1][a2]['weight'] += 1
                        else:
                            cooperation_network.add_edge(a1, a2, weight=1)

    # else:  # only one author (worked alone or co-authored with non-members of HSC) ???
    #     cooperation_network.add_node(names_per_paper[0])

    fig = pylab.figure()
    pos = nx.spring_layout(cooperation_network)

    degrees = nx.degree(cooperation_network, weight='weight')
    edges_data = cooperation_network.edges(data=True)
    weights = [e[2]['weight'] for e in edges_data]

    nx.draw_networkx_nodes(cooperation_network, pos, node_color='g', alpha=0.8,
                           nodelist=degrees.keys(),
                           node_size=[*map(lambda x: 10 * x + 1,
                                           degrees.values())])  # [deg * 10 for deg in degrees.values()] # larger nodes

    nx.draw_networkx_edges(cooperation_network, pos, alpha=0.5,
                           edgelist=cooperation_network.edges(),
                           width=weights)  # [*map(lambda x: x * 1, weights)] # thicker lines

    nx.draw_networkx_labels(cooperation_network, pos, font_size=8)
    # nx.draw_networkx_edge_labels(cooperation_network, pos, font_size=8,
    #                              edge_labels=dict(zip(cooperation_network.edges(), weights)))

    print(degrees)
    print(len(degrees))
    pylab.show()
