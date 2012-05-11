from mechanize import Browser, _http
from BeautifulSoup import BeautifulSoup

br = Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.open('http://iedb.ebi.ac.uk/tools/ElliPro/iedb_input')
br.select_form(name='predictionForm')
br.form['protein_type'] = ['structure',]
br.form['pdbId'] = '5LYM'
submit_response = br.submit(name='Submit', label='Submit')
html = submit_response.read()
soup = BeautifulSoup(html)
table = soup.find("table",cellspacing=1)
for row in table.findAll('tr')[1:]:
    columns = row.findAll('td')
    rank = columns
    print rank
