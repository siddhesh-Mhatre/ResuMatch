import os
import PyPDF2
from nltk.tokenize import word_tokenize
import shutil


def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''.join(page.extract_text() for page in reader.pages)
    return text


def extract_skills(text):
    tokens = word_tokenize(text.lower())
    return list(set(map(str.strip, tokens)))  # Remove duplicates case-insensitively


def calculate_match_score(candidate_skills):
    # Define the required skills for the job (based on the job description)
    required_skills = {"python", "c", "sql", "react", "mongodb", "pandas", "numpy", "matplotlib"}

    # Calculate the intersection of candidate skills and required skills
    common_skills = set(candidate_skills).intersection(required_skills)

    # Calculate the match score
    match_score = len(common_skills) / len(required_skills) * 100
    return match_score




resumes_folder = 'D:\ResumeSortlister\Python Developer'  # Replace with the path to the folder containing resumes
selected_folder = 'Selected_candidates'  # Create a folder named 'Selected_candidates'

threshold = 70  # Threshold for selection

# Create 'Selected_candidates' folder if not exist
if not os.path.exists(selected_folder):
    os.makedirs(selected_folder)

# Iterate through resumes in the folder
for resume_file in os.listdir(resumes_folder):
    resume_path = os.path.join(resumes_folder, resume_file)

    # Extract text from the resume
    resume_text = extract_text_from_pdf(resume_path)

    # Extract unique skills from the resume text
    candidate_skills = extract_skills(resume_text)

    # Calculate match score
    match_score = calculate_match_score(set(candidate_skills))
    print(match_score)
    # Check if the candidate meets the threshold
    if match_score >= threshold:
        # Move the selected resume to 'Selected_candidates' folder
        shutil.move(resume_path, os.path.join(selected_folder, resume_file))
        print(f"{resume_file} selected with a match score of {match_score}%")
