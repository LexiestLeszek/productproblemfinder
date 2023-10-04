from playwright.sync_api import sync_playwright

def google_search(subreddit, keywords):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        common_problems = []

        for keyword in keywords:
            search_query = f'{keyword} site:https://www.reddit.com/r/{subreddit}/ after:2023-01-01'

            page.goto('https://www.google.com/')
            page.fill('//*[@id="input"]', search_query)
            page.press('input[name=q]', 'Enter')

            # Wait for search results to load
            page.wait_for_selector('h3')

            # Extract and append search results to the common problems list
            search_results = page.evaluate('(results) => Array.from(results, result => result.innerText)', 'h3')
            common_problems += [result for result in search_results]

        browser.close()

        return common_problems

if __name__ == '__main__':
    # subreddit = input('Enter subreddit (e.g., legaladvice): ')
    subreddit = "legaladvice"
    keywords = [
        "Struggling with", "Challenges in", "Frustrated with", "Difficulty in",
        "Issues with", "Can't figure out how to", "Need help with", "Looking for advice on",
        "Not sure how to", "Overwhelmed by", "Feeling lost in", "Dealing with"
    ]

    common_problems = google_search(subreddit, keywords)

    if common_problems:
        print("Common problems identified:")
        for i, problem in enumerate(common_problems, 1):
            print(f'{i}. {problem}')
    else:
        print("No common problems found.")
