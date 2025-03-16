class Translator:
    def __init__(self):
        self.translations = {}
        self.current_lang = "en"
    
    def add_translations(self, translations_dict):
        """Add translations dictionary"""
        self.translations = translations_dict
    
    def set_lang(self, lang_code):
        """Set current language"""
        self.current_lang = lang_code
    
    def get_text(self, key, **kwargs):
        """Get translated text for the given key in current language"""
        try:
            text = self.translations.get(self.current_lang, {}).get(key, key)
            # Handle string formatting with arguments
            if kwargs:
                return text.format(**kwargs)
            return text
        except Exception as e:
            # Return the key if any error occurs
            return key

# Create a singleton instance
translator = Translator()