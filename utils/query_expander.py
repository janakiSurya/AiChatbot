"""
Query expansion utilities for better search results
Optimized and consolidated
"""

def expand_query(query, history=None):
    """Expand query with synonyms and related terms for better search"""
    query_lower = query.lower()
    
    # Handle pronouns using history
    if history and len(history) >= 2:
        # Check for pronouns
        pronouns = [' it ', ' that ', ' he ', ' his ', ' she ', ' her ', ' they ', ' them ', ' there ']
        if any(p in f" {query_lower} " for p in pronouns):
            # Get the last user query from history
            last_user_query = None
            for msg in reversed(history):
                if msg['role'] == 'user':
                    last_user_query = msg['content']
                    break
            
            if last_user_query:
                # Combine last query with current query for context
                query = f"{last_user_query} {query}"
                query_lower = query.lower()
    
    # Query expansion mappings
    expansions = {
        'best work': ['best work', 'best project', 'greatest achievement', 'top accomplishment', 'notable work', 'significant project'],
        'project': ['project', 'work', 'application', 'system', 'platform', 'solution'],
        'company': ['company', 'employer', 'organization', 'firm', 'corporation', 'workplace', 'acer', 'mindtree', 'tata'],
        'job': ['job', 'role', 'position', 'work', 'employment', 'career'],
        'skill': ['skill', 'expertise', 'technology', 'knowledge', 'ability', 'proficiency'],
        'experience': ['experience', 'background', 'history', 'career', 'work history'],
        'education': ['education', 'degree', 'study', 'academic', 'university', 'college']
    }
    
    # Find matching expansions
    expanded_terms = []
    for key, synonyms in expansions.items():
        if key in query_lower:
            expanded_terms.extend(synonyms)
    
    # Special handling for reputation queries
    if any(word in query_lower for word in ['reputation', 'reputated', 'prestigious', 'famous', 'well-known']):
        expanded_terms.extend(['company', 'employer', 'organization'])
    
    # If no specific expansion found, add common related terms
    if not expanded_terms:
        if 'work' in query_lower:
            expanded_terms.extend(['project', 'achievement', 'accomplishment'])
        if 'what' in query_lower:
            expanded_terms.extend(['details', 'information', 'about'])
    
    # Combine original query with expansions
    if expanded_terms:
        expanded_query = query + " " + " ".join(expanded_terms[:3])  # Limit to 3 expansions
        return expanded_query
    
    return query


def classify_query_intent(query):
    """Classify the intent of the query for better search"""
    query_lower = query.lower()
    
    # Intent classification
    if any(word in query_lower for word in ['company', 'employer', 'work', 'job', 'role', 'position']):
        return 'work'
    elif any(word in query_lower for word in ['project', 'best', 'achievement', 'accomplishment', 'developed', 'built']):
        return 'projects'
    elif any(word in query_lower for word in ['skill', 'technology', 'expertise', 'know', 'experience']):
        return 'skills'
    elif any(word in query_lower for word in ['education', 'study', 'degree', 'university', 'college']):
        return 'education'
    elif any(word in query_lower for word in ['contact', 'email', 'phone', 'reach', 'location']):
        return 'contact'
    else:
        return 'general'