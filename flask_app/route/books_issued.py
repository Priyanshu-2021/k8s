import logging
from flask_app.models.books_issued.book_issued_orm import Books_Issued
from datetime import datetime
from datetime import timedelta
from flask import Blueprint
from flask import request
from flask import make_response
from flask import jsonify
from flask_app.connection.connector import BackendConnector


logger = logging.getLogger(__name__)

books_issued_blueprint = Blueprint("books_issued", __name__)

@books_issued_blueprint.route("/health", methods=["GET"])
def health():
    """This route gets the data of all image available in Annotation Pool

    Returns:
        Response: The method returns a Response Object with message and data
    """
    logger.info("Getting all issued books details")

    session=BackendConnector.get_session()
    
    resp_obj={
        'message':'API working',
    }
    return make_response(
        jsonify(**resp_obj),
        200
    )


@books_issued_blueprint.route("", methods=["GET"])
def books_issued():
    """This route gets the data of all image available in Annotation Pool

    Returns:
        Response: The method returns a Response Object with message and data
    """
    logger.info("Getting all issued books details")
    session=BackendConnector.get_session()
    try:
        data = session.query(Books_Issued).with_entities(
            Books_Issued.member_no,
            Books_Issued.book_title,
            Books_Issued.author,
            Books_Issued.issue_date,
            Books_Issued.return_date
        ).all()

    except Exception as e:
        resp_obj={
            'message':'Error occurred',
            'error': str(e), 
            'data':[]
        }
        return make_response(
            jsonify(**resp_obj),
            422
        )
    
    data_dict=[]
    for item in data:
        temp={
            "member_no":item.member_no,
            "book_title":item.book_title,
            "author":item.author,
            "issue_date":item.issue_date,
            "return_date":item.return_date
        }
        data_dict.append(temp)

    resp_obj={
        'message':'All books issued details returned successfully',
        'data':data_dict,
        'count':len(data_dict)
    }
    return make_response(
        jsonify(**resp_obj),
        200
    )


@books_issued_blueprint.route("", methods=["POST"])
def add_books_issued_record():

    payload = request.get_json()
    logger.info(f'Payload: {payload}')
    if payload.get('member_no'):
        member_no=payload.get('member_no')
    if payload.get('book_title'):
        book_title=payload.get('book_title')
    if payload.get('author'):
        author=payload.get('author')
    
    issue_date=datetime.now()
    return_date=datetime.now()+timedelta(days=15)

    session=BackendConnector.get_session()

    logger.info('Checking if record already exists...')
    is_exist = session.query(Books_Issued).filter(
        Books_Issued.member_no==member_no,
        Books_Issued.book_title==book_title,
    ).with_entities(Books_Issued.issue_date,).first()
    if is_exist:
        logger.info(f'record already exists, book issued on {is_exist}')
        return make_response(
            jsonify({
                "message":"Record already exists",
                "data":[]
            }),
            201
        )

    books_issued_obj=Books_Issued(
        member_no = member_no,
        book_title = book_title,
        author = author,
        issue_date= issue_date,
        return_date= return_date
    )

    logger.info("Inserting record...")
    
    try:
        session.add(books_issued_obj)
    except Exception as e:
        logger.error(f"Image addition to Annotation Pool Failed {e}")
        logger.warning("Rolling Back Session")
        session.rollback()
        raise Exception(f"Record addition failed with error {str(e)}")
    else:
        session.commit()
    logger.info("Record Inserted...")


    return make_response(
        jsonify({
            "message":"Record inserted",
            "data":[]
        }),
        201
    )