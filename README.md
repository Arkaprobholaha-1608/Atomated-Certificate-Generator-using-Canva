# Certificate Generator

This project is a Flask web application that automates the generation and renaming of certificates using the Canva API. Users can upload an Excel file containing participant information, and the application will generate customized certificates based on a provided Canva template URL.

## Features

- Upload an Excel file with participant data
- Generate customized certificates using the Canva Connect API
- Rename certificates based on participant information

## Prerequisites

- Python 3.x
- Canva Connect API credentials
- Flask
- Openpyxl
- Requests
- Python-dotenv

## Installation

1. Clone the repository:

```sh
git clone https://github.com/Arkaprobholaha-1608/cert_gen1.git
cd cert_gen1
```

2. Create a virtual environment and activate it:

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required dependencies:

```sh
pip install -r requirements.txt
```

4. Create a `.env` file in the project directory and add your Canva API credentials and Flask secret key:

```plaintext
FLASK_SECRET_KEY=your_flask_secret_key
CANVA_CLIENT_ID=your_canva_client_id
CANVA_CLIENT_SECRET=your_canva_client_secret
```

Replace `your_flask_secret_key`, `your_canva_client_id`, and `your_canva_client_secret` with your actual credentials.

## Usage

1. Run the Flask application:

```sh
python app.py
```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. Follow the steps on the web interface:
   - Upload an Excel file with participant data and provide the Canva template URL.
   - Confirm downloads and rename the certificates.

## Excel File Format

The Excel file should have the following format:

| Name          | Event         |
| ------------- | ------------- |
| John Doe      | Event Name    |
| Jane Smith    | Event Name    |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Openpyxl](https://openpyxl.readthedocs.io/)
- [Requests](https://docs.python-requests.org/en/latest/)
- [Python-dotenv](https://saurabh-kumar.com/python-dotenv/)
