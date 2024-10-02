import React,{ useState } from 'react'


function CreateTransactionFunc({save,am,descr,update}){

    return(
        <div className='create'>
            <h5>New Transaction</h5>
            <div>
                <label>Description</label>
                <input type="text" onChange={descr} value={update.descr} />
            </div>

            <div>
                <label >Amount</label>
                <input type="number" onChange={am} value={update.am}/>
            </div>
            {update.am && update.descr?
                <button onClick={save}>Save Transaction</button>
                :
                null
            }
        </div>
    )
}

export default CreateTransactionFunc;
