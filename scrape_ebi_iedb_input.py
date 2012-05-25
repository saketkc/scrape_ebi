from mechanize import Browser, _http
from BeautifulSoup import BeautifulSoup
import sys
import os
def get_data_from_ebi(*arg):
    br = Browser()
    args = arg[0]
    filename = args[0]
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.open('http://iedb.ebi.ac.uk/tools/ElliPro/iedb_input')
    br.select_form(name='predictionForm')
    br.form['protein_type'] = ['structure',]
    if os.path.exists(filename):
        br.form.add_file(open(filename), 'text/plain', filename)
    else:
        br.form['pdbId'] = filename.split('.')[0]
    submit_response = br.submit(name='Submit', label='Submit')
    html = submit_response.read()
    soup = BeautifulSoup(html)
    all_tables = soup.findAll("table",cellspacing=1)
    if len(all_tables) == 1:
	    table = soup.find("table",cellspacing=1)
	    all_protein_chains = {}
	    for row in table.findAll('tr')[1:-1]:
        	columns = row.findAll('td')
	        number = columns[1]
        	chain = columns[2]
	        number_of_residues = columns[3]
        	all_protein_chains[number.string] = chain.string
    	    br.select_form(name='selectChainForm')
   
    	    br.form['chainIndex'] = [None] * (len(args)-1)
    
            for index,seqchoice in enumerate(args[1:]):
		
		for k,v in all_protein_chains.iteritems():
		
			if str(v) == str(seqchoice):
				choice = k
            br.form['chainIndex'][index] = (str(int(choice)-1))
    	    submit_response = br.submit().read()
            soup = BeautifulSoup(submit_response)
    
    for index,tables in enumerate(soup.findAll("table",cellspacing=1)[1:3]):
        if index == 0:
            print "Predicted Linear Epitope(s): "
            for row in tables.findAll('tr'):
                columns = row.findAll('td')
                output = ""
                for column in columns[:-1]:
                    output += column.string + "  "
                print output
        if index == 1:
            print "Predicted Discontinous Epitope(s): "
            for row in tables.findAll('tr')[1:]:
                columns = row.findAll('td') 
                output = ""
                for column in columns[:-1]:
                    if column.string == None:
                        column = column.find('div')
                    output += column.string + " "
                print output

if __name__ == "__main__":
    get_data_from_ebi(sys.argv[1:])