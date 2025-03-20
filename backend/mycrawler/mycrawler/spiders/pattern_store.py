class PatternStore:
    """Stores regex patterns in object format for modularity."""

    EMAIL_PATTERNS = [
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        r"[a-zA-Z0-9._%+-]+\s?\[at\]\s?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # Obfuscated emails
        r"[a-zA-Z0-9._%+-]+\s?\(at\)\s?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"  # Another obfuscation
    ]

    PHONE_PATTERNS = [
        r"\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",
        r"\+\d{1,3}[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}",
        r"\d{3}[\s.-]\d{3}[\s.-]\d{4}",
        r"00\d{1,3}[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,4}",
        r"\+\d{1,3}\s?\d{1,4}\s\d{3}\s\d{4}",  # International numbers with spaces
        r"\d{1,4}\s\d{1,4}\s\d{1,4}"  # Generic spaced numbers
    ]

    SOCIAL_PATTERNS = [
        r"https?://(?:www\.)?(?:facebook\.com|fb\.com)/[a-zA-Z0-9._%+-]+",
        r"https?://(?:www\.)?instagram\.com/[a-zA-Z0-9_\.]+",
        r"https?://(?:www\.)?linkedin\.com/(?:in|company)/[a-zA-Z0-9_\-]+",
        r"https?://(?:www\.)?twitter\.com/[a-zA-Z0-9_]+",
        r"https?://(?:www\.)?youtube\.com/(?:user|channel|c)/[a-zA-Z0-9_\-]+",
        r"https?://(?:www\.)?t\.me/[a-zA-Z0-9_]+",
        r"https?://(?:www\.)?wa\.me/[0-9]+",
        r"https?://(?:www\.)?github\.com/[a-zA-Z0-9_\-]+",
        r"https?://(?:www\.)?pinterest\.com/[a-zA-Z0-9_\-]+",
        r"https?://(?:www\.)?tiktok\.com/@[a-zA-Z0-9_\.]+",
        r"https?://(?:www\.)?snapchat\.com/add/[a-zA-Z0-9_\-]+",
        r"https?://(?:www\.)?reddit\.com/user/[a-zA-Z0-9_]+",
        r"https?://(?:www\.)?medium\.com/@[a-zA-Z0-9_]+",
        r"https?://(?:www\.)?tumblr\.com/blog/[a-zA-Z0-9_\-]+",
        r"https?://(?:www\.)?quora\.com/profile/[a-zA-Z0-9_\-]+",
        r"https?://(?:www\.)?discord\.com/invite/[a-zA-Z0-9]+"
    ]
