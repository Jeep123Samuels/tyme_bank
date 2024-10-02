import React from 'react'


function Stats({account,total}){
    return(
        <div className='statistics'>
            <span>
                <h6>Account</h6>
                <p>{account.name}</p>
            </span>

            <span>
                <h6>Total</h6>
                <p>R{total}</p>
            </span>
        </div>
    )
}

export default Stats;
