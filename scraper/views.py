import re

import requests
import pandas as pd
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from tabulate import tabulate
from bs4 import BeautifulSoup

from . import utils


@api_view(["GET"])
def getAbout(_):
    return Response({
        "name": "Navigate to /etxract endpoint to start Scraping!"
    })


@api_view(["GET", "POST"])
def extract(request):
    # Returning data only if it is a Post Method.
    if request.method != "POST":
        return Response({
            "Attach the URL with the body of the POST request under key `url`"
        })

    # Raise Error 400 if Request Body missing
    if request.data is None or request.data == {} or "url" not in request.data:
        return Response(
            {
                "error": "URL is required. Attach the URL with the body of the POST request under key `url`"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    URL = request.data["url"]
    FILENAME = "data.txt"
    REMOVE_SPECIAL_CHARACTERS = False
    TO_LOWERCASE = False

    if "fileName" in request.data and (request.data["fileName"]).strip() != "":
        FILENAME = request.data["fileName"]
    
    if "remove_special_characters" in request.data:
        if not isinstance(request.data["remove_special_characters"], bool):
            return Response(
                {
                    "error": "`remove_special_characters` should be of type Boolean (true/false)"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        REMOVE_SPECIAL_CHARACTERS = request.data["remove_special_characters"]

    if "to_lowercase" in request.data:
        if not isinstance(request.data["to_lowercase"], bool):
            return Response(
                {
                    "error": "`to_lowercase` should be of type Boolean (true/false)"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        TO_LOWERCASE = request.data["to_lowercase"]

    # Getting Data in English
    headers = {"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7"}
    params = dict(lang="en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7")

    # Get Webpage data
    try:
        r = requests.get(URL, headers=headers, params=params)
    except Exception as e:
        return Response(
            {"error": e},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    soup = BeautifulSoup(r.content, "html5lib")

    # Removing unnecessary informations such as navbars, footers, headers, etc.
    decompose_tags = ["script", "style", "sidebar", "nav", "header", "footer"]
    elements_to_be_eliminated = soup.find_all(decompose_tags)
    for element in elements_to_be_eliminated:
        element.decompose()

    regex = re.compile(".*(sidebar|footer|header|navbar|nav|menu).*")
    elements = soup.find_all("div", {"class": regex})
    for element in elements:
        element.decompose()

    # Fetching all tables
    tables = soup.find_all("table")
    generated_tables = []
    for table in tables:
        generated_tables.append(utils.getTable(table))

    # Remove the tables since we extract them separately
    for table in tables:
        table.decompose()

    # Clean text (remove extra whitespaces, newline characters, etc.)
    data = soup.get_text().split("\n")
    data = [text.strip() for text in data if text.strip() != ""]
    data = "\n".join(data)

    if REMOVE_SPECIAL_CHARACTERS:
        data = re.sub('[^a-zA-Z0-9\s]', '', data)

    if TO_LOWERCASE:
        data = data.lower()

    file = open(FILENAME, "w")
    file.write(data)
    file.close()

    file = open(FILENAME, "a")
    for table in generated_tables:
        df = pd.DataFrame(table)
        prettyprint = tabulate(df, headers="keys", tablefmt="psql")
        file.write("\n")
        file.write(prettyprint)
    file.close()

    return Response(
        {"message": f"Data stored in file {FILENAME}"},
        status=status.HTTP_200_OK
    )
