import React from 'react';
import '../Style/StarRating.css';

function StarRating(probs) {
    let widthPixels = (parseFloat(probs.rating) * 40).toString() + 'px';
    return (
        <div className='StarRating'>
            <span className='stars'>
                <span style={{ width: widthPixels }}></span>
            </span>
        </div>
    );
}



export default StarRating;