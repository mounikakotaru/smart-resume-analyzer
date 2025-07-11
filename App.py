import streamlit as st
import nltk
import spacy
nltk.download('stopwords')
spacy.load('en_core_web_sm')

import pandas as pd
import base64, random
import time, datetime
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io
from streamlit_tags import st_tags
from PIL import Image
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
import pafy
import youtube_dl
from sklearn.feature_extraction.text import CountVectorizer


def fetch_yt_video(link):
    video = pafy.new(link)
    return video.title

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations**")
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c, (c_name, c_link) in enumerate(course_list[:no_of_reco], 1):
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
    return rec_course

def extract_sections(text):
    sections = {}
    headings = ["summary", "objective", "education", "experience", "projects", "certifications", "skills", "achievements"]
    current = None
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        lower = line.lower()
        if any(h in lower for h in headings):
            current = lower
            sections[current] = ""
        elif current:
            sections[current] += line + "\n"
    return sections

def match_job_description(resume_text, job_desc):
    vectorizer = CountVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, job_desc])
    tokens = vectorizer.get_feature_names_out()
    resume_vec = set(vectors.toarray()[0].nonzero()[0])
    jd_vec = set(vectors.toarray()[1].nonzero()[0])
    matched = [tokens[i] for i in resume_vec & jd_vec]
    missing = [tokens[i] for i in jd_vec - resume_vec]
    score = int(len(matched) / (len(matched) + len(missing) + 1e-6) * 100)
    return matched, missing, score

st.set_page_config(page_title="Smart Resume Analyzer", page_icon='📄')

def run():
    st.title("Smart Resume Analyser")
    img = Image.open('./Logo/SRA_Logo.jpg')
    img = img.resize((250, 250))
    st.image(img)

    pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
    job_desc = st.text_area("Paste a Job Description (optional for matching):")

    if pdf_file is not None:
        save_image_path = './Uploaded_Resumes/' + pdf_file.name
        with open(save_image_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        show_pdf(save_image_path)
        resume_data = ResumeParser(save_image_path).get_extracted_data()

        if resume_data:
            resume_text = pdf_reader(save_image_path)
            st.header("**Resume Analysis**")
            st.success("Hello " + str(resume_data.get('name', 'User')))
            st.subheader("**Basic Information**")
            st.text(f"Name: {resume_data.get('name', 'N/A')}")
            st.text(f"Email: {resume_data.get('email', 'N/A')}")
            st.text(f"Contact: {resume_data.get('mobile_number', 'N/A')}")
            st.text(f"Pages: {resume_data.get('no_of_pages', 'N/A')}")

            pages = resume_data.get('no_of_pages', 0)
            if pages == 1:
                st.markdown('''<h4 style='color: #d73b5c;'>You seem to be a Fresher.</h4>''', unsafe_allow_html=True)
            elif pages == 2:
                st.markdown('''<h4 style='color: #1ed760;'>Intermediate Level Detected.</h4>''', unsafe_allow_html=True)
            elif pages >= 3:
                st.markdown('''<h4 style='color: #fba171;'>Experienced Level Detected.</h4>''', unsafe_allow_html=True)

            st.subheader("**Skills**")
            st_tags(label='Your Skills:', text='Skills extracted from Resume', value=resume_data['skills'], key='skills')

            st.subheader("**Suggestions & Recommendations**")
            recommended = course_recommender(ds_course + web_course + uiux_course + ios_course + android_course)

            if job_desc:
                st.subheader("**Job Description Match Score**")
                matched, missing, score = match_job_description(resume_text, job_desc)
                st.success(f"✅ Matched Keywords: {', '.join(matched)}")
                st.warning(f"❌ Missing Keywords: {', '.join(missing)}")
                st.info(f"📊 Match Score: {score}%")

            st.subheader("**Resume Score**")
            resume_score = 0
            sections = ["Objective", "Declaration", "Hobbies", "Achievements", "Projects"]
            for sec in sections:
                if sec.lower() in resume_text.lower():
                    resume_score += 20
                    st.success(f"[+] Great! You included: {sec}")
                else:
                    st.warning(f"[-] Consider adding: {sec}")

            my_bar = st.progress(0)
            for percent_complete in range(resume_score):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1)
            st.success(f'Your Resume Score: {resume_score}')
            st.balloons()

            st.subheader("**📑 Resume Sections Extracted**")
            extracted_sections = extract_sections(resume_text)
            for section, content in extracted_sections.items():
                st.markdown(f"### {section.title()}")
                st.code(content)

            st.subheader("**📺 Resume Tips Video**")
            yt_link = random.choice(resume_videos)
            st.video(yt_link)

            st.subheader("**📺 Interview Tips Video**")
            yt2 = random.choice(interview_videos)
            st.video(yt2)

run()
