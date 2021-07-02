import React from 'react'

const CompanyHeader = ({title}) => {
    return (
        <div className="header">
            <h3 style={{color:'black',backgroundColor:'silver'}}>{title}</h3>
        </div>
    )
}

export default CompanyHeader