# Computer Vision Automation in Attendance and Library System


### 📚 Abstract
This project aims to automate institutional tasks like student attendance and library book management using computer vision and artificial intelligence.  
The system includes a website with dashboards for students, faculty, and admin, integrated with:
- Face recognition for attendance.
- Generative AI-powered chatbot for student-library interaction.

Students can upload PDF books and ask questions, with the chatbot processing the content intelligently, reducing manual workload and bringing automation to the education system.

---
![(Home Page)](college_backend/IMG-20250422-WA0008(1).jpg)
### 🏗️ Architecture

#### Modules Involved:
- **Frontend (ReactJS):**
    - Dashboards for students, faculty, and admin.
    - Live camera access for face recognition.
    - Library search and chatbot interaction.

- **Backend (Django):**
    - APIs for attendance, user authentication, and face recognition.
    - AI integration using LangChain or Transformers for question answering from PDFs.

- **Face Recognition Module:**
    - OpenCV + Neural Network based encoding and recognition.
    - Real-time frame comparison with stored face encodings.

- **Chatbot with Generative AI:**
    - Parses PDFs → Converts to QA context → Handles student questions.

- **Database:**
    - PostgreSQL/MySQL for storing user data, attendance records, and book metadata.

#### Flow Diagram:

![(Flow Diagram)](college_backend/IMG-20250411-WA0001(1).jpg)
OpenCV + Neural Network based encoding and recognition.


Compares real-time frames with stored face encodings.


Chatbot with Generative AI:


Uses PDF parsers and NLP models (like GPT, BERT, or Haystack) to convert PDFs to QA context.


Enables students to ask natural language questions.


Database:


PostgreSQL/MySQL for storing user data, attendance records, and book metadata.


Flow Diagram: User → Dashboard → (Attendance / Library Chatbot)
 → Face Recognition / Ask AI → Backend → DB or PDF → Response
4. Software and Hardware Requirements
Software:
Frontend: React JS, HTML, CSS, JavaScript
![Chatbot](college_backend/IMG-20250422-WA0011(1).jpg)

Backend: Django (Python), Django REST Framework


Libraries: OpenCV, face_recognition, PyMuPDF, LangChain/Haystack, NLTK


Database: PostgreSQL / MySQL


IDE/Tools: VS Code, Anaconda, Postman
Hardware:
Webcam (Laptop/USB/Phone as webcam via DroidCam)

![Dashboard](college_backend/IMG-20250422-WA0012(1).jpg)

4 GB RAM minimum, 64-bit OS


Optional: GPU support for faster face recognition


5. Working Procedure
Registration & Login:


Admin registers faculty and students.


Users login via role-based dashboards.


Face Recognition Attendance:


Admin uploads student face images into the system.


Students face the camera; system marks attendance in real-time.


Faculty Dashboard:

![Register page of students](college_backend/IMG-20250422-WA0010(1).jpg)

View students under their department.


Modify attendance, mark absentees, filter by branch/date.


Library Dashboard & Chatbot:


Students browse books and register interest.


Faculty/admin approves requests.


Students can upload book PDFs and ask questions to the AI-powered chatbot.


Generative AI for PDF QA:


Uploads PDF → Extracts text → Embeds data → Uses AI to answer student queries.


For example: “What is the definition of AI from this book?” → AI replies contextually.


6. Screenshots

![User Interface (Home Page)](college_backend/IMG-20250422-WA0013(1).jpg)






7. Conclusion and Future Enhancement
Conclusion:
The system demonstrates how computer vision and AI can automate routine tasks in academic institutions. By combining face recognition with intelligent chatbots, it provides a user-friendly and efficient platform for attendance tracking and library usage.
Future Enhancements:
Mobile app version for portability.


Integration with biometric sensors.


Auto-suggestion of related books using AI.


QR code scanning for book issue/return.


Voice-enabled chatbot assistant.


Notifications to students on overdue books or missed attendance.
8. References
OpenCV Documentation – https://docs.opencv.org


Django Documentation – https://docs.djangoproject.com


face_recognition library – https://github.com/ageitgey/face_recognition


LangChain – https://www.langchain.com


Haystack – https://haystack.deepset.ai


PyMuPDF (fitz) – https://pymupdf.readthedocs.io



![User Interface (Home Page)](college_backend/IMG-20250422-WA0009(1).jpg)



Additional AI Chatbot with PDF Feature
How It Works:
Students upload a PDF book to the library system.


The backend extracts content using PyMuPDF or pdfminer.


The content is split into chunks and embedded using a language model (BERT/GPT).


A question-answering model receives student queries and returns context-aware answers.
Tech Stack Used:
LangChain / Haystack for document-based QA.


Embedding models (Sentence Transformers).


Vector database (FAISS) for fast retrieval.


React chatbot UI with backend integration.


---

### ⚙️ Software and Hardware Requirements

#### Software:
- Frontend: React JS, HTML, CSS, JavaScript  
- Backend: Django (Python), Django REST Framework  
- Libraries: OpenCV, face_recognition, PyMuPDF, LangChain/Haystack, NLTK  
- Database: PostgreSQL / MySQL  
- IDE/Tools: VS Code, Anaconda, Postman  

#### Hardware:
- Webcam (Laptop/USB/Phone as webcam via DroidCam)  
- Minimum 4 GB RAM, 64-bit OS  
- Optional: GPU support for faster face recognition  

---

### 🚀 Working Procedure

1. **Registration & Login:**  
   Admin registers faculty and students.  
   Role-based dashboard login for users.

2. **Face Recognition Attendance:**  
   Admin uploads student face images.  
   Students face the camera to mark attendance automatically.

3. **Faculty Dashboard:**  
   - View students by department.  
   - Modify attendance, mark absentees, filter by branch/date.

4. **Library Dashboard & Chatbot:**  
   - Students browse books and register interest.  
   - Faculty/admin approves requests.  
   - Students upload PDFs and ask questions.

5. **Generative AI for PDF QA:**  
   - PDF → Extract Text → Embed Data → AI Answers Student Queries.  
   Example:  
   *"What is the definition of AI from this book?"* → AI responds contextually.

---


### ✅ Conclusion and Future Enhancement

**Conclusion:**  
This system demonstrates how computer vision and AI can automate routine academic tasks, providing an efficient platform for attendance and library management.

**Future Enhancements:**  
- Mobile app version for portability.  
- Integration with biometric sensors.  
- Auto-suggestion of related books using AI.  
- QR code scanning for book issue/return.  
- Voice-enabled chatbot assistant.  
- Notifications for overdue books and missed attendance.

---

### 📚 References
- [OpenCV Documentation](https://docs.opencv.org)  
- [Django Documentation](https://docs.djangoproject.com)  
- [face_recognition library](https://github.com/ageitgey/face_recognition)  
- [LangChain](https://www.langchain.com)  
- [Haystack](https://haystack.deepset.ai)  
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io)

---


### 🤖 Additional AI Chatbot with PDF Feature

#### How It Works:
- Student uploads PDF → Backend extracts text (PyMuPDF/pdfminer) → Content split into chunks and embedded → QA model provides context-aware answers.

#### Tech Stack Used:
- LangChain / Haystack for document-based QA  
- Embedding models (Sentence Transformers)  
- Vector database (FAISS) for fast retrieval  
- React Chatbot UI with backend integration  

---


