
def extract_next_page_url(link_header):
    # Extract the URL for the next page from the Link header
    # Example: <https://api.github.com/search/code?q=org%3Aorg_name+filename%3Afile_name+in%3Afile+search_text&page=2&per_page=100>; rel="next"
    parts = link_header.split(";")
    for part in parts:
        if "rel=\"next\"" in part:
            # Extract the URL between the angle brackets
            start = part.find("<") + 1
            end = part.find(">")
            return part[start:end]
    return None