import React, {Component} from 'react';
import '../Style/MainMenu.css';
import Search from './Search';
import StarRating from './StarRating';
import ProfileIcon from './ProfileIcon'
class MainMenu extends Component {
  render(){
    console.log(this.props);
    return (
      <div className="MainMenu">
        <ProfileIcon src={this.props.user.profileIcon}></ProfileIcon>
        <h1>{this.props.user.name}</h1>
        <StarRating rating={this.props.user.rating.toString()}></StarRating>
        
        <Search toNoti={this.props.toNoti}></Search>
      </div>
      
    );
    
  }
}

export default MainMenu;
