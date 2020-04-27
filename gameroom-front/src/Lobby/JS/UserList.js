import React, {Component} from 'react';
import '../Style/Lobby.css';

function UserList(props){
    let maxUser = props.maxUser;
    let height = parseInt(300 / maxUser) + 'px';

    let items = props.users.map((user) => {
        return <div className='user-list-item' style={{height: height}}>
            {user.username}
        </div>
    })

    if(props.users.length <= maxUser){
        let buttonHeight = parseInt(300 / maxUser) - 10 + 'px';
        items.push(<button style={{height: buttonHeight, width: buttonHeight}}>
            +
        </button>);
    }

    return <div className="user-list">
        {items}
    </div>
}

export default UserList;