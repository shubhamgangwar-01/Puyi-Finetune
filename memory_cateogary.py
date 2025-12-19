"""
Memory categories for synthetic dataset generation
"""

MEMORY_CATEGORIES = {
    "childhood": {
        "description": "Early life memories, family, school, friends",
        "examples": [
            "first day of school",
            "family vacations",
            "childhood friends",
            "favorite toys",
            "learning to ride a bike"
        ]
    },
    "education": {
        "description": "School, college, learning experiences",
        "examples": [
            "favorite subjects",
            "teachers who inspired me",
            "study habits",
            "graduation day",
            "college life"
        ]
    },
    "career": {
        "description": "Work experiences, achievements, challenges",
        "examples": [
            "first job",
            "career milestones",
            "work projects",
            "professional relationships",
            "career transitions"
        ]
    },
    "relationships": {
        "description": "Family, friends, romantic relationships",
        "examples": [
            "best friends",
            "family traditions",
            "important relationships",
            "social gatherings",
            "support systems"
        ]
    },
    "hobbies": {
        "description": "Interests, passions, recreational activities",
        "examples": [
            "favorite hobbies",
            "sports and fitness",
            "creative pursuits",
            "travel experiences",
            "collections or interests"
        ]
    },
    "achievements": {
        "description": "Personal accomplishments and proud moments",
        "examples": [
            "awards and recognition",
            "personal goals achieved",
            "overcoming challenges",
            "skills learned",
            "proud moments"
        ]
    },
    "life_events": {
        "description": "Significant life moments and transitions",
        "examples": [
            "moving to a new place",
            "major life decisions",
            "transformative experiences",
            "celebrations",
            "life lessons"
        ]
    },
    "preferences": {
        "description": "Likes, dislikes, values, beliefs",
        "examples": [
            "favorite foods",
            "music preferences",
            "personal values",
            "life philosophy",
            "pet peeves"
        ]
    }
}

CONVERSATION_TYPES = [
    "recall_specific",  # User asks about specific memory
    "general_question",  # User asks about general topic
    "emotional_reflection",  # Reflecting on feelings about memories
    "comparison",  # Comparing different memories or experiences
    "advice_based",  # Giving advice based on personal experiences
]