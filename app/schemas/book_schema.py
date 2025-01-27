from pydantic import BaseModel, Field, field_validator
import re
from typing import Optional

class Book(BaseModel):
    title: str =Field(..., description="Title of the book",min_length=1, max_length=150)
    author: str =Field(..., description="Author of the book",min_length=1, max_length=150)
    isbn: str =Field(...,description="International Standard Book Number (ISBN) of the book(without hyphens)",min_length=1, max_length=13)
    publication_year: Optional[int] = None
    description: Optional[str] = None
    
    @field_validator("title")
    def validate_title(cls, value):
        """Custom validation for title field"""
        if not value.strip():  
           raise ValueError("Title cannot be empty or just spaces.")
        return value

    @field_validator("author")
    def validate_author(cls, value):
        """Custom validation for author field"""
        if not value.strip():  
            raise ValueError("Author cannot be empty or just spaces.")
        return value

    @field_validator("isbn")
    def validate_isbn(cls, value):
        """Regular expression for validating ISBN-13 format (can adjust for ISBN-10 too)"""
        isbn_regex = r'^\d{13}$'  # ISBN-13 without hyphens
        if value:
            if not re.match(isbn_regex, value):
                raise ValueError("Invalid ISBN-13 format. ISBN must be exactly 13 digits.")
        return value

class UpdateBook(BaseModel):
    title: Optional[str] =Field(None,description="Title of the book",min_length=1, max_length=150)
    author: Optional[str] =Field(None,description="Author of the book",min_length=1, max_length=150)
    isbn: Optional[str] =Field(None,description="International Standard Book Number (ISBN) of the book")
    publication_year: Optional[int] = Field(None,description="Publication year of the book")
    description: Optional[str] = Field(None,description="Description of the book") 
