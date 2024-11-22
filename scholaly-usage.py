# Created on Fri Nov 22
# Thanks to the Scholarly module and ChatGPT! 

mport pandas as pd
from scholarly import scholarly

def fetch_multiple_authors(authors, start_year=2020, end_year=2025):
    """
    Fetch publications for multiple authors by Scholar IDs.
    Aggregates their publications into a single DataFrame filtered by year range.

    Args:
        authors (list of dict): List of dictionaries with `name` and `scholar_id`.
        start_year (int): Start year for filtering publications.
        end_year (int): End year for filtering publications.

    Returns:
        pd.DataFrame: A DataFrame containing aggregated data for all authors.
    """
    all_data = []

    for author_info in authors:
        author_name = author_info['name']
        scholar_id = author_info['scholar_id']

        print(f"Fetching data for: {author_name}")
        # Search for the author by name
        search_query = scholarly.search_author(author_name)
        author = None
        for result in search_query:
            if result['scholar_id'] == scholar_id:
                author = scholarly.fill(result)
                break

        if not author:
            print(f"Author with Scholar ID {scholar_id} not found. Skipping...")
            continue

        # Extract publication data
        for pub in author['publications']:
            title = pub['bib'].get('title', 'No Title')
            pub_year = pub['bib'].get('pub_year', 'No Year')
            citations = pub.get('num_citations', 0)  # Number of citations (default is 0 if missing)

            # Filter publications by year
            if pub_year != 'No Year' and start_year <= int(pub_year) <= end_year:
                all_data.append([author_name, pub_year, title, citations])

    # Create and return a DataFrame
    df = pd.DataFrame(all_data, columns=["Author Name", "Year", "Article Title", "Citations"])
    return df


def count_repeated_articles(authors_df):
    """
    Count the number of articles that are repeated more than once in the DataFrame.

    Args:
        authors_df (pd.DataFrame): DataFrame containing author names, publication years, and article titles.

    Returns:
        int: Count of repeated articles.
        pd.DataFrame: DataFrame of repeated articles with their counts.
    """
    # Group by 'Article Title' and count occurrences
    repeated_articles = authors_df['Article Title'].value_counts()

    # Filter for articles with more than one occurrence
    repeated_articles = repeated_articles[repeated_articles > 1]

    # Return the count and the filtered DataFrame
    return len(repeated_articles), repeated_articles.reset_index().rename(columns={'index': 'Article Title', 'Article Title': 'Count'})


# Example usage
if __name__ == "__main__":
    # List of authors with their names and Scholar IDs
    authors = [
        {"name": "Benjamin Haibe-Kains", "scholar_id": "hfGa2RMAAAAJ"},
        {"name": "Cheryl Arrowsmith", "scholar_id": "ygu2VxQAAAAJ"},
        {"name": "Anna Goldenberg", "scholar_id": "cEepZOEAAAAJ"},
        {"name": "Levon Halabelian", "scholar_id": "G45xgdAAAAAJ"},
        {"name": "Rachel Harding", "scholar_id": "mFSmAqUAAAAJ"},
        {"name": "Chris J. Maddison", "scholar_id": "WjCG3owAAAAJ"},
        {"name": "Matthieu Schapira", "scholar_id": "LZyOFQoAAAAJ"},
        {"name": "Bo Wang", "scholar_id": "37FDILIAAAAJ"}
    ]

    try:
        # Fetch articles for all authors between 2020 and 2025
        authors_df = fetch_multiple_authors(authors, start_year=2020, end_year=2025)
        print(authors_df)
        # Save to a CSV file if needed
        authors_df.to_csv("aggregated_publications_with_citations.csv", index=False)
    except ValueError as e:
        print(e)

    # Count repeated articles
    repeated_count, repeated_articles_df = count_repeated_articles(authors_df)

    print("Number of Articles between 2020 and 2025:")
    print(len(authors_df))

    print("Repeated Articles:")
    print(len(repeated_articles_df))

    # Calculate the total number of citations
    total_citations = authors_df['Citations'].sum()
    print("Total Number of Citations for Articles between 2020 and 2025:")
    print(total_citations)
