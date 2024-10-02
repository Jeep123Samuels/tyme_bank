import React ,{useState,useEffect} from "react";

import "../App.css"

import Tablelist from "./Tablelist";
import CreateTransactionFunc from "./CreateTransaction";
import Stats from "./Stats";
import { deleteRequest, getData, postRequest } from './Helpers'

function Parent({account, transactions, setTransactions}){

    const [total,setTotal]=useState();

    const [amount,setAmount]=useState('');
    const [description,setDescription]=useState('');

    const updateValues={
      am:amount,
      descr:description,
    }

    const saveTransaction= async ()=>{
      try {
          await postRequest(
            'transactions',
            {
                'amount': amount,
                'account_id': account.id,
                'description': description,
            }
          );
      } catch(err) {
         console.log(err);
         alert(err.response.data[0].msg);
      }

      const transAll = await getData(`transactions?account_id=${account.id}`);
      setTransactions(transAll);
      setAmount('')
      setDescription('')
    }

    useEffect(()=>{
        const totalArray=transactions.map((item)=>{
          const value= item.amount;
          const num= parseFloat(value);
          return num
        });
        setTotal(
          totalArray.reduce((a,b)=>{
            return a+b
          },0));
    },[transactions])


    const _amount=(e)=>{
      setAmount(e.target.value)
    }
    const _description=(e)=>{
      setDescription(e.target.value)
    }

    async function deleteTransaction(id){
      await deleteRequest(`transactions/${id}`);
      const transAll = await getData(`transactions?account_id=${account.id}`);
      setTransactions(transAll);
    }


    return(
        <div className="parent">
          <div className="dashboard">
            <Stats account={account} total={total}/>
          </div>

        <CreateTransactionFunc save={saveTransaction} am={_amount} descr={_description} update={updateValues}/>

        {
        transactions.length === 0 ?
            <div className='createaccount'>
                <h1>No transactions to display.</h1>
            </div>
            :
            transactions.map((row)=>(
                <Tablelist key={row.id} trans={row} del={deleteTransaction}/>
            ))
        }
        </div>
    )
}


export default Parent
