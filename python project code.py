#!/usr/bin/env python3
"""
AI Resume Checker System
Uses arrays, sorting, text processing, and file storage (JSON).
"""

import re
import json
import os
import datetime

DATA_DIR = "resume_data"
REPORT_FILE = os.path.join(DATA_DIR, "reports.json")

# Example skills database
SKILL_DATABASE = [
    "python", "java", "c++", "sql", "javascript", "html", "css",
    "machine learning", "deep learning", "data analysis",
    "excel", "communication", "leadership", "problem solving"
]

JOB_KEYWORDS = [
    "project", "experience", "team", "analysis",
    "development", "design", "database", "reporting"
]

# -------- Storage --------
def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_reports():
    ensure_data_dir()
    if not os.path.exists(REPORT_FILE):
        return []
    with open(REPORT_FILE, "r") as f:
        return json.load(f)

def save_reports(reports):
    ensure_data_dir()
    with open(REPORT_FILE, "w") as f:
        json.dump(reports, f, indent=2)

# -------- Extractors --------
def extract_email(text):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r"\b\d{10}\b", text)
    return match.group(0) if match else None

def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in SKILL_DATABASE:
        if skill.lower() in text_lower:
            found.append(skill)
    return found

# -------- Scoring --------
def score_contact(email, phone):
    score = 0
    if email:
        score += 50
    if phone:
        score += 50
    return score  # /100

def score_skills(found_skills):
    return min(100, len(found_skills) * 10)

def score_keywords(text):
    text_lower = text.lower()
    count = 0
    for word in JOB_KEYWORDS:
        if word in text_lower:
            count += 1
    return (count / len(JOB_KEYWORDS)) * 100

def overall_score(contact, skills, keywords):
    return round(contact * 0.2 + skills * 0.4 + keywords * 0.4, 2)

# -------- Suggestions --------
def generate_suggestions(email, phone, found_skills, keyword_score):
    tips = []

    if not email:
        tips.append("Add a professional email address.")
    if not phone:
        tips.append("Include a valid 10-digit phone number.")
    if len(found_skills) < 4:
        tips.append("Add more relevant technical and soft skills.")
    if keyword_score < 50:
        tips.append("Add stronger keywords related to the job description.")
    if not tips:
        tips.append("Resume is strong. Minor improvements needed.")
    
    return tips

# -------- Sorting helper --------
def sort_reports_by_score(reports):
    return sorted(reports, key=lambda x: x['total_score'], reverse=True)

def sort_reports_by_date(reports):
    return sorted(reports, key=lambda x: x['timestamp'])

# -------- Main Analyzer --------
def analyze_resume(text):
    email = extract_email(text)
    phone = extract_phone(text)
    found_skills = extract_skills(text)

    c_score = score_contact(email, phone)
    s_score = score_skills(found_skills)
    k_score = score_keywords(text)
    total = overall_score(c_score, s_score, k_score)

    suggestions = generate_suggestions(email, phone, found_skills, k_score)

    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "email": email,
        "phone": phone,
        "skills_found": found_skills,
        "contact_score": c_score,
        "skills_score": s_score,
        "keyword_score": k_score,
        "total_score": total,
        "suggestions": suggestions
    }

    return report

# -------- CLI Menu --------
def main_menu():
    reports = load_reports()

    while True:
        print("\n===== AI Resume Checker =====")
        print("1) Analyze new resume")
        print("2) List past reports (by score)")
        print("3) List past reports (by date)")
        print("4) Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            print("Paste your resume text:")
            text = []
            print("(Enter an empty line to finish)")
            while True:
                line = input()
                if line.strip() == "":
                    break
                text.append(line)
            resume_text = "\n".join(text)
            report = analyze_resume(resume_text)
            reports.append(report)
            save_reports(reports)
            print("\nAnalysis Report:")
            print(json.dumps(report, indent=2))

        elif choice == "2":
            sorted_reports = sort_reports_by_score(reports)
            for r in sorted_reports:
                print(r["timestamp"], "=> Score:", r["total_score"])

        elif choice == "3":
            sorted_reports = sort_reports_by_date(reports)
            for r in sorted_reports:
                print(r["timestamp"], "=> Score:", r["total_score"])

        elif choice == "4":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main_menu()
