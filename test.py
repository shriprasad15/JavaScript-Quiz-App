import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up OAuth2 credentials
scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds_shri.json', scope)  # Replace with your JSON credentials file
client = gspread.authorize(creds)

def read_data_from_sheet(sheet_name, worksheet_name):
    try:
        sheet = client.open(sheet_name).worksheet(worksheet_name)
        data = sheet.get_all_records()
        return data
    except (ValueError, IndexError):
        # Handle the exceptions or log the error here
        return None

def generate_html_from_data(data):
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Data from Google Sheets</title>
        <style>
            table {
                border-collapse: collapse;
                width: 50%;
                margin: 20px auto;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>Data from Google Sheets</h1>
        <table>
            <thead>
                <tr>
                    {% for header in headers %}
                        <th>{{ header }}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for row in rows %}
                    <tr>
                        {% for cell in row %}
                            <td>{{ cell }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """

    headers = list(data[0].keys())
    rows = [list(row.values()) for row in data]

    with open('output.html', 'w') as file:
        file.write(html_template.render(headers=headers, rows=rows))

# Replace 'YourSheetName' and 'YourWorksheetName' with your actual sheet and worksheet names
sheet_data = read_data_from_sheet('tesr', 'Sheet1')
generate_html_from_data(sheet_data)
