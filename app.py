from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_mitre_cve(cve_id):
    url = f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        description_elem = soup.find('div', class_='cvedetail_description')
        if description_elem:
            return description_elem.text.strip()
        else:
            return "Description not available"
    else:
        return f"Failed to retrieve data for CVE ID: {cve_id}"

@app.route('/', methods=['GET', 'POST'])
def index():
    description = None
    if request.method == 'POST':
        cve_id = request.form['cve_id']
        description = scrape_mitre_cve(cve_id)
    return render_template('index.html', description=description)

if __name__ == '__main__':
    app.run(debug=True)