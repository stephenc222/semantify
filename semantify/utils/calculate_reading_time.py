#!/usr/bin/env python3

def calculate_reading_time(content, words_per_minute=265):
    """Calculates the reading time for a given file."""
    word_count = len(content.split(" "))
    reading_time_minutes = round(word_count / words_per_minute)
    return reading_time_minutes
