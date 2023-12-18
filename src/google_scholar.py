import requests

url = "https://scholar.google.com/citations?view_op=list_works&hl=en&hl=en&user=UESASpwAAAAJ&sortby=pubdate"

response = requests.get(url)

html_content = response.text

print(html_content)
