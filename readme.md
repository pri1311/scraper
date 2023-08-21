# Webpage Text Extractor

This project demonstrates how to create an endpoint that extracts and cleans text from a given webpage URL.

## Installation and Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install required packages: `pip3 install -r requirements.txt`.
4. Run the Django development server: `python3 manage.py runserver`.

## How to Use

1. Send a POST request to the `/extract/` endpoint with a JSON payload containing the URL to be extracted.\
   Example: `{"url": "https://example.com"}`
2. The endpoint will extract the text content from the URL and clean it.
3. The cleaned text will be saved in a document.

### Additional Options

1. To save data with a specific file name, add the path to the  JSON payload. If no file name is specified, text will be stored to file `data.txt`\
   Example: `{"fileName": "fileName.txt"}`\
   **PLEASE NOTE**: If there exists a file with the same name, it will be overwritten.
2. To remove special characters from the text set `remove_special_characters` to `true` in the payload. It should be a Boolean. Default is false.\
   Example: `{"remove_special_characters": true}`
3. To convert all text to lowercase, set `to_lowercase` to `true` in the payload. It should be a Boolean. Default is false.\
   Example: `{"to_lowercase": true}`

## Testing

1. Run tests using the command: `python3 manage.py test scraper`.

## Additional Notes

- The codebase follows Django best practices for views, URLs, and tests.
- Cleaning process:
   - Whitespace and Newline Removal:
      The initial step involves removing extra whitespaces, tabs, and newline characters. These characters don't usually add value to the extracted text and can make the text harder to process.
   - HTML Tags Removal:
      Web pages often contain HTML tags for formatting, styling, and structuring the content. These tags are removed using libraries Beautiful Soup along with html5lib, which is a Python library for parsing HTML and XML documents.
   - Extract Tables:
      Beatifulsoup's get text method returns tables as a list, losing all rows and columns information. We extract them separately to make them more readable and useful.
   - Special Character Handling:
      Some special characters might still be present in the text after removing HTML tags. Depending on your requirements, you might want to handle or remove special characters, punctuation, and non-alphanumeric characters. We use use regular expressions to filter out non-alphanumeric characters or specific patterns in this demo. 
   - Lowercasing:
      For consistency and to treat words regardless of their capitalization, you might choose to convert all text to lowercase.

## Repository Structure
```
   scraper/
   ├── manage.py
   ├── main/
   │   ├── __init__.py
   │   ├── asgi.py
   │   ├── settings.py
   │   ├── urls.py
   │   └── wsgi.py
   ├── scraper/
   │   ├── __init__.py
   │   ├── tests.py
   │   ├── urls.py
   │   └── views.py
   ├── .gitignore
   ├── readme.md
   └── requirements.txt
```