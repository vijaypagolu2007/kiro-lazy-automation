
# Kiro Lazy Automation

This project was built for **Kiro Heroes Week 2: Lazy Automation**.  
It automates a boring digital task — organizing cluttered folders and creating backups.

## 🚀 What it does
- Sorts files into folders based on their extensions  
- Creates categorized folders automatically (Images, Documents, Archives, etc.)  
- Generates an `organize_index.json` log  
- Creates a ZIP backup of the entire source directory  
- Supports **dry-run mode** to preview changes safely  

## 🛠 How to Run

### 1. Dry run (safe test)
This shows what will happen without actually moving files:
"C:\Users\YourName\kiro_test_desktop" --backup 
"C:\Users\YourName\kiro_backups" --dry-run


### 2. Real run (perform the actual organization)
"C:\Users\YourName\kiro_test_desktop" --backup 
"C:\Users\YourName\kiro_backups"


## 📁 File Structure
/organize_desktop.py → Main automation script
/.kiro/README.md → Kiro hooks configuration
/organize_index.json → Log generated after running the script

---

## License
Free to use for learning and Kiro challenges.
