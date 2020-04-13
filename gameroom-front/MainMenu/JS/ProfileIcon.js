import React, { Component } from 'react';
import '../Style/ProfileIcon.css';

class ProfileIcon extends Component {
    render() {
        let icon = this.props.src;
        return (
            <div className='ProfileIcon'>
                <a href="https://ibb.co/sg0q559"><img src={icon} alt="icon"></img></a>
            </div>
        );
    }
}



export default ProfileIcon;