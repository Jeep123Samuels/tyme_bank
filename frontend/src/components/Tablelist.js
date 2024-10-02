import React from 'react'

function Tablelist({trans,del,handleF}){
    return(
        <div id={trans.id} className='list'>
            <p className='amount'>{trans.amount}</p>
            <p className='description'>{trans.description}</p>
            <p className='type'>{trans.type}</p>
            <p className='date'>{trans.created_time.split('T')[0]}</p>
            <button onClick={async()=>await del(trans.id)}>DEL</button>
        </div>
    )
}

export default Tablelist;
