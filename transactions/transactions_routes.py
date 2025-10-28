from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session_db, verify_token
from models.models import Transaction, User
from schemas.schemas import TransactionSchema, ResponseTransactionSchema
from typing import List

transaction_router = APIRouter(prefix='/transactions', tags=['transactions']) # dependencies=[Depends(verify_token)]


@transaction_router.get('/')
async def get_transactions():
    return { 'message': 'Transactions List' }


@transaction_router.post('/transaction')
async def create_transaction(transaction_schema: TransactionSchema, session=Depends(get_session_db), user: User = Depends(verify_token)):
    new_transaction = Transaction(user= transaction_schema.user)
    session.add(new_transaction)
    session.commit()
    return { 'message': f'Transaction created successfully' }


@transaction_router.get('/transaction/{transaction_id}')
async def get_transaction_details(transaction_id: int, session=Depends(get_session_db), user: User = Depends(verify_token)):
    transaction = session.query(Transaction).filter(Transaction.id==transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=400, detail='Transaction not found')
    if not user.admin and user.id != transaction.user:
        raise HTTPException(status_code=401, detail='Access denied for this action')
    
    return {
        'transaction': transaction
    }
    

@transaction_router.get('/list/transactions-user', response_model=List[ResponseTransactionSchema])
async def transactions_list_user(session=Depends(get_session_db), user: User = Depends(verify_token)):
    transations = session.query(Transaction).filter(Transaction.user==user.id).all()
    return  transations


@transaction_router.get('/list')
async def transactions_list(session=Depends(get_session_db), user: User = Depends(verify_token)):
    if not user.admin:
        raise HTTPException(status_code=401, detail='Access denied for this action')
    else:
        transactions = session.query(Transaction).all()

    return { 
        'transactions': transactions 
    }

