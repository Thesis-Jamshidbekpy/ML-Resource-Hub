"""Realistic ML demo content used by seed_demo_data management command."""

from __future__ import annotations

# (name, name_uz, slug, category, algorithm_type, algorithm_type_uz)
ALGORITHM_SPECS: list[tuple[str, str, str, str, str, str]] = [
    ("Linear Regression", "Chiziqli regressiya", "linear-regression", "regression", "Supervised Learning", "Nazoratli o'qitish"),
    ("Logistic Regression", "Logistik regressiya", "logistic-regression", "classification", "Supervised Learning", "Nazoratli o'qitish"),
    ("Ridge Regression", "Ridge regressiyasi", "ridge-regression", "regression", "Regularized Regression", "Regulyarlashtirilgan regressiya"),
    ("Lasso Regression", "Lasso regressiyasi", "lasso-regression", "regression", "Regularized Regression", "Regulyarlashtirilgan regressiya"),
    ("Decision Tree", "Qaror daraxti", "decision-tree", "classification", "Tree-based Model", "Daraxt asosidagi model"),
    ("Random Forest", "Tasodifiy o'rmon", "random-forest", "ensemble_learning", "Ensemble Learning", "Ansambil o'qitish"),
    ("Gradient Boosting", "Gradient boosting", "gradient-boosting", "ensemble_learning", "Ensemble Learning", "Ansambil o'qitish"),
    ("XGBoost", "XGBoost", "xgboost", "ensemble_learning", "Boosting Framework", "Boosting freymvorki"),
    ("LightGBM", "LightGBM", "lightgbm", "ensemble_learning", "Boosting Framework", "Boosting freymvorki"),
    ("Support Vector Machine", "Support Vector Machine", "support-vector-machine", "classification", "Kernel Method", "Yadro usuli"),
    ("K-Nearest Neighbors", "K yaqin qo'shnilar", "k-nearest-neighbors", "classification", "Instance-based Learning", "Namuna asosidagi o'qitish"),
    ("Naive Bayes", "Naive Bayes", "naive-bayes", "classification", "Probabilistic Model", "Ehtimollik modeli"),
    ("K-Means Clustering", "K-Means klasterlash", "k-means-clustering", "clustering", "Unsupervised Learning", "Nazoratsiz o'qitish"),
    ("DBSCAN", "DBSCAN", "dbscan", "clustering", "Density-based Clustering", "Zichlik asosidagi klasterlash"),
    ("Hierarchical Clustering", "Ierarxik klasterlash", "hierarchical-clustering", "clustering", "Unsupervised Learning", "Nazoratsiz o'qitish"),
    ("Principal Component Analysis", "Asosiy komponent tahlili", "principal-component-analysis", "dimensionality_reduction", "Dimensionality Reduction", "O'lchamni kamaytirish"),
    ("t-SNE", "t-SNE", "t-sne", "dimensionality_reduction", "Visualization Technique", "Vizualizatsiya usuli"),
    ("Convolutional Neural Network", "Konvolyutsion neyron tarmoq", "convolutional-neural-network", "deep_learning", "Deep Learning", "Chuqur o'qitish"),
    ("Recurrent Neural Network", "Takrorlanuvchi neyron tarmoq", "recurrent-neural-network", "deep_learning", "Deep Learning", "Chuqur o'qitish"),
    ("LSTM Network", "LSTM tarmoq", "lstm-network", "deep_learning", "Sequence Modeling", "Ketma-ket modellashtirish"),
    ("Transformer", "Transformer", "transformer", "deep_learning", "Attention Architecture", "Attention arxitekturasi"),
    ("Autoencoder", "Avtoenkoder", "autoencoder", "deep_learning", "Representation Learning", "Vakillik o'qitish"),
    ("Q-Learning", "Q-Learning", "q-learning", "reinforcement_learning", "Reinforcement Learning", "Mustahkamlashgan o'qitish"),
    ("Policy Gradient", "Policy Gradient", "policy-gradient", "reinforcement_learning", "Reinforcement Learning", "Mustahkamlashgan o'qitish"),
    ("AdaBoost", "AdaBoost", "adaboost", "ensemble_learning", "Boosting Algorithm", "Boosting algoritmi"),
    ("CatBoost", "CatBoost", "catboost", "ensemble_learning", "Gradient Boosting", "Gradient boosting"),
    ("Elastic Net", "Elastic Net", "elastic-net", "regression", "Regularized Regression", "Regulyarlashtirilgan regressiya"),
    ("Gaussian Mixture Model", "Gauss aralash modeli", "gaussian-mixture-model", "clustering", "Probabilistic Clustering", "Ehtimollik klasterlash"),
    ("Apriori Algorithm", "Apriori algoritmi", "apriori-algorithm", "classification", "Association Rules", "Assotsiatsiya qoidalari"),
    ("Isolation Forest", "Isolation Forest", "isolation-forest", "classification", "Anomaly Detection", "Anomaliya aniqlash"),
]

