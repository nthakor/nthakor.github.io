from pybtex.database.input import bibtex

parser = bibtex.Parser()
bibdata = parser.parse_file('adversarial_ml/adversarial_ml.bib')


data = [['Title','Year','Authors']]
for bib_id in bibdata.entries:
    b = bibdata.entries[bib_id].fields
    try:
        # change these lines to create a SQL insert
        # print((b["title"]))
        # print(b["year"])
        #deal with multiple authors
        lead_author = bibdata.entries[bib_id].persons["author"][0]
        authors = "{} {} et al.".format(lead_author.first()[0],lead_author.last()[0])
        row = [b['title'].split('{')[1].split('}')[0], b['year'], authors]
        data.append(row)
        print(row)
        # for author in bibdata.entries[bib_id].persons["author"]:
        #     print(author.first(), author.last())
    # field may not exist for a reference
    except(KeyError):
        continue


def make_markdown_table(array):
    """ Input: Python list with rows of table as lists
               First element as header. 
        Output: String to put into a .md file 
        
    Ex Input: 
        [["Name", "Age", "Height"],
         ["Jake", 20, 5'10],
         ["Mary", 21, 5'7]] 
    """

    markdown = "\n" + str("| ")

    for e in array[0]:
        to_add = " " + str(e) + str(" |")
        markdown += to_add
    markdown += "\n"

    markdown += '|'
    for i in range(len(array[0])):
        markdown += str("-------------- | ")
    markdown += "\n"

    for entry in array[1:]:
        markdown += str("| ")
        for e in entry:
            to_add = str(e) + str(" | ")
            markdown += to_add
        markdown += "\n"

    return markdown + "\n"

print(make_markdown_table(data))