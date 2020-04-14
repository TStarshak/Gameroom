import React, {Component} from 'react';
import '../Style/MainMenu.css';
import Search from './Search';
import StarRating from './StarRating';
import ProfileIcon from './ProfileIcon'


class MainMenu extends Component {
  render(){
  
    return (
      <div className="MainMenu">
        <ProfileIcon src="https://i.ibb.co/sg0q559/Featherknight-Summoner-Icon-TFT-Lo-L.jpg"></ProfileIcon>
        <h1>{this.props.user.username}</h1>
        <h2>Rating: {this.props.user.rating}</h2>
        
        <Search matching = {this.props.matching} all_players={this.props.all_players} user={this.props.user} toNoti={this.props.toNoti}></Search>
      </div>
      
    );
    
  }
}

export default MainMenu;
