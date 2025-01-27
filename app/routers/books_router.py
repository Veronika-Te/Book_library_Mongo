from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId
from app.utils.config import settings
from app.database.database_mongo import db
from app.schemas.book_schema import Book, UpdateBook

router=APIRouter(prefix="/books", tags=["Book"])

def get_collection(db):
  """Gets collection from the database"""
  books_collection = db[settings.COLLECTION]
  return books_collection

def serialize_objectid(book):
    """
    Convert the ObjectId to a string in a MongoDB document.
    This function checks if the input dictionary (e.g., a MongoDB document) contains
    an ObjectId in the "_id" field. If an ObjectId is found, it is converted to a string
    so that the document can be easily serialized to JSON (e.g., for API responses).
    """
    if "_id" in book and isinstance(book["_id"], ObjectId):
        book["_id"] = str(book["_id"])
    return book

@router.get('/books/', response_class=JSONResponse)
async def get_books():
  books_collection=get_collection(db)
  book_cursor = books_collection.find()
  books = await book_cursor.to_list(length=100)
  books = [serialize_objectid(book) for book in books]
  return books

@router.post("/createbook/", response_model=Book)
async def create_book(book: Book):
  collection = get_collection(db)
  result = await collection.insert_one(book.model_dump())
  book_with_id = book.model_dump()
  book_with_id["_id"] = str(result.inserted_id)
  return book_with_id

@router.post("/updatebook/{book_id}", response_model=Book)
async def update_book(book_id: str, update_book: UpdateBook):
  collection = get_collection(db)
  if not ObjectId.is_valid(book_id):
    raise HTTPException(status_code=400, detail="Invalid book ID format")
  result = await collection.update_one(
        {"_id": ObjectId(book_id)},  
        {"$set": update_book.model_dump()}  
    )
  if result.matched_count == 0:
    raise HTTPException(status_code=404, detail="Book not found")
  updated_book = await collection.find_one({"_id": ObjectId(book_id)})
  updated_book["_id"] = str(updated_book.get("_id"))  
  return updated_book

@router.patch("/updatebook/{book_id}", response_model=Book)
async def update_book(book_id: str, update_book: UpdateBook):
    collection = get_collection(db)
    if not ObjectId.is_valid(book_id):
      raise HTTPException(status_code=400, detail="Invalid book ID format")
    update_data = update_book.model_dump(exclude_unset=True)
    if not update_data:
      raise HTTPException(status_code=400, detail="No fields to update")
    result = await collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": update_data}  
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    updated_book = await collection.find_one({"_id": ObjectId(book_id)})
    updated_book["_id"] = str(updated_book["_id"])
    return updated_book


@router.delete("/deletebook/{book_id}", response_model=Book)
async def delete_book(book_id: str):
  collection = get_collection(db)
  if not ObjectId.is_valid(book_id):
     raise HTTPException(status_code=400, detail="Invalid book ID format")
  book_to_delete = await collection.find_one({"_id": ObjectId(book_id)})
  if not book_to_delete:
    raise HTTPException(status_code=404, detail="Book not found")
  result = await collection.delete_one({"_id": ObjectId(book_id)})
  if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
  book_to_delete["_id"] = str(book_to_delete["_id"])  
  return book_to_delete


