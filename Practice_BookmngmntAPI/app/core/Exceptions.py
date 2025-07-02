from fastapi import HTTPException, status



class BookNotFoundException (Exception):
    """Exception raised when a book is not found."""
    pass

class  BookalreadyexistsException (Exception):
    """Exception raised when a book is already existing."""
    pass



def Book_not_Found_Exception():
    return HTTPException (
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Book not found."
    )

def Book_already_exists_Exception():
    return HTTPException (
        status_code = status.HTTP_400_BAD_REQUEST,
        detail = "Book already exists."
    )


