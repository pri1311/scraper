def getTable(table):
    rows = []
    trs = table.find_all("tr")
    headerow = [td.get_text(strip=True)
                for td in trs[0].find_all("th")]  # header row
    if headerow:  # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs:  # for every table row
        rows.append([td.get_text(strip=True)
                    for td in tr.find_all("td")])  # data row
    return rows