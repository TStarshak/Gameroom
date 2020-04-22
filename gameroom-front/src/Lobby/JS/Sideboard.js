import React, { Component } from 'react';
import { Container } from 'react-bootstrap';
import '../Style/Lobby.css';
import UserList from './UserList';
class Sideboard extends Component {


    constructor(props){
        super(props)
    }

    render() {
        console.log(this.props.user.username)
        return (
            <div className="sideboard flex-container-column">
                <div className="flex-item upper-sideboard">
                    <div className='game-name red'>League of Legend</div>
                    <div className='player-list green'>
                        <UserList users={this.props.users} maxUser={6} inviteUser={() =>{}}></UserList>
                    </div>

                </div>
                <div className='flex-item profile '>
                    <p>{this.props.user.username}</p>
                    {/* <div className='flex-item'>
                        <div className='imwrap'>
                            <img src="https://i.ibb.co/sg0q559/Featherknight-Summoner-Icon-TFT-Lo-L.jpg" width='30px' height='30px' alt="icon"></img>
                        </div>
                    </div>
                    <div className='flex-item'>b134</div> */}
                </div>
            </div>
        );
    }
}

export default Sideboard;