DESCRIPTION_TEMPLATE = (
    "{name} is widely used in academic and industry projects for structured prediction tasks. "
    "It balances interpretability with predictive performance when data is prepared carefully."
)
DESCRIPTION_TEMPLATE_UZ = (
    "{name_uz} akademik va amaliy loyihalarda keng qo'llaniladi. "
    "Ma'lumotlar to'g'ri tayyorlanganda model ishonchlilik va aniqlikni yaxshi muvozanatlashtiradi."
)

MATH_FOUNDATION = (
    "The method optimizes an objective function over model parameters using training data, "
    "with regularization or constraints when needed to control variance."
)
MATH_FOUNDATION_UZ = (
    "Usul o'quv ma'lumotlari bo'yicha model parametrlarini optimallashtiradi va kerak bo'lsa "
    "dispersiyani boshqarish uchun regulyarizatsiya qo'llaydi."
)

ADVANTAGES = "Strong baseline performance, well-documented theory, and broad library support in Python."
ADVANTAGES_UZ = "Yaxshi boshlang'ich natija, boy nazariy asos va Python kutubxonalarida keng qo'llab-quvvatlash."

DISADVANTAGES = "Performance may degrade on highly noisy data or when feature engineering is insufficient."
DISADVANTAGES_UZ = "Shovqinli ma'lumotlar yoki yetarli feature engineering bo'lmaganda natija pasayishi mumkin."

APPLICATIONS = "Student projects, research prototypes, teaching labs, and production analytics pipelines."
APPLICATIONS_UZ = "Talaba loyihalari, ilmiy prototiplar, laboratoriya mashg'ulotlari va analitika tizimlari."

COMPLEXITY = "Training cost grows with dataset size and feature dimensionality; inference is usually efficient."
COMPLEXITY_UZ = "O'qitish vaqti ma'lumot hajmi va belgilar soniga bog'liq; inferens odatda tez."

RESOURCE_TITLES: list[tuple[str, str, str]] = [
    ("Hands-On Machine Learning", "Hands-On Machine Learning", "book"),
    ("Pattern Recognition and Machine Learning", "Pattern Recognition and Machine Learning", "book"),
    ("Deep Learning (Goodfellow)", "Deep Learning (Goodfellow)", "book"),
    ("Scikit-learn User Guide", "Scikit-learn qo'llanmasi", "documentation"),
    ("Stanford CS229 Lecture Notes", "Stanford CS229 ma'ruzalari", "article"),
    ("MIT 6.S191 Deep Learning", "MIT 6.S191 chuqur o'qitish", "video"),
    ("Attention Is All You Need", "Attention Is All You Need", "research_paper"),
    ("UCI Machine Learning Repository", "UCI ML repozitoriyasi", "dataset"),
    ("Kaggle Learn Track", "Kaggle Learn kursi", "video"),
    ("Google ML Crash Course", "Google ML Crash Course", "video"),
    ("Fast.ai Practical Deep Learning", "Fast.ai amaliy DL", "video"),
    ("PyTorch Official Tutorials", "PyTorch rasmiy darslari", "documentation"),
    ("TensorFlow Core Guide", "TensorFlow Core qo'llanma", "documentation"),
    ("Elements of Statistical Learning", "Elements of Statistical Learning", "book"),
    ("Machine Learning Yearning", "Machine Learning Yearning", "book"),
    ("Distill.pub Interactive Articles", "Distill.pub interaktiv maqolalar", "article"),
    ("arXiv cs.LG Recent Papers", "arXiv cs.LG yangi ishlar", "research_paper"),
    ("Papers With Code Benchmarks", "Papers With Code benchmarklar", "documentation"),
    ("Coursera ML Specialization", "Coursera ML mutaxassisligi", "video"),
    ("IBM ML Fundamentals", "IBM ML asoslari", "video"),
    ("OpenML Datasets Portal", "OpenML dataset portali", "dataset"),
    ("Hugging Face Course", "Hugging Face kursi", "documentation"),
    ("StatQuest YouTube Series", "StatQuest video seriyasi", "video"),
    ("3Blue1Brown Neural Networks", "3Blue1Brown neyron tarmoqlar", "video"),
    ("Andrew Ng Lecture Slides", "Andrew Ng slaydlari", "article"),
    ("NeurIPS Proceedings Archive", "NeurIPS arxivi", "research_paper"),
    ("ICML Open Access Papers", "ICML ochiq maqolalar", "research_paper"),
    ("Google Research Publications", "Google Research nashrlar", "research_paper"),
    ("Microsoft ML Blog", "Microsoft ML blogi", "article"),
    ("Amazon Science ML Articles", "Amazon Science ML maqolalar", "article"),
]

