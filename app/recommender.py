from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models import Organisation

COURSE_KEYWORD_MAP = {
    'Computer Science': 'software development programming web applications database systems networking cybersecurity artificial intelligence machine learning data analysis system administration IT infrastructure python java javascript',
    'Computer Engineering': 'hardware software embedded systems networking telecommunications electronics programming microprocessors circuit design ICT infrastructure firmware',
    'Software Engineering': 'software development programming web applications mobile apps testing agile systems design code deployment devops python java',
    'Information Technology': 'IT support networking systems administration database web development software hardware helpdesk infrastructure cloud computing',
    'Cybersecurity': 'network security ethical hacking penetration testing information security data protection firewall intrusion detection encryption vulnerability',
    'Electrical Engineering': 'power systems electronics circuit design telecommunications control systems instrumentation transformer distribution grid renewable energy',
    'Mechanical Engineering': 'manufacturing design production maintenance machinery automotive engineering fabrication thermodynamics hydraulics',
    'Civil Engineering': 'construction infrastructure design surveying project management structural engineering roads bridges buildings materials',
    'Chemical Engineering': 'process engineering oil gas petrochemicals manufacturing laboratory quality control refinery chemicals reaction',
    'Accounting': 'audit finance taxation bookkeeping financial reporting budgeting accounts revenue fiscal treasury payroll financial statements',
    'Business Administration': 'management marketing operations human resources strategy business development procurement supply chain administration',
    'Economics': 'financial analysis policy research banking statistics economic planning macroeconomics fiscal monetary econometrics',
    'Mass Communication': 'journalism media broadcasting public relations advertising content creation press radio television newsroom reporting',
    'Medicine and Surgery': 'clinical healthcare hospital patient care surgery medical research diagnosis treatment ward physician doctor',
    'Pharmacy': 'pharmaceutical drugs dispensing healthcare clinical laboratory quality assurance drug regulation pharmacology',
    'Law': 'legal research litigation corporate law compliance contracts advisory prosecution regulatory solicitor barrister court tribunal legislation',
    'Architecture': 'design construction urban planning building surveying AutoCAD drawing structural aesthetics renovation',
    'Statistics': 'data analysis research quantitative methods statistical modelling survey sampling econometrics probability',
    'Mathematics': 'data analysis quantitative modelling statistics computation actuarial research numerical analysis',
    'Physics': 'research laboratory instrumentation data analysis engineering science radiation optics mechanics',
    'Chemistry': 'laboratory research quality control pharmaceutical oil gas analytical chemical synthesis reactions',
    'Biochemistry': 'laboratory research pharmaceutical healthcare biotechnology molecular biology clinical chemistry enzymes',
    'Microbiology': 'laboratory research healthcare pharmaceutical quality control bacteria virus infection clinical microbial',
    'Agricultural Science': 'farming agribusiness food production research extension services crop livestock irrigation soil',
    'Nursing Science': 'clinical healthcare hospital patient care community health ward bedside nursing medical treatment',
}

# How central is a course to an organisation's primary function
# Higher weight = this course is core to what the organisation does
SECTOR_COURSE_WEIGHT = {
    'Legal and Justice': {'Law': 3.0},
    'Judiciary': {'Law': 3.0},
    'Legal Services': {'Law': 3.0},
    'ICT Policy and Regulation': {'Computer Science': 3.0, 'Information Technology': 3.0, 'Cybersecurity': 3.0},
    'ICT Infrastructure': {'Computer Science': 3.0, 'Computer Engineering': 3.0},
    'Software and ERP Solutions': {'Computer Science': 3.0, 'Software Engineering': 3.0},
    'Fintech and Software': {'Computer Science': 3.0, 'Software Engineering': 3.0},
    'IT Consulting and Services': {'Computer Science': 3.0, 'Software Engineering': 3.0},
    'Banking and Finance': {'Accounting': 3.0, 'Economics': 3.0},
    'Taxation and Revenue': {'Accounting': 3.0, 'Law': 2.0},
    'Audit and Consulting': {'Accounting': 3.0, 'Law': 2.0},
    'Professional Services': {'Accounting': 3.0, 'Law': 2.0},
    'Healthcare': {'Medicine and Surgery': 3.0, 'Pharmacy': 3.0, 'Nursing Science': 3.0},
    'Private Healthcare': {'Medicine and Surgery': 3.0, 'Pharmacy': 3.0, 'Nursing Science': 3.0},
    'Public Health': {'Medicine and Surgery': 3.0, 'Nursing Science': 3.0},
    'Military Healthcare': {'Medicine and Surgery': 3.0, 'Nursing Science': 3.0},
    'Pharmaceutical Regulation': {'Pharmacy': 3.0, 'Biochemistry': 3.0, 'Microbiology': 3.0},
    'Broadcasting and Media': {'Mass Communication': 3.0},
    'Media and Broadcasting': {'Mass Communication': 3.0},
    'Public Communication': {'Mass Communication': 3.0},
    'Civil Engineering and Infrastructure': {'Civil Engineering': 3.0},
    'Construction and Engineering': {'Civil Engineering': 3.0, 'Mechanical Engineering': 2.0},
    'Power Distribution': {'Electrical Engineering': 3.0},
    'Power and Energy': {'Electrical Engineering': 3.0},
    'Oil and Gas': {'Chemical Engineering': 3.0, 'Mechanical Engineering': 2.0},
    'Agriculture': {'Agricultural Science': 3.0},
    'Agricultural Finance': {'Agricultural Science': 2.0, 'Accounting': 2.0},
    'Space and Technology': {'Computer Science': 2.0, 'Electrical Engineering': 2.0},
}

def get_recommendations(course, state, opportunity_type, top_n=69):
    organisations = Organisation.query.filter_by(
        state=state,
        opportunity_type=opportunity_type
    ).all()

    if not organisations:
        return []

    # Step 1 - filter by relevant_courses
    filtered_orgs = []
    for org in organisations:
        relevant = [c.strip() for c in org.relevant_courses.split(',')]
        if course in relevant:
            filtered_orgs.append(org)

    if not filtered_orgs:
        return []

    # Step 2 - TF-IDF cosine similarity
    course_keywords = COURSE_KEYWORD_MAP.get(course, course.lower())

    org_profiles = []
    for org in filtered_orgs:
        profile = f"{org.name} {org.sector} {org.description} {org.relevant_courses}"
        org_profiles.append(profile)

    all_profiles = [course_keywords] + org_profiles

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_profiles)

    student_vector = tfidf_matrix[0]
    org_vectors = tfidf_matrix[1:]
    similarities = cosine_similarity(student_vector, org_vectors).flatten()

    # Step 3 - apply sector weighting to boost primary-fit organisations
    for i, org in enumerate(filtered_orgs):
        sector_weights = SECTOR_COURSE_WEIGHT.get(org.sector, {})
        boost = sector_weights.get(course, 1.0)
        similarities[i] = similarities[i] * boost

    # Step 4 - normalise scores to 0-100 range
    max_score = similarities.max()
    if max_score > 0:
        similarities = (similarities / max_score) * 100

    # Step 5 - rank and return
    ranked_indices = similarities.argsort()[::-1]
    results = []
    for i in ranked_indices:
        score = round(float(similarities[i]), 1)
        results.append({
            'organisation': filtered_orgs[i],
            'score': score
        })

    return results[:top_n]