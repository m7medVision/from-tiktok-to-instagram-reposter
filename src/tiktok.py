from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # add useragent
    browser = p.chromium.launch(headless=False, slow_mo=500)
    browser = browser.new_context(
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36")
    page = browser.new_page()
    page.goto("http://tiktok.com/@majhc")
    latest_video = page.query_selector('xpath=/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/a').inner_text
    print(latest_video)
    browser.close()