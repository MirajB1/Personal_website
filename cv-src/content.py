# -*- coding: utf-8 -*-
"""Single source of truth for CV content. ATS-safe: plain text only."""

NAME = "MIRAJ BHATTARAI"
HEADLINE = "Machine Learning  |  Full-Stack Development  |  Python"

CONTACT_LINE_1 = "Budhanilkantha, Kathmandu, Nepal  |  +977 9863977099  |  mirajbhattarai7@gmail.com"
CONTACT_LINE_2 = "mirajbhattarai.com.np  |  linkedin.com/in/miraj-bhattarai-1122b6265  |  github.com/MirajB1"

LINKS = {
    "mirajbhattarai7@gmail.com": "mailto:mirajbhattarai7@gmail.com",
    "mirajbhattarai.com.np": "https://www.mirajbhattarai.com.np",
    "linkedin.com/in/miraj-bhattarai-1122b6265": "https://www.linkedin.com/in/miraj-bhattarai-1122b6265/",
    "github.com/MirajB1": "https://github.com/MirajB1",
}

SUMMARY = (
    "Associate Machine Learning Engineer at Techkey Technology and freelance full-stack developer with a "
    "year of delivering client web applications end to end. Trains models in Python and builds the REST "
    "APIs and interfaces around them. Multi-hackathon winner, experienced across the whole workflow: "
    "preprocessing, feature engineering, training and evaluation, API development and deployment."
)

SKILLS = [
    ("Languages", "Python, JavaScript, SQL, C, C++, Java"),
    ("Machine Learning and Data", "Scikit-learn, TensorFlow, PyTorch, OpenCV, Random Forest, Naive Bayes, "
                                  "Regression, Classification, Clustering, Feature Engineering, Model Fine-Tuning, "
                                  "Model Evaluation and Benchmarking, NumPy, Pandas, Matplotlib, Seaborn, EDA"),
    ("Web and APIs", "FastAPI, Flask, Node.js, REST APIs, JWT Authentication, React, Vite, HTML5, CSS3, "
                     "Tailwind CSS"),
    ("Databases and Tools", "MySQL, SQLite, MongoDB, Git, GitHub, Linux, VS Code, Vercel, Render, "
                            "Raspberry Pi, Microsoft Azure (Custom Vision, Blob Storage)"),
]

EXPERIENCE = [
    {
        "role": "Associate Machine Learning Engineer",
        "org": "Techkey Technology Pvt. Ltd., Kathmandu, Nepal",
        "dates": "Aug 2026 - Present",
        "bullets": [
            "Build, train and fine-tune machine learning models in Python with Scikit-learn, TensorFlow and "
            "PyTorch, across data preprocessing, feature engineering, hyperparameter tuning and evaluation on "
            "accuracy, precision and recall.",
            "Fine-tune pre-trained models on task-specific datasets and benchmark each one against its baseline "
            "before it is taken forward, running structured experiments across candidate approaches.",
            "Document datasets, architectures and results for reproducibility, and refactor prototypes into "
            "modular Python reviewed by senior engineers.",
        ],
    },
    {
        "role": "Freelance Full-Stack Developer",
        "org": "Self-employed, Kathmandu, Nepal",
        "dates": "Nov 2025 - Present",
        "bullets": [
            "Built and deployed rajubhada.com.np for a utensil retailer in Gaighat: a bilingual public shopfront "
            "with a point-of-sale and inventory management system behind a login, over a REST API and "
            "relational database.",
            "Delivered a full-stack web application for a pest control company in Sydney, Australia, owning "
            "requirements, database schema, API, interface and deployment, plus fixes and changes after launch.",
        ],
    },
]

PROJECTS = [
    {
        "title": "AgniDrishti Nepal - AI Wildfire Prediction and Early Warning System",
        "meta": "Capstone Project  |  2026  |  Live: agnidrishti.vercel.app",
        "stack": "React, FastAPI, MongoDB, Scikit-learn (Random Forest, Naive Bayes), NASA FIRMS API, OpenWeatherMap API",
        "bullets": [
            "Built a full-stack platform predicting wildfire risk across Nepal with custom-trained Random Forest "
            "and Naive Bayes models on weather, elevation and satellite fire-hotspot data, with Vapour Pressure "
            "Deficit as an engineered feature.",
            "Developed a JWT-secured FastAPI backend with role-based access, public alerting and automated "
            "country-wide risk scans over NASA FIRMS, OpenWeatherMap and Open-Elevation.",
        ],
    },
    {
        "title": "QR-Based Digital Academic System",
        "meta": "Winner, TechSprint Hackathon 2026  |  React, Vite, Tailwind CSS, Node.js",
        "stack": "",
        "bullets": [
            "Built a platform replacing paper-based lab submissions at Tribhuvan University for students, "
            "teachers and external evaluators, with per-student QR generation, batch scanning and role-based "
            "portals. Delivered across 201+ commits in a 4-person team.",
        ],
    },
    {
        "title": "Project Ecolog - Forest Fire and Intrusion Detection System",
        "meta": "Winner, Tech Conclave 2024  |  Python, Raspberry Pi, Azure Custom Vision, OpenCV",
        "stack": "",
        "bullets": [
            "Designed a Raspberry Pi system pairing real-time audio classification (gunshot and smoke) with "
            "Azure Custom Vision imaging to trigger forest fire hardware alerts and stream live data to a web "
            "dashboard.",
        ],
    },
]

EDUCATION = [
    {
        "degree": "B.Sc. Computer Science and Information Technology",
        "org": "Tribhuvan University - Madan Bhandari Memorial College, Kathmandu  |  "
               "CGPA 3.0+ across all semesters, no backlogs",
        "dates": "2023 - 2026",
        "detail": "",
    },
    {
        "degree": "Higher Secondary Education (NEB, +2 Science)",
        "org": "Liverpool International College, Kathmandu  |  CGPA 3.01",
        "dates": "2020 - 2022",
        "detail": "",
    },
]

ACHIEVEMENTS = [
    "Hackathon wins: TechSprint 2026 (NEC), Tech Conclave 2024, BPC Hackfest 2024. DataCamp Fellowship 2025.",
    "Lead Organizer, MBMC IdeaX 2025; Organizing Committee Member, Hult Prize at MBMC 2025.",
]
