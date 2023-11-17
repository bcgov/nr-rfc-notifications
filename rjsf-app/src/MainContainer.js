import FormComponent from './FormComponents';
import React from 'react';
import "./MainContainer.css";

function MainContainer(){
    return(
        <div className="parentContainer">
            <FormComponent/>
        </div>
    );
}

export default MainContainer;