AUTHORS = [
    "Gareth James et al.",
    "Christopher Bishop",
    "Ian Goodfellow",
    "Scikit-learn Team",
    "Andrew Ng",
    "MIT OpenCourseWare",
    "Vaswani et al.",
    "UCI Repository",
    "Kaggle Education",
    "Google Developers",
    "Jeremy Howard",
    "PyTorch Team",
    "TensorFlow Team",
    "Trevor Hastie",
    "Andrew Ng",
    "Distill Editors",
    "arXiv Community",
    "Papers With Code",
    "Coursera",
    "IBM Skills Network",
    "OpenML Team",
    "Hugging Face",
    "Josh Starmer",
    "Grant Sanderson",
    "Stanford AI Lab",
    "NeurIPS Foundation",
    "ICML Committee",
    "Google Research",
    "Microsoft Research",
    "Amazon Science",
]

INSTITUTIONS = [
    "Tashkent University of Information Technologies",
    "INHA University in Tashkent",
    "Westminster International University in Tashkent",
    "Tashkent State Technical University",
    "Samarkand State University",
    "National University of Uzbekistan",
    "Turin Polytechnic University in Tashkent",
    "New Uzbekistan University",
    "Tashkent University of Economics",
    "Kimyo International University",
]

ACADEMIC_INTERESTS = [
    "Computer Vision",
    "Natural Language Processing",
    "Reinforcement Learning",
    "Time Series Forecasting",
    "Recommender Systems",
    "MLOps",
    "Data Mining",
    "Bayesian Methods",
    "Graph Machine Learning",
    "Healthcare AI",
]

COMMENT_TEXTS = [
    "Very clear explanation for coursework preparation.",
    "The mathematical section helped me before the midterm exam.",
    "Good balance between theory and practical examples.",
    "I used this algorithm in my semester project with strong results.",
    "Please add more visualization examples in future updates.",
    "Useful resource links, especially the official documentation.",
    "Easy to compare with related algorithms in the same category.",
    "The complexity notes are practical for deployment planning.",
    "Helped me understand when not to use this method.",
    "Excellent reference for thesis literature review.",
]

COMMENT_TEXTS_UZ = [
    "Kurs ishi uchun juda tushunarli tushuntirilgan.",
    "Matematik qism oraliq nazoratdan oldin yordam berdi.",
    "Nazariya va amaliy misollar yaxshi muvozanatlangan.",
    "Semestr loyihamda shu algoritmdan foydalandim, natija yaxshi chiqdi.",
    "Kelajakda ko'proq vizual misollar qo'shilsa yaxshi bo'lardi.",
    "Rasmiy dokumentatsiya havolalari ayniqsa foydali.",
    "Bir kategoriyadagi boshqa algoritmlar bilan solishtirish oson.",
    "Murakkablik haqidagi izoh deploy reja uchun foydali.",
    "Qachon ishlatmaslik kerakligini tushunishga yordam berdi.",
    "Diplom adabiyotlar review uchun ajoyib manba.",
]

DEMO_USER_PASSWORD = "DemoPass123!"
