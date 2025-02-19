# notion-weekly-report integration for iDSSP:

# **🚀 Notion Weekly Report Automation**  

This repo automates **weekly task reports from Notion** and sends them to **Slack** using GitHub Actions. It allows you to:  
✅ **Fetch tasks updated this week** from a Notion database  
✅ **Categorize tasks as "Ongoing" or "Completed"**  
✅ **Send the report automatically to a Slack channel** every Monday  
✅ **Run manually anytime** from GitHub Actions  

## **📌 How to Set Up Your Own GitHub Workflow**

## **🔹 Step 1: Fork This Repository**
1. Click the **"Fork"** (or clone) button at the top-right of this page.  
2. Choose **your GitHub account** to create your own copy of this repository.  

---

## **🔹 Step 2: Get Your Notion API Key & Database ID**
### **1️⃣ Get Your Notion API Key**
1. Go to **[Notion Integrations](https://www.notion.so/my-integrations)**.  
2. Click **"New Integration"**.  
3. **Name** your integration (e.g., `Weekly Report`).  
4. **Select your workspace** and click **Submit**.  
5. Copy the **"Internal Integration Token"** (this is your `NOTION_API_KEY`).  

### **2️⃣ Get Your Notion Database ID**
1. Open the **Notion database** you want to use.  
2. In the browser URL of the database page, find the part that looks like this:  
   ```
   https://www.notion.so/yourworkspace/8d5d28a856064783ad5adadf2c49b603?v=xxxxxxxx
   ```
3. Copy the long alphanumeric string **before** `?v=` → `8d5d28a856064783ad5adadf2c49b603`  
4. This is your **Notion Database ID**.

---

## **🔹 Step 3: Get Your Slack Webhook URL**
If you want to send reports to **a different Slack channel**:
1. Go to **[Slack API Webhooks](https://api.slack.com/messaging/webhooks)**.  
2. Click **"Create an App" → "From scratch"**.  
3. **Name your app** (e.g., `Weekly Report`).  
4. **Select your Slack workspace** and click **"Create App"**.  
5. In the left sidebar, go to **"Incoming Webhooks"**.  
6. Click **"Activate Incoming Webhooks"**.  
7. Click **"Add New Webhook to Workspace"**.  
8. Select the Slack channel (e.g., `#weekly-reports`).  
9. Copy the **Webhook URL** (this is your `SLACK_WEBHOOK_URL`).  

---

## **🔹 Step 4: Add Your Secrets in GitHub**
1. **Go to your forked repository** → Click **Settings**.  
2. In the left sidebar, go to **Secrets and variables → Actions**.  
3. Click **"New repository secret"**.  
4. Add the following secrets:  

| Secret Name           | Value |
|----------------------|----------------------------|
| `NOTION_API_KEY`     | *(Paste your Notion API Key)* |
| `NOTION_DATABASE_ID` | *(Paste your Notion Database ID)* |
| `SLACK_WEBHOOK_URL`  | *(Paste your Slack Webhook URL)* |


---

## **🔹 Step 5: Set Up GitHub Actions**
1. In your forked repo, navigate to `.github/workflows/`.  
2. Open **`notion_report.yml`** and update the **cron schedule** (if needed, according to your preferences).  
   ```yaml
   schedule:
     - cron: "0 0 * * 1"  # Runs every Monday at 08:00 Taipei time (UTC+8)
   ```
   - Use [crontab.guru](https://crontab.guru/) to adjust timings.  

3. **Commit and push changes**:
   ```sh
   git add .github/workflows/notion_report.yml
   git commit -m "Updated GitHub Actions schedule"
   git push origin main
   ```

---

## **🔹 Step 6: Run Your Workflow**
### **✅ Option 1: Run Automatically (Every Monday)**
- Your workflow **runs every Monday at 08:00 Taipei time (UTC+8)** automatically. (I set this as the default, but feel free to modify)

### **✅ Option 2: Run Manually**
1. **Go to your repository → Click "Actions"**.  
2. Click **"Notion Weekly Report"**.  
3. Click **"Run Workflow"** → Select the branch and click **Run**.  

---

## **🔹 Step 7: Customize Your Report**
If you want to:
- **Change the Slack message format**, modify `format_report()` in `notion_report.py`.  
- **Filter by a different date range**, modify `get_tasks()` in `notion_report.py`.  
- **Add more properties from Notion**, update `format_report()`.  

---

## **📌 Frequently Asked Questions**
### **1️⃣ Why is my GitHub Action not running?**
- Ensure `.github/workflows/notion_report.yml` exists.  
- Go to **Settings → Actions → General** → Enable workflows.  
- Check the **"Actions" tab** for error logs.

### **2️⃣ How do I debug API errors?**
- Add `print(response.json())` inside `get_tasks()` to **see Notion's API response**.
- Use `echo ${{ secrets.NOTION_API_KEY }}` inside the GitHub workflow to **check if secrets are loaded**.

### **3️⃣ Can I use this for multiple Slack channels and Notion databases?**
✅ Yes! Create **separate workflows** with different environment variables.  

---

If you have any issues, feel free to reach out! 😊
