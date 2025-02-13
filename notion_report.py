import requests
import datetime
import os
from dotenv import load_dotenv
load_dotenv()
# Load API keys from environment variables
NOTION_API_KEY = os.getenv("NOTION_API_KEY")  # Store in GitHub Secrets
DATABASE_ID = "8d5d28a856064783ad5adadf2c49b603"
# Notion will give you this really long link: https://www.notion.so/8d5d28a856064783ad5adadf2c49b603?v=4ce8edb545e644209686c852a37425f3
#You need to extract the alphanumeric part between / and ? to get the DATABASE_ID
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")  # Optional

# Notion API Headers
print(NOTION_API_KEY)
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Get last week's tasks from Notion
# Get tasks updated in the last 7 days from Notion
def get_tasks():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    # Calculate the start of the week (7 days ago)
    last_week = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()

    payload = {
        "filter": {
            "property": "Last Modification",  # ✅ Uses your correct Notion property name
            "date": {
                "on_or_after": last_week  # ✅ Filters tasks modified in the last 7 days
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print("❌ Error fetching tasks:", response.json())
        return []

    tasks = response.json().get("results", [])
    return tasks


# Format tasks into a weekly report
# Format tasks for a report
def format_report(tasks):
    report_date = datetime.date.today().strftime("%Y-%m-%d")
    
    task_list = "\n".join(
        [
            f"- {task['properties']['Task name']['title'][0]['text']['content']}" 
            for task in tasks if 'Task name' in task['properties'] and task['properties']['Task name']['title']
        ]
    ) or "No tasks updated this week."

    return f"📊 *Weekly Report - {report_date}*\n\n{task_list}"


# Create a new Notion page for the report
def create_notion_report(report_text):
    url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Task name": {  # ✅ Uses your actual "Task name" property
                "title": [{"text": {"content": f"Weekly Report - {datetime.date.today()}"}}]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": report_text}}]  # ✅ Fix: Added `rich_text`
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Send the report to Slack
def send_to_slack(report_text):
    if not SLACK_WEBHOOK_URL:
        print("Slack Webhook URL not found, skipping Slack notification.")
        return (None, None)  # Fix unpacking error

    message = {"text": report_text}
    response = requests.post(SLACK_WEBHOOK_URL, json=message)

    return response.status_code, response.text


# Run the script
if __name__ == "__main__":
    tasks = get_tasks()
    report_text = format_report(tasks)
    
    # Create Notion report
    notion_response = create_notion_report(report_text)
    print("✅ Notion report created:", notion_response)

    # Send to Slack (optional)
    if report_text:
        slack_status, slack_response = send_to_slack(report_text)
        print(f"✅ Slack response: {slack_status} - {slack_response}")
    else:
        print("No tasks to report, skipping Slack notification.")