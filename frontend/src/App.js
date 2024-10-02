import './App.css';
import React,{useState, useEffect} from 'react'
import axios from 'axios';

import Parent from './components/Parent';
import { getData, postRequest } from './components/Helpers'

function App() {

  const [accountName,setAccountName]=useState();
  const [account,setAccount]=useState({});
  const [accountNames,setAccountNames]=useState();
  const [page,setPage]=useState(true);
  const [transactions,setTransactions]=useState([]);

  const getAccounts = async () => {
     let allAccounts_ = await getData('accounts');
     let accountsName = [];
     let acc;
     for (acc of allAccounts_) {
        accountsName.push(acc.name);
     }
     setAccountNames(accountsName.join());
     console.log(allAccounts_);
  }

  const updateAccountName=(e)=>{
    setAccountName(e.target.value);
  }

  const saveAccountName = async () =>{
    const accountCreated = await postRequest(
       'accounts',
       {name: accountName}
    );
    const transAll = await getData(`transactions?account_id=${accountCreated.id}`);
    setAccount(accountCreated);
    setTransactions(transAll);

    console.log(account);
    setPage(!page);
  }


  return (
    <div className="App">
      {page?
        <div className='createaccount'>
            <h1>Get started by creating a new Account or enter current one.</h1>
            <input onChange={updateAccountName} type="text"/>
            <button onClick={()=>{saveAccountName()}}>Create</button>
            <h1>Click for current accounts</h1>
            <h5>
                {accountNames}
            </h5>
            <button onClick={async()=>await getAccounts()}>Show</button>
        </div>
            :
      <Parent account={account} transactions={transactions} setTransactions={setTransactions}/>}
    </div>
  );
}

export default App;
