import json
import os
import requests
import base64
import re
from db import test_mysql_connection1
from playwright.sync_api import sync_playwright


def down_apis():
    conn, cursor = test_mysql_connection1()

    select_query = """
        SELECT video FROM db7uhz37amwvyv.diamond_labgrown
        WHERE video != ''
    """

    cursor.execute(select_query)
    result = cursor.fetchall()

    # Use Playwright to automate browser interactionc
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode
        context = browser.new_context()

        for row in result:

            video_link = row[0]
            print(f"\n Processing: {video_link}")

            if ".html" not in video_link:
                continue

            try:
                if not video_link.startswith("http"):
                    video_link = f"https://{video_link}"

                # Parse diamond ID
                if "=" in video_link:
                    diamond_id = video_link.split("=")[1]
                else:
                    diamond_id = video_link.split("/")[-1]

                # Build JSON URL to test availability
                base_url = re.split(r'vision360\.html|view\.html',
                                    video_link, flags=re.IGNORECASE)[0].lower()
                json_0 = f"{base_url}imaged/{diamond_id}/0.json"

                # Fetch 0.json
                print(f"Checking JSON: {json_0}")
                json_resp = requests.get(json_0)
                if json_resp.status_code != 200:
                    print(f"0.json not available, skipping... {video_link}")
                    continue

                data = json_resp.json()
                if not data.get("image"):
                    print("JSON has no image content, skipping...")
                    continue

                # Use Playwright to load the page and intercept the API call
                page = context.new_page()

                # Variable to store the captured API data
                captured_data = {}

                # Intercept the POST request to /upload-base64
                page.on("request", lambda request: captured_data.update({
                    "base64_str": json.loads(request.post_data)["data"],
                    "moviename": json.loads(request.post_data)["moviename"]
                }) if request.url.endswith("/upload-base64") and request.method == "POST" else None)

                # Navigate to the page
                page_url = f"http://192.168.29.71:2500/vision360.html?moviename={video_link}"
                print(f"Loading page: {page_url}")
                response = page.goto(page_url)

                if response.status != 200:
                    print(
                        f"Failed to load page, status: {response.status}, skipping...")
                    page.close()
                    continue

                # Wait for the API call to be intercepted (or timeout after 15 seconds)
                print("Waiting for API call to /upload-base64...")
                page.wait_for_timeout(15000)  # 15 seconds in milliseconds

                page.close()

            except requests.exceptions.RequestException as e:
                print("Request failed:", e)
            except Exception as e:
                print(f"Playwright error: {e}")

        browser.close()

    # Close MySQL connection
    cursor.close()
    conn.close()


down_apis()
